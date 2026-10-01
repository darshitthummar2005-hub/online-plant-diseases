"""
Plant disease document model.

Stored in the `plant_diseases` collection. Serves as the knowledge base used by
search and the (simulated) prediction service. Managed by admins.
"""

from typing import Any

from pydantic import Field

from app.models.base import MongoModel


class PlantDisease(MongoModel):
    """A plant disease record with symptoms, causes and rich treatment plans.

    The rich fields (chemical/biological/organic treatment, prevention tips,
    fertilizer plan, severity levels, weather guidance and emergency actions)
    power the "AI Plant Doctor" detection report.
    """

    name: str = Field(min_length=1, max_length=120)
    category: str = Field(default="Fungal")  # Fungal | Pest | Deficiency | Viral | Bacterial | Other
    scientific_name: str | None = None
    severity: str = Field(default="Moderate")  # Mild | Moderate | Severe
    description: str | None = None
    symptoms: list[str] = Field(default_factory=list)
    causes: list[str] = Field(default_factory=list)
    treatment: list[str] = Field(default_factory=list)
    prevention: list[str] = Field(default_factory=list)
    affected_plants: list[str] = Field(default_factory=list)
    image_url: str | None = None
    # ---- AI Plant Doctor rich treatment data ----
    chemical_treatment: list[dict[str, Any]] = Field(default_factory=list)
    biological_treatment: list[dict[str, Any]] = Field(default_factory=list)
    organic_remedies: list[dict[str, Any]] = Field(default_factory=list)
    prevention_tips: list[dict[str, Any]] = Field(default_factory=list)
    fertilizer: dict[str, Any] = Field(default_factory=dict)
    severity_levels: dict[str, Any] = Field(default_factory=dict)
    weather_conditions: dict[str, Any] = Field(default_factory=dict)
    emergency_actions: list[str] = Field(default_factory=list)
    # Schema/seed version so older docs can be migrated on startup.
    seed_version: int | None = None
    # Extra flexible metadata (e.g. "slug", "emoji") without schema changes.
    extra: dict[str, Any] = Field(default_factory=dict)
