"""
Additional crop disease records (AI Plant Doctor knowledge base).

Every entry here is a documented, real-world disease. Active ingredients and
cultural practices are described generically and defer to the local product
label, because rates and permitted crops differ by country - always read the
label before applying anything.

This module covers crops the earlier seed files did not reach: cereals
(wheat, sorghum), sugarcane, coffee, cotton, tobacco, sunflower, cassava, tea,
hops, turf and several pulses.
"""

from app.seed_data_common import _disease


def _entry(
    *,
    name,
    category,
    scientific_name,
    severity,
    description,
    symptoms,
    causes,
    treatment,
    prevention,
    affected_plants,
    organic_remedies,
    prevention_tips,
    chemical=None,
    fertilizer=None,
    weather=None,
    emergency=None,
) -> dict:
    """Wrap :func:`_disease`, converting the shorthand used here to schema shapes.

    Callers pass plain strings for the structured blocks (remedies, tips,
    fertilizer, severity, weather). The API schemas require typed objects, so
    this normalises them into the exact shape `DiseaseOut` expects.
    """
    """Build a record, filling the optional detail blocks with safe defaults."""
    chemical = chemical or [
        {
            "name": "Registered fungicide or bactericide for this crop",
            "brand_names": [],
            "active_ingredients": [],
            "dosage": "Apply strictly at the label rate for this crop; rates vary by country",
            "safety_precautions": [
                "Wear full PPE",
                "Never mix products unless the label allows it",
                "Observe the pre-harvest interval",
            ],
            "waiting_period": "As stated on the product label",
        }
    ]

    # Shorthand -> schema shape.
    weather_text = weather or "Long leaf wetness from rain, dew or overhead irrigation favours infection."
    if isinstance(weather_text, dict):
        # Merge a detailed override over the shared defaults.
        weather_humidity = weather_text.get("humidity") or weather_text.get("favours") or ""
        weather_temp = weather_text.get("temperature") or weather_text.get("notes") or ""
        weather_rain = weather_text.get("rainfall") or "Rain splash spreads spores and bacteria between plants"
    else:
        weather_humidity, weather_temp, weather_rain = (
            weather_text,
            "See the disease description for the favourable range",
            "Rain splash spreads spores and bacteria between plants",
        )
    weather = {
        "humidity": weather_humidity,
        "temperature": weather_temp,
        "rainfall": weather_rain,
        "temperature": "See the disease description for the favourable range",
        "rainfall": "Rain splash spreads spores and bacteria between plants",
    }
    emergency = emergency or [
        "Remove and destroy (do not compost) badly infected plant material",
        "Improve air circulation around remaining plants",
        "Avoid overhead irrigation until symptoms settle",
        "Contact a local extension officer if the outbreak is spreading fast",
    ]
    fertilizer = {
        "organic": fertilizer or ["Well-rotted compost", "Seaweed extract as a foliar feed"],
        "micronutrients": ["Potassium hardens tissue and reduces infection"],
        "npk": "Balanced feed; avoid excess nitrogen, which softens tissue",
        "soil_improvement": ["Mulch to stop soil splash onto leaves"],
    }
    severity_levels = {
        "mild": "A few affected leaves or spots; remove and monitor closely",
        "moderate": "Spots on roughly a quarter of the canopy; treat promptly",
        "severe": "Most of the canopy affected or stem/collar damage; act immediately",
    }
    organic_remedies = [
        {"name": remedy, "application": "Follow any local guidance for rates and timing"}
        for remedy in organic_remedies
    ]
    prevention_tips = [
        {"category": "Prevention", "title": tip, "description": tip}
        for tip in prevention_tips
    ]
    return _disease(
        name=name,
        category=category,
        scientific_name=scientific_name,
        severity=severity,
        description=description,
        symptoms=symptoms,
        causes=causes,
        treatment=treatment,
        prevention=prevention,
        affected_plants=affected_plants,
        chemical_treatment=chemical,
        biological_treatment=[
            {
                "agent": "Beneficial soil microbes",
                "type": "Beneficial microbe",
                "application": "Apply to soil or as a seed treatment, following product directions",
                "when_to_apply": "At planting, and again whenever the soil is disturbed",
                "notes": "Compost tea, Trichoderma and Bacillus products suppress many soil-borne pathogens",
            },
        ],
        organic_remedies=organic_remedies,
        prevention_tips=prevention_tips,
        fertilizer=fertilizer,
        severity_levels={
            "Mild": "A few affected leaves; remove and monitor",
            "Moderate": "Spots on a quarter of the canopy; treat and keep watching",
            "Severe": "More than half the canopy affected or stem/collar damage; act immediately",
        },
        weather_conditions=weather,
        emergency_actions=emergency,
    )


