"""End-to-end verification of the ONLINE PLANT DISEASES auth system.

Run from the backend folder:  .venv\\Scripts\\python.exe auth_e2e_test.py
Uses only the stdlib so it needs no extra packages.

Admin credentials are read from the backend's own configuration
(`ADMIN_ACCOUNTS` in `.env`) so no password is ever stored in this file.
Set `E2E_BASE` to point the suite at a different API.
"""

import json
import os
import sys
import urllib.error
import urllib.request
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.environ.get("E2E_BASE", "http://localhost:8000/api").rstrip("/")
passed, failed = 0, []


def admin_credentials():
    """Pull the configured admin accounts out of the backend settings.

    Returns a list of (identifier, password) tuples. Reads from the real
    `.env` so this file never has to contain a secret.
    """
    try:
        from app.config import get_settings

        accounts = get_settings().admin_accounts_list
    except Exception as exc:  # noqa: BLE001 - config problems should not be fatal here
        print(f"Could not read ADMIN_ACCOUNTS from backend config: {exc}")
        accounts = []

    if not accounts:
        print(
            "\nNo ADMIN_ACCOUNTS configured, so the admin log-in checks are skipped.\n"
            "Set ADMIN_ACCOUNTS in backend/.env, or pass E2E_ADMIN_USER / E2E_ADMIN_PASS."
        )
        return []

    env_user = os.environ.get("E2E_ADMIN_USER")
    env_pass = os.environ.get("E2E_ADMIN_PASS")
    if env_user and env_pass:
        return [(env_user, env_pass)]

    return [(a["username"], a["password"]) for a in accounts if a.get("username")]


def call(method, path, body=None, token=None):
    req = urllib.request.Request(f"{BASE}{path}", method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urllib.request.urlopen(req, data, timeout=15) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw or b"null")
        except json.JSONDecodeError:
            return e.code, raw.decode(errors="replace")


def check(name, cond, extra=""):
    global passed
    if cond:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed.append(name)
        print(f"  FAIL  {name} {extra}")


print("\n=== 1. Admin accounts log in and receive the admin role ===")
ADMINS = admin_credentials()
admin_tokens = {}
primary_admin = None
for user, password in ADMINS:
    st, res = call("POST", "/auth/login", {"identifier": user, "password": password})
    ok = st == 200 and res.get("user", {}).get("role") == "admin"
    check(f"{user} logs in as admin", ok, f"(status={st})")
    if ok:
        admin_tokens[user] = res["access_token"]
        if primary_admin is None:
            primary_admin = res["user"]
        check(f"{user} -> Welcome, {res['user'].get('full_name') or user}", True)

if not ADMINS:
    print("SKIPPED: no admin credentials available.")

# The remaining admin-side checks all run as this one account.
ADMIN_TOKEN = next(iter(admin_tokens.values()), None)

print("\n=== 2. Admin login by email works too ===")
if primary_admin and primary_admin.get("email"):
    st, res = call("POST", "/auth/login",
                   {"identifier": primary_admin["email"], "password": ADMINS[0][1]})
    check("login with email address",
          st == 200 and res["user"]["username"] == primary_admin["username"], f"(status={st})")
else:
    print("SKIPPED: no admin email available.")

print("\n=== 3. Wrong credentials are rejected ===")
if primary_admin:
    st, res = call("POST", "/auth/login",
                   {"identifier": primary_admin["username"], "password": "wrong-password"})
    check("wrong password -> 401", st == 401, f"(status={st})")
    check("error message is generic", "Invalid credentials" in json.dumps(res), f"({res})")
    st, _ = call("POST", "/auth/login", {"identifier": "no-such-user-xyz", "password": "Whatever1"})
    check("unknown user -> 401", st == 401, f"(status={st})")
else:
    print("SKIPPED: no admin account to test against.")

print("\n=== 4. Normal user registration and login ===")
uname = "testuser" + uuid.uuid4().hex[:6]
st, reg = call("POST", "/auth/register", {
    "full_name": "Test Grower", "email": f"{uname}@example.com", "password": "Garden2025",
})
check("register new user -> 201", st == 201, f"(status={st} {reg})")
check("new account gets the user role", reg.get("role") == "user", f"(role={reg.get('role')})")

st, res = call("POST", "/auth/login", {"identifier": uname, "password": "Garden2025"})
check("new user logs in", st == 200 and res["user"]["username"] == uname, f"(status={st})")
user_token = res.get("access_token") if st == 200 else None
user_id = res["user"]["id"] if st == 200 else None

print("\n=== 5. Role escalation is impossible ===")
st, res = call("POST", "/auth/register", {
    "full_name": "Sneaky", "email": f"sneaky{uuid.uuid4().hex[:6]}@example.com",
    "password": "Garden2025", "role": "admin",
})
check("role field in register body -> 422", st == 422, f"(status={st})")

print("\n=== 6. Duplicate registration is blocked ===")
st, _ = call("POST", "/auth/register", {
    "full_name": "Dupe", "email": f"{uname}@example.com", "password": "Garden2025",
})
check("duplicate email -> 409", st == 409, f"(status={st})")

