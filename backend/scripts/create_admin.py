"""
Admin account management CLI.

Create, update, disable or delete administrator accounts from the terminal
without ever putting a password in source control, the frontend bundle or a
shell history file.

Usage (run from the `backend` folder, with the virtualenv active):

    # create a new admin (password is prompted, never echoed, never a CLI arg)
    python -m scripts.create_admin --username darshit --email darshit@example.com

    # set / reset the password of an existing admin
    python -m scripts.create_admin --username darshit --reset-password

    # change the role of an existing account
    python -m scripts.create_admin --username darshit --role admin

    # deactivate without deleting
    python -m scripts.create_admin --username darshit --deactivate

    # delete permanently
    python -m scripts.create_admin --username darshit --delete

Passwords are read with `getpass` (hidden input) unless `--password-env VAR` is
used, in which case the value is read from an environment variable so CI can
supply it without a TTY. The password is bcrypt-hashed before it is written.
"""

import argparse
import asyncio
import getpass
import os
import sys
from datetime import datetime

from bson import ObjectId

from app.auth.security import hash_password
from app.database import close_db, get_database
from app.utils.logger import setup_logging


def read_password(env_var: str | None) -> str:
    """Read a password from an env var, or prompt for it without echoing."""
    if env_var:
        value = os.environ.get(env_var, "")
        if not value:
            sys.exit(f"Environment variable {env_var} is empty or not set.")
        return value

    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        sys.exit("Passwords do not match.")
    if len(password) < 8:
        sys.exit("Password must be at least 8 characters.")
    if not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
        sys.exit("Password must contain at least one uppercase letter and one digit.")
    return password


async def main() -> None:
    parser = argparse.ArgumentParser(description="Manage ONLINE PLANT DISEASES admin accounts.")
    parser.add_argument("--username", required=True, help="Username of the account")
    parser.add_argument("--email", help="Email (required when creating)")
    parser.add_argument("--full-name", help="Display name")
    parser.add_argument("--role", choices=["user", "admin"], help="Set the account role")
    parser.add_argument("--reset-password", action="store_true", help="Set a new password")
    parser.add_argument("--password-env", help="Read the password from this env var (CI use)")
    parser.add_argument("--deactivate", action="store_true", help="Set is_active = False")
    parser.add_argument("--activate", action="store_true", help="Set is_active = True")
    parser.add_argument("--delete", action="store_true", help="Delete the account permanently")
    args = parser.parse_args()

    setup_logging()
    db = get_database()
    users = db.users
    username = args.username.strip()

    existing = await users.find_one(
        {"$or": [{"username": username}, {"username": {"$regex": f"^{username}$", "$options": "i"}}]}
    )

    if args.delete:
        if not existing:
            sys.exit(f"No account named {username!r}.")
        if existing.get("role") == "admin":
            others = await users.count_documents(
                {"_id": {"$ne": existing["_id"]}, "role": "admin", "is_active": True}
            )
            if others == 0:
                sys.exit("Refusing to delete the last active admin account.")
        await users.delete_one({"_id": existing["_id"]})
        print(f"Deleted account {username!r}.")
        await close_db()
        return

    # --- update paths ------------------------------------------------------
    if existing:
        updates: dict = {}
        if args.email:
            new_email = args.email.strip().lower()
            taken = await users.find_one({"email": new_email, "_id": {"$ne": existing["_id"]}})
            if taken:
                sys.exit(f"Email {new_email!r} is already in use by another account.")
            updates["email"] = new_email
        if args.role:
            updates["role"] = args.role
        if args.full_name is not None:
            updates["full_name"] = args.full_name.strip() or None
        if args.deactivate:
            updates["is_active"] = False
        if args.activate:
            updates["is_active"] = True
        if args.reset_password:
            updates["hashed_password"] = hash_password(read_password(args.password_env))

        if not updates:
            sys.exit("Nothing to do: pass --role/--reset-password/--activate/--deactivate.")

        losing_admin = existing.get("role") == "admin" and (
            updates.get("role") == "user" or updates.get("is_active") is False
        )
        if losing_admin:
            others = await users.count_documents(
                {"_id": {"$ne": existing["_id"]}, "role": "admin", "is_active": True}
            )
            if others == 0:
                sys.exit("Refusing to remove the last active admin account.")

        updates["updated_at"] = datetime.utcnow()
        await users.update_one({"_id": existing["_id"]}, {"$set": updates})
        print(f"Updated {username!r}: {', '.join(updates)}")
        await close_db()
        return

    # --- create path -------------------------------------------------------
    if not args.email:
        sys.exit("--email is required when creating a new account.")
    if not args.reset_password:
        sys.exit("Pass --reset-password to set the initial password for a new account.")

    email = args.email.strip().lower()
    if await users.find_one({"email": email}):
        sys.exit(f"Email {email!r} is already in use by another account.")

    await users.insert_one(
        {
            "username": username,
            "email": email,
            "hashed_password": hash_password(read_password(args.password_env)),
            "full_name": (args.full_name or "").strip() or "Portal Admin",
            "role": args.role or "admin",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    )
    print(f"Created {args.role or 'admin'} account {username!r} <{email}>.")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
