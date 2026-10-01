"""
Feedback service layer.

Persists user ratings/messages and lists feedback (for admins).
"""

from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackOut
from app.utils.logger import get_logger
from app.utils.pagination import paginate_async

logger = get_logger(__name__)


class FeedbackService:
    """Operations on the feedback collection."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def create(self, user_id: str, payload: FeedbackCreate) -> FeedbackOut:
        """Store a new feedback record for the authenticated user."""
        record = Feedback(
            user_id=user_id,
            rating=payload.rating,
            message=payload.message,
            prediction_id=payload.prediction_id,
        )
        doc = record.to_doc()
        result = await self.collection.insert_one(doc)
        logger.info("Feedback saved by user %s (rating %d)", user_id, payload.rating)

        return FeedbackOut(
            id=str(result.inserted_id),
            rating=payload.rating,
            message=payload.message,
            prediction_id=payload.prediction_id,
            submitted_at=record.submitted_at,
        )

    async def list_all(self, page: int, page_size: int):
        """Paginated feedback list (admin view)."""
        items, total = await paginate_async(
            self.collection,
            {},
            page,
            page_size,
            sort=[("submitted_at", -1)],
        )
        outs = [
            FeedbackOut(
                id=str(doc["_id"]),
                rating=doc.get("rating", 0),
                message=doc.get("message"),
                prediction_id=str(doc["prediction_id"]) if doc.get("prediction_id") else None,
                submitted_at=doc.get("submitted_at"),
            )
            for doc in items
        ]
        return outs, total

    async def average_rating(self) -> float:
        """Overall average rating across all feedback."""
        cursor = self.collection.aggregate(
            [{"$group": {"_id": None, "avg": {"$avg": "$rating"}}}]
        )
        result = await cursor.to_list(length=1)
        if not result:
            return 0.0
        return round(result[0]["avg"], 2)