EXPANDED_DISEASES: list[dict] = [
    # ---------------- Cereals: wheat ----------------
    _entry(
        name="Stripe Rust",
        category="Fungal",
        scientific_name="Puccinia striiformis",
        severity="Severe",
        description=(
            "Yellow-orange stripes of pustules running in parallel lines along the leaves, "
            "later turning black. Spores blow in on wind over long distances and can "
            "devastate a wheat field within weeks."
        ),
        symptoms=["yellow stripes of pustules", "pustules in straight lines", "leaves turn yellow then brown", "black pustules late in season"],
        causes=["Puccinia striiformis fungus", "wind-borne spores from distant fields", "cool moist weather", "high humidity and dew"],
        treatment=["Remove volunteer wheat hosts", "Apply a labelled fungicide at first sign of stripes", "Sow resistant varieties next season"],
        prevention=["Plant resistant cultivars", "Remove leftover wheat stubble", "Avoid late sowing that extends leaf wetness"],
        affected_plants=["Wheat", "Barley"],
        organic_remedies=["Remove and burn infected residue", "Apply sulphur or a seaweed foliar feed to support the crop"],
        prevention_tips=["Scout fields weekly from tillering onwards", "Watch for outbreaks reported in nearby districts"],
    ),
    _entry(
        name="Wheat Leaf Rust",
        category="Fungal",
        scientific_name="Puccinia triticina",
        severity="Moderate",
        description=(
            "Round orange-brown pustules scattered on the upper leaf surface. Losses come "
            "from early infection reducing grain fill, so timing of fungicide application matters."
        ),
        symptoms=["round orange pustules", "scattered pustules on upper leaf", "premature leaf senescence", "shrivelled grain"],
        causes=["Puccinia triticina fungus", "cool moist nights with dew", "stubble carry-over"],
        treatment=["Apply a labelled foliar fungicide early", "Keep the crop watered to avoid drought stress"],
        prevention=["Rotate with non-cereal crops", "Sow resistant varieties", "Remove volunteer cereals"],
        affected_plants=["Wheat"],
        organic_remedies=["Encourage airflow by correct plant spacing", "Remove early infections and destroy them"],
        prevention_tips=["Scout at flag-leaf stage", "Prioritise fields that are flowering now"],
    ),
    _entry(
        name="Loose Smut of Wheat",
        category="Fungal",
        scientific_name="Ustilago tritici",
        severity="Severe",
        description=(
            "A seed-borne disease. Infected heads emerge with black sooty spores replacing "
            "the entire ear, which is destroyed and cannot be recovered."
        ),
        symptoms=["black sooty mass replacing the ear", "heads emerge early and smelly", "no grain produced"],
        causes=["Ustilago tritici fungus carried in seed", "fungal spores surviving on seed surface"],
        treatment=["No field cure once heads are infected", "Treat seed before sowing with a systemic seed treatment"],
        prevention=["Use certified disease-free seed", "Treat every seed lot", "Do not save seed from infected crops"],
        affected_plants=["Wheat"],
        organic_remedies=["Sow only certified clean seed", "Rotate crops to reduce soil inoculum"],
        prevention_tips=["Treat seed at recommended label rate", "Buy certified seed each season"],
    ),
    _entry(
        name="Wheat Powdery Mildew",
        category="Fungal",
        scientific_name="Blumeria graminis",
        severity="Moderate",
        description=(
            "White fluffy growth in patches on leaves, later turning grey-brown. Thrives in "
            "dense canopies with moderate temperatures and alternating dry and humid days."
        ),
        symptoms=["white powdery patches on leaves", "grey-brown fungal growth later", "premature leaf death"],
        causes=["Blumeria graminis fungus", "dense canopy", "moderate temperatures with humid nights", "excess nitrogen"],
        treatment=["Apply a labelled fungicide early in the epidemic", "Avoid excessive nitrogen"],
        prevention=["Use resistant varieties", "Maintain plant spacing for airflow", "Rotate crops"],
        affected_plants=["Wheat", "Barley"],
        organic_remedies=["Milk spray (1 part milk to 9 parts water) can suppress early growth", "Improve airflow and reduce crowding"],
        prevention_tips=["Scout lower leaves first, where the disease starts", "Reduce nitrogen rates"],
    ),
    _entry(
        name="Fusarium Head Blight",
        category="Fungal",
        scientific_name="Fusarium graminearum",
        severity="Severe",
        description=(
            "Heads bleach prematurely and partially fill; a pinkish-white mould appears under "
            "the glumes. Fungal toxins can also cause vomitoxin contamination in grain, so "
            "affected grain may be unsafe for feed or food."
        ),
        symptoms=["heads bleach early", "pinkish white mould under glumes", "poor grain fill", "russeting on kernels"],
        causes=["Fusarium graminearum fungus", "warm humid flowering period", "corn residue from a previous crop"],
        treatment=["Apply a labelled fungicide at flowering if risk is high", "Harvest severely affected fields early and separately"],
        prevention=["Rotate away from maize and wheat", "Plough in corn residue", "Choose tolerant varieties"],
        affected_plants=["Wheat", "Barley", "Maize"],
        organic_remedies=["Reduce surface residue after harvest", "Delay sowing to shift flowering away from wet spells"],
        prevention_tips=["Do not irrigate at flowering", "Test grain if a vomitoxin-tolerant variety is unavailable"],
        weather={"favours": "Warm (20-30C) humid weather during flowering", "suppresses": "Dry weather at flowering", "notes": "Risk peaks when warm days coincide with wet nights during anthesis"},
    ),
    _entry(
        name="Septoria Nodorum Blotch",
        category="Fungal",
        scientific_name="Zymoseptoria tritici",
        severity="Moderate",
        description=(
            "Oval brown lesions with pale centres and tiny black dots, first on lower leaves. "
            "Severe infection before grain fill causes significant yield loss."
        ),
        symptoms=["oval brown lesions with pale centres", "tiny black dots inside lesions", "lower leaves die first"],
        causes=["Zymoseptoria tritici fungus", "cool wet weather", "wheat residue on the soil surface"],
        treatment=["Apply a labelled fungicide if infection reaches the upper leaves before grain fill"],
        prevention=["Rotate crops", "Bury residue after harvest", "Use tolerant varieties"],
        affected_plants=["Wheat"],
        organic_remedies=["Deep plough residue to speed decomposition", "Avoid dense sowing"],
        prevention_tips=["Scout from stem elongation onwards", "Protect the top two leaves, which drive yield"],
    ),
    _entry(
        name="Tan Spot of Wheat",
        category="Fungal",
        scientific_name="Pyrenophora tritici-repentis",
        severity="Moderate",
        description=(
            "Oval tan lesions with a yellow halo and a darker centre. A major disease of "
            "continuous wheat cropping systems."
        ),
        symptoms=["oval tan spots with yellow halo", "dark centre in older lesions", "leaf senescence"],
        causes=["Pyrenophora tritici-repentis fungus", "continuous wheat cropping", "crop residue survival"],
        treatment=["Apply a labelled foliar fungicide when lesions reach mid-canopy"],
        prevention=["Break the wheat-wheat cycle with a break crop", "Manage residue", "Use resistant cultivars"],
        affected_plants=["Wheat"],
        organic_remedies=["Rotate with a pulse or oilseed break crop", "Bury residue after harvest"],
        prevention_tips=["Watch for disease in second-rotation wheat", "Diversify cultivars"],
    ),
    _entry(
        name="Karnal Bunt",
        category="Fungal",
        scientific_name="Tilletia indica",
        severity="Severe",
        description=(
            "Kernels are partly replaced by dark powdery bunt balls that give off a foul smell. "
            "Grain from infected fields is unfit for human consumption."
        ),
        symptoms=["dark powdery balls replacing kernel", "foul fishy odour in threshing", "partially filled kernels"],
        causes=["Tilletia indica fungus", "soil-borne spores persisting for years", "contaminated seed and equipment"],
        treatment=["Treat seed with a labelled systemic fungicide", "Remove infected plants and destroy them"],
        prevention=["Use certified clean seed", "Clean machinery between fields", "Do not carry soil from infected areas"],
        affected_plants=["Wheat", "Barley"],
        organic_remedies=["Rogue infected plants before harvest", "Avoid moving contaminated soil"],
        prevention_tips=["Never save seed from infected crops", "Follow regional quarantine rules"],
    ),
    # ---------------- Sugarcane ----------------
    _entry(
        name="Sugarcane Red Rot",
        category="Fungal",
        scientific_name="Colletotrichum falcatum",
        severity="Severe",
        description=(
            "Red internal discolouration of stalks with white patches, drying of the top leaves "
            "and a sour alcohol smell from the affected crop. Causes heavy losses in ratoon cane."
        ),
        symptoms=["red discolouration inside stalk", "white patches in the red tissue", "drying top leaves", "sour smell from the field"],
        causes=["Colletotrichum falcatum fungus", "soil-borne inoculum surviving on stubble", "wounds from borers"],
        treatment=["Remove and burn infected clumps with their stubble", "Set healthy seed cane", "Apply a labelled fungicide to setts where recommended"],
        prevention=["Destroy crop residue after harvest", "Avoid ratooning heavily infected fields", "Use disease-free planting material"],
        affected_plants=["Sugarcane"],
        organic_remedies=["Uproot infected clumps completely and burn them", "Rotate with a non-host crop where land allows"],
        prevention_tips=["Control borers, which create infection entry points", "Inspect seed cane before planting"],
    ),
    _entry(
        name="Sugarcane Smut",
        category="Fungal",
        scientific_name="Sporisorium scitamineum",
        severity="Moderate",
        description=(
            "Slimy whip-like inflorescences replace the normal top of affected stalks. "
            "Reveals itself in the monsoon, when affected stalks stand out as thin whips."
        ),
        symptoms=["thin whip-like flowering structures", "no normal cane top", "reduced stalk weight"],
        causes=["Sporisorium scitamineum fungus", "airborne spores", "wounds from harvesting tools"],
        treatment=["Rogue out affected clumps", "Burn infected material", "Treat setts with a labelled fungicide"],
        prevention=["Hot-water treatment of seed cane", "Clean cutting tools between fields", "Plant resistant varieties"],
        affected_plants=["Sugarcane"],
        organic_remedies=["Remove whips before they release spores", "Avoid moving contaminated soil or cane"],
        prevention_tips=["Roguing is most effective if done before flowering", "Check seed cane every season"],
    ),
    _entry(
        name="Sugarcane Orange Rust",
        category="Fungal",
        scientific_name="Puccinia kuehnii",
        severity="Severe",
        description=(
            "Orange-brown pustules on the underside of leaves, causing premature leaf drying "
            "and heavy loss of photosynthetic area. Spores spread rapidly in humid weather."
        ),
        symptoms=["orange rust pustules under leaves", "yellow streaks above the pustules", "premature leaf drying"],
        causes=["Puccinia kuehnii fungus", "airborne urediniospores", "high humidity and moderate temperature"],
        treatment=["Apply a labelled fungicide promptly on first detection", "Remove volunteer cane hosts"],
        prevention=["Plant resistant varieties", "Remove volunteer cane", "Avoid excessive nitrogen"],
        affected_plants=["Sugarcane"],
        organic_remedies=["Strip and destroy heavily infected lower leaves", "Improve canopy aeration"],
        prevention_tips=["Scout after every rain", "Report outbreaks to local extension services"],
    ),
    _entry(
        name="Grassy Shoot Disease of Sugarcane",
        category="Bacterial",
        scientific_name="Candidatus Phytoplasma",
        severity="Severe",
        description=(
            "Profuse tillering gives a grassy appearance; stalks are thin, weak and pale, and "
            "the crop never forms a normal cane. Spreads mainly through infected planting material."
        ),
        symptoms=["excessive tillering", "thin pale stalks", "no proper cane formation", "stunted growth"],
        causes=["Phytoplasma", "infected seed cane", "leafhopper vectors", "cane knife transmission"],
        treatment=["Remove and burn infected clumps", "Replant with clean certified seed cane", "Control leafhoppers"],
        prevention=["Use certified disease-free setts", "Hot-water treat setts", "Control leafhopper vectors"],
        affected_plants=["Sugarcane"],
        organic_remedies=["Uproot and destroy affected clumps with roots", "Do not propagate from affected cane"],
        prevention_tips=["Reject nursery cane showing grassy symptoms", "Disinfect cutting tools"],
    ),
    _entry(
        name="Pokkah Boeng",
        category="Fungal",
        scientific_name="Fusarium moniliforme",
        severity="Severe",
        description=(
            "A malformed top with a twisted, wrinkled crown, caused by a complex of Fusarium "
            "species. Damages are worst after drought followed by heavy rain."
        ),
        symptoms=["twisted wrinkled crown", "deformed top leaves", "cracks and splits in the crown", "stunted tillering"],
        causes=["Fusarium species complex", "drought stress followed by heavy rain", "warm humid conditions"],
        treatment=["Remove severely deformed clumps", "Avoid planting in drought-prone pockets"],
        prevention=["Maintain even irrigation", "Improve soil drainage", "Use healthy planting material"],
        affected_plants=["Sugarcane"],
        organic_remedies=["Apply organic mulch to buffer soil moisture", "Improve drainage before planting"],
        prevention_tips=["Prevent drought stress; that is the main trigger", "Scout after drought then rain"],
    ),
    # ---------------- Coffee ----------------
    _entry(
        name="Coffee Leaf Rust",
        category="Fungal",
        scientific_name="Hemileia vastatrix",
        severity="Severe",
        description=(
            "Yellow-orange powdery spots on the underside of leaves that turn to brown with "
            "time. Causes defoliation, weakens the bush and cuts both yield and bean quality."
        ),
        symptoms=["yellow spots on upper leaf", "orange powdery growth underneath", "premature leaf fall", "reduced berry fill"],
        causes=["Hemileia vastatrix fungus", "wind and rain splash of spores", "high humidity", "dense shade canopy"],
        treatment=["Apply a labelled fungicide programme starting early in the wet season", "Apply nutrition with potassium to strengthen leaves"],
        prevention=["Shade and spacing that balance airflow with protection", "Remove fallen infected leaves", "Use resistant cultivars"],
        affected_plants=["Coffee"],
        organic_remedies=["Collect and destroy fallen leaves", "Improve canopy airflow by adjusting shade", "Mulch to keep soil moisture steady"],
        prevention_tips=["Scout the underside of leaves monthly", "Begin control before the wet season, not after"],
    ),
    _entry(
        name="Coffee Berry Disease",
        category="Fungal",
        scientific_name="Colletotrichum kahawae",
        severity="Severe",
        description=(
            "Dark lesions on green berries with pink spore masses; affected berries are "
            "defective, hollowed and worthless. Epidemics in wet weather can destroy the crop."
        ),
        symptoms=["dark lesions on green berries", "pink spore masses on lesions", "hollow defective berries", "berries stick to the branch"],
        causes=["Colletotrichum kahawae fungus", "warm wet conditions", "water splash", "overhead shade"],
        treatment=["Apply a labelled fungicide on a preventive schedule during the wet season", "Strip off and destroy infected berries"],
        prevention=["Remove mummified berries", "Improve shade and airflow", "Use resistant planting material"],
        affected_plants=["Coffee"],
        organic_remedies=["Pick and destroy infected berries", "Avoid overhead irrigation"],
        prevention_tips=["Start preventive spraying before berries are affected", "Keep the shade canopy well managed"],
    ),
    _entry(
        name="Coffee Brown Eye Spot",
        category="Fungal",
        scientific_name="Cercospora coffeicola",
        severity="Moderate",
        description=(
            "Circular brown spots with a light centre and a darker border, giving a "
            "'brown eye' look. Severe on seedlings in the nursery."
        ),
        symptoms=["brown spots with pale centres", "yellow halo around spots", "leaf drop in seedlings", "poor seedling vigour"],
        causes=["Cercospora coffeicola fungus", "warm humid conditions", "crowded nursery conditions"],
        treatment=["Apply a labelled fungicide in the nursery", "Remove affected leaves"],
        prevention=["Raise seedlings in a clean, airy nursery", "Avoid overhead watering of seedlings", "Space seedlings to allow airflow"],
        affected_plants=["Coffee"],
        organic_remedies=["Shade and ventilate the nursery properly", "Remove and destroy affected leaves"],
        prevention_tips=["Inspect nursery beds weekly", "Disinfect nursery soil before sowing"],
    ),
    _entry(
        name="Coffee Anthracnose",
        category="Fungal",
        scientific_name="Colletotrichum gloeosporioides",
        severity="Moderate",
        description=(
            "Brown twig dieback and leaf spots, often following cold, wet or damaged tissue. "
            "Common on young plants and after bad weather."
        ),
        symptoms=["brown twig dieback", "leaf spots and blight", "branch dieback from the tip", "young plant collapse"],
        causes=["Colletotrichum fungi", "cold wet conditions", "mechanical injury", "poor drainage"],
        treatment=["Prune out dead branches", "Apply a labelled fungicide", "Improve drainage and shelter"],
        prevention=["Protect young plants from cold stress", "Maintain plant nutrition", "Avoid wounding plants"],
        affected_plants=["Coffee"],
        organic_remedies=["Cut back affected branches well below the dead tissue", "Mulch to buffer soil moisture"],
        prevention_tips=["Monitor young plantations closely in cold spells", "Keep windbreaks intact"],
    ),
    # ---------------- Cotton ----------------
    _entry(
        name="Cotton Bacterial Blight",
        category="Bacterial",
        scientific_name="Xanthomonas citri pv. malvacearum",
        severity="Severe",
        description=(
            "Angular water-soaked leaf spots that turn dark brown or black, then vein blight "
            "where infection reaches the veins, causing leaf drop and defoliation."
        ),
        symptoms=["angular water-soaked spots", "veins turn black", "leaf drop and defoliation", "boll damage"],
        causes=["Xanthomonas bacteria", "stormy wet weather", "wounds and insect feeding", "contaminated seed"],
        treatment=["Remove heavily affected plants", "Apply copper-based bactericide where permitted", "Manage boll worms to reduce wounds"],
        prevention=["Use certified disease-free seed", "Rotate with non-host crops", "Avoid working fields when wet"],
        affected_plants=["Cotton"],
        organic_remedies=["Destroy crop residue after harvest", "Rotate for at least two seasons", "Avoid overhead irrigation"],
        prevention_tips=["Handle plants only when dry", "Control insects that create entry wounds"],
    ),
    _entry(
        name="Alternaria Leaf Spot of Cotton",
        category="Fungal",
        scientific_name="Alternaria alternata",
        severity="Moderate",
        description=(
            "Concentric brown spots on lower leaves, typically after stress. Causes defoliation "
            "which exposes bolls to sun and reduces fibre quality."
        ),
        symptoms=["brown spots with concentric rings", "lower leaf yellowing and drop", "defoliation"],
        causes=["Alternaria alternata fungus", "nutrient or moisture stress", "warm humid weather"],
        treatment=["Correct potassium and nitrogen balance", "Apply a labelled fungicide if severe", "Maintain even irrigation"],
        prevention=["Balanced nutrition", "Avoid plant stress", "Remove crop residue"],
        affected_plants=["Cotton"],
        organic_remedies=["Maintain steady soil moisture", "Add compost to improve nutrition"],
        prevention_tips=["Watch stressed patches first", "Do not over-fertilise with nitrogen"],
    ),
    _entry(
        name="Cotton Leaf Curl Virus",
        category="Viral",
        scientific_name="Begomovirus",
        severity="Severe",
        description=(
            "Upward curling, vein thickening and leaf cupping, with stunting. Transmitted by "
            "whiteflies; causes severe yield loss in susceptible varieties."
        ),
        symptoms=["upward leaf curling", "thickened veins", "leaf cupping and crinkling", "stunted plants"],
        causes=["Begomovirus", "whitefly vector", "nearby infected cotton or weeds"],
        treatment=["Remove and destroy infected plants", "Control whitefly populations", "Use tolerant varieties"],
        prevention=["Sow tolerant varieties", "Maintain rogueing of infected plants", "Control whitefly early"],
        affected_plants=["Cotton"],
        organic_remedies=["Uproot infected plants and destroy them", "Grow a border of trap crops", "Use neem-based whitefly control"],
        prevention_tips=["Scout for whiteflies from sowing", "Keep field borders clean of weeds"],
    ),
    # ---------------- Tobacco ----------------
    _entry(
        name="Tobacco Mosaic Virus",
        category="Viral",
        scientific_name="Tobacco mosaic virus",
        severity="Severe",
        description=(
            "Mottled light and dark green mosaic pattern, distorted leaves and stunted plants. "
            "Extremely stable and easily spread by handling, tools and hands."
        ),
        symptoms=["light and dark green mosaic mottling", "distorted narrow leaves", "stunted plants", "scorch-like patches on some varieties"],
        causes=["Tobacco mosaic virus", "mechanical transmission on hands and tools", "contaminated seed and tobacco products"],
        treatment=["Remove and destroy infected plants", "No curative treatment exists", "Disinfect all tools and hands"],
        prevention=["Use certified virus-free seed and seedlings", "Disinfect tools with a 10% bleach solution", "Wash hands after handling tobacco"],
        affected_plants=["Tobacco", "Tomato", "Pepper", "Cucumber"],
        organic_remedies=["Remove infected plants immediately", "Milk or detergent washes help sanitise hands"],
        prevention_tips=["Never handle plants after handling tobacco products", "Rogue infected plants early"],
    ),
    _entry(
        name="Tobacco Blue Mold",
        category="Fungal",
        scientific_name="Peronospora tabacina",
        severity="Severe",
        description=(
            "Yellow patches on the upper leaf with bluish-grey fuzzy growth underneath, which "
            "turns brown as the tissue dies. Devastates seedlings in cool, humid conditions."
        ),
        symptoms=["yellow upper leaf patches", "bluish grey fuzzy growth underneath", "brown dead tissue", "seedling collapse"],
        causes=["Peronospora tabacina fungus", "cool humid conditions", "dense canopies", "infected seed"],
        treatment=["Apply a labelled fungicide preventively", "Remove and destroy infected plants", "Ventilate seedbeds"],
        prevention=["Use certified seed", "Wider plant spacing", "Heat-treat seedbed soil before planting"],
        affected_plants=["Tobacco"],
        organic_remedies=["Improve seedbed ventilation", "Remove infected plants early"],
        prevention_tips=["Scout seedbeds daily in cool weather", "Avoid dense transplant beds"],
    ),
    _entry(
        name="Black Shank of Tobacco",
        category="Fungal",
        scientific_name="Phytophthora nicotianae",
        severity="Severe",
        description=(
            "Blackening at the base of the stem, sudden wilting and rapid death of plants, "
            "usually in patches along the row."
        ),
        symptoms=["black lesions at the stem base", "sudden wilting in patches", "rapid plant death", "brown discoloured stem pith"],
        causes=["Phytophthora nicotianae fungus-like pathogen", "waterlogged soil", "infested transplants"],
        treatment=["Remove and destroy affected plants with soil around roots", "Apply a soil-applied fungicide where permitted", "Improve drainage"],
        prevention=["Use clean transplants", "Avoid waterlogging", "Rotate with non-hosts", "Do not reuse infested beds"],
        affected_plants=["Tobacco"],
        organic_remedies=["Raise beds higher for drainage", "Solarise bed soil before planting"],
        prevention_tips=["Inspect transplant beds before lifting", "Watch for patches after heavy rain"],
    ),
    # ---------------- Sunflower ----------------
    _entry(
        name="Sunflower Downy Mildew",
        category="Fungal",
        scientific_name="Plasmopara halstedii",
        severity="Severe",
        description=(
            "Pale angular patches on upper leaves with white downy growth underneath, plus "
            "stunting and shortened internodes. The seed can also carry the pathogen."
        ),
        symptoms=["pale angular leaf patches", "white downy growth on the underside", "stunted plants", "short internodes"],
        causes=["Plasmopara halstedii pathogen", "soil-borne oospores", "infected seed", "cool wet conditions"],
        treatment=["Remove affected plants", "Apply a labelled fungicide", "Use clean seed"],
        prevention=["Resistant hybrids", "Long rotation away from sunflower", "Treat seed with a labelled fungicide"],
        affected_plants=["Sunflower"],
        organic_remedies=["Rogue infected plants early", "Rotate for at least three years"],
        prevention_tips=["Buy certified clean seed", "Report outbreaks, as seed-borne spread is possible"],
    ),
    _entry(
        name="Sunflower Sclerotinia Head Rot",
        category="Fungal",
        scientific_name="Sclerotinia sclerotiorum",
        severity="Severe",
        description=(
            "Flower heads develop a white cottony mould with black sclerotia, and the head "
            "becomes a light, hollow shell. Very destructive in wet years."
        ),
        symptoms=["white cottony mould on the head", "black sclerotia in and on the head", "light hollow heads", "stem rot and lodging"],
        causes=["Sclerotinia sclerotiorum fungus", "sclerotia surviving in soil", "cool wet conditions"],
        treatment=["Apply a labelled fungicide at early flowering", "Remove infected heads"],
        prevention=["Rotate with non-host crops", "Deep plough to bury sclerotia", "Use clean seed"],
        affected_plants=["Sunflower"],
        organic_remedies=["Bury crop residue after harvest", "Improve drainage"],
        prevention_tips=["Scout at bud stage in high-risk fields", "Avoid dense planting"],
    ),
    _entry(
        name="Sunflower Alternaria Blight",
        category="Fungal",
        scientific_name="Alternaria helianthi",
        severity="Moderate",
        description=(
            "Dark brown spots with concentric rings on leaves, starting on older leaves and "
            "spreading upward, causing premature defoliation."
        ),
        symptoms=["dark brown spots with concentric rings", "yellowing older leaves", "premature defoliation", "stem and head lesions"],
        causes=["Alternaria helianthi fungus", "warm humid weather", "crop residue", "plant stress"],
        treatment=["Apply a labelled fungicide if it reaches mid-canopy", "Maintain plant nutrition"],
        prevention=["Rotate crops", "Remove residue", "Use tolerant hybrids"],
        affected_plants=["Sunflower"],
        organic_remedies=["Maintain even irrigation to reduce stress", "Remove badly affected residue"],
        prevention_tips=["Scout from flowering", "Protect the upper canopy which drives yield"],
    ),
    # ---------------- Cassava, tea, hops, turf ----------------
    _entry(
        name="Cassava Bacterial Blight",
        category="Bacterial",
        scientific_name="Xanthomonas axonopodis pv. manihotis",
        severity="Severe",
        description=(
            "Angular water-soaked leaf spots, wilting of shoots, gum exudate at the stem base, "
            "and rapid dieback. One of the most destructive cassava diseases."
        ),
        symptoms=["angular leaf spots", "wilting shoots", "gum at the stem base", "dieback and root rot"],
        causes=["Xanthomonas bacteria", "contaminated planting material", "wounds and storm damage"],
        treatment=["Remove infected plants", "Use clean planting material", "Apply copper where permitted"],
        prevention=["Certified disease-free stem cuttings", "Avoid moving contaminated planting material", "Rotate and rest fields"],
        affected_plants=["Cassava"],
        organic_remedies=["Uproot and destroy infected plants", "Sanitise tools between fields"],
        prevention_tips=["Inspect cuttings before planting", "Report suspected cases to extension services"],
    ),
    _entry(
        name="Cassava Mosaic Disease",
        category="Viral",
        scientific_name="Cassava mosaic begomoviruses",
        severity="Severe",
        description=(
            "Distorted leaves with a characteristic mosaic pattern, reduced leaf lobes and "
            "severe yield loss. Spread by whiteflies and by infected cuttings."
        ),
        symptoms=["mosaic mottling on leaves", "distorted and reduced leaf lobes", "leaf drop", "severe yield loss"],
        causes=["Cassava mosaic begomoviruses", "whitefly vector", "infected cuttings"],
        treatment=["Remove infected plants", "Control whitefly", "Use tolerant varieties"],
        prevention=["Certified clean cuttings", "Whitefly control", "Rogue infected plants"],
        affected_plants=["Cassava"],
        organic_remedies=["Uproot infected plants", "Use neem-based whitefly control"],
        prevention_tips=["Never propagate from infected plants", "Scout for whitefly early"],
    ),
    _entry(
        name="Tea Blister Blight",
        category="Fungal",
        scientific_name="Exobasidium vexans",
        severity="Severe",
        description=(
            "Small translucent blisters on young leaves that enlarge into pinkish-white "
            "growths, then turn brown. Destroys the finest tea shoots in humid weather."
        ),
        symptoms=["translucent blisters on young leaves", "pinkish white velvety growth", "brown scabby leaves", "twisted deformed leaves"],
        causes=["Exobasidium vexans fungus", "high humidity and warm shade", "shade-tree management"],
        treatment=["Apply a labelled fungicide before the monsoon", "Pick and destroy infected leaves"],
        prevention=["Balance shade to reduce humidity", "Adopt tolerant clones", "Improve drainage and spacing"],
        affected_plants=["Tea"],
        organic_remedies=["Harvest and destroy infected shoots", "Adjust shade-tree canopies to admit light and air"],
        prevention_tips=["Monitor shade humidity before the monsoon", "Replace severely affected sections"],
    ),
    _entry(
        name="Tea Red Rust",
        category="Fungal",
        scientific_name="Aecidium camelliae",
        severity="Moderate",
        description=(
            "Yellow orange spots on the upper leaf surface with a mass of orange spores "
            "underneath, causing leaf drop and reduced quality in made tea."
        ),
        symptoms=["yellow orange spots on upper surface", "orange spore masses underneath", "leaf drop"],
        causes=["Aecidium camelliae fungus", "warm humid conditions", "dense shade"],
        treatment=["Apply a labelled fungicide", "Remove infected leaf litter"],
        prevention=["Reduce shade humidity", "Use tolerant clones", "Clear fallen leaves"],
        affected_plants=["Tea"],
        organic_remedies=["Collect and destroy fallen infected leaves", "Improve canopy airflow"],
        prevention_tips=["Scout after the monsoon starts", "Maintain plucking hygiene"],
    ),
    _entry(
        name="Hops Powdery Mildew",
        category="Fungal",
        scientific_name="Pseudoperonospora humuli",
        severity="Severe",
        description=(
            "Pale powdery colonies on leaves, bines and cones, which can ruin a whole crop and "
            "make cones unsaleable. Spreads extremely fast in warm humid weather."
        ),
        symptoms=["white powdery colonies", "bumpy deformed cones", "browning and dying shoots"],
        causes=["Pseudoperonospora humuli fungus", "warm humid weather", "dense canopies"],
        treatment=["Apply a labelled fungicide programme from early growth", "Remove and destroy infected bines"],
        prevention=["Plant resistant cultivars", "Thin canopies for airflow", "Remove infected material in autumn"],
        affected_plants=["Hops"],
        organic_remedies=["Thin the canopy aggressively", "Remove infected cones and bines"],
        prevention_tips=["Scout weekly through the season", "Act at the first white colonies"],
    ),
    _entry(
        name="Turf Dollar Spot",
        category="Fungal",
        scientific_name="Sclerotinia dollar spot",
        severity="Moderate",
        description=(
            "Circular straw-coloured patches a few centimetres across, often with a tan centre "
            "and darker margin, spreading in warm humid nights on cool-season turf."
        ),
        symptoms=["small circular straw patches", "tan centre with darker margin", "spreading in rings", "fine mycelium in the morning"],
        causes=["Sclerotinia species fungi", "warm humid nights and cool days", "excess nitrogen and evening irrigation"],
        treatment=["Apply a labelled fungicide", "Reduce evening irrigation", "Avoid excess nitrogen"],
        prevention=["Water early in the day", "Maintain balanced nutrition", "Improve drainage"],
        affected_plants=["Turf", "Bermuda grass", "Kentucky bluegrass"],
        organic_remedies=["Water deeply and early morning only", "Aerate compacted areas"],
        prevention_tips=["Check lawns after warm wet spells", "Keep mowing heights moderate"],
    ),
    _entry(
        name="Turf Brown Patch",
        category="Fungal",
        scientific_name="Rhizoctonia solani",
        severity="Moderate",
        description=(
            "Large irregular brown areas with a distinct dark green or purple rim, often in "
            "circles, appearing in warm humid weather on cool-season turf."
        ),
        symptoms=["irregular brown areas", "dark green or purple rim", "circular patches", "thinned and dying turf"],
        causes=["Rhizoctonia solani fungus", "warm nights and high humidity", "excess nitrogen", "thatch buildup"],
        treatment=["Apply a labelled fungicide", "Reduce nitrogen", "Manage thatch"],
        prevention=["Avoid late-day irrigation", "Balanced nutrition", "Aerate and dethatch"],
        affected_plants=["Turf", "Bermuda grass", "Kentucky bluegrass"],
        organic_remedies=["Improve drainage", "Avoid excess nitrogen", "Top-dress with compost"],
        prevention_tips=["Monitor during humid spells", "Raise mowing height slightly during stress"],
    ),
    _entry(
        name="Turf Fairy Ring",
        category="Fungal",
        scientific_name="Basidiomycete fungi",
        severity="Low",
        description=(
            "Circular rings of dark green or dead turf, sometimes with mushrooms, spreading "
            "outward a few centimetres each year as the fungal mat advances."
        ),
        symptoms=["circular rings of dark green turf", "dead patches within the ring", "mushrooms at the ring edge"],
        causes=["Basidiomycete soil fungi", "outward-spreading fungal mycelium", "thatch and organic debris"],
        treatment=["Fungicides rarely cure fairy ring", "Remove the fungal mat and replace with clean soil and turf"],
        prevention=["Avoid over-thatching", "Maintain balanced watering", "Improve drainage"],
        affected_plants=["Turf"],
        organic_remedies=["Dig out the mat and refill with clean soil", "Re-sod the affected area"],
        prevention_tips=["Expect rings to expand each year if untreated", "Improve airflow and drainage"],
    ),
]