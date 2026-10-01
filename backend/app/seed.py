"""
Database seeding (AI Plant Doctor knowledge base).

Populates the plant_diseases collection with a rich starter knowledge base. Each
disease carries chemical / biological / organic treatments, prevention tips,
fertilizer recommendations, severity levels, weather guidance and emergency
actions — everything the detection report needs.

Seeding strategy:
  - Uses `SEED_VERSION` so existing databases are upgraded in place: every seed
    disease is upserted by name with `replace_one(upsert=True)`, so old docs get
    the new rich fields while custom admin entries are left untouched.
  - A default admin user is created from environment variables if configured.
  - Any number of extra admins can be configured with ADMIN_ACCOUNTS (a JSON
    array in `.env`). All admin passwords are bcrypt-hashed on creation.

Set ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD in `.env` to create an admin
account on first boot, or ADMIN_ACCOUNTS to create several at once.
"""

from datetime import datetime

from app.config import get_settings
from app.database import Database, get_database
from app.seed_data_bacterial import BACTERIAL_DISEASES
from app.seed_data_deficiency import DEFICIENCY_DISEASES
from app.seed_data_fungal import FUNGAL_DISEASES
from app.seed_data_pest import PEST_DISEASES
from app.seed_data_viral import VIRAL_DISEASES
from app.utils.logger import get_logger

logger = get_logger(__name__)
_settings = get_settings()

SEED_VERSION = 4

