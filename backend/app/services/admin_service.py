"""
Admin service layer.

All data access for the admin dashboard lives here so the router stays thin and
the queries are unit-testable. Nothing in this module performs authorisation —
that is enforced by the `get_current_admin` dependency on every route.
"""

from datetime import datetime, timedelta

from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.admin import (
    ActivityOut,
    AdminStats,
    AdminUserOut,
    AdminUserUpdate,
    CategoryCount,
    DetectionOut,
)
from app.schemas.user import UserOut
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AdminService:
    """Read/write operations backing the admin dashboard."""

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.users = db["users"]
        self.predictions = db["predictions"]
        self.diseases = db["plant_diseases"]
        self.feedback = db["feedback"]

    # ------------------------------------------------------------------ stats
    async def stats(self) -> AdminStats:
        """Aggregate the platform counters shown at the top of the dashboard."""
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)

        total_users = await self.users.count_documents({})
        active_users = await self.users.count_documents({"is_active": True})
        total_admins = await self.users.count_documents({"role": "admin", "is_active": True})
        new_users_7d = await self.users.count_documents({"created_at": {"$gte": week_ago}})
        total_diseases = await self.diseases.count_documents({})
        total_predictions = await self.predictions.count_documents({})
        detections_7d = await self.predictions.count_documents(
            {"created_at": {"$gte": week_ago}}
        )
        total_feedback = await self.feedback.count_documents({})

        pipeline = [{"$group": {"_id": None, "avg": {"$avg": "$rating"}}}]
        cursor = self.feedback.aggregate(pipeline)
        row = await cursor.to_list(length=1)
        average_rating = round(float(row[0]["avg"]), 2) if row and row[0]["avg"] else 0.0

        return AdminStats(
            total_users=total_users,
            active_users=active_users,
            disabled_users=total_users - active_users,
            total_admins=total_admins,
            new_users_7d=new_users_7d,
            total_diseases=total_diseases,
            total_predictions=total_predictions,
            total_feedback=total_feedback,
            average_rating=average_rating,
            detections_7d=detections_7d,
        )

    async def disease_categories(self) -> list[CategoryCount]:
        """Count diseases per category, for the overview bar chart."""
        pipeline = [
            {"$group": {"_id": {"$ifNull": ["$category", "Uncategorised"]}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1, "_id": 1}},
        ]
        rows = await self.diseases.aggregate(pipeline).to_list(length=None)
        return [CategoryCount(label=r["_id"], count=r["count"]) for r in rows]

    async def recent_activity(self, limit: int = 8) -> list[ActivityOut]:
        """Most recent sign-ups and detections, merged into one feed."""
        limit = max(1, min(limit, 25))
        users = await self.users.find({}).sort("created_at", -1).limit(limit).to_list(limit)
        detections = await (
            self.predictions.find({}).sort("created_at", -1).limit(limit).to_list(limit)
        )

        feed: list[ActivityOut] = []
        for doc in users:
            feed.append(
                ActivityOut(
                    kind="user",
                    title="New account registered",
                    detail=f"{doc.get('username', 'unknown')} · {doc.get('role', 'user')}",
                    at=doc.get("created_at") or datetime.utcnow(),
                )
            )
        for doc in detections:
            feed.append(
                ActivityOut(
                    kind="detection",
                    title="Disease detection run",
                    detail=f"{doc.get('disease_name', 'Unknown')} · "
                    f"{round(float(doc.get('confidence', 0)) * 100)}% confidence",
                    at=doc.get("created_at") or datetime.utcnow(),
                )
            )

        feed.sort(key=lambda a: a.at, reverse=True)
        return feed[:limit]

    # ------------------------------------------------------------------ users
    async def list_users(
        self,
        page: int,
        page_size: int,
        q: str | None = None,
        role: str | None = None,
    ) -> tuple[list[AdminUserOut], int]:
        """Paginated user list with an optional search and role filter."""
        query: dict = {}
        if q:
            # Escape user input: it is only ever used as a literal substring.
            import re

            needle = re.escape(q.strip())
            rx = {"$regex": needle, "$options": "i"}
            query["$or"] = [{"username": rx}, {"email": rx}, {"full_name": rx}]
        if role in ("user", "admin"):
            query["role"] = role

        total = await self.users.count_documents(query)
        cursor = (
            self.users.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
        docs = await cursor.to_list(page_size)
        return [_to_admin_user(d) for d in docs], total

    async def update_user(
        self, user_id: str, payload: AdminUserUpdate, acting_admin: UserOut
    ) -> AdminUserOut:
        """
        Apply an admin change to a user.

        Two guards protect the admin tier from self-inflicted lockout:
          - an admin cannot disable or demote their own account, and
          - the last remaining active admin cannot be demoted or disabled.
        """
        target = await self.users.find_one({"_id": _oid(user_id)})
        if not target:
            raise HTTPException(status_code=404, detail="User not found")

        updates: dict = {}
        if payload.full_name is not None:
            updates["full_name"] = payload.full_name
        if payload.role is not None:
            updates["role"] = payload.role
        if payload.is_active is not None:
            updates["is_active"] = payload.is_active

        if not updates:
            return _to_admin_user(target)

        losing_admin = (
            target.get("role") == "admin"
            and (payload.role == "user" or payload.is_active is False)
        )
        if losing_admin and str(target["_id"]) == acting_admin.id:
            raise HTTPException(
                status_code=400,
                detail="You cannot remove your own admin access",
            )
        if losing_admin and await self._is_last_active_admin(target):
            raise HTTPException(
                status_code=400,
                detail="At least one active admin account must remain",
            )

        updates["updated_at"] = datetime.utcnow()
        await self.users.update_one({"_id": target["_id"]}, {"$set": updates})
        logger.info(
            "Admin %s updated user %s: %s",
            acting_admin.username,
            target.get("username"),
            ", ".join(updates),
        )
        updated = await self.users.find_one({"_id": target["_id"]})
        return _to_admin_user(updated or target)

    async def delete_user(self, user_id: str, acting_admin: UserOut) -> None:
        """Delete a user account, with the same self/last-admin guards."""
        target = await self.users.find_one({"_id": _oid(user_id)})
        if not target:
            raise HTTPException(status_code=404, detail="User not found")

        if str(target["_id"]) == acting_admin.id:
            raise HTTPException(status_code=400, detail="You cannot delete your own account")
        if target.get("role") == "admin" and await self._is_last_active_admin(target):
            raise HTTPException(
                status_code=400, detail="At least one active admin account must remain"
            )

        await self.users.delete_one({"_id": target["_id"]})
        logger.info(
            "Admin %s deleted user %s", acting_admin.username, target.get("username")
        )

    async def _is_last_active_admin(self, target: dict) -> bool:
        """True when `target` is the only active admin left in the database."""
        others = await self.users.count_documents(
            {
                "_id": {"$ne": target["_id"]},
                "role": "admin",
                "is_active": True,
            }
        )
        return others == 0

    # ------------------------------------------------------------- detections
    async def list_detections(
        self, page: int, page_size: int, q: str | None = None
    ) -> tuple[list[DetectionOut], int]:
        """
        Paginated detection/prediction records, enriched with the username.

        Detections written by the rule-based service store confidence in 0..1;
        older documents may store it as a percentage, so the value is normalised
        for display here rather than in the detection pipeline.
        """
        query: dict = {}
        if q:
            import re

            query["disease_name"] = {"$regex": re.escape(q.strip()), "$options": "i"}

        total = await self.predictions.count_documents(query)
        docs = await (
            self.predictions.find(query)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
            .to_list(page_size)
        )

        usernames = await self._username_map([d.get("user_id") for d in docs])
        items = [
            DetectionOut(
                id=str(d.get("_id")),
                user_id=str(d.get("user_id", "")),
                username=usernames.get(str(d.get("user_id", ""))),
                disease_name=d.get("disease_name") or d.get("disease") or "Unknown",
                confidence=_normalise_confidence(d.get("confidence")),
                severity=d.get("severity"),
                plant=d.get("plant"),
                status=d.get("status", "completed"),
                symptoms=list(d.get("symptoms") or d.get("matched_symptoms") or []),
                predicted_at=d.get("predicted_at") or d.get("created_at") or datetime.utcnow(),
            )
            for d in docs
        ]
        return items, total

    async def _username_map(self, user_ids: list) -> dict[str, str]:
        """Map user id -> username for the given ids, skipping anonymous runs."""
        oids = []
        for raw in filter(None, user_ids):
            try:
                oids.append(ObjectId(str(raw)))
            except Exception:
                continue
        if not oids:
            return {}
        docs = await self.users.find({"_id": {"$in": oids}}, {"username": 1}).to_list(len(oids))
        return {str(d["_id"]): d.get("username", "") for d in docs}


# --------------------------------------------------------------------- helpers
def _to_admin_user(doc: dict) -> AdminUserOut:
    """Build an AdminUserOut from a raw MongoDB document (never leaks the hash)."""
    return AdminUserOut(
        id=str(doc.get("_id")),
        username=doc.get("username", ""),
        email=doc.get("email", ""),
        full_name=doc.get("full_name"),
        role=doc.get("role", "user"),
        is_active=bool(doc.get("is_active", True)),
        created_at=doc.get("created_at") or datetime.utcnow(),
        updated_at=doc.get("updated_at"),
    )


def _normalise_confidence(value) -> float:
    """Return confidence as a 0..100 float regardless of how it was stored."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if 0 < number <= 1:
        number *= 100
    return round(min(number, 100), 1)


def _oid(value: str):
    """Convert a string id to a bson ObjectId, tolerating malformed input."""
    try:
        return ObjectId(value)
    except Exception:
        return value
