"""
Detection service (AI Plant Doctor).

Scores the user's symptoms against the disease knowledge base — taking the
selected plant/crop into account — computes a confidence score and severity
level, decides whether an expert consultation is recommended, and returns a
full diagnosis report with rich treatment data.

Matching strategy:
  - Each disease carries an `affected_plants` list (species + crop groups).
  - When the user selects a plant, diseases that affect that plant are ranked
    strongly above ones that don't, so the same symptoms on different plants
    produce different, plant-correct diagnoses.
  - If nothing in the knowledge base affects the chosen plant, the engine falls
    back to symptom-only matching and warns the user.

This is a transparent rule-based matcher. A real ML model would plug into
`score_symptoms()` / `_analyze_image()` without changing the rest of the flow.
"""

import re
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorCollection

from app.schemas.detection import DetectRequest, DetectResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

MODEL_VERSION = "ai-plant-doctor-v2"

# Confidence is reported as 0-100 (%).
CONFIDENCE_CAP = 97
LOW_CONFIDENCE = 70

# Strongly favour diseases that affect the selected plant.
PLANT_MATCH_SCORE = 60
PLANT_MISMATCH_PENALTY = 45
SYMPTOM_POINTS = 10

# Broad crop groups used by `affected_plants` entries such as "Cucurbits".
PLANT_GROUPS: dict[str, list[str]] = {
    "cucurbits": ["cucumber", "squash", "pumpkin", "zucchini", "melon", "watermelon", "gourd"],
    "nightshades": ["tomato", "potato", "eggplant", "pepper", "chili", "chilli", "bell pepper"],
    "leafy greens": ["lettuce", "spinach", "cabbage", "kale", "broccoli", "swiss chard", "arugula"],
    "brassicas": ["cabbage", "broccoli", "cauliflower", "kale", "brussels sprout", "radish"],
    "alliums": ["onion", "garlic", "leek", "shallot", "chive"],
    "legumes": ["bean", "pea", "lentil", "soybean", "chickpea", "cowpea"],
    "houseplants": ["monstera", "peace lily", "snake plant", "aloe vera", "pothos", "philodendron", "orchid", "spider plant"],
    "herbs": ["basil", "mint", "rosemary", "thyme", "cilantro", "parsley", "sage", "oregano"],
    "stone fruits": ["peach", "plum", "cherry", "apricot", "nectarine"],
    "pome fruits": ["apple", "pear", "quince"],
    "citrus": ["orange", "lemon", "lime", "grapefruit", "mandarin", "clementine"],
    "berries": ["strawberry", "blueberry", "raspberry", "blackberry", "cranberry"],
    "grains": ["wheat", "corn", "maize", "rice", "barley", "oat"],
    "ornamentals": ["rose", "geranium", "zinnia", "petunia", "marigold", "gardenia", "azalea", "hydrangea"],
    "root vegetables": ["carrot", "beet", "radish", "potato", "turnip", "onion"],
    "heavy feeders": ["tomato", "corn", "cabbage", "potato", "squash", "pepper"],
}