# --------------------------------------------------------------------------
# Rich disease knowledge base
#
# Base records live here; the expanded records from the seed_data_*.py
# modules are merged in after this list.
# --------------------------------------------------------------------------
SEED_DISEASES: list[dict] = [
    {
        "name": "Powdery Mildew",
        "category": "Fungal",
        "scientific_name": "Erysiphales spp.",
        "severity": "Moderate",
        "description": (
            "White, powdery fungal coating on leaves, stems and buds that blocks "
            "photosynthesis and weakens the plant. Spreads fast in warm, humid air "
            "with poor circulation."
        ),
        "symptoms": ["white powder", "dusty spots", "stunted growth", "curled leaves", "yellowing"],
        "causes": ["high humidity", "poor airflow", "overhead watering", "crowded planting"],
        "treatment": [
            "Baking soda + soap spray weekly",
            "Neem oil at dusk",
            "Sulfur or potassium bicarbonate fungicide",
        ],
        "prevention": ["Space plants well", "Water at the base", "Choose resistant varieties"],
        "affected_plants": ["Roses", "Cucurbits", "Grapes", "Cucumber", "Zinnia"],
        "chemical_treatment": [
            {
                "name": "Sulfur fungicide",
                "brand_names": ["Safer Brand Garden Fungicide", "Bonide Sulfur"],
                "active_ingredients": ["Micronized sulfur (80% WDG)"],
                "dosage": "2–4 g per litre of water (foliar spray every 7–10 days)",
                "safety_precautions": [
                    "Do not apply within 2 weeks of an oil-based spray.",
                    "Avoid spraying in temperatures above 30°C.",
                    "Wear a mask, gloves and goggles while spraying.",
                ],
                "waiting_period": "1 day before harvest",
            },
            {
                "name": "Potassium bicarbonate fungicide",
                "brand_names": ["GreenCure", "MilStop"],
                "active_ingredients": ["Potassium bicarbonate (85%)"],
                "dosage": "4 g per litre of water; repeat every 7 days",
                "safety_precautions": ["Test on a small leaf first", "Avoid direct sun application"],
                "waiting_period": "0 days",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray at 2 g/L every 7 days at first signs",
                "when_to_apply": "Early morning, before dew dries",
                "notes": "Colonises the leaf surface and out-competes the mildew fungus.",
            },
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench + foliar spray at 5 g/L",
                "when_to_apply": "At transplanting and monthly during humid weather",
                "notes": "Boosts root immunity and suppresses soil-borne spores.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 tsp liquid soap + 1 L water",
                "application": "Spray all leaf surfaces every 7 days",
                "frequency": "Weekly until symptoms clear",
            },
            {
                "name": "Neem oil spray",
                "recipe": "2 ml cold-pressed neem oil + 1 L warm water + few drops of soap",
                "application": "Spray at dusk, covering both leaf sides",
                "frequency": "Every 7–10 days",
            },
            {
                "name": "Milk spray",
                "recipe": "1 part milk mixed with 9 parts water",
                "application": "Spray affected foliage twice a week",
                "frequency": "Twice weekly",
            },
        ],
        "prevention_tips": [
            {"category": "Spacing", "title": "Space plants for airflow", "description": "Keep 30–45 cm between plants so air circulates and leaves dry fast."},
            {"category": "Irrigation", "title": "Water at the base", "description": "Avoid wetting leaves; use drip irrigation in the morning."},
            {"category": "Resistant varieties", "title": "Grow resistant cultivars", "description": "Choose mildew-tolerant tomato, cucumber and rose varieties."},
            {"category": "Nutrient management", "title": "Avoid excess nitrogen", "description": "Over-fertilising produces soft growth that mildew loves."},
            {"category": "Field sanitation", "title": "Remove infected debris", "description": "Pull and bin infected leaves; do not compost them."},
        ],
        "fertilizer": {
            "organic": ["Composted manure", "Fish emulsion (diluted)"],
            "micronutrients": ["Silicon (potassium silicate)"],
            "npk": "Low-nitrogen feed 5-10-10 once disease appears",
            "soil_improvement": ["Add compost to boost soil biology and drainage"],
        },
        "severity_levels": {
            "mild": "A few white patches on upper leaves; plant vigour unaffected.",
            "moderate": "Powder covers up to 40% of foliage; leaves begin to curl.",
            "severe": "Dense coating across most leaves; yellowing, leaf drop and fruit distortion.",
        },
        "weather_conditions": {
            "humidity": "High humidity (>60%) — risk is highest at 55–70%",
            "temperature": "18–27°C favours spread; outbreaks pause above 30°C",
            "rainfall": "Dry periods with heavy morning dew still trigger outbreaks",
        },
        "emergency_actions": [
            "Strip the most infected leaves and bag them immediately.",
            "Apply a potassium bicarbonate fungicide the same day.",
            "Remove badly hit plants and disinfect tools with 70% alcohol.",
        ],
    },
    {
        "name": "Leaf Spot (Septoria)",
        "category": "Fungal",
        "scientific_name": "Septoria lycopersici",
        "severity": "Moderate",
        "description": (
            "Brown circular spots with darker rings that start on the oldest leaves "
            "and move upward. Heavy spotting causes premature leaf drop and reduced yield."
        ),
        "symptoms": ["brown spots", "rings on leaves", "yellowing", "leaf drop"],
        "causes": ["wet foliage", "soil splash", "infected debris", "overhead watering"],
        "treatment": ["Remove infected leaves", "Copper-based fungicide", "Mulch the soil"],
        "prevention": ["Water at the base", "Rotate crops", "Clean tools between plants"],
        "affected_plants": ["Tomatoes", "Leafy greens", "Potatoes"],
        "chemical_treatment": [
            {
                "name": "Copper fungicide",
                "brand_names": ["Bonide Copper Fungicide", "Cueva", "Captain Jack"],
                "active_ingredients": ["Copper octanoate (copper soap)", "Copper hydroxide"],
                "dosage": "15–30 ml per litre of water every 7–10 days",
                "safety_precautions": [
                    "Copper can build up in soil — rotate with other fungicides.",
                    "Wear gloves and avoid spray drift to water bodies.",
                ],
                "waiting_period": "1 day before harvest",
            },
            {
                "name": "Chlorothalonil fungicide",
                "brand_names": ["Daconil", "Bonide Fung-onil"],
                "active_ingredients": ["Chlorothalonil 54%"],
                "dosage": "15 ml per 4 litres; cover both leaf surfaces",
                "safety_precautions": ["Highly toxic to fish — keep away from drains", "Wear full protective gear"],
                "waiting_period": "7 days before harvest",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Bacillus amyloliquefaciens",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L every 7 days at symptom onset",
                "when_to_apply": "Evening to avoid UV degradation",
                "notes": "Suppresses fungal spore germination on the leaf surface.",
            },
            {
                "agent": "Trichoderma viride",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L at transplant and after heavy rain",
                "when_to_apply": "After rainfall or irrigation",
                "notes": "Reduces soil-borne inoculum that splashes onto lower leaves.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Baking soda + oil spray",
                "recipe": "1 tbsp baking soda + 1 tbsp vegetable oil + 1 tsp soap + 1 L water",
                "application": "Spray every 7 days, especially the lower leaves",
                "frequency": "Weekly",
            },
            {
                "name": "Neem oil spray",
                "recipe": "2 ml neem oil + 1 L water + few drops of soap",
                "application": "Spray at dusk",
                "frequency": "Every 7–10 days",
            },
            {
                "name": "Compost tea foliar feed",
                "recipe": "Steep 1 cup mature compost in 1 L water for 24 h, strain",
                "application": "Spray on foliage to boost natural leaf resistance",
                "frequency": "Every 2 weeks",
            },
        ],
        "prevention_tips": [
            {"category": "Crop rotation", "title": "Rotate away from nightshades", "description": "Avoid planting tomatoes/potatoes in the same bed for 2–3 years."},
            {"category": "Irrigation", "title": "Water at the soil line", "description": "Drip or soaker hose keeps foliage dry and stops splash."},
            {"category": "Field sanitation", "title": "Clean up old vines", "description": "Remove and destroy infected debris at season end."},
            {"category": "Nutrient management", "title": "Feed balanced compost", "description": "Healthy plants outgrow infection faster."},
            {"category": "Spacing", "title": "Stake and prune", "description": "Prune lower leaves and keep plants off the ground."},
            {"category": "Resistant varieties", "title": "Choose tolerant hybrids", "description": "Many tomato hybrids have Septoria resistance."},
        ],
        "fertilizer": {
            "organic": ["Well-rotted compost", "Seaweed extract"],
            "micronutrients": ["Zinc", "Manganese foliar feed"],
            "npk": "Balanced 10-10-10 during fruit set",
            "soil_improvement": ["Mulch 5–8 cm to stop soil splash"],
        },
        "severity_levels": {
            "mild": "Scattered spots on older leaves only.",
            "moderate": "Spots on 30–50% of foliage with some yellowing.",
            "severe": "Widespread leaf drop, exposed fruit and severe defoliation.",
        },
        "weather_conditions": {
            "humidity": "Humid, wet foliage (>85% RH on leaves)",
            "temperature": "20–27°C is the infection window",
            "rainfall": "Rain or heavy overhead watering spreads spores",
        },
        "emergency_actions": [
            "Prune all symptomatic lower leaves and dispose of them in sealed bags.",
            "Apply a copper fungicide immediately, repeat after 7 days.",
            "If defoliation exceeds 50%, treat the crop as lost and sanitise the bed.",
        ],
    },
    {
        "name": "Rust",
        "category": "Fungal",
        "scientific_name": "Puccinia spp.",
        "severity": "Severe",
        "description": (
            "Orange-to-rust coloured pustules, mainly on the underside of leaves, that "
            "burst open to release spores. Severe attacks cause yellowing and complete leaf drop."
        ),
        "symptoms": ["orange pustules", "rust spots", "leaf drop", "yellowing", "brown spots"],
        "causes": ["wet leaves", "crowded growth", "low airflow", "infected plant debris"],
        "treatment": ["Remove infected foliage", "Sulfur or myclobutanil fungicide"],
        "prevention": ["Water early in the day", "Prune for airflow"],
        "affected_plants": ["Roses", "Beans", "Asparagus", "Wheat", "Geranium"],
        "chemical_treatment": [
            {
                "name": "Myclobutanil fungicide",
                "brand_names": ["Immunox", "Monterey Fungi-Max"],
                "active_ingredients": ["Myclobutanil 1.55%"],
                "dosage": "15 ml per 4 L water every 14 days",
                "safety_precautions": ["Avoid spraying flowers in bloom", "Wear long sleeves and gloves"],
                "waiting_period": "30 days before harvest",
            },
            {
                "name": "Sulfur fungicide",
                "brand_names": ["Safer Brand", "Bonide Sulfur"],
                "active_ingredients": ["Micronized sulfur"],
                "dosage": "3 g per litre of water weekly",
                "safety_precautions": ["Do not apply in heat above 30°C", "Keep away from skin and eyes"],
                "waiting_period": "1 day",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L weekly during outbreak",
                "when_to_apply": "Morning after dew dries",
                "notes": "Prevents spore germination on healthy tissue.",
            },
            {
                "agent": "Trichoderma asperellum",
                "type": "Beneficial microbe",
                "application": "Foliar spray 5 g/L every 10 days",
                "when_to_apply": "During humid spells",
                "notes": "Suppresses rust spore build-up on leaf surfaces.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem oil + 1 L water + soap emulsifier",
                "application": "Spray undersides of leaves at dusk",
                "frequency": "Every 7 days",
            },
            {
                "name": "Garlic + chilli spray",
                "recipe": "Blend 6 garlic cloves + 2 chillies in 1 L water, steep overnight, strain",
                "application": "Spray foliage weekly",
                "frequency": "Weekly",
            },
            {
                "name": "Baking soda spray",
                "recipe": "1 tsp baking soda + 1 L water + soap",
                "application": "Spray on pustule spots",
                "frequency": "Every 5–7 days",
            },
        ],
        "prevention_tips": [
            {"category": "Irrigation", "title": "Water in the morning", "description": "Leaves dry before nightfall, cutting spore germination time."},
            {"category": "Spacing", "title": "Prune for airflow", "description": "Open the canopy so sunlight dries stems and leaves."},
            {"category": "Field sanitation", "title": "Clear fallen leaves", "description": "Rust survives on debris — collect and burn it."},
            {"category": "Crop rotation", "title": "Rotate susceptible crops", "description": "Do not grow beans/roses on the same ground yearly."},
            {"category": "Resistant varieties", "title": "Plant rust-resistant cultivars", "description": "Many rose and bean varieties are bred for resistance."},
        ],
        "fertilizer": {
            "organic": ["Compost", "Kelp meal"],
            "micronutrients": ["Potassium silicate foliar"],
            "npk": "Moderate nitrogen; boost potassium (0-10-20)",
            "soil_improvement": ["Maintain good drainage to reduce standing wetness"],
        },
        "severity_levels": {
            "mild": "A few pustules on lower leaves.",
            "moderate": "Pustules spreading to upper leaves with mild yellowing.",
            "severe": "Heavy pustule cover, curling and premature leaf drop.",
        },
        "weather_conditions": {
            "humidity": "High humidity with free water on leaves",
            "temperature": "15–25°C is ideal for rust",
            "rainfall": "Rainy spells with morning dew drive outbreaks",
        },
        "emergency_actions": [
            "Strip infected leaves into sealed bags — do not compost.",
            "Apply myclobutanil fungicide immediately, reapply after 14 days.",
            "Quarantine new plants away from the outbreak for 2 weeks.",
        ],
    },
    {
        "name": "Early Blight",
        "category": "Fungal",
        "scientific_name": "Alternaria solani",
        "severity": "Severe",
        "description": (
            "Dark, target-like lesions with concentric rings appear on older leaves first, "
            "spreading upward. Defoliation reduces photosynthesis and yields drop sharply."
        ),
        "symptoms": ["dark spots", "target rings", "yellow halo", "lower leaf yellowing", "brown spots"],
        "causes": ["Alternaria solani", "wet foliage", "soil splash", "nutrient stress"],
        "treatment": ["Copper fungicide", "Stake plants for airflow", "Remove lower leaves"],
        "prevention": ["Rotate nightshades", "Mulch around stems", "Avoid wetting leaves"],
        "affected_plants": ["Tomatoes", "Potatoes", "Eggplant"],
        "chemical_treatment": [
            {
                "name": "Chlorothalonil fungicide",
                "brand_names": ["Daconil", "Bonide Fung-onil"],
                "active_ingredients": ["Chlorothalonil 54%"],
                "dosage": "15 ml per 4 L water every 7 days",
                "safety_precautions": ["Toxic to aquatic life", "Wear protective clothing"],
                "waiting_period": "7 days before harvest",
            },
            {
                "name": "Mancozeb fungicide",
                "brand_names": ["Dithane M-45", "Fore 80 WP"],
                "active_ingredients": ["Mancozeb 75% WP"],
                "dosage": "2 g per litre of water weekly",
                "safety_precautions": ["Wear a dust mask when mixing", "Do not graze treated area"],
                "waiting_period": "7 days",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Bacillus subtilis (QST 713)",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L every 5–7 days",
                "when_to_apply": "At first sign or preventively in humid weather",
                "notes": "Forms a protective biofilm on foliage.",
            },
            {
                "agent": "Streptomyces lydicus",
                "type": "Bio-fungicide",
                "application": "Soil + foliar application per label",
                "when_to_apply": "Before disease pressure peaks",
                "notes": "Stimulates plant defences against Alternaria.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Copper soap spray",
                "recipe": "Commercial copper octanoate at 15 ml/L",
                "application": "Spray foliage weekly",
                "frequency": "Weekly",
            },
            {
                "name": "Neem oil spray",
                "recipe": "2 ml neem oil + 1 L water + soap",
                "application": "Spray at dusk",
                "frequency": "Every 7 days",
            },
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 L water + soap",
                "application": "Spray lower leaves",
                "frequency": "Weekly",
            },
        ],
        "prevention_tips": [
            {"category": "Crop rotation", "title": "Rotate nightshades", "description": "3-year rotation away from tomato, potato and eggplant."},
            {"category": "Mulching", "title": "Mulch around stems", "description": "Straw mulch stops soil splash carrying spores."},
            {"category": "Irrigation", "title": "Avoid wetting leaves", "description": "Drip-irrigate at the soil line, never overhead."},
            {"category": "Nutrient management", "title": "Feed consistently", "description": "Steady potassium and calcium keep plants resilient."},
            {"category": "Field sanitation", "title": "Remove lower leaves", "description": "Strip the first 30 cm of leaves by mid-season."},
            {"category": "Resistant varieties", "title": "Plant resistant hybrids", "description": "e.g., 'Defiant', 'Jasper' tomatoes."},
        ],
        "fertilizer": {
            "organic": ["Composted manure", "Bone meal"],
            "micronutrients": ["Calcium foliar spray (to strengthen tissue)"],
            "npk": "Balanced 10-10-10 at planting, 5-10-10 at fruiting",
            "soil_improvement": ["Maintain pH 6.0–6.8 and add compost yearly"],
        },
        "severity_levels": {
            "mild": "A few target spots on lowest leaves.",
            "moderate": "Spots moving upward with yellow halos.",
            "severe": "Rapid defoliation, bare stems and sun-scalded fruit.",
        },
        "weather_conditions": {
            "humidity": "Wet foliage for 6+ hours aids infection",
            "temperature": "24–29°C peak activity",
            "rainfall": "Frequent rain or heavy dew triggers outbreaks",
        },
        "emergency_actions": [
            "Remove all infected lower leaves immediately.",
            "Apply chlorothalonil or mancozeb within 24 hours.",
            "If defoliation >50%, stop spraying and rogue the worst plants.",
        ],
    },
    {
        "name": "Late Blight",
        "category": "Fungal",
        "scientific_name": "Phytophthora infestans",
        "severity": "Severe",
        "description": (
            "Water-soaked, greasy patches that collapse the foliage within days, followed "
            "by white mould rings and rotten fruit. One of the most destructive potato "
            "and tomato diseases worldwide."
        ),
        "symptoms": ["dark water soaked patches", "white mold ring", "plant collapse", "brown spots"],
        "causes": ["Phytophthora infestans", "cool wet weather", "contaminated plants", "volunteer tubers"],
        "treatment": ["Remove infected plants immediately", "Copper or systemic fungicide"],
        "prevention": ["Avoid wetting leaves", "Use certified seed", "Crop rotation"],
        "affected_plants": ["Tomatoes", "Potatoes"],
        "chemical_treatment": [
            {
                "name": "Mancozeb (protectant)",
                "brand_names": ["Dithane M-45", "Ridomil Gold (metalaxyl+mancozeb)"],
                "active_ingredients": ["Mancozeb 75%", "Metalaxyl 4% + Mancozeb 64%"],
                "dosage": "2–2.5 g per litre every 7 days",
                "safety_precautions": ["Alternate chemistries to avoid resistance", "Wear full PPE"],
                "waiting_period": "14 days before harvest",
            },
            {
                "name": "Copper hydroxide",
                "brand_names": ["Kocide 3000"],
                "active_ingredients": ["Copper hydroxide 46%"],
                "dosage": "1.5 g per litre every 7–10 days",
                "safety_precautions": ["Phytotoxic to young foliage in high heat", "Keep out of waterways"],
                "waiting_period": "1 day",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Preventive foliar spray 2 g/L weekly",
                "when_to_apply": "Before cool, wet weather arrives",
                "notes": "Best used preventively; limited effect once lesions appear.",
            },
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L at planting",
                "when_to_apply": "At tuber/seedling planting",
                "notes": "Suppresses soil-borne inoculum in the root zone.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Copper spray (organic-approved)",
                "recipe": "Copper octanoate 15 ml/L",
                "application": "Spray all foliage before wet weather",
                "frequency": "Weekly in outbreak season",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Supportive spray at dusk",
                "frequency": "Every 7 days",
            },
        ],
        "prevention_tips": [
            {"category": "Crop rotation", "title": "Long rotation away from nightshades", "description": "At least 4 years without tomatoes/potatoes on the same land."},
            {"category": "Irrigation", "title": "Never wet the leaves", "description": "Drip irrigation only; irrigate in the morning."},
            {"category": "Resistant varieties", "title": "Use certified, blight-resistant seed", "description": "Avoid saving tubers from infected crops."},
            {"category": "Field sanitation", "title": "Destroy volunteer plants", "description": "Late blight overwinters in culls and volunteer tubers."},
            {"category": "Weather awareness", "title": "Spray before cold fronts", "description": "Treat preventively when cool wet weather is forecast."},
        ],
        "fertilizer": {
            "organic": ["Compost", "Fish emulsion"],
            "micronutrients": ["Manganese foliar"],
            "npk": "Balanced feed; avoid lush nitrogen-driven growth",
            "soil_improvement": ["Raise beds for drainage; avoid waterlogged soil"],
        },
        "severity_levels": {
            "mild": "Small water-soaked patches on a few lower leaves.",
            "moderate": "Spreading lesions with white mould rings in humid air.",
            "severe": "Whole plants collapse and fruit/tubers rot within days.",
        },
        "weather_conditions": {
            "humidity": "Near-saturation humidity (90%+)",
            "temperature": "15–20°C — cool, wet conditions",
            "rainfall": "Rainy, misty spells trigger explosive outbreaks",
        },
        "emergency_actions": [
            "Uproot infected plants immediately — bag and burn, never compost.",
            "Apply a systemic protectant and re-spray weekly.",
            "If weather stays cool and wet, destroy the entire crop to protect neighbours.",
        ],
    },
    {
        "name": "Aphid Infestation",
        "category": "Pest",
        "scientific_name": "Aphidoidea spp.",
        "severity": "Mild",
        "description": (
            "Tiny soft-bodied insects that suck sap from tender shoots, excreting sticky "
            "honeydew that invites sooty mould and ants. They also transmit viruses."
        ),
        "symptoms": ["curled leaves", "sticky leaves", "ants on plants", "tiny green insects", "yellowing"],
        "causes": ["over-fertilized growth", "lack of predators", "dry stress"],
        "treatment": ["Strong water jet", "Neem oil every 5 days", "Insecticidal soap"],
        "prevention": ["Attract ladybugs", "Companion herbs", "Check leaf undersides"],
        "affected_plants": ["Vegetables", "Roses", "Ornamentals", "Peppers"],
        "chemical_treatment": [
            {
                "name": "Insecticidal soap",
                "brand_names": ["Safer Insecticidal Soap"],
                "active_ingredients": ["Potassium salts of fatty acids"],
                "dosage": "20 ml per litre of water; drench colonies",
                "safety_precautions": ["Do not spray in direct sunlight", "Reapply after rain"],
                "waiting_period": "0 days",
            },
            {
                "name": "Imidacloprid (soil drench)",
                "brand_names": ["Bonide Systemic Insect Control"],
                "active_ingredients": ["Imidacloprid 2%"],
                "dosage": "Apply per label for potted/ornamental use",
                "safety_precautions": ["Highly toxic to bees — never spray open flowers", "Keep away from waterways"],
                "waiting_period": "Not for food crops near harvest",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Ladybird beetles (Coccinella)",
                "type": "Beneficial insect",
                "application": "Release 1,000–1,500 adults per 1,000 m²",
                "when_to_apply": "When aphid colonies first appear",
                "notes": "Each adult can eat 50+ aphids a day.",
            },
            {
                "agent": "Lacewing larvae (Chrysoperla)",
                "type": "Beneficial insect",
                "application": "Release eggs/larvae near colonies",
                "when_to_apply": "Early infestation",
                "notes": "Vigorous predators of aphids and mites.",
            },
            {
                "agent": "Beauveria bassiana",
                "type": "Bio-insecticide",
                "application": "Foliar spray at label rate",
                "when_to_apply": "Dusk to avoid UV killing the fungus",
                "notes": "Entomopathogenic fungus that infects aphids.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Soap solution",
                "recipe": "1 tbsp mild liquid soap + 1 L water",
                "application": "Spray directly on aphid clusters",
                "frequency": "Every 3–4 days",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem oil + 1 L warm water + soap",
                "application": "Spray tender shoots and leaf undersides",
                "frequency": "Every 5–7 days",
            },
            {
                "name": "Garlic spray",
                "recipe": "Steep 4 crushed garlic cloves in 1 L hot water overnight, strain",
                "application": "Spray foliage as a deterrent",
                "frequency": "Weekly",
            },
            {
                "name": "Strong water jet",
                "recipe": "Plain hose water",
                "application": "Blast aphids off plants, repeat as needed",
                "frequency": "Daily for 3–4 days",
            },
        ],
        "prevention_tips": [
            {"category": "Companion planting", "title": "Grow aphid-repelling herbs", "description": "Basil, mint, garlic and marigold mask plants and deter aphids."},
            {"category": "Predator conservation", "title": "Attract ladybugs and lacewings", "description": "Plant dill, fennel and yarrow to host natural enemies."},
            {"category": "Nutrient management", "title": "Avoid excess nitrogen", "description": "Soft, fast growth attracts aphids — feed moderately."},
            {"category": "Weed management", "title": "Control weeds", "description": "Weeds harbour aphid populations early in the season."},
            {"category": "Field sanitation", "title": "Inspect leaf undersides", "description": "Catch colonies early before they explode."},
        ],
        "fertilizer": {
            "organic": ["Compost tea", "Seaweed extract"],
            "micronutrients": ["Silicon for stronger cell walls"],
            "npk": "Balanced feed; low first-number nitrogen",
            "soil_improvement": ["Healthy soil = resilient, unpalatable growth"],
        },
        "severity_levels": {
            "mild": "A few small colonies on new shoots.",
            "moderate": "Colonies on many stems with curling and honeydew.",
            "severe": "Heavy sooty mould, stunted growth and virus transmission.",
        },
        "weather_conditions": {
            "humidity": "Low-to-moderate humidity favours aphids",
            "temperature": "20–28°C is peak breeding",
            "rainfall": "Heavy rain knocks aphids down naturally",
        },
        "emergency_actions": [
            "Blast plants with a strong water jet every morning.",
            "Apply insecticidal soap and repeat after 3 days.",
            "If sooty mould appears, wash leaves with soapy water.",
        ],
    },
    {
        "name": "Spider Mites",
        "category": "Pest",
        "scientific_name": "Tetranychus urticae",
        "severity": "Moderate",
        "description": (
            "Tiny mites that pierce leaf cells and drink the sap, leaving yellow speckles "
            "and fine webbing. Outbreaks explode in hot, dry, dusty conditions."
        ),
        "symptoms": ["fine webbing", "yellow speckles", "dry leaf texture", "leaf drop"],
        "causes": ["low humidity", "hot weather", "dusty leaves", "overuse of pesticides"],
        "treatment": ["Rinse leaves", "Raise humidity", "Apply miticide or neem"],
        "prevention": ["Keep humidity above 50%", "Isolate new plants", "Mist regularly"],
        "affected_plants": ["Tomatoes", "Cucumbers", "Houseplants", "Strawberries"],
        "chemical_treatment": [
            {
                "name": "Spinosad",
                "brand_names": ["Monterey Garden Insect Spray"],
                "active_ingredients": ["Spinosad 0.5%"],
                "dosage": "15 ml per 4 L water every 7 days",
                "safety_precautions": ["Toxic to bees until dry", "Reapply after rain"],
                "waiting_period": "1 day",
            },
            {
                "name": "Bifenthrin miticide",
                "brand_names": ["Talstar"],
                "active_ingredients": ["Bifenthrin 7.9%"],
                "dosage": "10 ml per 4 L water",
                "safety_precautions": ["Keep away from water sources", "Wear gloves"],
                "waiting_period": "7 days",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Predatory mite (Phytoseiulus persimilis)",
                "type": "Beneficial mite",
                "application": "Release 2–5 per plant at first sign",
                "when_to_apply": "Early morning, before heat",
                "notes": "Specialist predator that out-eats spider mite colonies.",
            },
            {
                "agent": "Beauveria bassiana",
                "type": "Bio-insecticide",
                "application": "Foliar spray at label rate",
                "when_to_apply": "Dusk",
                "notes": "Fungal pathogen of mites; needs humidity to work.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Cover undersides of leaves",
                "frequency": "Every 5–7 days",
            },
            {
                "name": "Rubbing alcohol mist",
                "recipe": "1 part isopropyl alcohol + 3 parts water",
                "application": "Mist infested plants (test on one leaf first)",
                "frequency": "Every 3 days",
            },
            {
                "name": "Humidity boost",
                "recipe": "Mist plants or place a humidifier nearby",
                "application": "Keep air moist around plants",
                "frequency": "Daily",
            },
        ],
        "prevention_tips": [
            {"category": "Environment", "title": "Keep humidity above 50%", "description": "Mites thrive in dry air — mist regularly."},
            {"category": "Irrigation", "title": "Wash off dust", "description": "Rinse foliage occasionally; dust attracts mites."},
            {"category": "Field sanitation", "title": "Isolate new plants", "description": "Quarantine newcomers for 2 weeks."},
            {"category": "Weed management", "title": "Clear weedy hosts", "description": "Weeds harbour mites between crops."},
            {"category": "Nutrient management", "title": "Avoid nitrogen excess", "description": "Lush growth is a mite magnet."},
        ],
        "fertilizer": {
            "organic": ["Kelp extract foliar"],
            "micronutrients": ["Silicon"],
            "npk": "Light balanced feed; avoid excess N",
            "soil_improvement": ["Mulch to hold soil moisture and raise humidity"],
        },
        "severity_levels": {
            "mild": "Speckling on a few leaves, light webbing.",
            "moderate": "Widespread stippling and visible webbing.",
            "severe": "Browning, leaf drop and plant decline.",
        },
        "weather_conditions": {
            "humidity": "Low humidity (<50%) accelerates outbreaks",
            "temperature": "30°C+ is peak activity",
            "rainfall": "Cool, rainy weather naturally suppresses mites",
        },
        "emergency_actions": [
            "Prune the worst-infested foliage into bags.",
            "Wash plants top to bottom, then apply a miticide.",
            "Repeat treatment every 3–5 days to break the egg cycle.",
        ],
    },
    {
        "name": "Nitrogen Deficiency",
        "category": "Deficiency",
        "scientific_name": "Nutrient deficiency (N)",
        "severity": "Mild",
        "description": (
            "Uniform yellowing that starts on the oldest leaves and moves upward while the "
            "plant grows slowly. Nitrogen is mobile, so the plant relocates it from old leaves "
            "to new growth."
        ),
        "symptoms": ["yellow old leaves", "pale foliage", "slow growth", "yellowing"],
        "causes": ["poor soil", "excessive watering", "compost competition", "sandy soil"],
        "treatment": ["Blood meal or fish emulsion", "Balanced compost"],
        "prevention": ["Feed with organic compost", "Test soil annually"],
        "affected_plants": ["Heavy feeders", "Leafy greens", "Corn", "Tomatoes"],
        "chemical_treatment": [
            {
                "name": "Urea-based nitrogen",
                "brand_names": ["Agro-Urea", "Scotts Turf Builder"],
                "active_ingredients": ["Urea 46% N"],
                "dosage": "10–20 g per m², watered in",
                "safety_precautions": ["Do not over-apply — burn risk", "Water in thoroughly after application"],
                "waiting_period": "Not applicable (soil amendment)",
            },
            {
                "name": "Balanced NPK granules",
                "brand_names": ["Osmocote", "Dr. Earth 4-6-6"],
                "active_ingredients": ["NPK 14-14-14 or 4-6-6"],
                "dosage": "Follow label for container/field size",
                "safety_precautions": ["Keep off foliage", "Water after application"],
                "waiting_period": "Not applicable",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Nitrogen-fixing cover crops (legumes)",
                "type": "Beneficial microbe",
                "application": "Grow clover, vetch or beans and turn under before planting",
                "when_to_apply": "In the season before the heavy-feeding crop",
                "notes": "Rhizobia bacteria fix atmospheric nitrogen into the soil.",
            },
            {
                "agent": "Compost + manure (compost tea)",
                "type": "Organic amendment",
                "application": "Drench compost tea at 5 L/m²",
                "when_to_apply": "Every 2 weeks during growth",
                "notes": "Feeds soil microbes that release nitrogen.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Blood meal",
                "recipe": "Sprinkle 60 g per m² and rake in",
                "application": "Side-dress around plants",
                "frequency": "Once a month",
            },
            {
                "name": "Fish emulsion",
                "recipe": "30 ml fish emulsion + 1 L water",
                "application": "Foliar feed / soil drench",
                "frequency": "Every 2 weeks",
            },
            {
                "name": "Compost tea",
                "recipe": "Steep 1 cup compost in 1 L water 24 h, strain",
                "application": "Water at the base",
                "frequency": "Weekly",
            },
        ],
        "prevention_tips": [
            {"category": "Nutrient management", "title": "Feed with organic compost", "description": "Add 2–3 cm of compost each season."},
            {"category": "Soil testing", "title": "Test soil annually", "description": "Know your N/P/K baseline before planting."},
            {"category": "Irrigation", "title": "Avoid over-watering", "description": "Excess water leaches nitrogen below the root zone."},
            {"category": "Crop rotation", "title": "Grow legumes before heavy feeders", "description": "Beans and peas add nitrogen for the next crop."},
        ],
        "fertilizer": {
            "organic": ["Blood meal", "Fish emulsion", "Manure", "Compost"],
            "micronutrients": ["Manganese (works with N uptake)"],
            "npk": "High-N feed, e.g., 10-5-5 during vegetative growth",
            "soil_improvement": ["Add compost yearly to build organic matter"],
        },
        "severity_levels": {
            "mild": "Slight yellowing of oldest leaves.",
            "moderate": "Marked yellowing of lower foliage, slower growth.",
            "severe": "Nearly all foliage pale yellow, severely stunted plants.",
        },
        "weather_conditions": {
            "humidity": "Not disease-related",
            "temperature": "Cold soil slows N uptake",
            "rainfall": "Heavy rain leaches nitrogen quickly",
        },
        "emergency_actions": [
            "Apply a fast-release organic N source (fish emulsion) immediately.",
            "Foliar-feed with seaweed extract for quick green-up.",
            "Re-test soil after two weeks to confirm recovery.",
        ],
    },
    {
        "name": "Iron Deficiency (Chlorosis)",
        "category": "Deficiency",
        "scientific_name": "Nutrient deficiency (Fe)",
        "severity": "Moderate",
        "description": (
            "Yellow leaves with distinct green veins (interveinal chlorosis), appearing on the "
            "youngest leaves first. Caused by low available iron, usually from alkaline soil."
        ),
        "symptoms": ["yellow between veins", "young leaf yellowing", "pale new growth", "yellowing"],
        "causes": ["alkaline soil pH", "overwatering", "poor drainage", "high phosphorus soil"],
        "treatment": ["Chelated iron", "Adjust soil pH to 5.5-6.5"],
        "prevention": ["Balance pH", "Avoid waterlogged soil"],
        "affected_plants": ["Citrus", "Blueberries", "Gardenias", "Azaleas"],
        "chemical_treatment": [
            {
                "name": "Chelated iron (Fe-EDDHA)",
                "brand_names": ["Iron Chelate EDDHA", "Miracle-Gro Iron"],
                "active_ingredients": ["Fe-EDDHA 6%"],
                "dosage": "5 g per 10 L water as soil drench",
                "safety_precautions": ["Keep away from children and pets", "Do not mix with phosphates"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Iron sulphate (soil acidifier)",
                "brand_names": ["Bonide Iron Sulfate"],
                "active_ingredients": ["Ferrous sulphate 30% Fe"],
                "dosage": "150–300 g per m² for acidifying",
                "safety_precautions": ["Can stain paths", "Water in well"],
                "waiting_period": "Not applicable",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Mycorrhizal fungi",
                "type": "Beneficial microbe",
                "application": "Inoculate roots at planting",
                "when_to_apply": "Transplant time",
                "notes": "Improves root reach and micronutrient uptake.",
            },
            {
                "agent": "Compost + acidifying mulch",
                "type": "Organic amendment",
                "application": "Mulch with pine needles / peat",
                "when_to_apply": "Season start",
                "notes": "Gently lowers soil pH over time.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Foliar seaweed + iron tea",
                "recipe": "Seaweed extract + chelated iron at label dose",
                "application": "Spray young leaves",
                "frequency": "Every 10 days",
            },
            {
                "name": "Acidic compost application",
                "recipe": "Mix pine needle compost into the root zone",
                "application": "Top-dress around the drip line",
                "frequency": "Seasonal",
            },
        ],
        "prevention_tips": [
            {"category": "Soil pH", "title": "Keep pH 5.5–6.5", "description": "Iron becomes unavailable in alkaline soils — acidify gently."},
            {"category": "Irrigation", "title": "Improve drainage", "description": "Waterlogged soil locks up iron."},
            {"category": "Nutrient management", "title": "Avoid excess phosphorus", "description": "High P precipitates iron in the soil."},
            {"category": "Resistant varieties", "title": "Choose tolerant rootstocks", "description": "e.g., some citrus and blueberry cultivars."},
        ],
        "fertilizer": {
            "organic": ["Pine-needle mulch", "Acidic compost"],
            "micronutrients": ["Chelated iron (EDDHA)", "Zinc", "Manganese"],
            "npk": "Low-phosphorus feed, e.g., 6-2-4 with micronutrients",
            "soil_improvement": ["Add sulphur or peat to acidify; test pH first"],
        },
        "severity_levels": {
            "mild": "Light interveinal yellowing on young leaves.",
            "moderate": "Bright yellow leaves with green veins.",
            "severe": "Almost white leaves, dieback of shoot tips.",
        },
        "weather_conditions": {
            "humidity": "Not disease-related",
            "temperature": "Cold, wet soils worsen chlorosis",
            "rainfall": "Excess rain promotes iron lock-up in clay soils",
        },
        "emergency_actions": [
            "Foliar-spray chelated iron for rapid green-up.",
            "Check and correct soil pH to below 6.5.",
            "Improve drainage around the root zone.",
        ],
    },
    {
        "name": "Mosaic Virus",
        "category": "Viral",
        "scientific_name": "Cucumber mosaic virus (CMV) / TMV",
        "severity": "Severe",
        "description": (
            "Mottled yellow-green mosaic patterns on leaves with stunted, distorted growth. "
            "Spread by aphids, infected seeds and contaminated tools. There is no cure — "
            "prevention and vector control are everything."
        ),
        "symptoms": ["mosaic pattern", "mottled leaves", "stunted growth", "curled leaves", "yellowing"],
        "causes": ["aphid vectors", "infected seeds", "contaminated tools", "tobacco use near crops"],
        "treatment": ["No cure - destroy infected plants", "Disinfect tools"],
        "prevention": ["Use virus-free seed", "Control aphids", "Wash hands between plants"],
        "affected_plants": ["Squash", "Cucumbers", "Peppers", "Tomatoes", "Tobacco"],
        "chemical_treatment": [
            {
                "name": "No chemical cure exists",
                "brand_names": [],
                "active_ingredients": ["—"],
                "dosage": "None — remove infected plants instead",
                "safety_precautions": ["Do not waste sprays on virus-affected plants"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Mineral oil (vector suppression)",
                "brand_names": ["JMS Stylet-Oil"],
                "active_ingredients": ["Paraffinic oil"],
                "dosage": "10 ml per litre; spray weekly",
                "safety_precautions": ["Do not spray in heat above 30°C", "Test for phytotoxicity"],
                "waiting_period": "0 days",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Predators of aphid vectors",
                "type": "Beneficial insect",
                "application": "Release ladybugs / lacewings to control aphids",
                "when_to_apply": "When aphids appear",
                "notes": "Stops the virus from moving plant to plant.",
            },
            {
                "agent": "Reflective mulch (cultural)",
                "type": "Cultural practice",
                "application": "Silver/white plastic mulch around plants",
                "when_to_apply": "At transplanting",
                "notes": "Repels aphids and delays virus spread.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Neem oil (vector control)",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray to deter aphid vectors",
                "frequency": "Weekly",
            },
            {
                "name": "Garlic-chilli spray",
                "recipe": "Blend garlic + chilli in water, steep, strain",
                "application": "Repellent spray for aphids",
                "frequency": "Weekly",
            },
        ],
        "prevention_tips": [
            {"category": "Crop rotation", "title": "Rotate virus-prone crops", "description": "Avoid replanting cucurbits/nightshades back-to-back."},
            {"category": "Vector control", "title": "Control aphids early", "description": "Virus spreads fastest when aphid numbers rise."},
            {"category": "Seed hygiene", "title": "Use certified virus-free seed", "description": "Never save seed from infected plants."},
            {"category": "Field sanitation", "title": "Disinfect tools and hands", "description": "Wash tools and hands between plants, especially after tobacco use."},
            {"category": "Weed management", "title": "Remove weed hosts", "description": "Many weeds harbour the virus over winter."},
        ],
        "fertilizer": {
            "organic": ["Balanced compost"],
            "micronutrients": ["Zinc (supports stress tolerance)"],
            "npk": "Balanced feed to keep plants vigorous",
            "soil_improvement": ["Good drainage to reduce plant stress"],
        },
        "severity_levels": {
            "mild": "Slight mottling on a few leaves.",
            "moderate": "Clear mosaic pattern, mild stunting.",
            "severe": "Severe distortion, reduced fruit set, plant collapse.",
        },
        "weather_conditions": {
            "humidity": "Not a direct factor",
            "temperature": "20–30°C aids aphid transmission",
            "rainfall": "Cool wet spells boost aphid populations",
        },
        "emergency_actions": [
            "Rogue and destroy all infected plants immediately.",
            "Disinfect every tool and surface you have touched.",
            "Apply reflective mulch and control aphids to protect the rest.",
        ],
    },
    {
        "name": "Root Rot",
        "category": "Fungal",
        "scientific_name": "Pythium, Rhizoctonia, Fusarium spp.",
        "severity": "Severe",
        "description": (
            "Mushy, brown-to-black roots caused by overwatering and waterlogged soil. Plants "
            "wilt despite wet soil, and a foul smell comes from decomposing roots."
        ),
        "symptoms": ["wilting despite wet soil", "mushy brown roots", "foul smell", "yellowing"],
        "causes": ["overwatering", "poor drainage", "pathogenic fungi", "compacted soil"],
        "treatment": ["Repot in sterile soil", "Trim rotted roots", "Reduce watering"],
        "prevention": ["Use well-draining pots", "Never leave pots in standing water"],
        "affected_plants": ["Houseplants", "Succulents", "Tomatoes", "Peppers"],
        "chemical_treatment": [
            {
                "name": "Fungicide drench (Mefenoxam)",
                "brand_names": ["Subdue Maxx", "Bonide Revitalize"],
                "active_ingredients": ["Mefenoxam 21%"],
                "dosage": "Apply as soil drench per label",
                "safety_precautions": ["Drench only; avoid foliage", "Wear gloves"],
                "waiting_period": "See label for food crops",
            },
            {
                "name": "Hydrogen peroxide soil flush",
                "brand_names": ["3% food-grade H2O2"],
                "active_ingredients": ["Hydrogen peroxide 3%"],
                "dosage": "Mix 1 part H2O2 with 3 parts water; flush soil",
                "safety_precautions": ["Do not use on roots in full strength", "Ventilate the area"],
                "waiting_period": "Not applicable",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L after repotting",
                "when_to_apply": "Immediately after repotting",
                "notes": "Out-competes root rot pathogens and heals roots.",
            },
            {
                "agent": "Bacillus amyloliquefaciens",
                "type": "Bio-fungicide",
                "application": "Root soak at transplanting",
                "when_to_apply": "Transplant time",
                "notes": "Colonises the root zone and suppresses Pythium.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Repot + root trim",
                "recipe": "Remove plant, trim dark mushy roots, repot in dry sterile mix",
                "application": "Physical rescue",
                "frequency": "Once",
            },
            {
                "name": "Cinnamon dust",
                "recipe": "Ground cinnamon",
                "application": "Dust cut root ends as an antifungal",
                "frequency": "At repotting",
            },
            {
                "name": "Compost tea drench",
                "recipe": "Brewed compost tea",
                "application": "Water in after rescue",
                "frequency": "Weekly for a month",
            },
        ],
        "prevention_tips": [
            {"category": "Irrigation", "title": "Water only when the top 2 cm are dry", "description": "Use the finger test or a moisture meter."},
            {"category": "Drainage", "title": "Use well-draining pots and soil", "description": "Ensure drainage holes and add perlite."},
            {"category": "Field sanitation", "title": "Sterilise pots and tools", "description": "Wash pots between uses to avoid spreading fungi."},
            {"category": "Nutrient management", "title": "Avoid over-fertilising", "description": "Salts stress roots and invite disease."},
        ],
        "fertilizer": {
            "organic": ["Dilute compost tea (only after recovery)"],
            "micronutrients": ["Seaweed extract to support root regrowth"],
            "npk": "Hold off feeding until roots recover",
            "soil_improvement": ["Add perlite/coarse sand for aeration"],
        },
        "severity_levels": {
            "mild": "Slight root browning, mild wilting.",
            "moderate": "Visible mushy roots, persistent wilting.",
            "severe": "Roots largely decayed, foul smell, plant near collapse.",
        },
        "weather_conditions": {
            "humidity": "Waterlogging is the trigger, not humidity",
            "temperature": "Cool wet soils rot roots faster",
            "rainfall": "Heavy rain in poor-drainage soil causes root rot",
        },
        "emergency_actions": [
            "Stop watering immediately and let soil dry.",
            "Repot, trimming all mushy roots into sterile mix.",
            "Drench with Trichoderma and hold off fertilising for 2 weeks.",
        ],
    },
    {
        "name": "Potassium Deficiency",
        "category": "Deficiency",
        "scientific_name": "Nutrient deficiency (K)",
        "severity": "Moderate",
        "description": (
            "Scorched, brown leaf edges and weak stems, starting on older leaves. Potassium "
            "regulates water balance and sugar transport, so plants look burnt and yield drops."
        ),
        "symptoms": ["brown leaf edges", "scorched tips", "weak stems", "yellowing"],
        "causes": ["sandy soil", "heavy rainfall", "low organic matter", "excess nitrogen"],
        "treatment": ["Kelp meal or wood ash", "Consistent watering"],
        "prevention": ["Feed balanced organic fertilizer", "Mulch to hold moisture"],
        "affected_plants": ["Tomatoes", "Potatoes", "Bananas", "Corn"],
        "chemical_treatment": [
            {
                "name": "Potassium sulphate (0-0-50)",
                "brand_names": ["SOP", "Hi-Yield Sulphate of Potash"],
                "active_ingredients": ["Potassium sulphate 50% K2O"],
                "dosage": "10–20 g per m², watered in",
                "safety_precautions": ["Do not over-apply near young roots", "Water in well"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Muriate of potash (0-0-60)",
                "brand_names": ["MOP", "Red Potash"],
                "active_ingredients": ["Potassium chloride 60% K2O"],
                "dosage": "8–15 g per m²",
                "safety_precautions": ["High chloride can harm sensitive crops", "Use SOP for fruiting crops"],
                "waiting_period": "Not applicable",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Potassium-solubilising bacteria (Bacillus sp.)",
                "type": "Beneficial microbe",
                "application": "Soil drench at planting",
                "when_to_apply": "Planting time",
                "notes": "Mobilises locked-up soil potassium.",
            },
            {
                "agent": "Compost + mulch",
                "type": "Organic amendment",
                "application": "Mulch and top-dress with compost",
                "when_to_apply": "Season start and mid-season",
                "notes": "Holds moisture and slowly releases potassium.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Wood ash",
                "recipe": "Sprinkle 100 g per m², avoid piling",
                "application": "Rake lightly into the topsoil",
                "frequency": "Once or twice a season",
            },
            {
                "name": "Kelp meal",
                "recipe": "Handful per plant",
                "application": "Work into the root zone",
                "frequency": "Monthly",
            },
            {
                "name": "Banana peel tea",
                "recipe": "Soak 3–4 banana peels in 1 L water for 48 h",
                "application": "Water at the base",
                "frequency": "Weekly",
            },
        ],
        "prevention_tips": [
            {"category": "Nutrient management", "title": "Feed balanced organic fertilizer", "description": "Alternate N-heavy feeds with K-rich feeds."},
            {"category": "Irrigation", "title": "Mulch to hold moisture", "description": "Mulch reduces leaching of potassium."},
            {"category": "Soil testing", "title": "Test soil K levels", "description": "Correct before symptoms appear."},
            {"category": "Field sanitation", "title": "Return crop residue", "description": "Leaves and stems recycle potassium back to the soil."},
        ],
        "fertilizer": {
            "organic": ["Kelp meal", "Wood ash", "Compost", "Banana peels"],
            "micronutrients": ["Seaweed extract"],
            "npk": "High-K feed, e.g., 5-10-20 during fruiting",
            "soil_improvement": ["Add clay-organic matter to sandy soils"],
        },
        "severity_levels": {
            "mild": "Slight brown tipping of leaf edges.",
            "moderate": "Clear scorched margins on older leaves.",
            "severe": "Heavy marginal burn, weak stems, shrivelled fruit.",
        },
        "weather_conditions": {
            "humidity": "Not disease-related",
            "temperature": "Drought stress worsens symptoms",
            "rainfall": "Heavy rain leaches K from sandy soils",
        },
        "emergency_actions": [
            "Foliar-feed with potassium sulphate at 2 g/L for a quick response.",
            "Add kelp meal to the root zone.",
            "Irrigate consistently to reduce plant stress.",
        ],
    },
    {
        "name": "Downy Mildew",
        "category": "Fungal",
        "scientific_name": "Peronospora, Plasmopara spp.",
        "severity": "Moderate",
        "description": (
            "Yellow angular patches on the upper leaf surface with a grey-purple downy growth "
            "underneath. Favours cool, humid, wet conditions and spreads explosively."
        ),
        "symptoms": ["yellow spots", "grey fuzzy undersides", "angular leaf patches", "leaf drop"],
        "causes": ["cool humid nights", "wet leaves", "poor airflow", "dense planting"],
        "treatment": ["Remove affected leaves", "Copper or phosphonate fungicide"],
        "prevention": ["Space plants", "Water in the morning", "Avoid wet foliage"],
        "affected_plants": ["Cucurbits", "Onions", "Lettuce", "Grapes", "Basil"],
        "chemical_treatment": [
            {
                "name": "Phosphonate fungicide",
                "brand_names": ["Agri-Fos", "Alude"],
                "active_ingredients": ["Mono- and di-potassium phosphite"],
                "dosage": "20 ml per litre every 7–10 days",
                "safety_precautions": ["Phytotoxic in high heat — spray at dusk", "Wear gloves"],
                "waiting_period": "0 days",
            },
            {
                "name": "Copper fungicide",
                "brand_names": ["Cueva", "Bonide Copper"],
                "active_ingredients": ["Copper octanoate"],
                "dosage": "15 ml per litre weekly",
                "safety_precautions": ["Rotate with phosphonate to avoid buildup", "Avoid waterways"],
                "waiting_period": "1 day",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Preventive foliar spray 2 g/L",
                "when_to_apply": "Before cool wet nights",
                "notes": "Protects healthy tissue from new infections.",
            },
            {
                "agent": "Streptomyces lydicus",
                "type": "Bio-fungicide",
                "application": "Foliar spray per label",
                "when_to_apply": "At first signs",
                "notes": "Suppresses spore production on infected leaves.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 tsp oil + 1 L water",
                "application": "Spray both leaf surfaces",
                "frequency": "Every 5–7 days",
            },
            {
                "name": "Neem oil spray",
                "recipe": "2 ml neem + 1 L water + soap",
                "application": "Spray at dusk",
                "frequency": "Weekly",
            },
            {
                "name": "Milk spray",
                "recipe": "1 part milk + 9 parts water",
                "application": "Spray on young leaves",
                "frequency": "Twice weekly",
            },
        ],
        "prevention_tips": [
            {"category": "Spacing", "title": "Space plants for airflow", "description": "Prevents humid micro-climates that downy mildew loves."},
            {"category": "Irrigation", "title": "Water in the morning", "description": "Leaves dry before the cool night."},
            {"category": "Crop rotation", "title": "Rotate cucurbits", "description": "Spores survive in debris — rotate and clean up."},
            {"category": "Resistant varieties", "title": "Grow tolerant cultivars", "description": "Many cucumber and lettuce varieties are resistant."},
        ],
        "fertilizer": {
            "organic": ["Compost", "Seaweed extract"],
            "micronutrients": ["Silicon (strengthens cell walls)"],
            "npk": "Balanced feed; avoid nitrogen excess",
            "soil_improvement": ["Good drainage keeps humidity lower at the soil line"],
        },
        "severity_levels": {
            "mild": "A few angular yellow patches.",
            "moderate": "Spreading patches with downy undersides.",
            "severe": "Foliage collapse and fruit rot within days.",
        },
        "weather_conditions": {
            "humidity": "High humidity with cool nights",
            "temperature": "15–22°C with moist nights",
            "rainfall": "Dew and drizzle trigger outbreaks",
        },
        "emergency_actions": [
            "Remove infected leaves immediately — do not compost.",
            "Spray a phosphonate fungicide the same evening.",
            "Thin the canopy to dry it out faster.",
        ],
    },
    {
        "name": "Anthracnose",
        "category": "Fungal",
        "scientific_name": "Colletotrichum spp.",
        "severity": "Moderate",
        "description": (
            "Sunken, dark, water-soaked lesions on leaves, stems and fruit that expand into "
            "black spots. Spreads through splashing water and is common in warm, wet seasons."
        ),
        "symptoms": ["sunken dark lesions", "black spots", "leaf blight", "fruit rot"],
        "causes": ["splash irrigation", "warm wet weather", "infected seed", "dense canopy"],
        "treatment": ["Prune infected parts", "Copper-based fungicide"],
        "prevention": ["Use clean seed", "Water at the base", "Mulch to stop splash"],
        "affected_plants": ["Beans", "Mango", "Peppers", "Cucurbits", "Strawberries"],
        "chemical_treatment": [
            {
                "name": "Chlorothalonil fungicide",
                "brand_names": ["Daconil"],
                "active_ingredients": ["Chlorothalonil 54%"],
                "dosage": "15 ml per 4 L every 7 days",
                "safety_precautions": ["Toxic to aquatic life", "Wear PPE"],
                "waiting_period": "7 days",
            },
            {
                "name": "Copper fungicide",
                "brand_names": ["Cueva", "Bonide Copper"],
                "active_ingredients": ["Copper octanoate"],
                "dosage": "15 ml per litre weekly",
                "safety_precautions": ["Rotate with other chemistries", "Avoid drift"],
                "waiting_period": "1 day",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L weekly",
                "when_to_apply": "Before wet weather",
                "notes": "Protective biofilm on leaves and fruit.",
            },
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench at planting",
                "when_to_apply": "Transplant time",
                "notes": "Reduces soil-borne Colletotrichum inoculum.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 L water + soap",
                "application": "Spray affected areas",
                "frequency": "Weekly",
            },
            {
                "name": "Neem oil spray",
                "recipe": "2 ml neem + 1 L water + soap",
                "application": "Spray foliage and fruit",
                "frequency": "Every 7 days",
            },
        ],
        "prevention_tips": [
            {"category": "Seed hygiene", "title": "Use certified, disease-free seed", "description": "Anthracnose travels in infected seed."},
            {"category": "Irrigation", "title": "Water at the base", "description": "Stop splashing that spreads spores."},
            {"category": "Mulching", "title": "Mulch to prevent soil splash", "description": "A clean soil barrier cuts re-infection."},
            {"category": "Field sanitation", "title": "Prune and remove infected parts", "description": "Do not compost infected debris."},
            {"category": "Crop rotation", "title": "Rotate legumes and cucurbits", "description": "2–3 year breaks reduce inoculum."},
        ],
        "fertilizer": {
            "organic": ["Compost", "Kelp meal"],
            "micronutrients": ["Calcium (firm tissue)"],
            "npk": "Balanced feed; moderate nitrogen",
            "soil_improvement": ["Mulch to keep soil off leaves"],
        },
        "severity_levels": {
            "mild": "A few small dark lesions on leaves.",
            "moderate": "Spread of lesions, some fruit spotting.",
            "severe": "Widespread blight and fruit rot.",
        },
        "weather_conditions": {
            "humidity": "Warm, wet, humid conditions",
            "temperature": "22–30°C",
            "rainfall": "Rain and overhead watering spread spores",
        },
        "emergency_actions": [
            "Prune infected foliage and fruit immediately.",
            "Apply a copper fungicide within 24 hours.",
            "Remove badly hit plants and sanitise stakes/trellis.",
        ],
    },
    {
        "name": "Fusarium Wilt",
        "category": "Fungal",
        "scientific_name": "Fusarium oxysporum",
        "severity": "Severe",
        "description": (
            "Vascular wilt where leaves yellow and droop on one side of the plant, progressing "
            "to whole-plant collapse. The fungus lives in soil for years and enters through roots."
        ),
        "symptoms": ["one sided wilting", "yellowing", "stunted growth", "plant collapse", "brown streaks in stem"],
        "causes": ["Fusarium oxysporum", "infected soil", "root damage", "warm soil"],
        "treatment": ["No cure - remove plants", "Solarise soil", "Grow resistant varieties"],
        "prevention": ["Use resistant cultivars", "Rotate crops", "Avoid root damage"],
        "affected_plants": ["Tomatoes", "Bananas", "Melons", "Basil"],
        "chemical_treatment": [
            {
                "name": "Fungicide drench (Thiabendazole)",
                "brand_names": ["Mertect"],
                "active_ingredients": ["Thiabendazole 60%"],
                "dosage": "Soil drench per label for ornamental use only",
                "safety_precautions": ["Limited effect once wilt appears", "Wear gloves"],
                "waiting_period": "Not for food crops once infected",
            },
            {
                "name": "Soil solarisation (heat) instead of chemistry",
                "brand_names": ["Clear plastic sheeting"],
                "active_ingredients": ["Solar heat"],
                "dosage": "Cover moist soil with clear plastic for 4–6 weeks in summer",
                "safety_precautions": ["Do not solarise in overcast seasons", "Water soil first"],
                "waiting_period": "Not applicable",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Trichoderma viride / harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L at planting",
                "when_to_apply": "Transplant time",
                "notes": "Competes with Fusarium in the root zone.",
            },
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Root soak + soil drench at planting",
                "when_to_apply": "Planting time",
                "notes": "Colonises roots and suppresses Fusarium entry.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Soil solarisation",
                "recipe": "Water soil, cover with clear plastic 4–6 weeks",
                "application": "Summer only, before planting",
                "frequency": "Once per season",
            },
            {
                "name": "Compost tea drench",
                "recipe": "Brewed compost tea (microbe-rich)",
                "application": "Water around roots to build soil biology",
                "frequency": "Weekly",
            },
        ],
        "prevention_tips": [
            {"category": "Resistant varieties", "title": "Grow Fusarium-resistant cultivars", "description": "Look for 'F' or 'VFN' codes on tomato labels."},
            {"category": "Crop rotation", "title": "Long rotation", "description": "Fusarium persists in soil — rotate for 4+ years."},
            {"category": "Soil health", "title": "Feed soil biology", "description": "Compost and Trichoderma keep Fusarium in check."},
            {"category": "Field sanitation", "title": "Avoid root damage", "description": "Wounds let Fusarium enter the plant."},
        ],
        "fertilizer": {
            "organic": ["Compost", "Kelp extract"],
            "micronutrients": ["Silicon"],
            "npk": "Moderate nitrogen; balanced feed",
            "soil_improvement": ["Raise beds for drainage; solarise infested beds"],
        },
        "severity_levels": {
            "mild": "Slight one-sided yellowing.",
            "moderate": "Progressive wilt despite moist soil.",
            "severe": "Plant collapse; brown vascular streaks in stem.",
        },
        "weather_conditions": {
            "humidity": "Warm moist soil favours Fusarium",
            "temperature": "25–32°C soil temperature",
            "rainfall": "Waterlogged soil worsens infection",
        },
        "emergency_actions": [
            "Remove infected plants with surrounding soil, bag them.",
            "Solarise the bed before replanting.",
            "Replant only resistant varieties and drench with Trichoderma.",
        ],
    },
    {
        "name": "Whitefly Infestation",
        "category": "Pest",
        "scientific_name": "Bemisia tabaci / Trialeurodes",
        "severity": "Moderate",
        "description": (
            "Small white winged insects that cluster on leaf undersides, sucking sap and "
            "excreting sticky honeydew. Heavy infestations cause yellowing and virus spread."
        ),
        "symptoms": ["tiny white insects", "sticky leaves", "yellowing", "sooty mould", "leaf drop"],
        "causes": ["warm greenhouse conditions", "over-fertilised growth", "lack of natural enemies"],
        "treatment": ["Yellow sticky traps", "Insecticidal soap", "Neem oil"],
        "prevention": ["Use reflective mulch", "Introduce predators", "Ventilate greenhouses"],
        "affected_plants": ["Tomatoes", "Cucumbers", "Poinsettia", "Brassicas"],
        "chemical_treatment": [
            {
                "name": "Insecticidal soap",
                "brand_names": ["Safer Insecticidal Soap"],
                "active_ingredients": ["Potassium salts of fatty acids"],
                "dosage": "20 ml per litre; cover undersides",
                "safety_precautions": ["Spray at dusk", "Repeat every 3–4 days"],
                "waiting_period": "0 days",
            },
            {
                "name": "Imidacloprid systemic",
                "brand_names": ["Bonide Systemic"],
                "active_ingredients": ["Imidacloprid"],
                "dosage": "Soil drench per label",
                "safety_precautions": ["Toxic to bees — avoid flowers", "Keep from waterways"],
                "waiting_period": "21 days for food crops",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Encarsia formosa (parasitic wasp)",
                "type": "Beneficial insect",
                "application": "Release 5 per m² weekly",
                "when_to_apply": "As soon as adults are seen",
                "notes": "Parasitises whitefly nymphs.",
            },
            {
                "agent": "Beauveria bassiana",
                "type": "Bio-insecticide",
                "application": "Foliar spray at label rate",
                "when_to_apply": "Dusk for humidity",
                "notes": "Fungal disease of whitefly.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray leaf undersides",
                "frequency": "Every 5 days",
            },
            {
                "name": "Soap + water wash",
                "recipe": "1 tbsp soap + 1 L water",
                "application": "Wash undersides of leaves",
                "frequency": "Every 3 days",
            },
            {
                "name": "Yellow sticky traps",
                "recipe": "Yellow cards coated with non-drying glue",
                "application": "Hang just above plant canopy",
                "frequency": "Replace weekly",
            },
        ],
        "prevention_tips": [
            {"category": "Predator conservation", "title": "Introduce parasitoids early", "description": "Encarsia formosa and ladybugs control whitefly."},
            {"category": "Environment", "title": "Ventilate greenhouses", "description": "Whitefly thrives in still, warm air."},
            {"category": "Field sanitation", "title": "Remove infested old leaves", "description": "Whitefly builds on the oldest foliage."},
            {"category": "Nutrient management", "title": "Avoid nitrogen excess", "description": "Soft lush growth attracts whitefly."},
        ],
        "fertilizer": {
            "organic": ["Balanced compost"],
            "micronutrients": ["Silicon"],
            "npk": "Moderate balanced feed",
            "soil_improvement": ["Mulch with reflective silver plastic at planting"],
        },
        "severity_levels": {
            "mild": "A few adults on lower leaves.",
            "moderate": "Clusters on many leaves with honeydew.",
            "severe": "Massive populations, sooty mould and yellowing.",
        },
        "weather_conditions": {
            "humidity": "Greenhouse warmth and humidity",
            "temperature": "25–30°C peaks",
            "rainfall": "Cool outdoor weather suppresses them",
        },
        "emergency_actions": [
            "Vacuum adults at dawn when they are slow.",
            "Apply insecticidal soap and repeat every 3 days.",
            "Hang many sticky traps and introduce parasitoids.",
        ],
    },
    {
        "name": "Citrus Canker",
        "category": "Bacterial",
        "scientific_name": "Xanthomonas citri",
        "severity": "Moderate",
        "description": (
            "Raised, corky brown lesions with a yellow halo on leaves, stems and fruit. A "
            "quarantine-regulated bacterial disease spread by wind-blown rain and citrus leaf miner."
        ),
        "symptoms": ["raised corky lesions", "yellow halo spots", "fruit spots", "leaf drop"],
        "causes": ["Xanthomonas citri", "wind-blown rain", "citrus leaf miner wounds", "infected nursery stock"],
        "treatment": ["Prune infected twigs", "Copper sprays", "Control leaf miner"],
        "prevention": ["Buy certified trees", "Windbreaks", "Copper before storms"],
        "affected_plants": ["Citrus", "Grapefruit", "Oranges", "Lemons"],
        "chemical_treatment": [
            {
                "name": "Copper bactericide",
                "brand_names": ["Kocide 3000", "Nordox 75 WG"],
                "active_ingredients": ["Copper hydroxide 46%", "Cuprous oxide 75%"],
                "dosage": "1.5–2 g per litre every 14 days",
                "safety_precautions": ["Wear PPE", "Avoid spraying open flowers", "Keep from waterways"],
                "waiting_period": "14 days before harvest",
            },
            {
                "name": "Streptomycin (nursery use only)",
                "brand_names": ["Agri-Mycin 17"],
                "active_ingredients": ["Streptomycin sulphate"],
                "dosage": "Per label — permitted in citrus nurseries",
                "safety_precautions": ["Regulated — follow local rules", "Not for home use"],
                "waiting_period": "Not for home orchards",
            },
        ],
        "biological_treatment": [
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-bactericide",
                "application": "Foliar spray 2 g/L weekly",
                "when_to_apply": "Before wet, windy weather",
                "notes": "Protective biofilm reduces bacterial entry.",
            },
            {
                "agent": "Citrus leaf-miner control (parasitoid)",
                "type": "Beneficial insect",
                "application": "Release parasitoids / use neem",
                "when_to_apply": "Flush growth periods",
                "notes": "Leaf miner wounds are the main entry point.",
            },
        ],
        "organic_remedies": [
            {
                "name": "Copper spray (organic-approved)",
                "recipe": "Copper octanoate 15 ml/L",
                "application": "Spray after storms and pruning",
                "frequency": "Every 14 days in wet season",
            },
            {
                "name": "Neem oil (leaf miner control)",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray new flush growth",
                "frequency": "Weekly during flush",
            },
        ],
        "prevention_tips": [
            {"category": "Plant hygiene", "title": "Buy certified disease-free trees", "description": "Never move fruit or plants from infected orchards."},
            {"category": "Wind protection", "title": "Plant windbreaks", "description": "Wind-blown rain is the main spreader."},
            {"category": "Pest management", "title": "Control citrus leaf miner", "description": "Wounds from leaf miner let bacteria enter."},
            {"category": "Field sanitation", "title": "Prune infected twigs in dry weather", "description": "Sanitise shears between cuts."},
        ],
        "fertilizer": {
            "organic": ["Compost", "Seaweed extract"],
            "micronutrients": ["Zinc", "Manganese (citrus mix)"],
            "npk": "Balanced citrus feed 6-3-3",
            "soil_improvement": ["Maintain pH 5.5–6.5"],
        },
        "severity_levels": {
            "mild": "A few lesions on leaves.",
            "moderate": "Scattered lesions on leaves and fruit.",
            "severe": "Heavy fruit blemish, twig dieback, defoliation.",
        },
        "weather_conditions": {
            "humidity": "Wet, stormy weather",
            "temperature": "20–35°C",
            "rainfall": "Rain + wind = rapid spread",
        },
        "emergency_actions": [
            "Prune and bag infected twigs immediately.",
            "Apply copper before the next storm.",
            "Report severe outbreaks to the local plant protection authority.",
        ],
    },
]


