"""Bacterial disease records (AI Plant Doctor knowledge base)."""

from app.seed_data_common import _disease

BACTERIAL_DISEASES: list[dict] = [
    _disease(
        name="Bacterial Leaf Spot",
        category="Bacterial",
        scientific_name="Xanthomonas campestris",
        severity="Moderate",
        description=(
            "Small, water-soaked spots that turn brown with a yellow halo on peppers, "
            "tomatoes and leafy greens. Leaves yellow and drop; fruit develops raised, "
            "scabby spots. Spreads by splashing water and on wet hands and tools."
        ),
        symptoms=["water soaked spots", "brown spots with yellow halo", "leaf drop", "scabby fruit"],
        causes=["Xanthomonas bacteria", "splashing water", "wet foliage", "contaminated seed", "working wet plants"],
        treatment=["Remove infected leaves", "Apply copper bactericide", "Water at the base"],
        prevention=["Use clean seed", "Avoid overhead watering", "Disinfect tools"],
        affected_plants=["Tomato", "Pepper", "Beans", "Cabbage", "Lettuce", "Melon"],
        chemical_treatment=[
            {
                "name": "Copper bactericide",
                "brand_names": ["Cueva", "Bonide Copper", "Kocide 3000"],
                "active_ingredients": ["Copper octanoate", "Copper hydroxide"],
                "dosage": "15 ml per litre every 7 days at first signs",
                "safety_precautions": ["Rotate with other products to avoid resistance", "Wear gloves", "Avoid waterways"],
                "waiting_period": "1 day before harvest",
            },
            {
                "name": "Fixed copper + mancozeb mix",
                "brand_names": ["Badge X2", "Dithane + copper tank mix"],
                "active_ingredients": ["Copper oxychloride + Mancozeb"],
                "dosage": "Follow label rates for vegetable crops",
                "safety_precautions": ["Phytotoxic in high heat - spray at dusk", "Wear full PPE"],
                "waiting_period": "7 days",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis",
                "type": "Bio-bactericide",
                "application": "Foliar spray 2 g/L weekly",
                "when_to_apply": "Before rain or when spots first appear",
                "notes": "Colonises the leaf surface and blocks bacterial entry.",
            },
            {
                "agent": "Bacillus amyloliquefaciens",
                "type": "Bio-bactericide",
                "application": "Foliar spray 2 g/L every 7 days",
                "when_to_apply": "Early season, preventively",
                "notes": "Produces compounds that suppress Xanthomonas growth.",
            },
        ],
        organic_remedies=[
            {
                "name": "Copper soap spray",
                "recipe": "Copper octanoate (organic-approved) 15 ml per litre",
                "application": "Spray all foliage including undersides",
                "frequency": "Every 7 days",
            },
            {
                "name": "Hydrogen peroxide spray",
                "recipe": "1 part 3% H2O2 + 4 parts water",
                "application": "Spray affected leaves on a cloudy day",
                "frequency": "Every 3-4 days",
            },
        ],
        prevention_tips=[
            {"category": "Seed hygiene", "title": "Use certified disease-free seed", "description": "Soak own seed in warm water to reduce seed-borne bacteria."},
            {"category": "Irrigation", "title": "Never overhead-water", "description": "Drip irrigation keeps foliage dry and stops splash."},
            {"category": "Field sanitation", "title": "Work plants when dry", "description": "Wet hands and tools spread the bacteria fast."},
            {"category": "Crop rotation", "title": "Rotate hosts", "description": "2-3 year break from peppers, tomatoes and beans."},
            {"category": "Resistant varieties", "title": "Grow resistant cultivars", "description": "Many tomato and pepper hybrids resist bacterial spot."},
        ],
        fertilizer={
            "organic": ["Compost", "Seaweed extract"],
            "micronutrients": ["Calcium (firm tissue)"],
            "npk": "Balanced feed; avoid excess nitrogen",
            "soil_improvement": ["Mulch to stop soil splash onto leaves"],
        },
        severity_levels={
            "mild": "A few water-soaked spots on lower leaves.",
            "moderate": "Spots spreading with yellow halos and some leaf drop.",
            "severe": "Heavy defoliation, scabby fruit and plant decline.",
        },
        weather_conditions={
            "humidity": "Wet foliage drives infection",
            "temperature": "24-30 C favours spread",
            "rainfall": "Rain and overhead irrigation spread bacteria",
        },
        emergency_actions=[
            "Remove and bag spotted leaves immediately - do not compost.",
            "Apply copper bactericide within 24 hours and repeat weekly.",
            "Switch to base watering and sterilise tools with alcohol.",
        ],
    ),
    _disease(
        name="Bacterial Wilt",
        category="Bacterial",
        scientific_name="Ralstonia solanacearum",
        severity="Severe",
        description=(
            "Rapid, irreversible wilting of the whole plant even though the soil is moist. "
            "Cut stems ooze sticky grey-white slime. The bacteria live in soil and water "
            "for years and attack many crop families."
        ),
        symptoms=["sudden wilting", "moist soil but wilted", "sticky stem ooze", "brown vascular tissue", "stunted plants"],
        causes=["Ralstonia bacteria", "infested soil", "contaminated water", "root wounds", "infected transplants"],
        treatment=["Remove infected plants immediately", "Solarise soil", "Grow resistant grafted plants"],
        prevention=["Use resistant rootstocks", "Rotate with grasses", "Sterilise tools"],
        affected_plants=["Tomato", "Potato", "Eggplant", "Pepper", "Banana", "Ginger"],
        chemical_treatment=[
            {
                "name": "No reliable chemical cure",
                "brand_names": [],
                "active_ingredients": ["-"],
                "dosage": "None - rely on sanitation and resistance",
                "safety_precautions": ["Do not waste sprays once wilt appears"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Soil solarisation (heat)",
                "brand_names": ["Clear plastic sheeting"],
                "active_ingredients": ["Solar heat"],
                "dosage": "Cover moist soil with clear plastic 4-6 weeks in summer",
                "safety_precautions": ["Requires a full-sun season", "Water soil first"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus amyloliquefaciens",
                "type": "Bio-bactericide",
                "application": "Root soak at transplant",
                "when_to_apply": "Transplant time",
                "notes": "Colonises roots and competes with Ralstonia.",
            },
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L at planting",
                "when_to_apply": "Planting time",
                "notes": "Suppresses soil-borne bacteria in the root zone.",
            },
        ],
        organic_remedies=[
            {
                "name": "Solarisation",
                "recipe": "Water soil, cover with clear plastic 4-6 weeks",
                "application": "Summer, before planting",
                "frequency": "Once per season",
            },
            {
                "name": "Grafted resistant plants",
                "recipe": "Use tomatoes grafted onto resistant rootstock",
                "application": "Plant instead of standard seedlings",
                "frequency": "Each season",
            },
        ],
        prevention_tips=[
            {"category": "Resistant varieties", "title": "Graft onto resistant rootstock", "description": "The most reliable protection in infested soil."},
            {"category": "Crop rotation", "title": "Rotate with grasses", "description": "Corn and grass crops do not host Ralstonia."},
            {"category": "Water management", "title": "Use clean water", "description": "Do not irrigate from ponds fed by infected fields."},
            {"category": "Field sanitation", "title": "Sterilise tools", "description": "Disinfect knives and stakes between plants."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp extract"],
            "micronutrients": ["Silicon (strengthens roots)"],
            "npk": "Moderate balanced feed; avoid nitrogen excess",
            "soil_improvement": ["Raise beds for drainage; solarise infested beds"],
        },
        severity_levels={
            "mild": "One or two plants wilt on hot afternoons.",
            "moderate": "Several plants wilting permanently.",
            "severe": "Whole crop collapses within days.",
        },
        weather_conditions={
            "humidity": "Warm, wet soil favours the bacteria",
            "temperature": "24-35 C soil temperature",
            "rainfall": "Heavy rain on infested soil spreads infection",
        },
        emergency_actions=[
            "Uproot wilted plants with surrounding soil and bag them.",
            "Solarise the bed and improve drainage.",
            "Replant only grafted or resistant varieties.",
        ],
    ),
    _disease(
        name="Fire Blight",
        category="Bacterial",
        scientific_name="Erwinia amylovora",
        severity="Severe",
        description=(
            "Blossoms, shoots and leaves suddenly turn black and look scorched, bending "
            "into a shepherd's crook. Bark forms sunken cankers that ooze. A serious "
            "disease of apple and pear trees spread by rain, bees and pruning."
        ),
        symptoms=["blackened shoots", "shepherd crook bends", "scorched blossoms", "oozing cankers", "bark blisters"],
        causes=["Erwinia amylovora", "rain during bloom", "bee pollination visits", "late pruning wounds", "hail damage"],
        treatment=["Prune out infected limbs 30 cm below canker", "Apply copper at bloom", "Remove fire blight strikes"],
        prevention=["Grow resistant varieties", "Prune in dry winter", "Sterilise shears between cuts"],
        affected_plants=["Apple", "Pear", "Quince", "Crabapple", "Hawthorn"],
        chemical_treatment=[
            {
                "name": "Copper spray at bloom",
                "brand_names": ["Kocide 3000", "Cueva"],
                "active_ingredients": ["Copper hydroxide", "Copper octanoate"],
                "dosage": "15 ml per litre from pink bloom through petal fall",
                "safety_precautions": ["Can russet fruit - use reduced rates", "Wear PPE", "Avoid drift"],
                "waiting_period": "1 day",
            },
            {
                "name": "Streptomycin (regulated)",
                "brand_names": ["Agri-Mycin 17"],
                "active_ingredients": ["Streptomycin sulphate"],
                "dosage": "Per label during bloom - where legally permitted",
                "safety_precautions": ["Regulated antibiotic - check local rules", "Not for home use in many regions"],
                "waiting_period": "Not for home orchards",
            },
        ],
        biological_treatment=[
            {
                "agent": "Bacillus subtilis (QST 713)",
                "type": "Bio-bactericide",
                "application": "Bloom spray 2 g/L every 3-4 days through bloom",
                "when_to_apply": "At 10% bloom",
                "notes": "Out-competes Erwinia on the blossom surface.",
            },
            {
                "agent": "Aureobasidium pullulans",
                "type": "Beneficial microbe",
                "application": "Bloom spray per label",
                "when_to_apply": "Before rain events at bloom",
                "notes": "Biocontrol yeasts that block blossom infection.",
            },
        ],
        organic_remedies=[
            {
                "name": "Prune-and-burn strikes",
                "recipe": "Cut 30 cm below visible cankers, burn the wood",
                "application": "Dry weather only",
                "frequency": "As needed in summer",
            },
            {
                "name": "Copper soap spray",
                "recipe": "Copper octanoate 15 ml per litre",
                "application": "Spray blossoms and new shoots",
                "frequency": "Weekly through bloom",
            },
        ],
        prevention_tips=[
            {"category": "Resistant varieties", "title": "Grow resistant cultivars", "description": "e.g., 'Empire', 'Enterprise', 'Freedom' apples."},
            {"category": "Pruning", "title": "Prune in dry winter", "description": "Summer pruning wounds are the main entry points."},
            {"category": "Field sanitation", "title": "Disinfect shears", "description": "Dip shears in 70% alcohol between every cut."},
            {"category": "Pest control", "title": "Control sucking insects", "description": "Aphids and psylla spread the bacteria."},
        ],
        fertilizer={
            "organic": ["Compost", "Bone meal"],
            "micronutrients": ["Calcium", "Boron (bloom health)"],
            "npk": "Low nitrogen; avoid lush succulent growth",
            "soil_improvement": ["Mulch and maintain pH 6.0-7.0"],
        },
        severity_levels={
            "mild": "A few scorched blossom spurs.",
            "moderate": "Several shoots blackened with shepherd's crook.",
            "severe": "Cankers girdle limbs, tree shows dieback.",
        },
        weather_conditions={
            "humidity": "Warm, wet bloom weather is the trigger",
            "temperature": "18-30 C during bloom",
            "rainfall": "Rain and hail during bloom spread bacteria",
        },
        emergency_actions=[
            "Cut out all fire blight strikes 30 cm below infection and burn them.",
            "Disinfect shears after every cut.",
            "Apply copper at bloom next spring before rain.",
        ],
    ),
    _disease(
        name="Crown Gall",
        category="Bacterial",
        scientific_name="Agrobacterium tumefaciens",
        severity="Moderate",
        description=(
            "Knobbly, corky tumours that form at the crown, roots or graft unions of many "
            "plants. The bacteria enter through wounds; galls girdle the stem and weaken "
            "the plant so it grows slowly and may die back."
        ),
        symptoms=["knobbly galls", "swollen crown", "wilted growth", "stunted plants", "galls at graft union"],
        causes=["Agrobacterium bacteria", "root wounds", "grafting cuts", "contaminated tools", "infested nursery stock"],
        treatment=["Cut off small galls", "Destroy badly galled plants", "Disinfect tools"],
        prevention=["Buy certified plants", "Avoid wounding roots", "Use gall-resistant rootstocks"],
        affected_plants=["Grape", "Rose", "Apple", "Cherry", "Tomato", "Pepper", "Chrysanthemum"],
        chemical_treatment=[
            {
                "name": "Gall excision + wound dressing",
                "brand_names": ["Tree wound dressing"],
                "active_ingredients": ["Asphalt-based dressing"],
                "dosage": "Cut out gall, dress the wound",
                "safety_precautions": ["Do not spray chemicals on galls - ineffective", "Disinfect knife after cutting"],
                "waiting_period": "Not applicable",
            },
            {
                "name": "Copper bactericide (preventive)",
                "brand_names": ["Kocide 3000"],
                "active_ingredients": ["Copper hydroxide"],
                "dosage": "Dip bare roots in copper solution before planting",
                "safety_precautions": ["Protective only - cannot cure existing galls", "Wear gloves"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Agrobacterium radiobacter K84",
                "type": "Biocontrol bacterium",
                "application": "Root dip before planting",
                "when_to_apply": "Planting time",
                "notes": "Competes with the gall-forming strain on root wounds.",
            },
            {
                "agent": "Trichoderma harzianum",
                "type": "Beneficial microbe",
                "application": "Soil drench 5 g/L at planting",
                "when_to_apply": "Transplant time",
                "notes": "Protects fresh root wounds from infection.",
            },
        ],
        organic_remedies=[
            {
                "name": "Excise small galls",
                "recipe": "Cut away galls with a clean knife",
                "application": "Dress the wound, disinfect knife",
                "frequency": "As galls appear",
            },
            {
                "name": "Root dip in compost tea",
                "recipe": "Brewed compost tea",
                "application": "Soak roots before planting",
                "frequency": "At planting",
            },
        ],
        prevention_tips=[
            {"category": "Plant hygiene", "title": "Buy certified nursery stock", "description": "Avoid plants with bumps at the crown or graft."},
            {"category": "Husbandry", "title": "Avoid wounding roots", "description": "Galls form at wounds - handle roots gently."},
            {"category": "Field sanitation", "title": "Disinfect tools", "description": "Bleach or alcohol tools after pruning galled plants."},
            {"category": "Resistant varieties", "title": "Use resistant rootstocks", "description": "Some grape and rose rootstocks resist crown gall."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp meal"],
            "micronutrients": ["Seaweed extract"],
            "npk": "Balanced feed to help the plant outgrow the gall",
            "soil_improvement": ["Ensure good drainage and loose soil"],
        },
        severity_levels={
            "mild": "Small galls, plant vigour barely affected.",
            "moderate": "Larger galls, slower growth and wilting in heat.",
            "severe": "Girdling galls, dieback and plant decline.",
        },
        weather_conditions={
            "humidity": "Wet soils favour infection at wounds",
            "temperature": "22-30 C is peak infection window",
            "rainfall": "Heavy rain on fresh wounds",
        },
        emergency_actions=[
            "Excise small galls and dress wounds immediately.",
            "Destroy badly galled plants - do not compost.",
            "Disinfect every tool and replace the topsoil around the plant.",
        ],
    ),
    _disease(
        name="Citrus Greening (HLB)",
        category="Bacterial",
        scientific_name="Candidatus Liberibacter asiaticus",
        severity="Severe",
        description=(
            "A devastating bacterial disease spread by the Asian citrus psyllid. Leaves "
            "mottle yellow, fruit stays green and lopsided and tastes bitter. There is no "
            "cure - the whole tree slowly declines and dies."
        ),
        symptoms=["yellow leaf mottling", "green lopsided fruit", "bitter fruit", "leaf drop", "twig dieback"],
        causes=["Liberibacter bacteria", "Asian citrus psyllid", "infected nursery stock", "grafting infected budwood"],
        treatment=["No cure - remove infected trees", "Control psyllid vector", "Scout frequently"],
        prevention=["Buy certified trees", "Monitor psyllid traps", "Remove infected trees early"],
        affected_plants=["Citrus", "Orange", "Lemon", "Grapefruit", "Mandarin", "Lime"],
        chemical_treatment=[
            {
                "name": "Psyllid vector control",
                "brand_names": ["Neem oil", "Safer Insecticidal Soap", "Malathion (regulated)"],
                "active_ingredients": ["Neem oil", "Potassium salts of fatty acids"],
                "dosage": "Spray flush growth per label",
                "safety_precautions": ["Target the psyllid, not the tree", "Avoid spraying open flowers"],
                "waiting_period": "Check label for food crops",
            },
            {
                "name": "No cure for the infection",
                "brand_names": [],
                "active_ingredients": ["-"],
                "dosage": "None - remove infected trees to protect the grove",
                "safety_precautions": ["Do not spray antibiotics at home"],
                "waiting_period": "Not applicable",
            },
        ],
        biological_treatment=[
            {
                "agent": "Tamarixia radiata (parasitoid wasp)",
                "type": "Beneficial insect",
                "application": "Release to parasitise psyllid nymphs",
                "when_to_apply": "Throughout the year",
                "notes": "Cuts psyllid numbers that spread the bacteria.",
            },
            {
                "agent": "Beauveria bassiana",
                "type": "Bio-insecticide",
                "application": "Foliar spray against psyllid adults",
                "when_to_apply": "Dusk for humidity",
                "notes": "Fungal disease of the psyllid vector.",
            },
        ],
        organic_remedies=[
            {
                "name": "Sticky yellow traps",
                "recipe": "Yellow cards coated with glue",
                "application": "Hang in tree canopy",
                "frequency": "Replace weekly",
            },
            {
                "name": "Neem oil spray",
                "recipe": "3 ml neem + 1 L water + soap",
                "application": "Spray new flush growth",
                "frequency": "Weekly during flush",
            },
        ],
        prevention_tips=[
            {"category": "Plant hygiene", "title": "Buy certified trees", "description": "Never move plants or budwood from infected areas."},
            {"category": "Vector control", "title": "Control Asian citrus psyllid", "description": "No psyllid, no spread - trap and spray flush growth."},
            {"category": "Field sanitation", "title": "Remove infected trees promptly", "description": "Leaving one tree can infect the whole grove."},
            {"category": "Monitoring", "title": "Scout leaves for mottling", "description": "Early detection slows spread to neighbours."},
        ],
        fertilizer={
            "organic": ["Compost", "Kelp extract"],
            "micronutrients": ["Zinc", "Manganese", "Boron (foliar mix)"],
            "npk": "Frequent small feeds; balanced citrus formula",
            "soil_improvement": ["Mulch and keep the root zone cool"],
        },
        severity_levels={
            "mild": "First mottled leaves on one branch.",
            "moderate": "Widespread mottling, small misshapen fruit.",
            "severe": "Heavy fruit drop, dieback and tree decline.",
        },
        weather_conditions={
            "humidity": "Warm, humid climate favours psyllids",
            "temperature": "25-35 C speeds psyllid breeding",
            "rainfall": "Wet seasons increase psyllid numbers",
        },
        emergency_actions=[
            "Report suspected HLB to the local plant protection authority.",
            "Remove and destroy infected trees immediately.",
            "Step up psyllid control on all nearby citrus.",
        ],
    ),
]
