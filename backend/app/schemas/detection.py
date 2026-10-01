"""
Detection schemas.

Request/response models for the public AI Plant Doctor endpoint (POST /api/detect).
The response embeds the full disease knowledge base record plus diagnosis metadata
(confidence, severity level, expert recommendation).
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.disease import (
    BiologicalTreatmentItem,
    ChemicalTreatmentItem,
    FertilizerPlan,
    OrganicRemedyItem,
    PreventionTip,
    SeverityLevels,
    WeatherConditions,
)


class DetectRequest(BaseModel):
    """
    Payload for POST /detect.

    `symptoms` are user-selected symptom keywords. `image_data` accepts a base64
    (data-URL) image so the engine can run lightweight visual analysis and weight
    confidence higher. `image_url` records a remote image reference.
    """

    symptoms: list[str] = Field(default_factory=list, max_length=20)
    plant: str | None = None  # crop/houseplant name chosen by the user
    image_present: bool = False
    image_data: str | None = Field(default=None, max_length=15_000_000)
    image_url: str | None = None
    model_version: str | None = None


class DetectResponse(BaseModel):
    """Full diagnosis report returned by the AI Plant Doctor."""

    # --- Diagnosis metadata ---
    disease_id: str | None = None
    disease_name: str
    plant: str | None = None  # plant the diagnosis was made for
    confidence: int  # 0-100
    severity: str  # Mild | Moderate | Severe
    matched_symptoms: list[str] = Field(default_factory=list)
    unmatched_symptoms: list[str] = Field(default_factory=list)
    visual_signals: list[str] = Field(default_factory=list)
    expert_recommended: bool = False
    consult_reason: str | None = None
    model_version: str
    predicted_at: datetime

    # --- Disease knowledge base ---
    category: str | None = None
    scientific_name: str | None = None
    description: str | None = None
    symptoms: list[str] = Field(default_factory=list)
    causes: list[str] = Field(default_factory=list)
    treatment: list[str] = Field(default_factory=list)
    prevention: list[str] = Field(default_factory=list)
    affected_plants: list[str] = Field(default_factory=list)
    chemical_treatment: list[ChemicalTreatmentItem] = Field(default_factory=list)
    biological_treatment: list[BiologicalTreatmentItem] = Field(default_factory=list)
    organic_remedies: list[OrganicRemedyItem] = Field(default_factory=list)
    prevention_tips: list[PreventionTip] = Field(default_factory=list)
    fertilizer: FertilizerPlan = Field(default_factory=FertilizerPlan)
    severity_levels: SeverityLevels = Field(default_factory=SeverityLevels)
    weather_conditions: WeatherConditions = Field(default_factory=WeatherConditions)
    emergency_actions: list[str] = Field(default_factory=list)

    # Extra snapshot of any fields not explicitly modeled.
    extra: dict[str, Any] = Field(default_factory=dict)