# Merge the expanded module knowledge base into the seed list.
SEED_DISEASES += (
    FUNGAL_DISEASES
    + BACTERIAL_DISEASES
    + VIRAL_DISEASES
    + PEST_DISEASES
    + DEFICIENCY_DISEASES
)


async def seed_database() -> None:
    """Seed/upgrade the disease knowledge base and create the admin user."""
    db = get_database()

    await _seed_diseases(db)
    await _seed_admin(db)


async def _seed_diseases(db: Database) -> None:
    """Upsert every seed disease by name so existing databases get upgraded."""
    count = await db.plant_diseases.count_documents({})
    if count > 0:
        existing = await db.plant_diseases.find_one(
            {"seed_version": {"$ne": SEED_VERSION}}
        )
        if existing is None:
            logger.info(
                "Disease collection already on seed version %d (%d docs)",
                SEED_VERSION,
                count,
            )
            return

    now = datetime.utcnow()
    inserted = 0
    upgraded = 0

    for d in SEED_DISEASES:
        doc = {
            **d,
            "seed_version": SEED_VERSION,
            "image_url": None,
            "extra": {},
            "created_at": now,
            "updated_at": now,
        }
        result = await db.plant_diseases.replace_one(
            {"name": d["name"]},
            doc,
            upsert=True,
        )
        if result.upserted_id is not None:
            inserted += 1
        else:
            upgraded += 1

    logger.info("Disease seed complete: %d inserted, %d upgraded", inserted, upgraded)