class DetectService:
    """Runs plant + symptom based disease detection and builds the full report."""

    def __init__(self, diseases: AsyncIOMotorCollection) -> None:
        self.diseases = diseases

    async def detect(self, payload: DetectRequest) -> DetectResponse:
        """Run detection and return the complete diagnosis report."""
        symptoms = [s.strip().lower() for s in payload.symptoms if s.strip()]
        plant = self._clean_name(payload.plant or "")

        # Lightweight visual analysis of the attached image (if any).
        visual_signals: list[str] = []
        image_boost = 0
        has_image = bool(payload.image_present or payload.image_data or payload.image_url)
        if payload.image_data:
            visual_signals, image_boost = self._analyze_image(payload.image_data)
            for cue in visual_signals:
                if cue not in symptoms:
                    symptoms.append(cue)

        disease_docs = await self.diseases.find({}).to_list(length=10000)

        best = None
        best_score = -1
        best_matched: list[str] = []
        best_plant_match = False
        any_plant_match = False

        for doc in disease_docs:
            s_matched, matched = self._score_symptoms(doc, symptoms)
            p_match = self._plant_score(doc, plant) if plant else False
            if p_match:
                any_plant_match = True
            if p_match:
                score = s_matched * SYMPTOM_POINTS + PLANT_MATCH_SCORE
            elif plant:
                score = s_matched * SYMPTOM_POINTS - PLANT_MISMATCH_PENALTY
            else:
                score = s_matched * SYMPTOM_POINTS
            if score > best_score:
                best = doc
                best_score = score
                best_matched = matched
                best_plant_match = p_match

        if best is None:
            logger.warning("Detection ran with an empty disease knowledge base")
            return self._unknown_report(payload, symptoms, visual_signals, plant)

        plant_unknown = bool(plant) and not any_plant_match
        if best_plant_match or not plant:
            # Symptoms + plant agree (or no plant selected).
            confidence = min(100, self._confidence(len(best_matched), len(symptoms), has_image) + image_boost)
        else:
            # Best match does not affect the chosen plant — down-weight heavily.
            confidence = min(100, self._confidence(len(best_matched), len(symptoms), has_image) - 15)

        severity = str(best.get("severity") or "Moderate")
        expert, reason = self._expert_advice(confidence, severity, plant, plant_unknown)

        matched_set = set(best_matched)
        unmatched = [s for s in symptoms if s not in matched_set]

        logger.info(
            "Detection -> %s (plant=%s conf=%d sev=%s expert=%s)",
            best.get("name"),
            plant or "-",
            confidence,
            severity,
            expert,
        )

        return DetectResponse(
            disease_id=str(best["_id"]),
            disease_name=best.get("name", "Unknown"),
            plant=payload.plant or None,
            confidence=confidence,
            severity=severity,
            matched_symptoms=best_matched,
            unmatched_symptoms=unmatched,
            visual_signals=visual_signals,
            expert_recommended=expert,
            consult_reason=reason,
            model_version=payload.model_version or MODEL_VERSION,
            predicted_at=datetime.utcnow(),
            category=best.get("category"),
            scientific_name=best.get("scientific_name"),
            description=best.get("description"),
            symptoms=best.get("symptoms", []),
            causes=best.get("causes", []),
            treatment=best.get("treatment", []),
            prevention=best.get("prevention", []),
            affected_plants=best.get("affected_plants", []),
            chemical_treatment=best.get("chemical_treatment", []),
            biological_treatment=best.get("biological_treatment", []),
            organic_remedies=best.get("organic_remedies", []),
            prevention_tips=best.get("prevention_tips", []),
            fertilizer=best.get("fertilizer", {}) or {},
            severity_levels=best.get("severity_levels", {}) or {},
            weather_conditions=best.get("weather_conditions", {}) or {},
            emergency_actions=best.get("emergency_actions", []),
            extra=best.get("extra", {}) or {},
        )

    # ---------- Scoring helpers ----------
    @staticmethod
    def _clean_name(value: str) -> str:
        """Lowercase and strip punctuation from a plant name."""
        return re.sub(r"[^a-z ]", " ", value.lower()).strip()

    @classmethod
    def _plant_score(cls, doc: dict, plant: str) -> bool:
        """True if the disease's affected_plants include the chosen plant."""
        if not plant:
            return False
        affected = [cls._clean_name(str(a)) for a in doc.get("affected_plants", [])]
        return any(cls._plant_equivalent(a, plant) for a in affected if a)

    @classmethod
    def _plant_equivalent(cls, affected: str, plant: str) -> bool:
        """Check whether an affected_plants entry covers the given plant."""
        if not affected or not plant:
            return False
        if affected == plant:
            return True
        # Singular/plural handling, e.g. "tomatoes" vs "tomato".
        if affected.startswith(plant) and len(affected) <= len(plant) + 3:
            return True
        if plant.startswith(affected) and len(plant) <= len(affected) + 3:
            return True
        # Group membership, e.g. "Cucurbits" contains "cucumber".
        if plant in PLANT_GROUPS.get(affected, []):
            return True
        # Token overlap, e.g. "bell pepper" vs "pepper".
        affected_tokens = set(affected.split())
        plant_tokens = set(plant.split())
        return bool(affected_tokens & plant_tokens)

    @staticmethod
    def _score_symptoms(doc: dict, symptoms: list[str]) -> tuple[int, list[str]]:
        """Return (matched_count, matched_symptoms) for a disease document.

        A symptom keyword matches if it appears anywhere in the disease's searchable
        text (name, description, symptom list, causes, treatment).
        """
        if not symptoms:
            return 0, []

        haystack = " ".join(
            [
                str(doc.get("name", "")),
                str(doc.get("description", "")),
                " ".join(doc.get("symptoms", [])),
                " ".join(doc.get("causes", [])),
                " ".join(doc.get("treatment", [])),
            ]
        ).lower()

        matched = [s for s in symptoms if s in haystack]
        return len(matched), matched

    @staticmethod
    def _analyze_image(image_data: str) -> tuple[list[str], int]:
        """Decode a base64 image and run a tiny pixel heuristic.

        Returns (visual_signals, confidence_boost). The heuristic looks at colour
        ratios to guess visual cues such as yellowing, browning, a powdery (white)
        coating or healthy foliage. This is intentionally lightweight — a real ML
        model would replace this function without changing the rest of the flow.
        Any decode/analysis error degrades gracefully to ([], 0).
        """
        try:
            import base64
            import io

            from PIL import Image

            if "," in image_data:  # strip the "data:image/...;base64," prefix
                image_data = image_data.split(",", 1)[1]
            raw = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(raw)).convert("RGB")
            img.thumbnail((96, 96))
            pixels = list(img.getdata())
            n = max(1, len(pixels))

            yellows = browns = whites = greens = 0
            for r, g, b in pixels:
                hi, lo = max(r, g, b), min(r, g, b)
                sat = hi - lo
                if hi < 60:
                    continue  # too dark to classify reliably
                if sat < 55 and hi > 150:
                    whites += 1  # pale / whitish coating
                elif g >= r and g >= b and (g - r) > 10 and (g - b) > 10:
                    greens += 1  # healthy green foliage
                elif r >= 90 and g >= 90 and b < r - 20 and b < g - 20 and abs(r - g) < 40:
                    yellows += 1  # yellowed foliage (red+green high, blue low)
                elif r >= g and r >= b and (r - b) > 25:
                    browns += 1  # warm reds/oranges/browns

            signals: list[str] = []
            if yellows / n > 0.20:
                signals.append("yellowing")
            if browns / n > 0.15:
                signals.append("browning")
            if whites / n > 0.30:
                signals.append("powder")
            if greens / n > 0.45:
                signals.append("healthy foliage")

            boost = min(8, 2 + 2 * len(signals))
            return signals, boost
        except Exception:
            return [], 0

    @staticmethod
    def _confidence(matched_count: int, symptom_count: int, image_present: bool) -> int:
        """Map symptom overlap + image presence to a 0-100 confidence score."""
        if symptom_count == 0:
            base = 58 if image_present else 30
        else:
            ratio = matched_count / symptom_count
            base = 40 + ratio * 52

        if image_present:
            base += 6
        return max(0, min(CONFIDENCE_CAP, round(base)))

    @staticmethod
    def _expert_advice(
        confidence: int,
        severity: str,
        plant: str,
        plant_unknown: bool,
    ) -> tuple[bool, str | None]:
        """Recommend an expert consult when confidence is low or severity high."""
        reasons: list[str] = []
        severe = severity.lower() in {"severe", "high"}

        if plant_unknown:
            reasons.append(
                f"No disease in our database is known to affect {plant} — "
                "the diagnosis below is based on symptoms only and should be confirmed."
            )
        if confidence < LOW_CONFIDENCE:
            reasons.append(
                "Confidence is below 70% — this diagnosis should be confirmed by an expert."
            )
        if severe:
            reasons.append(
                "Severity is high — seek professional help immediately to limit spread."
            )
        return (len(reasons) > 0, " ".join(reasons) if reasons else None)

    @staticmethod
    def _unknown_report(
        payload: DetectRequest,
        symptoms: list[str],
        visual_signals: list[str] | None = None,
        plant: str = "",
    ) -> DetectResponse:
        """Report used when the knowledge base is empty or nothing matched."""
        return DetectResponse(
            disease_id=None,
            disease_name="Unknown",
            plant=payload.plant or None,
            confidence=0,
            severity="Unknown",
            matched_symptoms=[],
            unmatched_symptoms=symptoms,
            visual_signals=visual_signals or [],
            expert_recommended=True,
            consult_reason=(
                f"No disease could be identified for {plant} from the knowledge base."
                if plant
                else "No disease could be identified from the knowledge base."
            ),
            model_version=payload.model_version or MODEL_VERSION,
            predicted_at=datetime.utcnow(),
        )
