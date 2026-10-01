"""Viral disease records (AI Plant Doctor knowledge base)."""

from app.seed_data_common import _disease

VIRAL_DISEASES: list[dict] = [
    _disease(
        name="Tomato Yellow Leaf Curl Virus",
        category="Viral",
        scientific_name="TYLCV (Begomovirus)",
        severity="Severe",
        description=(
            "Leaves roll upward and inward, turn yellow along the margins and the plant "
            "stops growing almost completely. Fruit set collapses. Spread rapidly by "
            "whiteflies; there is no cure - only vector control."
        ),
        symptoms=["yellow leaf edges", "upward curled leaves", "severe stunting", "no fruit set", "leaf yellowing"],
        causes=["whitefly vectors", "infected transplants", "volunteer tomato plants", "shared weed hosts"],
        treatment=["Rogue infected plants", "Control whitefly hard", "Grow resistant varieties"],
        prevention=["Use resistant hybrids", "Net or screen the crop", "Remove weeds and volunteers"],
        affected_plants=["Tomato", "Pepper", "Bean", "Chilli"],
        chemical_treatment=[
            {
                "name": "No cure for the virus",
                "brand_names": [],
                "active_ingredients": ["-"],
                "dosage": "None - remove infected plants instead",
                "safety_precautions": ["Do not waste sprays on virus-affected plants"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Whitefly vector control",
                "brand_names": ["Safer Insecticidal Soap", "Bonide Systemic"],
                "active_ingredients": ["Potassium salts of fatty acids", "Imidacloprid (regulated)"],
                "dosage": "Spray undersides at first whitefly sign",
                "safety_precautions": ["Toxic to bees - avoid flowers", "Repeat every 3-4 days"],
                "waiting_period": "0 days (soap); 21 days (systemic on food crops)",
            },
        ],
        biological_treatment=[
            {
                "agent": "Encarsia formosa (parasitic wasp)",
                "type": "Beneficial insect",
                "application": "Release near whitefly populations",
                "when_to_apply": "As soon as whitefly appears",
                "notes": "Parasitises whitefly nymphs that spread the virus.",
            },
            {
                "agent": "Beauveria bassiana",
                "type": "Bio-insecticide",
                "application": "Foliar spray at dusk",
                "when_to_apply": "When whitefly pressure builds",
                "notes": "Infects and kills whitefly adults.",
            },
        ],
        organic_remedies=[
            {
                "name": "Silver reflective mulch",
                "recipe": "Silver plastic or aluminium foil strips",
                "application": "Lay around plants to repel whitefly",
                "frequency": "At planting",
            },
            {
                "name": "Yellow sticky traps",
                "recipe": "Yellow glue cards",
                "application": "Hang above the canopy",
                "frequency": "Replace weekly",
            },
        ],
        prevention_tips=[
            {"category": "Resistant varieties", "title": "Grow TYLCV-resistant hybrids", "description": "Most modern hybrids carry Ty resistance genes."},
            {"category": "Vector control", "title": "Screen and net the crop", "description": "Fine mesh excludes whitefly from seedlings."},
            {"category": "Field sanitation", "title": "Remove weeds and volunteers", "description": "They carry the virus between crops."},
            {"category": "Plant hygiene", "title": "Buy certified transplants", "description": "Never move plants from infected fields."},
        ],
        fertilizer={
            "organic": ["Compost", "Seaweed extract"],
            "micronutrients": ["Zinc (stress tolerance)"],
            "npk": "Moderate balanced feed",
            "soil_improvement": ["Mulch to reduce plant stress"],
        },
        severity_levels={
            "mild": "Slight yellowing and curling on new growth.",
            "moderate": "Strong leaf curl, stunting, little flowering.",
            "severe": "No fruit, whole plants stunted and yellow.",
        },
        weather_conditions={
            "humidity": "Warm, dry conditions favour whitefly",
            "temperature": "28-35 C is peak whitefly activity",
            "rainfall": "Dry spells boost whitefly numbers",
        },
        emergency_actions=[
            "Rogue and destroy infected plants immediately.",
            "Step up whitefly control on all remaining plants.",
            "Net new transplants and use reflective mulch.",
        ],
    ),
    _disease(
        name="Potato Leafroll Virus",
        category="Viral",
        scientific_name="PLRV (Polerovirus)",
        severity="Moderate",
        description=(
            "The lower leaves of potato plants roll upward, stiffen and turn yellow, and "
            "the whole plant becomes dwarfed. Tubers show brown netted veins and may be "
            "unsellable. Spread persistently by aphids."
        ),
        symptoms=["upward leaf rolling", "stiff yellow leaves", "dwarfed plants", "netted brown tubers", "early death"],
        causes=["PLRV", "green peach aphid vector", "infected seed tubers", "nearby culls"],
        treatment=["No cure - remove infected plants", "Control aphids", "Plant certified seed"],
        prevention=["Use certified virus-free seed", "Control aphids early", "Remove volunteer potatoes"],
        affected_plants=["Potato", "Tomato", "Eggplant"],
        chemical_treatment=[
            {
                "name": "No cure for the virus",
                "brand_names": [],
                "active_ingredients": ["-"],
                "dosage": "None - remove infected plants instead",
                "safety_precautions": ["Do not waste sprays on infected plants"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Aphid vector control",
                "brand_names": ["Safer Insecticidal Soap", "Neem oil"],
                "active_ingredients": ["Potassium salts of fatty acids", "Neem oil"],
                "dosage": "Spray tender shoots and undersides",
                "safety_precautions": ["Spray at dusk", "Repeat every 5-7 days"],
                "waiting_period": "0 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Ladybird beetles (Coccinella)",
                "type": "Beneficial insect",
                "application": "Release near aphid colonies",
                "when_to_apply": "At first aphid sign",
                "notes": "Each adult eats 50+ aphids per day.",
            },
            {
                "agent": "Aphidius colemani (parasitic wasp)",
                "type": "Beneficial insect",
                "application": "Release at first aphid sign",
                "when_to_apply": "Early infestation",
                "notes": "Parasitises aphids that transmit the virus.",
            },
        ],
        organic_remedies=[
            {
                "name": "Strong water jet",
                "recipe": "Plain hose water",
                "application": "Blast aphids off plants daily",
                "frequency": "Daily for 3-4 days",
            },
            {
                "name": "Soap spray",
                "recipe": "1 tbsp liquid soap + 1 L water",
                "application": "Spray on aphid colonies",
                "frequency": "Every 3 days",
            },
        ],
        prevention_tips=[
            {"category": "Seed hygiene", "title": "Plant certified seed tubers", "description": "Never save tubers from infected crops."},
            {"category": "Vector control", "title": "Control aphids early", "description": "PLRV spreads fastest when aphids move in."},
            {"category": "Field sanitation", "title": "Remove volunteer potatoes", "description": "Volunteers keep the virus alive between seasons."},
            {"category": "Crop rotation", "title": "Rotate away from nightshades", "description": "Reduces aphid and virus build-up."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp extract"],
            "micronutrients": ["Potassium (tuber quality)"],
            "npk": "Balanced feed; avoid excess nitrogen",
            "soil_improvement": ["Mulch to keep tubers cool and covered"],
        },
        severity_levels={
            "mild": "Slight rolling of lower leaves.",
            "moderate": "Yellow rolling leaves, dwarfed plants.",
            "severe": "Netted tubers, early plant death, yield loss.",
        },
        weather_conditions={
            "humidity": "Mild conditions favour aphids",
            "temperature": "18-25 C is peak aphid activity",
            "rainfall": "Cool, dry spells boost aphid migration",
        },
        emergency_actions=[
            "Rogue infected plants immediately.",
            "Apply a fast aphid control within 3 days.",
            "Do not save seed from the affected crop.",
        ],
    ),
    _disease(
        name="Papaya Ringspot Virus",
        category="Viral",
        scientific_name="PRSV (Potyvirus)",
        severity="Severe",
        description=(
            "Young papaya leaves mottle and blister, petioles grow short, and the crown "
            "collapses into a 'bunchy top'. Fruit develops dark ringspots. Spread by aphids; "
            "young trees are often killed."
        ),
        symptoms=["leaf mottling", "blistered leaves", "short petioles", "bunchy crown", "ringspots on fruit"],
        causes=["PRSV", "aphid vectors", "infected volunteer papaya", "shared weed hosts"],
        treatment=["No cure - remove infected trees", "Control aphids", "Plant tolerant varieties"],
        prevention=["Grow tolerant varieties", "Net young trees", "Remove infected trees early"],
        affected_plants=["Papaya", "Cucurbits", "Squash", "Melon"],
        chemical_treatment=[
            {
                "name": "No cure for the virus",
                "brand_names": [],
                "active_ingredients": ["-"],
                "dosage": "None - remove infected trees",
                "safety_precautions": ["Do not waste sprays on infected trees"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Aphid vector control",
                "brand_names": ["Neem oil", "Safer Insecticidal Soap"],
                "active_ingredients": ["Neem oil", "Potassium salts of fatty acids"],
                "dosage": "Spray young flush growth weekly",
                "safety_precautions": ["Spray at dusk", "Do not spray flowers"],
                "waiting_period": "0 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Lacewing larvae (Chrysoperla)",
                "type": "Beneficial insect",
                "application": "Release near aphid colonies",
                "when_to_apply": "Early infestation",
                "notes": "Rapid predators of aphid vectors.",
            },
            {
                "agent": "Ladybird beetles",
                "type": "Beneficial insect",
                "application": "Release on infested trees",
                "when_to_apply": "At first aphid sign",
                "notes": "Suppresses aphids that spread PRSV.",
            },
        ],
        organic_remedies=[
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray new growth and undersides",
                "frequency": "Weekly",
            },
            {
                "name": "Yellow sticky traps",
                "recipe": "Yellow glue cards",
                "application": "Hang around young trees",
                "frequency": "Replace weekly",
            },
        ],
        prevention_tips=[
            {"category": "Resistant varieties", "title": "Plant PRSV-tolerant papaya", "description": "Transgenic and tolerant hybrids exist in many markets."},
            {"category": "Vector control", "title": "Net young trees", "description": "Protect the first year when trees are most at risk."},
            {"category": "Field sanitation", "title": "Remove infected trees early", "description": "A few trees removed early save the whole planting."},
            {"category": "Weed management", "title": "Clear weed hosts", "description": "Weeds harbour aphids between crops."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp extract"],
            "micronutrients": ["Zinc", "Manganese"],
            "npk": "Frequent small feeds of balanced formula",
            "soil_improvement": ["Mulch and keep roots evenly moist"],
        },
        severity_levels={
            "mild": "Mottling on a few young leaves.",
            "moderate": "Blistered leaves, short petioles, bunchy top.",
            "severe": "Ringspotted fruit, crown collapse, tree death.",
        },
        weather_conditions={
            "humidity": "Warm, humid climate favours aphids",
            "temperature": "25-32 C is peak aphid activity",
            "rainfall": "Dry spells push aphids into the crop",
        },
        emergency_actions=[
            "Cut down and remove infected trees immediately.",
            "Step up aphid control across the planting.",
            "Net remaining young trees until well established.",
        ],
    ),
    _disease(
        name="Bean Common Mosaic Virus",
        category="Viral",
        scientific_name="BCMV (Potyvirus)",
        severity="Moderate",
        description=(
            "Leaves of beans show a green-yellow mosaic, curl downward and distort, and "
            "pods set poorly. Plants may be stunted. Spread by aphids, seed and mechanical "
            "contact; there is no cure."
        ),
        symptoms=["green yellow mosaic", "downward curled leaves", "leaf distortion", "stunted plants", "poor pod set"],
        causes=["BCMV", "aphid vectors", "infected seed", "contaminated tools"],
        treatment=["No cure - remove infected plants", "Control aphids", "Plant clean seed"],
        prevention=["Use certified virus-free seed", "Control aphids", "Disinfect tools"],
        affected_plants=["Beans", "Runner Bean", "Lima Bean", "Soybean"],
        chemical_treatment=[
            {
                "name": "No cure for the virus",
                "brand_names": [],
                "active_ingredients": ["-"],
                "dosage": "None - remove infected plants instead",
                "safety_precautions": ["Do not waste sprays on infected plants"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Aphid vector control",
                "brand_names": ["Safer Insecticidal Soap", "Neem oil"],
                "active_ingredients": ["Potassium salts of fatty acids", "Neem oil"],
                "dosage": "Spray undersides weekly",
                "safety_precautions": ["Spray at dusk", "Do not spray flowers in bloom"],
                "waiting_period": "0 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Ladybird beetles",
                "type": "Beneficial insect",
                "application": "Release near aphid colonies",
                "when_to_apply": "At first aphid sign",
                "notes": "Controls the aphids that spread the virus.",
            },
            {
                "agent": "Aphidius colemani",
                "type": "Beneficial insect",
                "application": "Release at first aphid sign",
                "when_to_apply": "Early infestation",
                "notes": "Parasitises aphid vectors.",
            },
        ],
        organic_remedies=[
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray foliage weekly",
                "frequency": "Weekly",
            },
            {
                "name": "Silver reflective mulch",
                "recipe": "Silver plastic sheeting",
                "application": "Lay around bean rows at planting",
                "frequency": "At planting",
            },
        ],
        prevention_tips=[
            {"category": "Seed hygiene", "title": "Use certified virus-free seed", "description": "BCMV passes through infected seed."},
            {"category": "Vector control", "title": "Control aphids early", "description": "Aphid flights spread the virus quickly."},
            {"category": "Resistant varieties", "title": "Grow resistant cultivars", "description": "Many snap bean varieties carry resistance genes."},
            {"category": "Field sanitation", "title": "Disinfect tools", "description": "Wash hands and tools between rows."},
        ],
        fertilizer={
            "organic": ["Compost"],
            "micronutrients": ["Zinc (stress tolerance)"],
            "npk": "Light feed; beans fix their own nitrogen",
            "soil_improvement": ["Maintain pH 6.0-7.0"],
        },
        severity_levels={
            "mild": "Slight mosaic on a few leaves.",
            "moderate": "Clear mosaic, downward curling, mild stunting.",
            "severe": "Severe distortion, poor pod set, plant decline.",
        },
        weather_conditions={
            "humidity": "Mild conditions favour aphids",
            "temperature": "20-28 C is peak aphid activity",
            "rainfall": "Cool, dry spells boost aphid movement",
        },
        emergency_actions=[
            "Rogue infected plants immediately.",
            "Control aphids across the planting within 3 days.",
            "Disinfect tools and wash hands between rows.",
        ],
    ),
]