async def _seed_admin(db: Database) -> None:
    """
    Create every configured admin account, skipping ones that already exist.

    Accounts come from two sources, both kept in `.env` so no password ever
    lives in source control:
      - the single ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD triple, and
      - the ADMIN_ACCOUNTS JSON array (any number of extra admins).
    """
    accounts = _configured_admins()
    if not accounts:
        logger.info("No admin credentials configured; skipping admin seed")
        return

    from app.auth.security import hash_password

    for account in accounts:
        username = account["username"]
        email = account["email"]
        if await db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
            logger.info("Admin %s already exists; skipping", username)
            continue

        await db.users.insert_one(
            {
                "username": username,
                "email": email,
                "hashed_password": hash_password(account["password"]),
                "full_name": account["full_name"] or "Portal Admin",
                "role": "admin",
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        )
        logger.info("Seeded admin user: %s", username)


def _configured_admins() -> list[dict[str, str]]:
    """
    Normalise every env-configured admin into a uniform dict.

    Entries missing a username, email or password are dropped so a partial
    entry can never create a half-usable account.
    """
    raw: list[dict] = []

    single = {
        "username": _settings.admin_username,
        "email": _settings.admin_email,
        "password": _settings.admin_password,
    }
    raw.append(single)
    raw.extend(_settings.admin_accounts_list)

    accounts: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in raw:
        username = (item.get("username") or "").strip()
        email = (item.get("email") or "").strip()
        password = item.get("password") or ""
        if not (username and email and password):
            continue
        if username.lower() in seen:
            continue
        seen.add(username.lower())
        accounts.append(
            {
                "username": username,
                "email": email,
                "password": password,
                "full_name": (item.get("full_name") or "").strip(),
            }
        )
    return accounts
