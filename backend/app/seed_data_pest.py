"""Pest and insect-damage records (AI Plant Doctor knowledge base)."""

from app.seed_data_common import _disease

PEST_DISEASES: list[dict] = [
    _disease(
        name="Thrips Infestation",
        category="Pest",
        scientific_name="Frankliniella, Thrips spp.",
        severity="Moderate",
        description=(
            "Tiny slender insects that rasp leaf and flower cells, leaving silvery streaks "
            "and black specks of frass. Damaged buds fail to open and fruit develops corky "
            "scars. Thrips also transmit tomato spotted wilt virus."
        ),
        symptoms=["silvery streaks", "black specks", "deformed flowers", "corky fruit scars", "silver flecking"],
        causes=["dry warm weather", "overwintering weeds", "infested transplants", "broad spectrum pesticide use"],
        treatment=["Blue sticky traps", "Insecticidal soap", "Spinosad"],
        prevention=["Use reflective mulch", "Control weeds", "Avoid killing predators"],
        affected_plants=["Tomato", "Onion", "Pepper", "Strawberry", "Gladiolus", "Rose"],
        chemical_treatment=[
            {
                "name": "Spinosad",
                "brand_names": ["Monterey Garden Insect Spray"],
                "active_ingredients": ["Spinosad 0.5%"],
                "dosage": "15 ml per 4 L water every 5-7 days",
                "safety_precautions": ["Toxic to bees until dry - spray at dusk", "Reapply after rain"],
                "waiting_period": "1 day",
            },
            {
                "name": "Insecticidal soap",
                "brand_names": ["Safer Insecticidal Soap"],
                "active_ingredients": ["Potassium salts of fatty acids"],
                "dosage": "20 ml per litre; spray flower buds and undersides",
                "safety_precautions": ["Do not spray in direct sun", "Repeat every 3 days"],
                "waiting_period": "0 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Orius (minute pirate bug)",
                "type": "Beneficial insect",
                "application": "Release 1-2 per plant",
                "when_to_apply": "At first thrips sign",
                "notes": "Voracious predator of thrips larvae.",
            },
            {
                "agent": "Amblyseius cucumeris",
                "type": "Predatory mite",
                "application": "Broadcast on foliage",
                "when_to_apply": "Preventively in warm weather",
                "notes": "Feeds on thrips larvae in buds and flowers.",
            },
        ],
        organic_remedies=[
            {
                "name": "Blue sticky traps",
                "recipe": "Blue glue cards",
                "application": "Hang just above the canopy",
                "frequency": "Replace weekly",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray buds and leaf undersides",
                "frequency": "Every 5-7 days",
            },
        ],
        prevention_tips=[
            {"category": "Environment", "title": "Use reflective mulch", "description": "Silver mulch disorients thrips landing."},
            {"category": "Weed management", "title": "Control weeds", "description": "Weeds harbour thrips between crops."},
            {"category": "Predator conservation", "title": "Avoid broad spectrum sprays", "description": "They kill the predators that control thrips."},
            {"category": "Plant hygiene", "title": "Check transplants", "description": "Inspect new plants for silvery damage before planting."},
        ],
        fertilizer={
            "organic": ["Seaweed extract"],
            "micronutrients": ["Silicon"],
            "npk": "Moderate balanced feed",
            "soil_improvement": ["Mulch to keep soil moisture steady"],
        },
        severity_levels={
            "mild": "Light silvering on a few leaves.",
            "moderate": "Silver streaks, deformed buds and flower damage.",
            "severe": "Heavy scarring, fruit corking and virus spread.",
        },
        weather_conditions={
            "humidity": "Hot, dry weather favours thrips",
            "temperature": "25-35 C is peak activity",
            "rainfall": "Cool, wet weather suppresses them",
        },
        emergency_actions=[
            "Hang many blue sticky traps immediately.",
            "Apply spinosad at dusk and repeat after 5 days.",
            "Remove severely damaged buds to reduce breeding.",
        ],
    ),
    _disease(
        name="Mealybug Infestation",
        category="Pest",
        scientific_name="Pseudococcus, Planococcus spp.",
        severity="Moderate",
        description=(
            "Soft, segmented insects covered in white waxy fluff that cluster at leaf joints, "
            "undersides and roots. They suck sap, excrete honeydew and weaken plants, often "
            "hidden inside a waxy shield that repels sprays."
        ),
        symptoms=["white cottony masses", "sticky honeydew", "ants on plants", "yellowing leaves", "sooty mould"],
        causes=["infested new plants", "ant farming", "greenhouse warmth", "overcrowded plants"],
        treatment=["Wipe with alcohol swabs", "Insecticidal soap", "Systemic insecticide"],
        prevention=["Quarantine new plants", "Control ants", "Check leaf joints"],
        affected_plants=["Houseplants", "Citrus", "Grape", "Hibiscus", "Orchid", "Succulents"],
        chemical_treatment=[
            {
                "name": "Insecticidal soap + oil",
                "brand_names": ["Safer Insecticidal Soap", "Bonide All Seasons Oil"],
                "active_ingredients": ["Potassium salts of fatty acids", "Mineral oil"],
                "dosage": "Spray every 5-7 days, covering all joints",
                "safety_precautions": ["Repeat to hit emerging nymphs", "Do not spray in heat"],
                "waiting_period": "0 days",
            },
            {
                "name": "Imidacloprid systemic drench",
                "brand_names": ["Bonide Systemic Insect Control"],
                "active_ingredients": ["Imidacloprid 2%"],
                "dosage": "Soil drench per label (ornamental use)",
                "safety_precautions": ["Toxic to bees - do not use on flowering food crops", "Keep from waterways"],
                "waiting_period": "Not for food crops near harvest",
            },
        ],
        biological_treatment=[
            {
                "agent": "Cryptolaemus (mealybug destroyer)",
                "type": "Beneficial insect",
                "application": "Release 2-5 per plant",
                "when_to_apply": "When mealybugs appear",
                "notes": "Larvae look like big mealybugs and eat the pests.",
            },
            {
                "agent": "Leptomastix dactylopii",
                "type": "Parasitic wasp",
                "application": "Release at first sign",
                "when_to_apply": "Early infestation",
                "notes": "Parasitises citrus mealybug specifically.",
            },
        ],
        organic_remedies=[
            {
                "name": "Alcohol swab",
                "recipe": "70% isopropyl alcohol on a cotton swab",
                "application": "Dab each waxy mass directly",
                "frequency": "Every few days",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray all stems and joints",
                "frequency": "Every 5-7 days",
            },
        ],
        prevention_tips=[
            {"category": "Plant hygiene", "title": "Quarantine new plants", "description": "Isolate newcomers for 2-3 weeks."},
            {"category": "Ant control", "title": "Stop ant farming", "description": "Ants protect mealybugs - prune ant trails."},
            {"category": "Monitoring", "title": "Check leaf joints", "description": "Mealybugs hide where leaves meet stems."},
            {"category": "Environment", "title": "Avoid overcrowding", "description": "Good airflow slows mealybug spread."},
        ],
        fertilizer={
            "organic": ["Compost", "Seaweed extract"],
            "micronutrients": ["Seaweed"],
            "npk": "Balanced feed; avoid nitrogen excess",
            "soil_improvement": ["Repot in clean mix if root mealybugs are found"],
        },
        severity_levels={
            "mild": "A few cottony clusters at joints.",
            "moderate": "Waxy masses spreading, honeydew and ants.",
            "severe": "Yellowing, sooty mould and plant decline.",
        },
        weather_conditions={
            "humidity": "Warm greenhouse conditions",
            "temperature": "21-30 C is peak activity",
            "rainfall": "Outdoor cool weather slows them",
        },
        emergency_actions=[
            "Dab every visible mass with alcohol immediately.",
            "Apply insecticidal soap and repeat after 5 days.",
            "Quarantine the plant away from others.",
        ],
    ),
    _disease(
        name="Root-knot Nematode",
        category="Pest",
        scientific_name="Meloidogyne spp.",
        severity="Severe",
        description=(
            "Microscopic worms that invade roots and trigger knotted, galled swellings that "
            "block water and nutrient uptake. Plants look water-stressed even when watered, "
            "stunt, yellow and wilt. Very common in warm sandy soils."
        ),
        symptoms=["root galls", "wilting in heat", "stunted yellow plants", "poor root growth", "wilt despite watering"],
        causes=["Meloidogyne nematodes", "infested soil", "continuous host cropping", "warm sandy soil"],
        treatment=["Remove galled roots", "Solarise soil", "Grow resistant varieties"],
        prevention=["Rotate with grasses", "Use resistant rootstocks", "Add compost"],
        affected_plants=["Tomato", "Cucumber", "Carrot", "Okra", "Potato", "Beans", "Squash"],
        chemical_treatment=[
            {
                "name": "Soil solarisation (heat)",
                "brand_names": ["Clear plastic sheeting"],
                "active_ingredients": ["Solar heat"],
                "dosage": "Cover moist soil with clear plastic 4-6 weeks in summer",
                "safety_precautions": ["Requires a full-sun season", "Water soil first"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "No effective home-use nematicide",
                "brand_names": [],
                "active_ingredients": ["-"],
                "dosage": "None - rely on rotation and resistance",
                "safety_precautions": ["Do not use restricted nematicides at home"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Paecilomyces lilacinus",
                "type": "Beneficial fungus",
                "application": "Soil drench at planting",
                "when_to_apply": "Transplant time",
                "notes": "Infects nematode eggs and juveniles in the soil.",
            },
            {
                "agent": "Neem cake",
                "type": "Organic amendment",
                "application": "Work neem cake into the bed",
                "when_to_apply": "Before planting",
                "notes": "Suppresses nematode build-up in the root zone.",
            },
        ],
        organic_remedies=[
            {
                "name": "Marigold trap crop",
                "recipe": "Grow French marigolds before the crop",
                "application": "Turn under before planting",
                "frequency": "Each season",
            },
            {
                "name": "Compost amendment",
                "recipe": "Add 5 cm mature compost",
                "application": "Mix into the bed",
                "frequency": "Yearly",
            },
        ],
        prevention_tips=[
            {"category": "Resistant varieties", "title": "Use resistant rootstocks", "description": "Many tomato and pepper hybrids resist nematodes."},
            {"category": "Crop rotation", "title": "Rotate with grasses", "description": "Corn and grains do not host Meloidogyne."},
            {"category": "Soil health", "title": "Feed soil biology", "description": "Rich, composted soil suppresses nematode damage."},
            {"category": "Field sanitation", "title": "Remove all roots", "description": "Galled roots left in soil keep the cycle going."},
        ],
        fertilizer={
            "organic": ["Compost", "Neem cake"],
            "micronutrients": ["Seaweed extract"],
            "npk": "Balanced feed; steady watering reduces stress",
            "soil_improvement": ["Add organic matter to sandy soils"],
        },
        severity_levels={
            "mild": "A few small root galls, mild stunting.",
            "moderate": "Knotted roots, daytime wilting.",
            "severe": "Heavy galls, severe wilt and crop loss.",
        },
        weather_conditions={
            "humidity": "Warm, sandy soils favour nematodes",
            "temperature": "25-32 C soil temperature",
            "rainfall": "Drought stress worsens symptoms",
        },
        emergency_actions=[
            "Dig out galled plants with surrounding soil and bag them.",
            "Solarise the bed before replanting.",
            "Rotate to grasses and add compost next season.",
        ],
    ),
    _disease(
        name="Cutworm Damage",
        category="Pest",
        scientific_name="Agrotis, Noctua spp.",
        severity="Moderate",
        description=(
            "Fat grey-brown caterpillars that hide in soil by day and chew through seedling "
            "stems at the base at night, felling plants as if cut with a knife. Damage is "
            "worst in freshly worked beds and weedy gardens."
        ),
        symptoms=["cut seedling stems", "plants fallen overnight", "chewed stem bases", "holes at soil line"],
        causes=["cutworm larvae", "weedy beds", "freshly tilled soil", "mulch harbouring eggs"],
        treatment=["Search soil at dusk", "Collars around stems", "Bacillus thuringiensis"],
        prevention=["Clear weeds before planting", "Till soil before planting", "Remove hiding debris"],
        affected_plants=["Tomato", "Lettuce", "Cabbage", "Corn", "Bean", "All seedlings"],
        chemical_treatment=[
            {
                "name": "Bt-based insecticide",
                "brand_names": ["Monterey Bt", "Thuricide"],
                "active_ingredients": ["Bacillus thuringiensis kurstaki"],
                "dosage": "Spray stem bases and soil line at dusk",
                "safety_precautions": ["Target caterpillars only", "Reapply after rain"],
                "waiting_period": "0 days",
            },
            {
                "name": "Carbaryl bait (if allowed)",
                "brand_names": ["Sevin 5% bait"],
                "active_ingredients": ["Carbaryl"],
                "dosage": "Scatter bait around stems per label",
                "safety_precautions": ["Highly toxic to bees - use sparingly", "Keep away from edible parts"],
                "waiting_period": "7 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus thuringiensis (Bt)",
                "type": "Bio-insecticide",
                "application": "Drench around stem bases at dusk",
                "when_to_apply": "When first cut stems appear",
                "notes": "Kills only caterpillars; harmless to everything else.",
            },
            {
                "agent": "Ground beetles and birds",
                "type": "Natural predator",
                "application": "Encourage habitats for beetles and birds",
                "when_to_apply": "Ongoing",
                "notes": "Natural predators eat cutworm larvae.",
            },
        ],
        organic_remedies=[
            {
                "name": "Cardboard collars",
                "recipe": "Cut cardboard/paper cups into 5 cm collars",
                "application": "Sink around each seedling stem",
                "frequency": "At planting",
            },
            {
                "name": "Hand picking at dusk",
                "recipe": "Torch + bucket of soapy water",
                "application": "Search soil near cut stems at night",
                "frequency": "Every night for a week",
            },
        ],
        prevention_tips=[
            {"category": "Husbandry", "title": "Clear weeds before planting", "description": "Cutworms breed in weedy, undisturbed soil."},
            {"category": "Planting", "title": "Use stem collars", "description": "A 5 cm collar stops larvae reaching the stem."},
            {"category": "Field sanitation", "title": "Remove hiding debris", "description": "Planks, stones and clods shelter cutworms."},
            {"category": "Tillage", "title": "Till soil before planting", "description": "Exposes and kills resting larvae and pupae."},
        ],
        fertilizer={
            "organic": ["Compost"],
            "micronutrients": ["Seaweed extract"],
            "npk": "Light balanced feed for seedlings",
            "soil_improvement": ["Keep beds clear and friable"],
        },
        severity_levels={
            "mild": "A few seedlings cut at the base.",
            "moderate": "Several plants felled each night.",
            "severe": "Whole rows wiped out after transplant.",
        },
        weather_conditions={
            "humidity": "Moist, friable soil suits larvae",
            "temperature": "18-27 C is peak activity",
            "rainfall": "Warm, damp nights increase feeding",
        },
        emergency_actions=[
            "Replace cut seedlings and add collars immediately.",
            "Scatter Bt at the soil line at dusk.",
            "Hand-pick larvae for a week to break the cycle.",
        ],
    ),
    _disease(
        name="Tomato Hornworm",
        category="Pest",
        scientific_name="Manduca quinquemaculata",
        severity="Moderate",
        description=(
            "Large green caterpillars up to 10 cm long with a horn-like tail that strip "
            "leaves and fruit from tomato plants almost overnight, leaving bare stems and "
            "frass. Camouflage makes them hard to spot until the damage is severe."
        ),
        symptoms=["defoliated stems", "large green caterpillar", "black droppings on leaves", "chewed fruit", "stripped branches"],
        causes=["hornworm larvae", "overwintering pupae in soil", "no natural predators"],
        treatment=["Hand pick caterpillars", "Bt spray", "Tilling to destroy pupae"],
        prevention=["Till soil in spring", "Plant dill and flowers", "Inspect weekly"],
        affected_plants=["Tomato", "Potato", "Eggplant", "Pepper"],
        chemical_treatment=[
            {
                "name": "Bt-based insecticide",
                "brand_names": ["Monterey Bt", "Thuricide"],
                "active_ingredients": ["Bacillus thuringiensis kurstaki"],
                "dosage": "Spray foliage thoroughly when worms are small",
                "safety_precautions": ["Caterpillars must eat the spray", "Reapply after rain"],
                "waiting_period": "0 days",
            },
            {
                "name": "Spinosad",
                "brand_names": ["Monterey Garden Insect Spray"],
                "active_ingredients": ["Spinosad 0.5%"],
                "dosage": "15 ml per 4 L water",
                "safety_precautions": ["Toxic to bees until dry", "Spray at dusk"],
                "waiting_period": "1 day",
            },
        ],
        biological_treatment=[
            {
                "agent": "Braconid wasps",
                "type": "Parasitic wasp",
                "application": "Encourage wasp habitat (dill, fennel)",
                "when_to_apply": "Growing season",
                "notes": "Their larvae eat hornworms from the inside - leave parasitised worms alone.",
            },
            {
                "agent": "Bacillus thuringiensis (Bt)",
                "type": "Bio-insecticide",
                "application": "Foliar spray at dusk",
                "when_to_apply": "When worms are under 4 cm",
                "notes": "Kills the caterpillar within days of eating.",
            },
        ],
        organic_remedies=[
            {
                "name": "Hand picking",
                "recipe": "Check plants daily, remove worms",
                "application": "Look for frass droppings to find them",
                "frequency": "Daily in summer",
            },
            {
                "name": "Dill and marigold companions",
                "recipe": "Plant dill, marigold and basil nearby",
                "application": "Attracts wasps that control hornworms",
                "frequency": "Each season",
            },
        ],
        prevention_tips=[
            {"category": "Tillage", "title": "Till soil in spring", "description": "Destroys pupae that overwinter in the ground."},
            {"category": "Predator conservation", "title": "Grow dill and flowers", "description": "Attract parasitic wasps that control hornworms."},
            {"category": "Monitoring", "title": "Inspect plants weekly", "description": "Look under leaves and for black droppings."},
            {"category": "Field sanitation", "title": "Do not crush parasitised worms", "description": "Leave them - wasp cocoons mean they will die soon."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp extract"],
            "micronutrients": ["Seaweed"],
            "npk": "Balanced feed",
            "soil_improvement": ["Mulch to keep the soil cool"],
        },
        severity_levels={
            "mild": "One or two worms, minor leaf loss.",
            "moderate": "Several branches stripped, visible frass.",
            "severe": "Most leaves gone, fruit exposed and chewed.",
        },
        weather_conditions={
            "humidity": "Warm summer conditions",
            "temperature": "20-30 C is peak activity",
            "rainfall": "Active all warm season",
        },
        emergency_actions=[
            "Hand-pick all visible worms immediately.",
            "Apply Bt the same evening.",
            "Tillage at season end to destroy pupae.",
        ],
    ),
    _disease(
        name="Scale Insects",
        category="Pest",
        scientific_name="Coccidae, Diaspididae spp.",
        severity="Moderate",
        description=(
            "Small, shell-like bumps that cling to stems, leaf veins and fruit, sucking sap "
            "from under a waxy cover. Heavy infestations cause yellowing, sooty mould on "
            "honeydew and branch dieback on trees and houseplants."
        ),
        symptoms=["shell bumps on stems", "sticky honeydew", "sooty mould", "yellowing leaves", "branch dieback"],
        causes=["infested nursery plants", "ant farming", "overcrowding", "weak, stressed plants"],
        treatment=["Scrub off scale", "Horticultural oil", "Systemic insecticide"],
        prevention=["Quarantine new plants", "Control ants", "Prune infested branches"],
        affected_plants=["Citrus", "Grape", "Rose", "Ficus", "Houseplants", "Orchid"],
        chemical_treatment=[
            {
                "name": "Horticultural oil",
                "brand_names": ["Bonide All Seasons Oil"],
                "active_ingredients": ["Mineral oil 98%"],
                "dosage": "10 ml per litre in cool weather; suffocates scale",
                "safety_precautions": ["Do not spray in heat or on drought-stressed plants", "Cover every surface"],
                "waiting_period": "0 days",
            },
            {
                "name": "Imidacloprid systemic drench",
                "brand_names": ["Bonide Systemic Insect Control"],
                "active_ingredients": ["Imidacloprid 2%"],
                "dosage": "Soil drench per label (ornamental use)",
                "safety_precautions": ["Toxic to bees - avoid flowering plants", "Keep from waterways"],
                "waiting_period": "Not for food crops near harvest",
            },
        ],
        biological_treatment=[
            {
                "agent": "Rhyzobius lophanthae (ladybird)",
                "type": "Beneficial insect",
                "application": "Release near scale colonies",
                "when_to_apply": "When scale first appears",
                "notes": "Specialist predator of armoured scale.",
            },
            {
                "agent": "Aphytis melinus (parasitic wasp)",
                "type": "Beneficial insect",
                "application": "Release on infested trees",
                "when_to_apply": "Warm season",
                "notes": "Parasitises scale on citrus and ornamentals.",
            },
        ],
        organic_remedies=[
            {
                "name": "Scrubbing + oil",
                "recipe": "Soft brush + water, then horticultural oil",
                "application": "Scrub off covers, spray with oil",
                "frequency": "Every 10 days",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray stems and leaf veins",
                "frequency": "Weekly",
            },
        ],
        prevention_tips=[
            {"category": "Plant hygiene", "title": "Quarantine new plants", "description": "Scale rides in on nursery stock."},
            {"category": "Ant control", "title": "Control ants", "description": "Ants move and protect scale."},
            {"category": "Pruning", "title": "Prune infested branches", "description": "Remove the worst branches in winter."},
            {"category": "Monitoring", "title": "Scout stems and veins", "description": "Catch scale before it builds up."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp extract"],
            "micronutrients": ["Seaweed"],
            "npk": "Balanced feed; avoid nitrogen excess",
            "soil_improvement": ["Keep plants vigorous but not lush"],
        },
        severity_levels={
            "mild": "A few shells on stems.",
            "moderate": "Colonies on stems with honeydew and sooty mould.",
            "severe": "Heavy scale cover, yellowing and dieback.",
        },
        weather_conditions={
            "humidity": "Warm, sheltered conditions",
            "temperature": "22-30 C is peak activity",
            "rainfall": "Cool, wet weather slows them",
        },
        emergency_actions=[
            "Scrub off visible scale immediately.",
            "Apply horticultural oil within 3 days.",
            "Prune badly infested branches and control ants.",
        ],
    ),
    _disease(
        name="Fall Armyworm",
        category="Pest",
        scientific_name="Spodoptera frugiperda",
        severity="Severe",
        description=(
            "A destructive caterpillar with an inverted Y on its head that feeds in masses, "
            "stripping leaves, boring into cobs and cutting seedlings. It migrates fast and "
            "attacks corn, rice and many vegetable crops."
        ),
        symptoms=["chewed leaf windows", "falling frass", "holes in corn ears", "cut seedling bases", "masses of larvae"],
        causes=["migrating moths", "warm night flights", "wind-borne egg laying", "continuous host cropping"],
        treatment=["Bt or spinosad at dusk", "Hand pick egg masses", "Trap moths"],
        prevention=["Use pheromone traps", "Crop rotation", "Early planting"],
        affected_plants=["Corn", "Maize", "Rice", "Sorghum", "Tomato", "Cotton"],
        chemical_treatment=[
            {
                "name": "Spinosad",
                "brand_names": ["Monterey Garden Insect Spray"],
                "active_ingredients": ["Spinosad 0.5%"],
                "dosage": "15 ml per 4 L water at dusk",
                "safety_precautions": ["Toxic to bees until dry", "Reapply after rain"],
                "waiting_period": "1 day",
            },
            {
                "name": "Bt-based insecticide",
                "brand_names": ["Monterey Bt", "Thuricide"],
                "active_ingredients": ["Bacillus thuringiensis kurstaki"],
                "dosage": "Spray young larvae before they bore in",
                "safety_precautions": ["Target young worms", "Spray at dusk"],
                "waiting_period": "0 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Trichogramma wasps",
                "type": "Beneficial insect",
                "application": "Release egg parasitoids weekly",
                "when_to_apply": "At moth flight peaks",
                "notes": "Parasitises armyworm eggs before they hatch.",
            },
            {
                "agent": "Bacillus thuringiensis (Bt)",
                "type": "Bio-insecticide",
                "application": "Foliar spray at dusk",
                "when_to_apply": "Larvae under 2 cm",
                "notes": "Kills caterpillars that eat sprayed leaves.",
            },
        ],
        organic_remedies=[
            {
                "name": "Egg mass destruction",
                "recipe": "Scrape off furry egg masses",
                "application": "Crush or drop in soapy water",
                "frequency": "Weekly",
            },
            {
                "name": "Pheromone trap",
                "recipe": "Commercially available armyworm traps",
                "application": "Set at crop height",
                "frequency": "Monitor and reset weekly",
            },
        ],
        prevention_tips=[
            {"category": "Monitoring", "title": "Set pheromone traps", "description": "Detect moth flights before larvae appear."},
            {"category": "Crop rotation", "title": "Rotate away from host crops", "description": "Breaks the armyworm breeding cycle."},
            {"category": "Planting", "title": "Plant early", "description": "Early crops avoid peak moth flights."},
            {"category": "Field sanitation", "title": "Destroy crop residue", "description": "Larvae pupate in old stems and cobs."},
        ],
        fertilizer={
            "organic": ["Compost"],
            "micronutrients": ["Silicon"],
            "npk": "Balanced feed; avoid nitrogen excess",
            "soil_improvement": ["Good drainage keeps plants vigorous"],
        },
        severity_levels={
            "mild": "Window-pane feeding on a few leaves.",
            "moderate": "Masses stripping leaves, holes in ears.",
            "severe": "Whole fields stripped, ears ruined.",
        },
        weather_conditions={
            "humidity": "Warm, humid nights favour moths",
            "temperature": "24-32 C is peak activity",
            "rainfall": "Favoured after warm wet spells",
        },
        emergency_actions=[
            "Spray Bt or spinosad at dusk immediately.",
            "Hand-pick egg masses and young larvae.",
            "Set pheromone traps to track the next moth flight.",
        ],
    ),
]
