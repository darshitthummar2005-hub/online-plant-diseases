"""Nutrient deficiency records (AI Plant Doctor knowledge base)."""

from app.seed_data_common import _disease

DEFICIENCY_DISEASES: list[dict] = [
    _disease(
        name="Phosphorus Deficiency",
        category="Deficiency",
        scientific_name="Nutrient deficiency (P)",
        severity="Moderate",
        description=(
            "Leaves turn dull, dark green or purple, often with purple veins and petioles, "
            "and the plant stays small with weak stems and poor flowering. Phosphorus is "
            "immobile in soil and locks up in cold, acidic or waterlogged conditions."
        ),
        symptoms=["purple leaves", "dark green leaves", "stunted growth", "poor flowering", "weak roots"],
        causes=["cold soil", "acidic soil", "low organic matter", "waterlogging", "over-limed soil"],
        treatment=["Bone meal or rock phosphate", "Warm the soil", "Correct soil pH"],
        prevention=["Feed balanced compost", "Test soil annually", "Mulch to warm soil"],
        affected_plants=["Tomato", "Corn", "Strawberry", "Lettuce", "Rose", "Leafy greens"],
        chemical_treatment=[
            {
                "name": "Superphosphate",
                "brand_names": ["Triple Superphosphate", "0-46-0"],
                "active_ingredients": ["Monocalcium phosphate"],
                "dosage": "30 g per m2 worked into the root zone",
                "safety_precautions": ["Do not place directly on roots", "Water in well"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Balanced NPK granules",
                "brand_names": ["Osmocote", "Dr. Earth 4-6-6"],
                "active_ingredients": ["NPK with high middle number"],
                "dosage": "Follow label for container/field size",
                "safety_precautions": ["Keep off foliage", "Water after application"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Mycorrhizal fungi",
                "type": "Beneficial microbe",
                "application": "Inoculate roots at planting",
                "when_to_apply": "Transplant time",
                "notes": "Fungal networks mine phosphorus for the roots.",
            },
            {
                "agent": "Phosphorus-solubilising bacteria",
                "type": "Beneficial microbe",
                "application": "Soil drench at planting",
                "when_to_apply": "Planting time",
                "notes": "Mobilises locked-up soil phosphorus.",
            },
        ],
        organic_remedies=[
            {
                "name": "Bone meal",
                "recipe": "Handful of bone meal per plant",
                "application": "Work into the root zone",
                "frequency": "At planting",
            },
            {
                "name": "Rock phosphate",
                "recipe": "200 g per m2",
                "application": "Rake into topsoil",
                "frequency": "Yearly",
            },
        ],
        prevention_tips=[
            {"category": "Soil pH", "title": "Keep pH 6.0-6.8", "description": "Phosphorus is locked up in acid and alkaline soils."},
            {"category": "Nutrient management", "title": "Feed balanced compost", "description": "Compost releases phosphorus slowly and steadily."},
            {"category": "Irrigation", "title": "Avoid waterlogging", "description": "Cold, wet soil blocks phosphorus uptake."},
            {"category": "Mulching", "title": "Mulch to warm soil", "description": "Warm roots take up phosphorus faster."},
        ],
        fertilizer={
            "organic": ["Bone meal", "Rock phosphate", "Manure", "Compost"],
            "micronutrients": ["Zinc (works with P uptake)"],
            "npk": "High-P feed, e.g., 5-20-10 at planting",
            "soil_improvement": ["Add organic matter to release bound phosphorus"],
        },
        severity_levels={
            "mild": "Slight purple tint on older leaves.",
            "moderate": "Purple veins and petioles, slow growth.",
            "severe": "Severe stunting, dark leaves, few flowers.",
        },
        weather_conditions={
            "humidity": "Not disease-related",
            "temperature": "Cold soil blocks P uptake",
            "rainfall": "Waterlogging locks up phosphorus",
        },
        emergency_actions=[
            "Foliar-spray a phosphate feed for a fast response.",
            "Warm and drain the soil around the plants.",
            "Re-test soil pH and adjust towards 6.5.",
        ],
    ),
    _disease(
        name="Magnesium Deficiency",
        category="Deficiency",
        scientific_name="Nutrient deficiency (Mg)",
        severity="Moderate",
        description=(
            "Yellowing between the veins of older leaves while the veins stay green, often "
            "with a purple tint and curling of leaf edges. Magnesium is mobile, so the "
            "pattern starts on the oldest leaves and moves upward."
        ),
        symptoms=["yellow between veins", "green veins", "purple leaf edges", "curled leaf edges", "older leaf yellowing"],
        causes=["sandy soil", "heavy rain leaching", "excess potassium", "acidic soil"],
        treatment=["Epsom salt spray", "Dolomite lime", "Balanced feed"],
        prevention=["Feed balanced compost", "Test soil", "Avoid excess potassium"],
        affected_plants=["Tomato", "Potato", "Pepper", "Rose", "Cucumber", "Citrus"],
        chemical_treatment=[
            {
                "name": "Magnesium sulphate (Epsom salts)",
                "brand_names": ["Epsom Salts"],
                "active_ingredients": ["Magnesium sulphate 10% Mg"],
                "dosage": "20 g per litre as foliar spray, or 30 g per m2 to soil",
                "safety_precautions": ["Foliar spray early morning", "Do not over-apply"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Dolomitic lime",
                "brand_names": ["Dolomite"],
                "active_ingredients": ["Calcium magnesium carbonate"],
                "dosage": "100-150 g per m2 depending on soil test",
                "safety_precautions": ["Test pH before applying", "Do not over-lime"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Compost + mulch",
                "type": "Organic amendment",
                "application": "Mulch and top-dress with compost",
                "when_to_apply": "Season start and mid-season",
                "notes": "Slowly releases magnesium and holds moisture.",
            },
            {
                "agent": "Worm castings",
                "type": "Organic amendment",
                "application": "Mix into the root zone",
                "when_to_apply": "At planting and monthly",
                "notes": "Rich in available magnesium and micronutrients.",
            },
        ],
        organic_remedies=[
            {
                "name": "Epsom salt spray",
                "recipe": "20 g Epsom salts + 1 L water",
                "application": "Spray foliage",
                "frequency": "Every 2 weeks",
            },
            {
                "name": "Kelp extract foliar",
                "recipe": "Kelp extract at label dose",
                "application": "Spray leaves",
                "frequency": "Every 10 days",
            },
        ],
        prevention_tips=[
            {"category": "Nutrient management", "title": "Balance potassium", "description": "Too much K blocks magnesium uptake."},
            {"category": "Soil testing", "title": "Test soil Mg levels", "description": "Correct before symptoms appear."},
            {"category": "Irrigation", "title": "Mulch to hold moisture", "description": "Prevents magnesium leaching from sandy soil."},
            {"category": "Fertilisation", "title": "Feed balanced compost", "description": "Compost supplies magnesium slowly."},
        ],
        fertilizer={
            "organic": ["Epsom salts", "Dolomite", "Worm castings", "Compost"],
            "micronutrients": ["Magnesium (foliar)"],
            "npk": "Balanced feed; avoid high-K formulas",
            "soil_improvement": ["Add dolomite to acid, sandy soils"],
        },
        severity_levels={
            "mild": "Slight interveinal yellowing on old leaves.",
            "moderate": "Clear yellowing with green veins.",
            "severe": "Widespread yellowing, purple edges, leaf drop.",
        },
        weather_conditions={
            "humidity": "Not disease-related",
            "temperature": "Cold soil slows uptake",
            "rainfall": "Heavy rain leaches magnesium",
        },
        emergency_actions=[
            "Foliar-spray Epsom salts immediately for fast green-up.",
            "Apply dolomite to correct soil reserves.",
            "Re-test soil after two weeks.",
        ],
    ),
    _disease(
        name="Calcium Deficiency (Blossom End Rot)",
        category="Deficiency",
        scientific_name="Nutrient deficiency (Ca)",
        severity="Moderate",
        description=(
            "Dark, sunken, leathery patches on the blossom end of tomato, pepper and "
            "squash fruit. Caused by calcium not reaching the growing fruit, usually from "
            "uneven watering rather than low soil calcium."
        ),
        symptoms=["sunken dark fruit patches", "blossom end rot", "curled young leaves", "stunted new growth"],
        causes=["irregular watering", "excess nitrogen", "root damage", "cold or dry soil"],
        treatment=["Even watering", "Calcium foliar spray", "Mulch the soil"],
        prevention=["Water consistently", "Mulch to hold moisture", "Avoid nitrogen excess"],
        affected_plants=["Tomato", "Pepper", "Squash", "Eggplant", "Melon", "Cabbage"],
        chemical_treatment=[
            {
                "name": "Calcium nitrate foliar",
                "brand_names": ["YaraLiva", "Tropicote"],
                "active_ingredients": ["Calcium nitrate 15.5% Ca"],
                "dosage": "10 g per litre as foliar spray weekly",
                "safety_precautions": ["Do not mix with phosphates", "Spray early morning"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Gypsum (soil)",
                "brand_names": ["Pelletized gypsum"],
                "active_ingredients": ["Calcium sulphate"],
                "dosage": "200-300 g per m2 worked into soil",
                "safety_precautions": ["Do not use on saline soils", "Water in well"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Compost + mulch",
                "type": "Organic amendment",
                "application": "Mulch 5-8 cm around plants",
                "when_to_apply": "After transplanting",
                "notes": "Steadies soil moisture so calcium moves into fruit.",
            },
            {
                "agent": "Worm castings",
                "type": "Organic amendment",
                "application": "Mix into the planting hole",
                "when_to_apply": "At planting",
                "notes": "Adds plant-available calcium near the roots.",
            },
        ],
        organic_remedies=[
            {
                "name": "Crushed eggshells",
                "recipe": "Powdered eggshells",
                "application": "Work into the root zone",
                "frequency": "At planting and monthly",
            },
            {
                "name": "Even watering schedule",
                "recipe": "Consistent moisture, no dry-wet cycles",
                "application": "Water 2-3 times weekly in hot weather",
                "frequency": "Ongoing",
            },
        ],
        prevention_tips=[
            {"category": "Irrigation", "title": "Water consistently", "description": "Fluctuating moisture is the #1 cause of blossom end rot."},
            {"category": "Mulching", "title": "Mulch to hold moisture", "description": "Straw mulch steadies soil water."},
            {"category": "Nutrient management", "title": "Avoid nitrogen excess", "description": "Fast lush growth outstrips calcium supply."},
            {"category": "Soil testing", "title": "Test soil calcium", "description": "Low pH soils are often low in calcium."},
        ],
        fertilizer={
            "organic": ["Crushed eggshells", "Gypsum", "Worm castings", "Compost"],
            "micronutrients": ["Calcium (foliar)"],
            "npk": "Balanced feed; avoid high nitrogen during fruiting",
            "soil_improvement": ["Mulch heavily to steady soil moisture"],
        },
        severity_levels={
            "mild": "Small brown patch on one fruit.",
            "moderate": "Sunken rot on several fruit.",
            "severe": "Many fruit affected, severe blossom end rot.",
        },
        weather_conditions={
            "humidity": "Not disease-related",
            "temperature": "Heat waves and dry soil worsen it",
            "rainfall": "Dry spells followed by heavy watering trigger it",
        },
        emergency_actions=[
            "Even out watering immediately - do not let soil dry out.",
            "Foliar-spray calcium nitrate weekly.",
            "Pick and remove affected fruit to refocus plant energy.",
        ],
    ),
    _disease(
        name="Zinc Deficiency",
        category="Deficiency",
        scientific_name="Nutrient deficiency (Zn)",
        severity="Mild",
        description=(
            "New leaves grow small, narrow and bunched in a rosette, with yellowing between "
            "the veins and shortened internodes. Zinc is needed for growth hormones; "
            "deficiency causes little-leaf and rosetting in fruit trees and corn."
        ),
        symptoms=["small narrow leaves", "leaf rosetting", "short internodes", "yellow between veins", "little leaf"],
        causes=["alkaline soil", "high phosphorus soil", "waterlogged soil", "heavy liming"],
        treatment=["Zinc sulphate foliar", "Correct soil pH", "Balanced feed"],
        prevention=["Test soil", "Avoid over-liming", "Balanced fertilisation"],
        affected_plants=["Corn", "Citrus", "Grape", "Onion", "Bean", "Apple"],
        chemical_treatment=[
            {
                "name": "Zinc sulphate foliar",
                "brand_names": ["Zinc sulphate 36%"],
                "active_ingredients": ["Zinc sulphate heptahydrate"],
                "dosage": "5 g per litre as foliar spray",
                "safety_precautions": ["Do not mix with phosphates", "Spray early morning"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Chelated zinc",
                "brand_names": ["Zinc EDTA"],
                "active_ingredients": ["Zn-EDTA"],
                "dosage": "2 g per litre foliar or soil drench",
                "safety_precautions": ["Follow label rates", "Keep from waterways"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Compost + organic matter",
                "type": "Organic amendment",
                "application": "Add compost to the root zone",
                "when_to_apply": "Season start",
                "notes": "Releases zinc slowly and improves uptake.",
            },
            {
                "agent": "Mycorrhizal fungi",
                "type": "Beneficial microbe",
                "application": "Inoculate at planting",
                "when_to_apply": "Transplant time",
                "notes": "Improves micronutrient reach of the roots.",
            },
        ],
        organic_remedies=[
            {
                "name": "Kelp meal",
                "recipe": "Handful per plant",
                "application": "Work into the root zone",
                "frequency": "Monthly",
            },
            {
                "name": "Compost tea foliar",
                "recipe": "Brewed compost tea (micronutrient-rich)",
                "application": "Spray new growth",
                "frequency": "Every 2 weeks",
            },
        ],
        prevention_tips=[
            {"category": "Soil pH", "title": "Keep pH below 7", "description": "Alkaline soil locks up zinc."},
            {"category": "Nutrient management", "title": "Avoid excess phosphorus", "description": "High P precipitates zinc in the soil."},
            {"category": "Soil testing", "title": "Test for zinc", "description": "Correct before symptoms appear."},
            {"category": "Fertilisation", "title": "Feed micronutrient-rich compost", "description": "Compost and kelp supply zinc steadily."},
        ],
        fertilizer={
            "organic": ["Kelp meal", "Compost", "Worm castings"],
            "micronutrients": ["Zinc (sulphate or EDTA)"],
            "npk": "Low-phosphorus balanced feed",
            "soil_improvement": ["Acidify gently if pH is high"],
        },
        severity_levels={
            "mild": "Slight small-leaf on new growth.",
            "moderate": "Rosetting and yellowing between veins.",
            "severe": "Severe little-leaf, dead shoot tips.",
        },
        weather_conditions={
            "humidity": "Not disease-related",
            "temperature": "Cold, wet soil slows uptake",
            "rainfall": "Waterlogging worsens zinc lock-up",
        },
        emergency_actions=[
            "Foliar-spray zinc sulphate immediately.",
            "Check and correct soil pH towards 6.5.",
            "Improve drainage in the root zone.",
        ],
    ),
    _disease(
        name="Boron Deficiency",
        category="Deficiency",
        scientific_name="Nutrient deficiency (B)",
        severity="Moderate",
        description=(
            "New growth dies back, stems crack and cork, and fruit develops hollow or "
            "discoloured tissue. Boron is essential for cell walls and pollen; deficiency "
            "shows as distorted tips, poor fruit set and cracked bark."
        ),
        symptoms=["dead growing tips", "cracked stems", "corky fruit", "poor fruit set", "distorted new growth"],
        causes=["sandy soil", "heavy leaching", "over-limed soil", "dry spells"],
        treatment=["Borax solution", "Compost + mulch", "Correct pH"],
        prevention=["Test soil", "Mulch to hold moisture", "Avoid over-liming"],
        affected_plants=["Apple", "Grape", "Cauliflower", "Tomato", "Strawberry", "Beet"],
        chemical_treatment=[
            {
                "name": "Borax (soil)",
                "brand_names": ["Borax 20 Mule Team"],
                "active_ingredients": ["Sodium borate 11% B"],
                "dosage": "Small amounts only - 5-10 g per 10 m2",
                "safety_precautions": ["Boron is toxic in excess - apply precisely", "Evenly mix with soil"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Soluble boron foliar",
                "brand_names": ["Solubor"],
                "active_ingredients": ["Sodium borate 20% B"],
                "dosage": "1 g per litre as foliar spray at bloom",
                "safety_precautions": ["Spray sparingly - overdose burns leaves", "Do not exceed label"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Compost + mulch",
                "type": "Organic amendment",
                "application": "Mulch and top-dress with compost",
                "when_to_apply": "Season start",
                "notes": "Holds moisture and releases boron slowly.",
            },
            {
                "agent": "Worm castings",
                "type": "Organic amendment",
                "application": "Mix into the root zone",
                "when_to_apply": "At planting and monthly",
                "notes": "Supplies trace boron in a balanced form.",
            },
        ],
        organic_remedies=[
            {
                "name": "Dilute borax drench",
                "recipe": "1 tsp borax in 10 L water",
                "application": "Water around the drip line",
                "frequency": "Once per season",
            },
            {
                "name": "Compost tea foliar",
                "recipe": "Brewed compost tea",
                "application": "Spray at flowering",
                "frequency": "At bloom",
            },
        ],
        prevention_tips=[
            {"category": "Soil testing", "title": "Test soil boron", "description": "Boron range is narrow - test before correcting."},
            {"category": "Irrigation", "title": "Mulch to hold moisture", "description": "Dry soil blocks boron uptake."},
            {"category": "Soil pH", "title": "Avoid over-liming", "description": "High pH reduces boron availability."},
            {"category": "Fertilisation", "title": "Feed compost", "description": "Compost supplies boron safely and slowly."},
        ],
        fertilizer={
            "organic": ["Compost", "Worm castings", "Kelp meal"],
            "micronutrients": ["Boron (small precise doses)"],
            "npk": "Balanced feed",
            "soil_improvement": ["Mulch and maintain organic matter"],
        },
        severity_levels={
            "mild": "Slight tip distortion on new growth.",
            "moderate": "Cracked stems, corky fruit, poor set.",
            "severe": "Dieback of growing tips and fruit breakdown.",
        },
        weather_conditions={
            "humidity": "Not disease-related",
            "temperature": "Dry, hot spells worsen symptoms",
            "rainfall": "Heavy rain leaches boron",
        },
        emergency_actions=[
            "Foliar-spray a dilute boron feed at bloom.",
            "Mulch immediately to steady soil moisture.",
            "Re-test soil before any further boron application.",
        ],
    ),
    _disease(
        name="Sulfur Deficiency",
        category="Deficiency",
        scientific_name="Nutrient deficiency (S)",
        severity="Mild",
        description=(
            "Uniform yellowing of new leaves first (unlike nitrogen, which yellows old "
            "leaves first), with thin stems and slow growth. Sulfur is part of amino acids "
            "and enzymes; it is most common in sandy, low-organic soils."
        ),
        symptoms=["yellow new leaves", "uniform yellowing", "thin stems", "slow growth", "pale young growth"],
        causes=["sandy soil", "low organic matter", "heavy leaching", "low-sulfur fertilisers"],
        treatment=["Gypsum or sulfur fertiliser", "Compost", "Foliar sulfur"],
        prevention=["Feed compost", "Use gypsum", "Test soil"],
        affected_plants=["Brassicas", "Onion", "Garlic", "Grape", "Leafy greens", "Corn"],
        chemical_treatment=[
            {
                "name": "Gypsum (calcium sulfate)",
                "brand_names": ["Pelletized gypsum"],
                "active_ingredients": ["Calcium sulphate"],
                "dosage": "100-200 g per m2 worked in",
                "safety_precautions": ["Do not use on saline soils", "Water in well"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Ammonium sulfate",
                "brand_names": ["Sulfate of ammonia"],
                "active_ingredients": ["Ammonium sulphate 24% S"],
                "dosage": "20-30 g per m2",
                "safety_precautions": ["Water in after application", "Keep off foliage"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Compost + organic matter",
                "type": "Organic amendment",
                "application": "Top-dress with compost",
                "when_to_apply": "Season start",
                "notes": "Builds soil sulfur reserves slowly.",
            },
            {
                "agent": "Green manure (mustard, clover)",
                "type": "Cover crop",
                "application": "Grow and turn under before planting",
                "when_to_apply": "Previous season",
                "notes": "Adds sulfur and organic matter to the soil.",
            },
        ],
        organic_remedies=[
            {
                "name": "Gypsum application",
                "recipe": "Sprinkle 100 g per m2",
                "application": "Rake into the topsoil",
                "frequency": "Once per season",
            },
            {
                "name": "Compost top-dress",
                "recipe": "2-3 cm of mature compost",
                "application": "Spread around plants",
                "frequency": "Season start",
            },
        ],
        prevention_tips=[
            {"category": "Nutrient management", "title": "Feed compost", "description": "Compost supplies sulfur slowly and safely."},
            {"category": "Soil testing", "title": "Test soil sulfur", "description": "Correct before symptoms appear."},
            {"category": "Cover crops", "title": "Grow brassica green manures", "description": "Mustard and radish add sulfur to the soil."},
            {"category": "Fertilisation", "title": "Choose sulfur-containing feeds", "description": "Avoid pure NPK with no sulfur for brassicas."},
        ],
        fertilizer={
            "organic": ["Gypsum", "Compost", "Manure"],
            "micronutrients": ["Sulfur"],
            "npk": "Include sulfur-bearing sources in the feed",
            "soil_improvement": ["Add organic matter to sandy soils"],
        },
        severity_levels={
            "mild": "Slight yellowing of newest leaves.",
            "moderate": "Uniform yellow new growth, thin stems.",
            "severe": "Pale stunted plants with delayed maturity.",
        },
        weather_conditions={
            "humidity": "Not disease-related",
            "temperature": "Cool, wet soil slows uptake",
            "rainfall": "Heavy rain leaches sulfur",
        },
        emergency_actions=[
            "Foliar-spray a sulfur feed for fast green-up.",
            "Apply gypsum to the soil.",
            "Top-dress with compost to rebuild reserves.",
        ],
    ),
]
