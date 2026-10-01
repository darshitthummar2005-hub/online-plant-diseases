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

try:  # Optional real image classifier; absent TensorFlow/model just logs.
    from ml.inference import Prediction, classify_image
except Exception as _ml_import_error:  # noqa: BLE001 - never block the API on ML
    Prediction = None  # type: ignore[assignment]

    def classify_image(*_args, **_kwargs):  # type: ignore[misc]
        return None

    logger.debug("ML inference unavailable: %s", _ml_import_error)

MODEL_VERSION = "ai-plant-doctor-v2"

# Confidence is reported as 0-100 (%).
CONFIDENCE_CAP = 97
LOW_CONFIDENCE = 70

# Strongly favour diseases that affect the selected plant.
PLANT_MATCH_SCORE = 60
PLANT_MISMATCH_PENALTY = 45
SYMPTOM_POINTS = 10

# Tie-breaking: a disease that lists the symptom explicitly is far better
# evidence than one that merely mentions it in passing.
SPECIFIC_SYMPTOM_BONUS = 8
# "Healthy Foliage" reference rows must not win by default.
GENERIC_HEALTHY_PENALTY = 12
# Confidence reported when only a photo was supplied and nothing matched.
LOW_IMAGE_ONLY_CONFIDENCE = 15
# Confidence ceiling when the only evidence is the colour heuristic. These cues
# ("browning", "powder") are far too generic to assert a specific disease.
IMAGE_ONLY_CONFIDENCE = 35

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
        # Symptoms the user actually ticked. Kept separate from anything the
        # image analysis infers, because a colour heuristic is weak evidence and
        # must never be scored like a human observation.
        user_symptoms = [s.strip().lower() for s in payload.symptoms if s.strip()]
        plant = self._clean_name(payload.plant or "")

        # Lightweight visual analysis of the attached image (if any).
        visual_signals: list[str] = []
        image_boost = 0
        has_image = bool(payload.image_present or payload.image_data or payload.image_url)
        if payload.image_data:
            visual_signals, image_boost = self._analyze_image(payload.image_data)

        symptoms = list(user_symptoms)
        for cue in visual_signals:
            if cue not in symptoms:
                symptoms.append(cue)

        # Real CNN prediction when a trained model is installed. This is the
        # authoritative signal; symptom matching remains the fallback.
        ml_prediction = self._ml_prediction(payload.image_data)
        if ml_prediction is not None:
            logger.info(
                "ML image prediction -> %s (%.1f%%)",
                ml_prediction.disease_name,
                ml_prediction.confidence,
            )

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
            # Ties must never be resolved by database order. Without this, every
            # image produced the same arbitrary "first document" answer because
            # a colour heuristic rarely matches any symptom keywords.
            score += self._specificity_bonus(doc, symptoms)
            if score > best_score:
                best = doc
                best_score = score
                best_matched = matched
                best_plant_match = p_match

        if best is None:
            logger.warning("Detection ran with an empty disease knowledge base")
            return self._unknown_report(payload, symptoms, visual_signals, plant)

        # A photo alone cannot identify a disease. Without selected symptoms or
        # a trained model there is no real evidence, so say so instead of
        # confidently naming whichever record happened to sort first.
        if not symptoms and ml_prediction is None:
            logger.info("Image-only detection with no symptoms: returning low confidence")
            return self._insufficient_evidence_report(payload, visual_signals, plant)

        # A trained CNN outranks keyword matching when it produced a result.
        ml_doc = None
        ml_plant_agrees = False
        if ml_prediction is not None:
            ml_doc = self._find_by_name(disease_docs, ml_prediction.disease_name)
            if ml_doc is not None:
                ml_plant_agrees = (not plant) or self._plant_score(ml_doc, plant) or (
                    bool(ml_prediction.crop) and plant == ml_prediction.crop
                )
                if ml_plant_agrees:
                    best = ml_doc
                    best_matched = self._score_symptoms(ml_doc, symptoms)[1]
                    best_plant_match = True
                else:
                    # Model says one crop, the user selected another. Trust the
                    # user's plant choice and keep the symptom-based match.
                    logger.info(
                        "ML predicted crop '%s' but user selected '%s'; keeping "
                        "symptom match (%s)",
                        ml_prediction.crop or "?",
                        plant,
                        best.get("name"),
                    )
                    ml_prediction = None

        plant_unknown = bool(plant) and not any_plant_match
        if ml_doc is not None and ml_prediction is not None:
            # Report the model's probability, penalised when the crop disagrees.
            confidence = (
                min(100, ml_prediction.confidence)
                if ml_plant_agrees
                else max(5, min(100, ml_prediction.confidence) - 25)
            )
        elif not user_symptoms:
            # Nothing was ticked by the user; only crude colour cues from the
            # photo. A single generic cue ("browning") matches many records, so
            # this is a weak lead, not a diagnosis.
            confidence = IMAGE_ONLY_CONFIDENCE
        elif best_plant_match or not plant:
            # Symptoms + plant agree (or no plant selected).
            confidence = min(
                100,
                self._confidence(
                    len([m for m in best_matched if m in user_symptoms]),
                    len(user_symptoms),
                    has_image,
                )
                + image_boost,
            )
        else:
            # Best match does not affect the chosen plant — down-weight heavily.
            confidence = min(
                100,
                self._confidence(
                    len([m for m in best_matched if m in user_symptoms]),
                    len(user_symptoms),
                    has_image,
                )
                - 15,
            )

        severity = str(best.get("severity") or "Moderate")
        expert, reason = self._expert_advice(confidence, severity, plant, plant_unknown)

        matched_set = set(best_matched)
        unmatched = [s for s in user_symptoms if s not in matched_set]
        if not user_symptoms:
            # The colour cues that led here, so the UI can show what was measured.
            unmatched = list(visual_signals)

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
            extra=self._merge_extra(best.get("extra"), ml_prediction, ml_plant_agrees),
        )

    # ---------- Helpers ----------
    @staticmethod
    def _ml_prediction(image_data: str | None):
        """Run the optional CNN over the image, tolerating every failure."""
        if not image_data or classify_image is None:
            return None
        try:
            return classify_image(image_data)
        except Exception as exc:  # noqa: BLE001 - ML must never fail a request
            logger.error("ML classification failed, using symptoms: %s", exc)
            return None

    @staticmethod
    def _find_by_name(docs: list[dict], name: str) -> dict | None:
        """Locate a knowledge-base document by (case-insensitive) name."""
        if not name:
            return None
        target = re.sub(r"[^a-z0-9]", "", name.lower())
        for doc in docs:
            candidate = re.sub(r"[^a-z0-9]", "", str(doc.get("name", "")).lower())
            if candidate == target:
                return doc
        return None

    @staticmethod
    def _merge_extra(
        base: dict | None, ml_prediction, ml_plant_agrees: bool
    ) -> dict:
        """Attach classifier details to the response without losing stored extras."""
        merged = dict(base or {})
        if ml_prediction is None:
            return merged
        merged["ml"] = {
            **ml_prediction.as_dict(),
            "plant_agrees": ml_plant_agrees,
            "alternatives": [
                {"disease_name": name, "confidence": round(conf, 2)}
                for name, conf in ml_prediction.alternatives
            ],
        }
        return merged

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
    def _specificity_bonus(doc: dict, symptoms: list[str]) -> int:
        """
        Deterministic tie-breaker that favours well-evidenced records.

        Rewards documents that actually discuss the reported symptoms and
        penalises generic "Healthy Foliage" entries, so an uninformative photo
        cannot always resolve to the same reference record.
        """
        bonus = 0
        haystack = " ".join(
            [
                str(doc.get("name", "")),
                str(doc.get("description", "")),
                " ".join(doc.get("symptoms", [])),
            ]
        ).lower()
        # Count symptom occurrences in the disease's own symptom list.
        listed = {str(s).lower() for s in doc.get("symptoms", [])}
        for symptom in symptoms:
            if symptom in listed:
                bonus += SPECIFIC_SYMPTOM_BONUS
            elif symptom in haystack:
                bonus += 1
        # "Healthy" reference entries must earn their place on real evidence.
        if "healthy" in str(doc.get("name", "")).lower() and not bonus:
            bonus -= GENERIC_HEALTHY_PENALTY
        return bonus

    def _insufficient_evidence_report(
        self, payload: DetectRequest, visual_signals: list[str], plant: str
    ) -> DetectResponse:
        """
        Honest response when only a photo was supplied.

        Reports the colours that were actually measured, asks for symptoms, and
        sets confidence low instead of guessing a disease.
        """
        observed = (
            "The uploaded photo was measured but no symptom description was given."
        )
        if visual_signals:
            observed += " Colour analysis suggests: " + ", ".join(visual_signals) + "."
        else:
            observed += " No clear colour signal was detected in the image."

        return DetectResponse(
            disease_id="",
            disease_name="More information needed",
            plant=payload.plant or None,
            confidence=LOW_IMAGE_ONLY_CONFIDENCE,
            severity="Unknown",
            matched_symptoms=[],
            unmatched_symptoms=visual_signals,
            visual_signals=visual_signals,
            expert_recommended=True,
            consult_reason=(
                observed
                + " Select the symptoms you can see (or train the image model) for a "
                "reliable diagnosis."
            ),
            model_version=payload.model_version or MODEL_VERSION,
            predicted_at=datetime.utcnow(),
            category=None,
            scientific_name=None,
            description=observed,
            symptoms=[],
            causes=[],
            treatment=[
                "Take a clear, well-lit close-up of the affected leaf",
                "Select the symptoms you observe from the checklist",
                "Retest after removing background objects from the photo",
            ],
            prevention=[],
            affected_plants=[],
            chemical_treatment=[],
            biological_treatment=[],
            organic_remedies=[],
            prevention_tips=[],
            fertilizer={},
            severity_levels={},
            weather_conditions={},
            emergency_actions=[],
            extra={"needs_more_info": True, "observed_signals": visual_signals},
        )

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
