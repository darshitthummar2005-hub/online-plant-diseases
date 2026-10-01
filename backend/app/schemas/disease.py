"""
Disease schemas.

Request/response models for the plant disease knowledge base (admin CRUD + search).
Includes the rich "AI Plant Doctor" treatment fields.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChemicalTreatmentItem(BaseModel):
    """A recommended chemical product/class for a disease."""

    name: str
    brand_names: list[str] = Field(default_factory=list)
    active_ingredients: list[str] = Field(default_factory=list)
    dosage: str | None = None
    safety_precautions: list[str] = Field(default_factory=list)
    waiting_period: str | None = None


class BiologicalTreatmentItem(BaseModel):
    """A bio-pesticide or beneficial microorganism treatment."""

    agent: str
    type: str = Field(default="Bio-pesticide")  # Bio-fungicide | Bio-insecticide | Beneficial microbe
    application: str | None = None
    when_to_apply: str | None = None
    notes: str | None = None


class OrganicRemedyItem(BaseModel):
    """A home-made / organic remedy."""

    name: str
    recipe: str | None = None
    application: str | None = None
    frequency: str | None = None


class PreventionTip(BaseModel):
    """A single prevention tip grouped by category."""

    category: str = Field(default="General")
    title: str
    description: str | None = None


class FertilizerPlan(BaseModel):
    """Fertilizer + soil recommendations."""

    organic: list[str] = Field(default_factory=list)
    micronutrients: list[str] = Field(default_factory=list)
    npk: str | None = None
    soil_improvement: list[str] = Field(default_factory=list)


class SeverityLevels(BaseModel):
    """What each severity level looks like for this disease."""

    mild: str | None = None
    moderate: str | None = None
    severe: str | None = None


class WeatherConditions(BaseModel):
    """Weather guidance relevant to the disease."""

    humidity: str | None = None
    temperature: str | None = None
    rainfall: str | None = None


class DiseaseCreate(BaseModel):
    """Payload for POST /diseases (admin)."""

    name: str = Field(min_length=1, max_length=120)
    category: str = Field(default="Fungal")
    scientific_name: str | None = None
    severity: str = Field(default="Moderate")
    description: str | None = None
    symptoms: list[str] = Field(default_factory=list)
    causes: list[str] = Field(default_factory=list)
    treatment: list[str] = Field(default_factory=list)
    prevention: list[str] = Field(default_factory=list)
    affected_plants: list[str] = Field(default_factory=list)
    image_url: str | None = None
    chemical_treatment: list[ChemicalTreatmentItem] = Field(default_factory=list)
    biological_treatment: list[BiologicalTreatmentItem] = Field(default_factory=list)
    organic_remedies: list[OrganicRemedyItem] = Field(default_factory=list)
    prevention_tips: list[PreventionTip] = Field(default_factory=list)
    fertilizer: FertilizerPlan = Field(default_factory=FertilizerPlan)
    severity_levels: SeverityLevels = Field(default_factory=SeverityLevels)
    weather_conditions: WeatherConditions = Field(default_factory=WeatherConditions)
    emergency_actions: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class DiseaseUpdate(BaseModel):
    """Partial update payload for PATCH /diseases/{id} (admin)."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    category: str | None = None
    scientific_name: str | None = None
    severity: str | None = None
    description: str | None = None
    symptoms: list[str] | None = None
    causes: list[str] | None = None
    treatment: list[str] | None = None
    prevention: list[str] | None = None
    affected_plants: list[str] | None = None
    image_url: str | None = None
    chemical_treatment: list[ChemicalTreatmentItem] | None = None
    biological_treatment: list[BiologicalTreatmentItem] | None = None
    organic_remedies: list[OrganicRemedyItem] | None = None
    prevention_tips: list[PreventionTip] | None = None
    fertilizer: FertilizerPlan | None = None
    severity_levels: SeverityLevels | None = None
    weather_conditions: WeatherConditions | None = None
    emergency_actions: list[str] | None = None
    extra: dict[str, Any] | None = None


class DiseaseOut(BaseModel):
    """Public disease record."""

    id: str = Field(alias="_id")
    name: str
    category: str
    scientific_name: str | None = None
    severity: str
    description: str | None = None
    symptoms: list[str]
    causes: list[str]
    treatment: list[str]
    prevention: list[str]
    affected_plants: list[str]
    image_url: str | None = None
    chemical_treatment: list[ChemicalTreatmentItem] = Field(default_factory=list)
    biological_treatment: list[BiologicalTreatmentItem] = Field(default_factory=list)
    organic_remedies: list[OrganicRemedyItem] = Field(default_factory=list)
    prevention_tips: list[PreventionTip] = Field(default_factory=list)
    fertilizer: FertilizerPlan = Field(default_factory=FertilizerPlan)
    severity_levels: SeverityLevels = Field(default_factory=SeverityLevels)
    weather_conditions: WeatherConditions = Field(default_factory=WeatherConditions)
    emergency_actions: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=False)

    @field_validator("id", mode="before")
    @classmethod
    def _coerce_id(cls, value: Any) -> Any:
        """Convert bson ObjectId to str."""
        if value is not None:
            try:
                from bson import ObjectId

                if isinstance(value, ObjectId):
                    return str(value)
            except ImportError:  # pragma: no cover
                pass
        return value