print("\n=== 7. A normal user cannot reach admin functionality ===")
for path in ["/admin/stats", "/admin/overview", "/admin/users", "/admin/detections", "/admin/admins"]:
    st, _ = call("GET", path, token=user_token)
    check(f"user GET {path} -> 403", st == 403, f"(status={st})")

st, _ = call("PATCH", f"/admin/users/{user_id}", {"role": "admin"}, token=user_token)
check("user cannot self-promote -> 403", st == 403, f"(status={st})")
st, _ = call("DELETE", f"/admin/users/{user_id}", None, token=user_token)
check("user cannot delete accounts -> 403", st == 403, f"(status={st})")

print("\n=== 8. Admin APIs are protected and work for admins ===")
for path in ["/admin/stats", "/admin/overview", "/admin/users", "/admin/detections", "/admin/admins"]:
    st, _ = call("GET", path, token=ADMIN_TOKEN)
    check(f"admin GET {path} -> 200", st == 200, f"(status={st})")

st, res = call("GET", "/admin/users", token=ADMIN_TOKEN)
check("admin user list is paginated", "items" in res and "total" in res, f"(keys={list(res)})")
check("password hashes are never returned",
      all("hashed_password" not in u for u in res.get("items", [])))
st, res = call("GET", "/admin/stats", token=ADMIN_TOKEN)
check("stats include user counters", res.get("total_users", 0) > 0, f"({res.get('total_users')})")
check("all three admins are counted", res.get("total_admins", 0) >= 3, f"({res.get('total_admins')})")

print("\n=== 9. Admin cannot lock itself out ===")
st, res = call("PATCH", "/admin/users/" + call("GET", "/auth/me", token=ADMIN_TOKEN)[1]["id"],
               {"role": "user"}, token=ADMIN_TOKEN)
check("admin cannot demote self -> 400", st == 400, f"(status={st} {res})")

print("\n=== 10. Unauthenticated and forged tokens are rejected ===")
st, _ = call("GET", "/admin/stats")
check("no token -> 401", st == 401, f"(status={st})")
st, _ = call("GET", "/auth/me")
check("no token on /auth/me -> 401", st == 401, f"(status={st})")
st, _ = call("GET", "/auth/me", token="not.a.real.token")
check("garbage token -> 401", st == 401, f"(status={st})")
st, _ = call("GET", "/auth/me", token=ADMIN_TOKEN[:-6] + "AAAAAA")
check("tampered signature -> 401", st == 401, f"(status={st})")

print("\n=== 11. Logout revokes the token server-side ===")
st, _ = call("POST", "/auth/logout", None, token=user_token)
check("logout -> 200", st == 200, f"(status={st})")
st, _ = call("GET", "/auth/me", token=user_token)
check("reused token after logout -> 401", st == 401, f"(status={st})")
st, _ = call("GET", "/admin/stats", token=user_token)
check("revoked token cannot reach admin -> 401", st == 401, f"(status={st})")

print("\n=== 12. Existing plant-disease functionality still works ===")
st, res = call("GET", "/diseases?page_size=3")
check("public disease list -> 200", st == 200 and len(res.get("items", [])) == 3, f"(status={st})")
st, res = call("POST", "/detect", {"symptoms": ["yellow", "spots"], "plant": "Tomato"})
check("disease detection -> 200", st == 200 and res.get("disease_name"), f"(status={st})")
check("detection returns a report", bool(res.get("treatment") or res.get("confidence")), f"({res.get('disease_name')})")
st, res = call("GET", "/diseases/categories")
check("disease categories -> 200", st == 200, f"(status={st})")
# Use a live admin token here: the user token was revoked by the logout test.
st, _ = call("POST", "/diseases", {"name": "Hacked", "category": "Fungal"}, token=user_token)
check("revoked token on POST /diseases -> 401", st == 401, f"(status={st})")

# Unique name so repeated runs do not collide on the duplicate check.
probe_disease = "E2E Probe " + uuid.uuid4().hex[:8]
st, created = call("POST", "/diseases", {"name": probe_disease, "category": "Fungal"},
                   token=ADMIN_TOKEN)
check("admin can create a disease -> 201", st == 201, f"(status={st})")
new_disease_id = created.get("id") if st == 201 else None

st, session = call("POST", "/auth/login", {"identifier": uname, "password": "Garden2025"})
live_user_token = session.get("access_token")
st, _ = call("POST", "/diseases", {"name": probe_disease, "category": "Fungal"}, token=live_user_token)
check("normal user cannot create disease -> 403", st == 403, f"(status={st})")

# Leave the database as we found it.
if new_disease_id:
    st, _ = call("DELETE", f"/diseases/{new_disease_id}", None, token=ADMIN_TOKEN)
    check("test disease removed again -> 200", st == 200, f"(status={st})")

print("\n" + "=" * 58)
print(f"  {passed} passed, {len(failed)} failed")
if failed:
    print("  FAILED:")
    for f in failed:
        print("   -", f)
print("=" * 58)
raise SystemExit(1 if failed else 0)
