"""Expanded fungal disease records (AI Plant Doctor knowledge base)."""

from app.seed_data_common import _disease

FUNGAL_DISEASES: list[dict] = [
    _disease(
        name="Gray Mold (Botrytis)",
        category="Fungal",
        scientific_name="Botrytis cinerea",
        severity="Moderate",
        description=(
            "A fuzzy grey-brown mould that attacks flowers, buds, fruit and young stems, "
            "often starting at a wound or spent blossom. Spreads rapidly in cool, damp, "
            "poorly-ventilated conditions and can rot whole clusters of fruit."
        ),
        symptoms=["gray fuzzy mold", "brown water spots", "rotting flowers", "stem rot", "fruit rot"],
        causes=["cool damp air", "poor airflow", "wet flowers", "crowding", "wounded tissue"],
        treatment=["Remove infected parts immediately", "Improve airflow", "Apply copper or iprodione fungicide"],
        prevention=["Water at the base", "Prune crowding", "Harvest promptly", "Sanitise pruners"],
        affected_plants=["Tomato", "Strawberry", "Grape", "Rose", "Lettuce", "Onion", "Cucumber"],
        chemical_treatment=[
            {
                "name": "Iprodione fungicide",
                "brand_names": ["Rovral", "Chipco"],
                "active_ingredients": ["Iprodione 23%"],
                "dosage": "10 ml per litre every 7-10 days at first signs",
                "safety_precautions": ["Wear gloves and mask", "Do not spray near harvest window"],
                "waiting_period": "7 days before harvest",
            },
            {
                "name": "Copper fungicide",
                "brand_names": ["Cueva", "Bonide Copper"],
                "active_ingredients": ["Copper octanoate"],
                "dosage": "15 ml per litre weekly",
                "safety_precautions": ["Rotate with other chemistries", "Avoid waterways"],
                "waiting_period": "1 day",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L every 7 days",
                "when_to_apply": "Before cool damp nights",
                "notes": "Colonises flowers and wounds, blocking Botrytis entry.",
            },
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench + flower spray 5 g/L",
                "when_to_apply": "At flowering",
                "notes": "Suppresses grey mould spores on surfaces.",
            },
        ],
        organic_remedies=[
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 tsp oil + 1 L water",
                "application": "Spray flowers and fruit clusters",
                "frequency": "Every 5-7 days",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray at dusk",
                "frequency": "Weekly",
            },
            {
                "name": "Garlic tea",
                "recipe": "Steep 6 crushed garlic cloves in 1 L hot water, strain",
                "application": "Spray on affected parts",
                "frequency": "Weekly",
            },
        ],
        prevention_tips=[
            {"category": "Airflow", "title": "Space and prune plants", "description": "Open canopies dry out fast and stop grey mould."},
            {"category": "Irrigation", "title": "Water the soil, not the flowers", "description": "Wet blossoms are the number-one entry point."},
            {"category": "Field sanitation", "title": "Remove spent blooms", "description": "Deadheading denies Botrytis its starting point."},
            {"category": "Harvest", "title": "Pick fruit promptly", "description": "Overripe, bruised fruit rots quickly."},
            {"category": "Environment", "title": "Ventilate greenhouses", "description": "Lower night humidity to break the cycle."},
        ],
        fertilizer={
            "organic": ["Compost", "Seaweed extract"],
            "micronutrients": ["Calcium (firmer fruit tissue)"],
            "npk": "Balanced 10-10-10; avoid lush nitrogen growth",
            "soil_improvement": ["Mulch to stop soil splash onto flowers"],
        },
        severity_levels={
            "mild": "Small grey patches on a few spent flowers.",
            "moderate": "Grey mould spreading on fruit clusters and stems.",
            "severe": "Whole fruit clusters rot and stems collapse.",
        },
        weather_conditions={
            "humidity": "High humidity (>85%) with cool nights",
            "temperature": "15-22 C ideal for Botrytis",
            "rainfall": "Extended wet, misty spells trigger outbreaks",
        },
        emergency_actions=[
            "Bag and remove all mouldy fruit and flowers immediately.",
            "Apply copper fungicide the same day and repeat weekly.",
            "Prune to open the canopy and ventilate the area.",
        ],
    ),
    _disease(
        name="Black Spot (Rose)",
        category="Fungal",
        scientific_name="Diplocarpon rosae",
        severity="Moderate",
        description=(
            "Circular black spots with ragged, feathery edges on rose leaves, surrounded by "
            "a yellow halo. Infected leaves yellow and drop, weakening the rose bush over time."
        ),
        symptoms=["black circular spots", "yellow halo", "leaf drop", "bare lower stems"],
        causes=["wet foliage", "overhead watering", "cool humid weather", "fallen infected leaves"],
        treatment=["Remove spotted leaves", "Apply sulfur or myclobutanil", "Mulch around the bush"],
        prevention=["Water at the base", "Prune for airflow", "Rake up fallen leaves"],
        affected_plants=["Rose"],
        chemical_treatment=[
            {
                "name": "Myclobutanil fungicide",
                "brand_names": ["Immunox", "Bayer Rose & Flower"],
                "active_ingredients": ["Myclobutanil 1.55%"],
                "dosage": "15 ml per 4 L water every 14 days",
                "safety_precautions": ["Avoid spraying in bloom heat", "Wear gloves"],
                "waiting_period": "30 days on edibles",
            },
            {
                "name": "Sulfur fungicide",
                "brand_names": ["Safer Brand", "Bonide Sulfur"],
                "active_ingredients": ["Micronized sulfur"],
                "dosage": "3 g per litre weekly",
                "safety_precautions": ["Do not spray above 30 C", "Avoid in high heat"],
                "waiting_period": "1 day",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L weekly",
                "when_to_apply": "Morning after dew dries",
                "notes": "Protective biofilm blocks spore germination.",
            },
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Foliar + soil drench 5 g/L monthly",
                "when_to_apply": "During humid seasons",
                "notes": "Boosts natural defences of the rose.",
            },
        ],
        organic_remedies=[
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 tsp vegetable oil + 1 tsp soap + 1 L water",
                "application": "Spray all leaf surfaces weekly",
                "frequency": "Weekly",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray at dusk",
                "frequency": "Every 7 days",
            },
            {
                "name": "Milk spray",
                "recipe": "1 part milk + 2 parts water",
                "application": "Spray foliage",
                "frequency": "Twice weekly",
            },
        ],
        prevention_tips=[
            {"category": "Irrigation", "title": "Water at the base", "description": "Keep rose leaves dry - splash spreads spores."},
            {"category": "Field sanitation", "title": "Rake up fallen leaves", "description": "Black spot overwinters in leaf litter."},
            {"category": "Pruning", "title": "Prune for airflow", "description": "Open the centre of the bush so leaves dry fast."},
            {"category": "Resistant varieties", "title": "Grow resistant roses", "description": "Knock Out and many shrub roses resist black spot."},
            {"category": "Mulching", "title": "Mulch to stop splash", "description": "A 5 cm mulch layer keeps spores out of the soil."},
        ],
        fertilizer={
            "organic": ["Rose compost", "Fish emulsion", "Kelp meal"],
            "micronutrients": ["Seaweed extract"],
            "npk": "Balanced rose feed 5-5-5 or 6-4-4",
            "soil_improvement": ["Keep pH 6.0-6.5; add compost annually"],
        },
        severity_levels={
            "mild": "A few spotted leaves near the base.",
            "moderate": "Spots on many leaves with yellowing and drop.",
            "severe": "Bush largely defoliated and stunted.",
        },
        weather_conditions={
            "humidity": "Wet leaves for 6+ hours",
            "temperature": "18-26 C favours black spot",
            "rainfall": "Rainy springs drive outbreaks",
        },
        emergency_actions=[
            "Strip and bag all spotted leaves immediately.",
            "Apply myclobutanil within 24 hours.",
            "Clean up every fallen leaf before winter.",
        ],
    ),
    _disease(
        name="Apple Scab",
        category="Fungal",
        scientific_name="Venturia inaequalis",
        severity="Moderate",
        description=(
            "Olive-green to black velvety lesions on apple leaves and fruit. Heavy infection "
            "distorts leaves, cracks fruit skin and ruins the crop. Spores spread in spring rain."
        ),
        symptoms=["olive green spots", "black velvety lesions", "distorted leaves", "cracked fruit"],
        causes=["spring rain", "infected leaf litter", "humid conditions", "dense canopy"],
        treatment=["Remove infected leaves", "Apply myclobutanil or captan", "Rake fallen leaves"],
        prevention=["Rake autumn leaves", "Prune for airflow", "Grow scab-resistant varieties"],
        affected_plants=["Apple", "Pear", "Crabapple"],
        chemical_treatment=[
            {
                "name": "Captan fungicide",
                "brand_names": ["Bonide Captan", "Hi-Yield"],
                "active_ingredients": ["Captan 50%"],
                "dosage": "15 ml per 4 L water every 7-10 days in spring",
                "safety_precautions": ["Wear gloves and mask", "Do not spray in heat"],
                "waiting_period": "1 day before harvest",
            },
            {
                "name": "Myclobutanil fungicide",
                "brand_names": ["Immunox"],
                "active_ingredients": ["Myclobutanil 1.55%"],
                "dosage": "15 ml per 4 L every 14 days",
                "safety_precautions": ["Avoid spraying in bloom", "Wear gloves"],
                "waiting_period": "30 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L from pink bud stage",
                "when_to_apply": "Before rain events",
                "notes": "Protective coverage on young leaves.",
            },
            {
                "agent": "Trichoderma atroviride",
                "type": "Beneficial microbe",
                "application": "Leaf-litter spray at leaf fall",
                "when_to_apply": "Autumn",
                "notes": "Degrades overwintering spores on fallen leaves.",
            },
        ],
        organic_remedies=[
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 tsp oil + 1 L water",
                "application": "Spray young leaves weekly",
                "frequency": "Weekly in spring",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray at dusk",
                "frequency": "Every 7 days",
            },
        ],
        prevention_tips=[
            {"category": "Field sanitation", "title": "Rake up autumn leaves", "description": "Destroy leaves where scab overwinters."},
            {"category": "Pruning", "title": "Open the canopy", "description": "Sunlight and airflow dry leaves faster."},
            {"category": "Resistant varieties", "title": "Plant resistant cultivars", "description": "e.g., 'Liberty', 'Enterprise', 'GoldRush'."},
            {"category": "Irrigation", "title": "Avoid overhead watering", "description": "Water at the soil line."},
        ],
        fertilizer={
            "organic": ["Composted manure", "Kelp meal"],
            "micronutrients": ["Zinc"],
            "npk": "Balanced 10-10-10 in spring",
            "soil_improvement": ["Maintain pH 6.0-6.5"],
        },
        severity_levels={
            "mild": "A few lesions on lower leaves.",
            "moderate": "Scab on many leaves and some fruit.",
            "severe": "Fruit heavily cracked, leaves distorted and dropping.",
        },
        weather_conditions={
            "humidity": "Wet leaves in spring drive primary infections",
            "temperature": "15-24 C ideal",
            "rainfall": "Spring rains spread spores",
        },
        emergency_actions=[
            "Remove and destroy scabbed leaves and fruit.",
            "Apply a protectant fungicide before the next rain.",
            "Rake every fallen leaf at season end.",
        ],
    ),
    _disease(
        name="Brown Rot (Stone Fruit)",
        category="Fungal",
        scientific_name="Monilinia fructicola",
        severity="Severe",
        description=(
            "Rapidly spreading brown rot that mummifies peaches, plums and cherries. Blossoms "
            "turn brown, twigs form cankers and fruit rots with dusty grey-brown spore tufts."
        ),
        symptoms=["brown rotted fruit", "mummified fruit", "brown blossoms", "twig cankers"],
        causes=["wet bloom period", "fruit wounds", "insect damage", "overcrowded branches"],
        treatment=["Remove mummies and cankers", "Apply sulfur fungicide", "Prune for airflow"],
        prevention=["Thin fruit", "Prune out cankers", "Clean up fallen fruit"],
        affected_plants=["Peach", "Plum", "Cherry", "Apricot", "Nectarine"],
        chemical_treatment=[
            {
                "name": "Sulfur fungicide",
                "brand_names": ["Bonide Sulfur"],
                "active_ingredients": ["Micronized sulfur"],
                "dosage": "3 g per litre at bloom and pre-harvest",
                "safety_precautions": ["Do not spray in heat", "Wear gloves"],
                "waiting_period": "1 day",
            },
            {
                "name": "Iprodione fungicide",
                "brand_names": ["Rovral"],
                "active_ingredients": ["Iprodione 23%"],
                "dosage": "10 ml per litre at bloom and 2 weeks pre-harvest",
                "safety_precautions": ["Wear PPE", "Avoid spray drift"],
                "waiting_period": "7 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Bloom spray 2 g/L",
                "when_to_apply": "At pink bloom",
                "notes": "Protects blossoms, the main infection point.",
            },
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Foliar + soil spray monthly",
                "when_to_apply": "Growing season",
                "notes": "Competes with Monilinia on fruit surfaces.",
            },
        ],
        organic_remedies=[
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 tsp oil + 1 L water",
                "application": "Spray blossoms and fruit",
                "frequency": "Weekly during bloom",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray at dusk",
                "frequency": "Weekly",
            },
        ],
        prevention_tips=[
            {"category": "Field sanitation", "title": "Remove mummies", "description": "Pick and destroy all shrivelled fruit from tree and ground."},
            {"category": "Pruning", "title": "Prune out cankers", "description": "Cut 10 cm below brown, sunken cankers."},
            {"category": "Fruit thinning", "title": "Thin fruit", "description": "Fewer, spaced fruits dry faster and wound less."},
            {"category": "Pest control", "title": "Control fruit moths", "description": "Insect wounds are entry points for the fungus."},
        ],
        fertilizer={
            "organic": ["Composted manure", "Bone meal"],
            "micronutrients": ["Calcium"],
            "npk": "Balanced 10-10-10; avoid excess nitrogen",
            "soil_improvement": ["Mulch and maintain pH 6.0-6.5"],
        },
        severity_levels={
            "mild": "A few rotted fruit, minor blossom blight.",
            "moderate": "Mummies on the tree, cankers on twigs.",
            "severe": "Major fruit loss and limb dieback.",
        },
        weather_conditions={
            "humidity": "Wet bloom weather is the main trigger",
            "temperature": "20-28 C during wet spells",
            "rainfall": "Rain during bloom and before harvest",
        },
        emergency_actions=[
            "Remove every mummy and cankered twig immediately.",
            "Apply sulfur at first sign and repeat weekly.",
            "Do not compost infected fruit - bag and bin them.",
        ],
    ),
    _disease(
        name="Cercospora Leaf Spot",
        category="Fungal",
        scientific_name="Cercospora spp.",
        severity="Moderate",
        description=(
            "Small tan-to-brown circular spots with darker borders on leaves, most common on "
            "beets, peppers and beans. Heavy spotting causes premature leaf drop and poor yields."
        ),
        symptoms=["tan spots", "brown rings", "premature leaf drop", "dark borders"],
        causes=["warm humid weather", "overhead watering", "infected debris", "dense planting"],
        treatment=["Remove spotted leaves", "Apply copper fungicide", "Mulch to stop splash"],
        prevention=["Water at the base", "Rotate crops", "Clean up debris"],
        affected_plants=["Beet", "Pepper", "Bean", "Spinach", "Carrot"],
        chemical_treatment=[
            {
                "name": "Copper fungicide",
                "brand_names": ["Cueva", "Bonide Copper"],
                "active_ingredients": ["Copper octanoate"],
                "dosage": "15 ml per litre every 7-10 days",
                "safety_precautions": ["Rotate chemistries", "Avoid waterways"],
                "waiting_period": "1 day",
            },
            {
                "name": "Chlorothalonil fungicide",
                "brand_names": ["Daconil"],
                "active_ingredients": ["Chlorothalonil 54%"],
                "dosage": "15 ml per 4 L every 7 days",
                "safety_precautions": ["Toxic to fish", "Wear PPE"],
                "waiting_period": "7 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus amyloliquefaciens",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L weekly",
                "when_to_apply": "At first spotting",
                "notes": "Suppresses spore germination on leaves.",
            },
            {
                "agent": "Trichoderma viride",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L at planting",
                "when_to_apply": "Transplant time",
                "notes": "Reduces soil-borne inoculum.",
            },
        ],
        organic_remedies=[
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 L water + soap",
                "application": "Spray foliage weekly",
                "frequency": "Weekly",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray at dusk",
                "frequency": "Every 7 days",
            },
        ],
        prevention_tips=[
            {"category": "Irrigation", "title": "Water at the soil line", "description": "Keep foliage dry to stop spread."},
            {"category": "Crop rotation", "title": "Rotate host crops", "description": "2-3 year break between beet/bean crops."},
            {"category": "Field sanitation", "title": "Clean up debris", "description": "Spores overwinter on old leaves."},
            {"category": "Spacing", "title": "Space plants", "description": "Good airflow dries leaves faster."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp meal"],
            "micronutrients": ["Potassium silicate"],
            "npk": "Balanced feed; avoid nitrogen excess",
            "soil_improvement": ["Mulch to reduce splash"],
        },
        severity_levels={
            "mild": "Scattered spots on lower leaves.",
            "moderate": "Spots on 30-50% of foliage.",
            "severe": "Severe defoliation and crop loss.",
        },
        weather_conditions={
            "humidity": "Warm, humid conditions",
            "temperature": "25-30 C",
            "rainfall": "Rain and dew spread spores",
        },
        emergency_actions=[
            "Strip and bag heavily spotted leaves.",
            "Apply copper fungicide within 24 hours.",
            "Repeat every 7 days until new growth is clean.",
        ],
    ),
    _disease(
        name="Verticillium Wilt",
        category="Fungal",
        scientific_name="Verticillium dahliae",
        severity="Severe",
        description=(
            "A soil-borne wilt that yellows and wilts one branch at a time, progressing to "
            "whole-plant collapse. The fungus persists in soil for years inside resistant "
            "weed hosts and enters through the roots."
        ),
        symptoms=["one branch wilting", "leaf yellowing", "stunted growth", "brown stem streaks"],
        causes=["Verticillium dahliae", "infected soil", "root wounds", "resistant weeds"],
        treatment=["Remove affected plants", "Solarise soil", "Grow resistant varieties"],
        prevention=["Use resistant cultivars", "Rotate with grains/grasses", "Avoid root damage"],
        affected_plants=["Tomato", "Potato", "Pepper", "Eggplant", "Strawberry"],
        chemical_treatment=[
            {
                "name": "Soil solarisation (heat)",
                "brand_names": ["Clear plastic sheeting"],
                "active_ingredients": ["Solar heat"],
                "dosage": "Cover moist soil with clear plastic 4-6 weeks in summer",
                "safety_precautions": ["Requires full sun season", "Water soil first"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Fungicide drench (limited use)",
                "brand_names": ["Thiophanate-methyl"],
                "active_ingredients": ["Thiophanate-methyl 45%"],
                "dosage": "Soil drench per label",
                "safety_precautions": ["Low efficacy once wilt shows", "Wear gloves"],
                "waiting_period": "Not for food crops once infected",
            },
        ],
        biological_treatment=[
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L at planting",
                "when_to_apply": "Transplant time",
                "notes": "Colonises roots and suppresses Verticillium.",
            },
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Root soak at transplant",
                "when_to_apply": "Planting time",
                "notes": "Biocontrol against soil-borne wilt fungi.",
            },
        ],
        organic_remedies=[
            {
                "name": "Soil solarisation",
                "recipe": "Water soil, cover with clear plastic 4-6 weeks",
                "application": "Summer, before planting",
                "frequency": "Once per season",
            },
            {
                "name": "Compost tea drench",
                "recipe": "Brewed compost tea (microbe-rich)",
                "application": "Water around roots weekly",
                "frequency": "Weekly",
            },
        ],
        prevention_tips=[
            {"category": "Resistant varieties", "title": "Plant resistant cultivars", "description": "Look for 'V' codes on tomato labels."},
            {"category": "Crop rotation", "title": "Rotate with grasses", "description": "Grains and corn do not host Verticillium."},
            {"category": "Soil health", "title": "Feed soil biology", "description": "Compost and Trichoderma keep the fungus in check."},
            {"category": "Field sanitation", "title": "Control weeds", "description": "Many weeds carry the fungus."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp extract"],
            "micronutrients": ["Silicon"],
            "npk": "Moderate nitrogen, balanced feed",
            "soil_improvement": ["Raise beds for drainage"],
        },
        severity_levels={
            "mild": "One branch wilting.",
            "moderate": "Wilt spreading branch to branch.",
            "severe": "Whole plant collapses.",
        },
        weather_conditions={
            "humidity": "Cool moist soil favours infection",
            "temperature": "18-24 C soil temperature",
            "rainfall": "Waterlogged soil worsens it",
        },
        emergency_actions=[
            "Uproot affected plants with surrounding soil and bag them.",
            "Solarise the bed before replanting.",
            "Replant only resistant varieties with Trichoderma drench.",
        ],
    ),
    _disease(
        name="Clubroot",
        category="Fungal",
        scientific_name="Plasmodiophora brassicae",
        severity="Severe",
        description=(
            "Swollen, deformed 'club' roots on brassicas that can no longer take up water and "
            "nutrients. Plants wilt in the heat, yellow and collapse. Spores stay in the soil "
            "for up to 20 years."
        ),
        symptoms=["swollen roots", "wilting in heat", "stunted plants", "yellowing leaves"],
        causes=["acidic soil", "poor drainage", "infested soil", "brassica monoculture"],
        treatment=["Remove affected plants", "Lime the soil to pH 7.2", "Rotate brassicas"],
        prevention=["Keep pH above 7", "Improve drainage", "Use resistant varieties"],
        affected_plants=["Cabbage", "Broccoli", "Cauliflower", "Kale", "Brussels Sprout", "Radish"],
        chemical_treatment=[
            {
                "name": "Soil liming (cultural)",
                "brand_names": ["Garden lime / Dolomite"],
                "active_ingredients": ["Calcium carbonate"],
                "dosage": "Raise soil pH to 7.2 before planting",
                "safety_precautions": ["Test pH first", "Do not over-lime"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Fluazinam drench",
                "brand_names": ["Frowncide"],
                "active_ingredients": ["Fluazinam 50%"],
                "dosage": "Transplant drench per label",
                "safety_precautions": ["Highly regulated", "Follow local laws"],
                "waiting_period": "Not for home gardens",
            },
        ],
        biological_treatment=[
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L at transplant",
                "when_to_apply": "Transplant time",
                "notes": "Biocontrol against clubroot zoospores.",
            },
            {
                "agent": "Beneficial compost bacteria",
                "type": "Organic amendment",
                "application": "Add mature compost to beds",
                "when_to_apply": "Before planting",
                "notes": "Healthy soil biology suppresses resting spores.",
            },
        ],
        organic_remedies=[
            {
                "name": "Lime application",
                "recipe": "Work 100-150 g lime per m2 (pH-dependent)",
                "application": "Mix into topsoil before planting",
                "frequency": "Yearly",
            },
            {
                "name": "Raised bed drainage",
                "recipe": "Build raised beds with coarse compost",
                "application": "Improve root-zone drainage",
                "frequency": "Once",
            },
        ],
        prevention_tips=[
            {"category": "Soil pH", "title": "Keep pH above 7", "description": "Clubroot spores fail above pH 7.2."},
            {"category": "Drainage", "title": "Improve drainage", "description": "Wet acid soil is clubroot heaven."},
            {"category": "Crop rotation", "title": "Rotate brassicas", "description": "4+ years between brassica crops."},
            {"category": "Field sanitation", "title": "Clean tools", "description": "Wash mud from boots and tools between plots."},
        ],
        fertilizer={
            "organic": ["Lime", "Mature compost"],
            "micronutrients": ["Calcium", "Boron"],
            "npk": "Balanced 10-10-10 after pH correction",
            "soil_improvement": ["Lime + drainage + compost"],
        },
        severity_levels={
            "mild": "Slight root swelling.",
            "moderate": "Clubbed roots, daytime wilting.",
            "severe": "Severe root distortion, plant collapse.",
        },
        weather_conditions={
            "humidity": "Wet, waterlogged soil is the trigger",
            "temperature": "18-25 C soil temperature",
            "rainfall": "Heavy rain on poor drainage",
        },
        emergency_actions=[
            "Dig out infected plants and surrounding soil - bag and remove.",
            "Lime the bed to pH 7.2 immediately.",
            "Do not compost infected roots.",
        ],
    ),
    _disease(
        name="Damping Off",
        category="Fungal",
        scientific_name="Rhizoctonia, Pythium, Fusarium spp.",
        severity="Severe",
        description=(
            "Seedlings suddenly rot at the soil line, topple and die in the first weeks after "
            "germination. Caused by soil-borne fungi thriving in cold, wet, overcrowded trays."
        ),
        symptoms=["seedling collapse", "rotted stem base", "no germination", "white fuzz on soil"],
        causes=["overwatering", "cold soil", "crowded trays", "unsterile media", "poor drainage"],
        treatment=["Remove collapsed seedlings", "Improve drainage", "Water less frequently"],
        prevention=["Use sterile seed mix", "Provide air circulation", "Avoid overcrowding"],
        affected_plants=["Tomato", "Pepper", "Lettuce", "Cabbage", "Basil", "All seedlings"],
        chemical_treatment=[
            {
                "name": "Fungicide drench (mefenoxam)",
                "brand_names": ["Subdue Maxx"],
                "active_ingredients": ["Mefenoxam 21%"],
                "dosage": "Drench trays per label at planting",
                "safety_precautions": ["Drench only", "Wear gloves"],
                "waiting_period": "See label",
            },
            {
                "name": "Hydrogen peroxide flush",
                "brand_names": ["3% food-grade H2O2"],
                "active_ingredients": ["Hydrogen peroxide 3%"],
                "dosage": "Mix 1 part H2O2 with 4 parts water; water seedlings",
                "safety_precautions": ["Ventilate", "Do not overuse"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Seed-coat or tray drench before sowing",
                "when_to_apply": "Sowing time",
                "notes": "Colonises the root zone before pathogens do.",
            },
            {
                "agent": "Bacillus amyloliquefaciens",
                "type": "Bio-fungicide",
                "application": "Soil drench after sowing",
                "when_to_apply": "Immediately after sowing",
                "notes": "Suppresses Pythium and Rhizoctonia.",
            },
        ],
        organic_remedies=[
            {
                "name": "Cinnamon dust",
                "recipe": "Ground cinnamon powder",
                "application": "Dust soil surface after sowing",
                "frequency": "At sowing and after watering",
            },
            {
                "name": "Chamomile tea",
                "recipe": "Steep chamomile tea, cool, strain",
                "application": "Water seedlings gently",
                "frequency": "Weekly",
            },
        ],
        prevention_tips=[
            {"category": "Sanitation", "title": "Use sterile seed mix", "description": "Fresh bagged mix avoids soil-borne fungi."},
            {"category": "Environment", "title": "Keep soil warm", "description": "Use a heat mat to keep soil above 20 C."},
            {"category": "Irrigation", "title": "Water from below", "description": "Bottom-watering keeps the surface drier."},
            {"category": "Airflow", "title": "Ventilate trays", "description": "A gentle fan dries the soil surface and stops fungi."},
        ],
        fertilizer={
            "organic": ["Dilute seaweed extract after true leaves"],
            "micronutrients": ["Seaweed"],
            "npk": "No fertiliser until true leaves appear",
            "soil_improvement": ["Add perlite for drainage"],
        },
        severity_levels={
            "mild": "A few seedlings fall over.",
            "moderate": "Patches of tray collapse.",
            "severe": "Whole tray rots before true leaves form.",
        },
        weather_conditions={
            "humidity": "Cool wet soil is the main trigger",
            "temperature": "Below 18 C slows germination and rots seed",
            "rainfall": "Not applicable indoors",
        },
        emergency_actions=[
            "Remove and bin collapsed seedlings immediately.",
            "Scrape off the top 1 cm of wet soil.",
            "Let trays dry and water from below only.",
        ],
    ),
    _disease(
        name="Sooty Mold",
        category="Fungal",
        scientific_name="Capnodium spp.",
        severity="Mild",
        description=(
            "A black, sooty fungal film that grows on sticky honeydew excreted by aphids, "
            "whiteflies and scale. It blocks sunlight, weakening leaves, but does not invade "
            "plant tissue - control the pest and the mould disappears."
        ),
        symptoms=["black sooty film", "sticky leaves", "ants on plants", "honeydew"],
        causes=["aphid honeydew", "whitefly honeydew", "scale honeydew", "lack of pest control"],
        treatment=["Wash off sooty mould", "Control the sap-sucking pest", "Prune dense growth"],
        prevention=["Monitor pests early", "Use sticky traps", "Check leaf undersides"],
        affected_plants=["Citrus", "Tomato", "Rose", "Cucumber", "Gardenia", "Houseplants"],
        chemical_treatment=[
            {
                "name": "Insecticidal soap (for vector pests)",
                "brand_names": ["Safer Insecticidal Soap"],
                "active_ingredients": ["Potassium salts of fatty acids"],
                "dosage": "20 ml per litre; spray undersides",
                "safety_precautions": ["Spray at dusk", "Repeat every 3-4 days"],
                "waiting_period": "0 days",
            },
            {
                "name": "Horticultural oil",
                "brand_names": ["Bonide All Seasons"],
                "active_ingredients": ["Mineral oil 98%"],
                "dosage": "10 ml per litre in cool weather",
                "safety_precautions": ["Do not spray in heat", "Cover all leaf surfaces"],
                "waiting_period": "0 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Ladybird beetles",
                "type": "Beneficial insect",
                "application": "Release near aphid colonies",
                "when_to_apply": "When pests appear",
                "notes": "Removes the source of the honeydew.",
            },
            {
                "agent": "Parasitic wasp (Aphidius)",
                "type": "Beneficial insect",
                "application": "Release at first aphid signs",
                "when_to_apply": "Early infestation",
                "notes": "Parasitises aphids, cutting honeydew.",
            },
        ],
        organic_remedies=[
            {
                "name": "Soapy water wash",
                "recipe": "1 tbsp dish soap + 1 L water",
                "application": "Wipe or spray sooty leaves",
                "frequency": "Weekly until clean",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray to control sap-suckers",
                "frequency": "Every 7 days",
            },
        ],
        prevention_tips=[
            {"category": "Pest control", "title": "Control honeydew pests", "description": "No pests, no honeydew, no sooty mould."},
            {"category": "Monitoring", "title": "Check leaf undersides", "description": "Catch aphids/whitefly before they spread."},
            {"category": "Ant control", "title": "Stop ant-farming", "description": "Ants protect aphids - prune ant trails or use barriers."},
            {"category": "Pruning", "title": "Open the canopy", "description": "Less crowding reduces pest buildup."},
        ],
        fertilizer={
            "organic": ["Balanced compost"],
            "micronutrients": ["Seaweed extract"],
            "npk": "Moderate balanced feed",
            "soil_improvement": ["Mulch to reduce stress"],
        },
        severity_levels={
            "mild": "Light black film on a few leaves.",
            "moderate": "Leaves coated, sticky to the touch.",
            "severe": "Heavy coating blocks light, leaves yellow.",
        },
        weather_conditions={
            "humidity": "Warm conditions favour sap-sucking pests",
            "temperature": "20-30 C",
            "rainfall": "Rain washes some mould and pests off",
        },
        emergency_actions=[
            "Wash leaves with soapy water immediately.",
            "Treat the sap-sucking pest within 3 days.",
            "Hang sticky traps to monitor resurgence.",
        ],
    ),
    _disease(
        name="Corn Smut",
        category="Fungal",
        scientific_name="Ustilago maydis",
        severity="Moderate",
        description=(
            "Large grey-white galls that swell on corn ears, tassels and stems, bursting to "
            "release black dusty spores. Infected ears are inedible in the field stage, though "
            "young galls are eaten as a delicacy in Mexico."
        ),
        symptoms=["grey galls", "swollen ears", "black spore powder", "distorted tassels"],
        causes=["wounds from cultivation", "hail damage", "excess nitrogen", "dry then wet weather"],
        treatment=["Remove galls before they burst", "Avoid wounding plants", "Balance nitrogen"],
        prevention=["Rotate corn", "Avoid mechanical damage", "Manage nitrogen"],
        affected_plants=["Corn", "Maize", "Sweetcorn"],
        chemical_treatment=[
            {
                "name": "No effective chemical cure",
                "brand_names": [],
                "active_ingredients": ["-"],
                "dosage": "None - rely on cultural control",
                "safety_precautions": ["Do not waste sprays on smut galls"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L weekly in wet seasons",
                "when_to_apply": "Before tasselling",
                "notes": "Protective biofilm on wounds.",
            },
            {
                "agent": "Compost + balanced soil biology",
                "type": "Organic amendment",
                "application": "Add compost pre-plant",
                "when_to_apply": "Before sowing",
                "notes": "Healthy soil reduces stress and infection.",
            },
        ],
        organic_remedies=[
            {
                "name": "Remove galls early",
                "recipe": "Snap off galls before they turn black",
                "application": "Bag and destroy",
                "frequency": "Weekly through season",
            },
            {
                "name": "Crop rotation",
                "recipe": "Rotate away from corn for 2 years",
                "application": "Breaks the spore cycle",
                "frequency": "Seasonal",
            },
        ],
        prevention_tips=[
            {"category": "Field sanitation", "title": "Remove galls before rupture", "description": "Black spores survive in soil for years."},
            {"category": "Nutrient management", "title": "Balance nitrogen", "description": "Excess N boosts smut severity."},
            {"category": "Crop rotation", "title": "Rotate corn", "description": "2-year break reduces soil spores."},
            {"category": "Husbandry", "title": "Avoid wounding plants", "description": "Smut enters through mechanical or hail damage."},
        ],
        fertilizer={
            "organic": ["Composted manure"],
            "micronutrients": ["Zinc"],
            "npk": "Balanced 10-10-10; avoid nitrogen excess",
            "soil_improvement": ["Maintain pH 6.0-6.8"],
        },
        severity_levels={
            "mild": "A few small galls on tassels.",
            "moderate": "Galls on ears and stems.",
            "severe": "Many ears destroyed, heavy spore load.",
        },
        weather_conditions={
            "humidity": "Warm, humid conditions",
            "temperature": "24-30 C",
            "rainfall": "Dry-then-wet spells increase infection",
        },
        emergency_actions=[
            "Snap off and bag every gall before it bursts.",
            "Balance nitrogen for next season.",
            "Rotate the plot away from corn.",
        ],
    ),
    _disease(
        name="Rice Blast",
        category="Fungal",
        scientific_name="Magnaporthe oryzae",
        severity="Severe",
        description=(
            "Diamond-shaped grey lesions with brown borders on rice leaves, and rot of the "
            "neck (panicle) below the grain head. A devastating disease of paddy that can "
            "destroy entire fields in wet, humid conditions."
        ),
        symptoms=["diamond grey lesions", "brown borders", "neck rot", "bleached panicles"],
        causes=["humid nights", "excess nitrogen", "standing water", "dense sowing"],
        treatment=["Drain fields", "Reduce nitrogen", "Apply tricyclazole fungicide"],
        prevention=["Grow resistant varieties", "Space plants", "Balance nitrogen"],
        affected_plants=["Rice", "Paddy"],
        chemical_treatment=[
            {
                "name": "Tricyclazole fungicide",
                "brand_names": ["Beam", "Blast"],
                "active_ingredients": ["Tricyclazole 75%"],
                "dosage": "0.6 g per litre at first lesions",
                "safety_precautions": ["Wear PPE", "Follow local rice-spray guidance"],
                "waiting_period": "30 days",
            },
            {
                "name": "Azoxystrobin fungicide",
                "brand_names": ["Amistar"],
                "active_ingredients": ["Azoxystrobin 25% SC"],
                "dosage": "1 ml per litre at booting stage",
                "safety_precautions": ["Alternate with other classes", "Wear gloves"],
                "waiting_period": "14 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L at tillering",
                "when_to_apply": "Before humidity peaks",
                "notes": "Suppresses Magnaporthe infection on leaves.",
            },
            {
                "agent": "Pseudomonas fluorescens",
                "type": "Bio-fungicide",
                "application": "Seed treatment + foliar spray",
                "when_to_apply": "Sowing and tillering",
                "notes": "Induces systemic resistance in rice.",
            },
        ],
        organic_remedies=[
            {
                "name": "Neem cake soil amendment",
                "recipe": "Work neem cake into paddy soil",
                "application": "Pre-planting",
                "frequency": "Seasonal",
            },
            {
                "name": "Potassium boost",
                "recipe": "Apply muriate of potash at 2.5 kg/acre",
                "application": "Top-dress at tillering",
                "frequency": "Once",
            },
        ],
        prevention_tips=[
            {"category": "Resistant varieties", "title": "Plant blast-resistant rice", "description": "Most improved hybrids carry resistance genes."},
            {"category": "Nutrient management", "title": "Split nitrogen doses", "description": "Avoid a single heavy dose that fuels blast."},
            {"category": "Water management", "title": "Drain and flood cycles", "description": "Intermittent drainage cuts leaf wetness."},
            {"category": "Spacing", "title": "Avoid dense sowing", "description": "Wider spacing improves airflow."},
        ],
        fertilizer={
            "organic": ["Neem cake", "Composted manure"],
            "micronutrients": ["Zinc", "Silicon"],
            "npk": "Split nitrogen; add potassium 0-0-60",
            "soil_improvement": ["Maintain drainage in paddy fields"],
        },
        severity_levels={
            "mild": "A few leaf lesions.",
            "moderate": "Spread of lesions, some panicle rot.",
            "severe": "Widespread panicle blast, heavy grain loss.",
        },
        weather_conditions={
            "humidity": "High humidity with dew on leaves",
            "temperature": "24-28 C",
            "rainfall": "Rainy, misty spells",
        },
        emergency_actions=[
            "Drain the field and withhold nitrogen.",
            "Spray tricyclazole immediately.",
            "Remove heavily infected patches and rogue them.",
        ],
    ),
    _disease(
        name="Banana Sigatoka",
        category="Fungal",
        scientific_name="Mycosphaerella musicola",
        severity="Severe",
        description=(
            "Oval, grey-to-brown lesions that merge into large dead areas on banana leaves. "
            "Heavy infection kills leaves, stunts fruit and lowers yield. Spread by rain splash "
            "and wind."
        ),
        symptoms=["grey oval lesions", "brown dead patches", "leaf necrosis", "stunted fruit"],
        causes=["rain splash", "wind-borne spores", "humid tropics", "crowded plantation"],
        treatment=["Remove infected leaves", "Apply protectant fungicides", "Improve drainage"],
        prevention=["Grow resistant varieties", "Space plants", "Prune old leaves"],
        affected_plants=["Banana", "Plantain"],
        chemical_treatment=[
            {
                "name": "Mancozeb protectant",
                "brand_names": ["Dithane M-45"],
                "active_ingredients": ["Mancozeb 75%"],
                "dosage": "2-3 g per litre every 7 days in wet season",
                "safety_precautions": ["Wear PPE", "Alternate chemistries"],
                "waiting_period": "7 days",
            },
            {
                "name": "Propiconazole fungicide",
                "brand_names": ["Tilt"],
                "active_ingredients": ["Propiconazole 25%"],
                "dosage": "0.5 ml per litre every 21 days",
                "safety_precautions": ["Rotate with protectants", "Wear gloves"],
                "waiting_period": "60 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-fungicide",
                "application": "Foliar spray 2 g/L weekly",
                "when_to_apply": "During wet season",
                "notes": "Protects new leaves from spores.",
            },
            {
                "agent": "Trichoderma asperellum",
                "type": "Beneficial microbe",
                "application": "Foliar + soil application",
                "when_to_apply": "Monthly",
                "notes": "Suppresses leaf-spot fungi.",
            },
        ],
        organic_remedies=[
            {
                "name": "Remove infected leaves",
                "recipe": "Cut off spotted leaves at the petiole",
                "application": "Bag and destroy",
                "frequency": "Every 2 weeks",
            },
            {
                "name": "Baking soda spray",
                "recipe": "1 tbsp baking soda + 1 L water + soap",
                "application": "Spray young leaves",
                "frequency": "Weekly",
            },
        ],
        prevention_tips=[
            {"category": "Field sanitation", "title": "Prune infected leaves", "description": "Removing leaf litter cuts the spore source."},
            {"category": "Resistant varieties", "title": "Grow resistant cultivars", "description": "Some hybrids show strong Sigatoka tolerance."},
            {"category": "Spacing", "title": "Space plants", "description": "Better airflow and less humidity."},
            {"category": "Drainage", "title": "Improve field drainage", "description": "Standing water boosts disease."},
        ],
        fertilizer={
            "organic": ["Composted manure", "Kelp meal"],
            "micronutrients": ["Potassium", "Silicon"],
            "npk": "High potassium 3-1-6 for banana",
            "soil_improvement": ["Mulch and maintain organic matter"],
        },
        severity_levels={
            "mild": "A few lesions on lower leaves.",
            "moderate": "Lesions merging on several leaves.",
            "severe": "Most leaves dead, fruit yield collapses.",
        },
        weather_conditions={
            "humidity": "Humid tropical conditions",
            "temperature": "24-30 C",
            "rainfall": "Rainy seasons drive spread",
        },
        emergency_actions=[
            "Strip and bag all spotted leaves.",
            "Spray a protectant fungicide immediately.",
            "Thin the plantation for airflow.",
        ],
    ),
]
