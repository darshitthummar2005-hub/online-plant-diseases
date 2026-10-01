"""
Disease service layer.

Search + admin CRUD for the plant disease knowledge base.
"""

import re
from datetime import datetime

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.disease import PlantDisease
from app.schemas.disease import DiseaseCreate, DiseaseUpdate
from app.utils.logger import get_logger
from app.utils.pagination import paginate_async

logger = get_logger(__name__)

PUBLIC_FIELDS = {
    "name": 1,
    "category": 1,
    "scientific_name": 1,
    "severity": 1,
    "description": 1,
    "symptoms": 1,
    "causes": 1,
    "treatment": 1,
    "prevention": 1,
    "affected_plants": 1,
    "image_url": 1,
    "chemical_treatment": 1,
    "biological_treatment": 1,
    "organic_remedies": 1,
    "prevention_tips": 1,
    "fertilizer": 1,
    "severity_levels": 1,
    "weather_conditions": 1,
    "emergency_actions": 1,
    "extra": 1,
    "created_at": 1,
    "updated_at": 1,
}


class DiseaseService:
    """Operations on the plant_diseases collection."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    # ---------- Public ----------
    async def search(
        self,
        q: str | None = None,
        category: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ):
        """Case-insensitive full-text-ish search with pagination."""
        query: dict = {}
        if q:
            # Regex search across name, scientific name, description, symptoms.
            rx = re.compile(re.escape(q), re.IGNORECASE)
            query["$or"] = [
                {"name": rx},
                {"scientific_name": rx},
                {"description": rx},
                {"symptoms": rx},
                {"affected_plants": rx},
            ]
        if category:
            query["category"] = re.compile(f"^{re.escape(category)}$", re.IGNORECASE)

        items, total = await paginate_async(
            self.collection,
            query,
            page,
            page_size,
            sort=[("name", 1)],
        )
        return items, total

    async def get(self, disease_id: str) -> dict:
        """Fetch a single disease by id (raises 404 if missing)."""
        doc = await self.collection.find_one({"_id": __oid(disease_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Disease not found")
        return doc

    async def categories(self) -> list[str]:
        """Return the distinct disease categories present in the database."""
        return await self.collection.distinct("category")

    # ---------- Admin ----------
    async def create(self, payload: DiseaseCreate) -> dict:
        """Insert a new disease record (admin)."""
        if await self.collection.find_one({"name": payload.name}):
            raise HTTPException(status_code=409, detail="Disease with this name already exists")

        disease = PlantDisease(**payload.model_dump())
        doc = disease.to_doc()
        result = await self.collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        logger.info("Created disease: %s", payload.name)
        return doc

    async def update(self, disease_id: str, payload: DiseaseUpdate) -> dict:
        """Partially update a disease record (admin)."""
        updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
        if not updates:
            return await self.get(disease_id)
        updates["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one(
            {"_id": __oid(disease_id)},
            {"$set": updates},
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Disease not found")
        logger.info("Updated disease %s", disease_id)
        return await self.get(disease_id)

    async def delete(self, disease_id: str) -> None:
        """Delete a disease record (admin)."""
        result = await self.collection.delete_one({"_id": __oid(disease_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Disease not found")
        logger.info("Deleted disease %s", disease_id)


def __oid(value: str):
    """Convert a string id to a bson ObjectId."""
    from bson import ObjectId

    try:
        return ObjectId(value)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid disease id")
