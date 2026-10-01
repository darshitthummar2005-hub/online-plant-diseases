export const seedDiseases = [
  {
    name: 'Powdery Mildew',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'White, powdery fungal coating on leaves, stems and buds that blocks photosynthesis and weakens the plant.',
    symptomKeywords: ['white', 'powder', 'spots', 'dust', 'stunted', 'yellow'],
    treatment:
      'Spray a mix of 1 tbsp baking soda, 1 tsp liquid soap and 1L water weekly. Use neem oil at dusk. Improve air circulation.',
    prevention: 'Avoid overhead watering, space plants well, choose resistant varieties.',
    affectedPlants: ['Roses', 'Cucurbits', 'Grapes', 'Cucumber', 'Zinnia'],
  },
  {
    name: 'Leaf Spot (Septoria)',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'Brown circular spots with darker rings that start on the oldest leaves and move upward, causing leaf drop.',
    symptomKeywords: ['brown', 'spots', 'rings', 'holes', 'yellow'],
    treatment:
      'Remove infected leaves, apply copper-based fungicide, mulch to prevent soil splash.',
    prevention: 'Water at the base, rotate crops, clean tools between plants.',
    affectedPlants: ['Tomato', 'Leafy Greens', 'Potato'],
  },
  {
    name: 'Rust',
    type: 'Fungal',
    severity: 'High',
    description:
      'Orange-to-rust coloured pustules, mainly on the underside of leaves, that burst open to release spores.',
    symptomKeywords: ['orange', 'pustules', 'rust', 'spots', 'brown', 'yellow'],
    treatment:
      'Remove and destroy infected foliage. Apply sulfur fungicide and avoid wet leaves.',
    prevention: 'Water early in the day, ensure good airflow, prune crowded growth.',
    affectedPlants: ['Roses', 'Beans', 'Asparagus', 'Wheat', 'Geranium'],
  },
  {
    name: 'Early Blight',
    type: 'Fungal',
    severity: 'High',
    description:
      'Dark, target-like lesions with concentric rings on older leaves that spread upward and defoliate the plant.',
    symptomKeywords: ['brown', 'spots', 'blight', 'wilt', 'dark', 'yellow'],
    treatment:
      'Remove infected plants immediately, use copper fungicide, stake tomatoes for airflow.',
    prevention: 'Rotate nightshade crops, avoid wetting leaves, mulch around stems.',
    affectedPlants: ['Tomato', 'Potato', 'Eggplant'],
  },
  {
    name: 'Late Blight',
    type: 'Fungal',
    severity: 'High',
    description:
      'Water-soaked, greasy patches that collapse the foliage within days, followed by white mould rings and rotten fruit.',
    symptomKeywords: ['brown', 'blight', 'wilt', 'dark', 'water soaked', 'spots'],
    treatment:
      'Remove infected plants immediately, use copper or systemic fungicide, never compost infected vines.',
    prevention: 'Avoid wetting leaves, use certified seed, rotate crops.',
    affectedPlants: ['Tomato', 'Potato'],
  },
  {
    name: 'Root Rot',
    type: 'Fungal',
    severity: 'High',
    description:
      'Mushy, brown-to-black roots caused by overwatering and waterlogged soil. Plants wilt despite wet soil.',
    symptomKeywords: ['wilt', 'mushy', 'rotting', 'smell', 'yellow'],
    treatment:
      'Repot in fresh sterile soil, trim rotted roots, reduce watering, apply fungicide drench.',
    prevention: 'Use well-draining pots, never let pots sit in water.',
    affectedPlants: ['Houseplants', 'Succulents', 'Tomato', 'Pepper'],
  },
  {
    name: 'Downy Mildew',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'Yellow angular patches on the upper leaf surface with a grey-purple downy growth underneath.',
    symptomKeywords: ['yellow', 'spots', 'powder', 'wilting', 'curled'],
    treatment:
      'Remove affected leaves, apply copper or phosphonate fungicide, thin the canopy.',
    prevention: 'Space plants, water in the morning, avoid wet foliage.',
    affectedPlants: ['Cucurbits', 'Onion', 'Lettuce', 'Grape', 'Basil'],
  },
  {
    name: 'Anthracnose',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'Sunken, dark, water-soaked lesions on leaves, stems and fruit that expand into black spots.',
    symptomKeywords: ['brown', 'spots', 'holes', 'dark', 'wilt'],
    treatment:
      'Prune infected parts, apply copper-based fungicide, use clean seed.',
    prevention: 'Water at the base, mulch to stop splash, rotate crops.',
    affectedPlants: ['Beans', 'Mango', 'Pepper', 'Cucurbits', 'Strawberry'],
  },
  {
    name: 'Fusarium Wilt',
    type: 'Fungal',
    severity: 'High',
    description:
      'Vascular wilt where leaves yellow and droop on one side of the plant, progressing to whole-plant collapse.',
    symptomKeywords: ['wilt', 'yellow', 'stunted', 'brown', 'wilting'],
    treatment: 'No cure - remove plants, solarise soil, grow resistant varieties.',
    prevention: 'Use resistant cultivars, rotate crops, avoid root damage.',
    affectedPlants: ['Tomato', 'Banana', 'Melon', 'Basil'],
  },
  {
    name: 'Gray Mold (Botrytis)',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'A fuzzy grey-brown mould that attacks flowers, buds, fruit and young stems, often starting at a wound or spent blossom.',
    symptomKeywords: ['brown', 'spots', 'wilt', 'mold', 'mushy'],
    treatment:
      'Remove infected parts immediately, improve airflow, apply copper or iprodione fungicide.',
    prevention: 'Water at the base, prune crowding, harvest promptly.',
    affectedPlants: ['Tomato', 'Strawberry', 'Grape', 'Rose', 'Lettuce', 'Onion', 'Cucumber'],
  },
  {
    name: 'Black Spot (Rose)',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'Circular black spots with ragged, feathery edges on rose leaves, surrounded by a yellow halo.',
    symptomKeywords: ['brown', 'spots', 'yellow', 'holes', 'blight'],
    treatment:
      'Remove spotted leaves, apply sulfur or myclobutanil fungicide, mulch around the bush.',
    prevention: 'Water at the base, prune for airflow, rake up fallen leaves.',
    affectedPlants: ['Rose'],
  },
  {
    name: 'Apple Scab',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'Olive-green to black velvety lesions on apple leaves and fruit that distort leaves and crack fruit skin.',
    symptomKeywords: ['brown', 'spots', 'holes', 'dark'],
    treatment:
      'Remove infected leaves, apply myclobutanil or captan fungicide, rake fallen leaves.',
    prevention: 'Rake autumn leaves, prune for airflow, grow scab-resistant varieties.',
    affectedPlants: ['Apple', 'Pear', 'Crabapple'],
  },
  {
    name: 'Brown Rot (Stone Fruit)',
    type: 'Fungal',
    severity: 'High',
    description:
      'Rapidly spreading brown rot that mummifies peaches, plums and cherries with dusty grey-brown spore tufts.',
    symptomKeywords: ['brown', 'spots', 'mushy', 'rot'],
    treatment:
      'Remove mummies and cankers, apply sulfur fungicide, prune for airflow.',
    prevention: 'Thin fruit, prune out cankers, clean up fallen fruit.',
    affectedPlants: ['Peach', 'Plum', 'Cherry', 'Apricot', 'Nectarine'],
  },
  {
    name: 'Cercospora Leaf Spot',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'Small tan-to-brown circular spots with darker borders on leaves, common on beets, peppers and beans.',
    symptomKeywords: ['brown', 'spots', 'yellow', 'holes'],
    treatment: 'Remove spotted leaves, apply copper fungicide, mulch to stop splash.',
    prevention: 'Water at the base, rotate crops, clean up debris.',
    affectedPlants: ['Beet', 'Pepper', 'Bean', 'Spinach', 'Carrot'],
  },
  {
    name: 'Verticillium Wilt',
    type: 'Fungal',
    severity: 'High',
    description:
      'A soil-borne wilt that yellows and wilts one branch at a time, progressing to whole-plant collapse.',
    symptomKeywords: ['wilt', 'yellow', 'stunted', 'wilting'],
    treatment: 'Remove affected plants, solarise soil, grow resistant varieties.',
    prevention: 'Use resistant cultivars, rotate with grains, avoid root damage.',
    affectedPlants: ['Tomato', 'Potato', 'Pepper', 'Eggplant', 'Strawberry'],
  },
  {
    name: 'Clubroot',
    type: 'Fungal',
    severity: 'High',
    description:
      'Swollen, deformed club roots on brassicas that can no longer take up water and nutrients.',
    symptomKeywords: ['wilt', 'yellow', 'stunted', 'wilting'],
    treatment: 'Remove affected plants, lime the soil to pH 7.2, rotate brassicas.',
    prevention: 'Keep pH above 7, improve drainage, use resistant varieties.',
    affectedPlants: ['Cabbage', 'Broccoli', 'Cauliflower', 'Kale', 'Brussels Sprout', 'Radish'],
  },
  {
    name: 'Damping Off',
    type: 'Fungal',
    severity: 'High',
    description:
      'Seedlings suddenly rot at the soil line, topple and die in the first weeks after germination.',
    symptomKeywords: ['wilt', 'mushy', 'stunted', 'rotting'],
    treatment:
      'Remove collapsed seedlings, improve drainage, water less frequently.',
    prevention: 'Use sterile seed mix, provide air circulation, avoid overcrowding.',
    affectedPlants: ['Tomato', 'Pepper', 'Lettuce', 'Cabbage', 'Basil', 'All Seedlings'],
  },
  {
    name: 'Sooty Mold',
    type: 'Fungal',
    severity: 'Low',
    description:
      'A black, sooty fungal film that grows on sticky honeydew excreted by aphids, whiteflies and scale.',
    symptomKeywords: ['sticky', 'black', 'spots', 'white'],
    treatment:
      'Wash off sooty mould with soapy water, control the sap-sucking pest, prune dense growth.',
    prevention: 'Monitor pests early, use sticky traps, check leaf undersides.',
    affectedPlants: ['Citrus', 'Tomato', 'Rose', 'Cucumber', 'Gardenia', 'Houseplants'],
  },
  {
    name: 'Corn Smut',
    type: 'Fungal',
    severity: 'Medium',
    description:
      'Large grey-white galls that swell on corn ears, tassels and stems, bursting to release black dusty spores.',
    symptomKeywords: ['black', 'spots', 'brown', 'stunted'],
    treatment: 'Remove galls before they burst, avoid wounding plants, balance nitrogen.',
    prevention: 'Rotate corn, avoid mechanical damage, manage nitrogen.',
    affectedPlants: ['Corn', 'Maize', 'Sweetcorn'],
  },
  {
    name: 'Rice Blast',
    type: 'Fungal',
    severity: 'High',
    description:
      'Diamond-shaped grey lesions with brown borders on rice leaves, and rot of the neck below the grain head.',
    symptomKeywords: ['brown', 'spots', 'blight', 'yellow'],
    treatment: 'Drain fields, reduce nitrogen, apply tricyclazole fungicide.',
    prevention: 'Grow resistant varieties, space plants, balance nitrogen.',
    affectedPlants: ['Rice', 'Paddy'],
  },
  {
    name: 'Banana Sigatoka',
    type: 'Fungal',
    severity: 'High',
    description:
      'Oval, grey-to-brown lesions that merge into large dead areas on banana leaves, stunting fruit.',
    symptomKeywords: ['brown', 'spots', 'yellow', 'blight'],
    treatment:
      'Remove infected leaves, apply protectant fungicides, improve drainage.',
    prevention: 'Grow resistant varieties, space plants, prune old leaves.',
    affectedPlants: ['Banana', 'Plantain'],
  },
  {
    name: 'Citrus Canker',
    type: 'Bacterial',
    severity: 'Medium',
    description:
      'Raised, corky brown lesions with a yellow halo on leaves, stems and fruit of citrus trees.',
    symptomKeywords: ['brown', 'spots', 'yellow', 'holes'],
    treatment: 'Prune infected twigs, apply copper sprays, control leaf miner.',
    prevention: 'Buy certified trees, use windbreaks, apply copper before storms.',
    affectedPlants: ['Citrus', 'Grapefruit', 'Oranges', 'Lemons'],
  },
  {
    name: 'Bacterial Leaf Spot',
    type: 'Bacterial',
    severity: 'Medium',
    description:
      'Small water-soaked spots that turn brown with a yellow halo on peppers, tomatoes and leafy greens.',
    symptomKeywords: ['brown', 'spots', 'yellow', 'holes', 'blight'],
    treatment:
      'Remove infected leaves, apply copper bactericide, water at the base.',
    prevention: 'Use clean seed, avoid overhead watering, disinfect tools.',
    affectedPlants: ['Tomato', 'Pepper', 'Beans', 'Cabbage', 'Lettuce', 'Melon'],
  },
  {
    name: 'Bacterial Wilt',
    type: 'Bacterial',
    severity: 'High',
    description:
      'Rapid, irreversible wilting of the whole plant even though the soil is moist; cut stems ooze sticky slime.',
    symptomKeywords: ['wilt', 'wilting', 'yellow', 'stunted', 'brown'],
    treatment:
      'Remove infected plants immediately, solarise soil, grow resistant grafted plants.',
    prevention: 'Use resistant rootstocks, rotate with grasses, sterilise tools.',
    affectedPlants: ['Tomato', 'Potato', 'Eggplant', 'Pepper', 'Banana', 'Ginger'],
  },
  {
    name: 'Fire Blight',
    type: 'Bacterial',
    severity: 'High',
    description:
      'Blossoms, shoots and leaves suddenly turn black and look scorched, bending into a shepherd\'s crook.',
    symptomKeywords: ['brown', 'blight', 'wilt', 'dark', 'wilting'],
    treatment:
      'Prune out infected limbs 30 cm below the canker, apply copper at bloom, sterilise shears.',
    prevention: 'Grow resistant varieties, prune in dry winter, disinfect tools.',
    affectedPlants: ['Apple', 'Pear', 'Quince', 'Crabapple', 'Hawthorn'],
  },
  {
    name: 'Crown Gall',
    type: 'Bacterial',
    severity: 'Medium',
    description:
      'Knobbly, corky tumours at the crown, roots or graft unions that girdle the stem and weaken the plant.',
    symptomKeywords: ['brown', 'stunted', 'wilt', 'spots'],
    treatment:
      'Cut off small galls, destroy badly galled plants, disinfect tools.',
    prevention: 'Buy certified plants, avoid wounding roots, use resistant rootstocks.',
    affectedPlants: ['Grape', 'Rose', 'Apple', 'Cherry', 'Tomato', 'Pepper'],
  },
  {
    name: 'Citrus Greening (HLB)',
    type: 'Bacterial',
    severity: 'High',
    description:
      'A devastating bacterial disease spread by the Asian citrus psyllid; leaves mottle yellow and fruit turns bitter.',
    symptomKeywords: ['yellow', 'mottled', 'stunted', 'wilt', 'blight'],
    treatment:
      'No cure - remove infected trees, control the psyllid vector, scout frequently.',
    prevention: 'Buy certified trees, monitor psyllid traps, remove infected trees early.',
    affectedPlants: ['Citrus', 'Orange', 'Lemon', 'Grapefruit', 'Mandarin', 'Lime'],
  },
  {
    name: 'Mosaic Virus',
    type: 'Viral',
    severity: 'High',
    description:
      'Mottled yellow-green mosaic patterns on leaves with stunted, distorted growth. There is no cure.',
    symptomKeywords: ['mosaic', 'mottled', 'stunted', 'yellow', 'curled'],
    treatment:
      'No cure. Remove and destroy infected plants. Disinfect tools. Control aphid vectors.',
    prevention: 'Use virus-free seeds, control aphids, wash hands between plants.',
    affectedPlants: ['Squash', 'Cucumber', 'Pepper', 'Tomato', 'Tobacco'],
  },
  {
    name: 'Tomato Yellow Leaf Curl Virus',
    type: 'Viral',
    severity: 'High',
    description:
      'Leaves roll upward and inward, turn yellow along the margins and the plant stops growing almost completely.',
    symptomKeywords: ['yellow', 'curled', 'stunted', 'wilting'],
    treatment:
      'Rogue infected plants, control whitefly hard, grow resistant varieties.',
    prevention: 'Use resistant hybrids, net or screen the crop, remove weeds.',
    affectedPlants: ['Tomato', 'Pepper', 'Bean', 'Chilli'],
  },
  {
    name: 'Potato Leafroll Virus',
    type: 'Viral',
    severity: 'Medium',
    description:
      'Lower leaves roll upward, stiffen and turn yellow, and the whole potato plant becomes dwarfed.',
    symptomKeywords: ['yellow', 'curled', 'stunted', 'wilt'],
    treatment: 'No cure - remove infected plants, control aphids, plant certified seed.',
    prevention: 'Use certified virus-free seed, control aphids early, remove volunteers.',
    affectedPlants: ['Potato', 'Tomato', 'Eggplant'],
  },
  {
    name: 'Papaya Ringspot Virus',
    type: 'Viral',
    severity: 'High',
    description:
      'Papaya leaves mottle and blister, the crown collapses into a bunchy top and fruit develops ringspots.',
    symptomKeywords: ['mosaic', 'mottled', 'stunted', 'yellow', 'spots'],
    treatment: 'No cure - remove infected trees, control aphids, plant tolerant varieties.',
    prevention: 'Grow tolerant varieties, net young trees, remove infected trees early.',
    affectedPlants: ['Papaya', 'Cucurbits', 'Squash', 'Melon'],
  },
  {
    name: 'Bean Common Mosaic Virus',
    type: 'Viral',
    severity: 'Medium',
    description:
      'Leaves of beans show a green-yellow mosaic, curl downward and distort, and pods set poorly.',
    symptomKeywords: ['mosaic', 'mottled', 'curled', 'stunted', 'yellow'],
    treatment: 'No cure - remove infected plants, control aphids, plant clean seed.',
    prevention: 'Use certified virus-free seed, control aphids, disinfect tools.',
    affectedPlants: ['Beans', 'Runner Bean', 'Lima Bean', 'Soybean'],
  },
  {
    name: 'Aphid Infestation',
    type: 'Pest',
    severity: 'Low',
    description:
      'Tiny soft-bodied insects that suck sap from tender shoots, excreting sticky honeydew that invites sooty mould.',
    symptomKeywords: ['sticky', 'curled', 'aphids', 'ants', 'yellow'],
    treatment:
      'Spray strong water jet, apply neem oil or insecticidal soap every 5 days.',
    prevention: 'Attract ladybugs, plant companion herbs, check leaf undersides.',
    affectedPlants: ['Vegetables', 'Roses', 'Ornamentals', 'Pepper'],
  },
  {
    name: 'Spider Mites',
    type: 'Pest',
    severity: 'Medium',
    description:
      'Tiny mites that pierce leaf cells and drink the sap, leaving yellow speckles and fine webbing.',
    symptomKeywords: ['webbing', 'speckles', 'yellow', 'dry', 'curled'],
    treatment:
      'Rinse leaves, raise humidity, apply miticide or neem oil to undersides.',
    prevention: 'Keep humidity above 50%, isolate new plants, mist regularly.',
    affectedPlants: ['Tomato', 'Cucumber', 'Houseplants', 'Strawberry'],
  },
  {
    name: 'Whitefly Infestation',
    type: 'Pest',
    severity: 'Medium',
    description:
      'Small white winged insects that cluster on leaf undersides, sucking sap and excreting sticky honeydew.',
    symptomKeywords: ['white', 'flies', 'yellow', 'sticky', 'sooty'],
    treatment:
      'Use yellow sticky traps, spray neem oil or insecticidal soap weekly.',
    prevention: 'Vacuum adults, use reflective mulch, avoid dense planting.',
    affectedPlants: ['Tomato', 'Cucumber', 'Poinsettia', 'Brassicas'],
  },
  {
    name: 'Thrips Infestation',
    type: 'Pest',
    severity: 'Medium',
    description:
      'Tiny slender insects that rasp leaf and flower cells, leaving silvery streaks and black specks of frass.',
    symptomKeywords: ['silver', 'streaks', 'spots', 'curled', 'stunted'],
    treatment: 'Use blue sticky traps, spray insecticidal soap, apply spinosad.',
    prevention: 'Use reflective mulch, control weeds, avoid killing predators.',
    affectedPlants: ['Tomato', 'Onion', 'Pepper', 'Strawberry', 'Gladiolus', 'Rose'],
  },
  {
    name: 'Mealybug Infestation',
    type: 'Pest',
    severity: 'Medium',
    description:
      'Soft insects covered in white waxy fluff that cluster at leaf joints, sucking sap and excreting honeydew.',
    symptomKeywords: ['white', 'sticky', 'yellow', 'sooty', 'curled'],
    treatment:
      'Wipe with alcohol swabs, spray insecticidal soap, use a systemic insecticide.',
    prevention: 'Quarantine new plants, control ants, check leaf joints.',
    affectedPlants: ['Houseplants', 'Citrus', 'Grape', 'Hibiscus', 'Orchid', 'Succulents'],
  },
  {
    name: 'Root-knot Nematode',
    type: 'Pest',
    severity: 'High',
    description:
      'Microscopic worms that invade roots and trigger knotted galls that block water and nutrient uptake.',
    symptomKeywords: ['wilt', 'wilting', 'yellow', 'stunted', 'brown'],
    treatment:
      'Remove galled roots, solarise soil, grow resistant varieties, add compost.',
    prevention: 'Rotate with grasses, use resistant rootstocks, add compost.',
    affectedPlants: ['Tomato', 'Cucumber', 'Carrot', 'Okra', 'Potato', 'Beans', 'Squash'],
  },
  {
    name: 'Cutworm Damage',
    type: 'Pest',
    severity: 'Medium',
    description:
      'Fat grey-brown caterpillars that hide in soil by day and chew through seedling stems at the base at night.',
    symptomKeywords: ['holes', 'brown', 'wilt', 'wilting'],
    treatment:
      'Search soil at dusk, fit collars around stems, apply Bacillus thuringiensis.',
    prevention: 'Clear weeds before planting, till soil, remove hiding debris.',
    affectedPlants: ['Tomato', 'Lettuce', 'Cabbage', 'Corn', 'Bean', 'All Seedlings'],
  },
  {
    name: 'Tomato Hornworm',
    type: 'Pest',
    severity: 'Medium',
    description:
      'Large green caterpillars with a horn-like tail that strip leaves and fruit from tomato plants almost overnight.',
    symptomKeywords: ['holes', 'brown', 'curled', 'wilt'],
    treatment: 'Hand pick caterpillars, spray Bt, till soil to destroy pupae.',
    prevention: 'Till soil in spring, plant dill and flowers, inspect weekly.',
    affectedPlants: ['Tomato', 'Potato', 'Eggplant', 'Pepper'],
  },
  {
    name: 'Scale Insects',
    type: 'Pest',
    severity: 'Medium',
    description:
      'Small shell-like bumps that cling to stems and leaf veins, sucking sap from under a waxy cover.',
    symptomKeywords: ['sticky', 'yellow', 'sooty', 'brown', 'spots'],
    treatment:
      'Scrub off scale, apply horticultural oil, use a systemic insecticide.',
    prevention: 'Quarantine new plants, control ants, prune infested branches.',
    affectedPlants: ['Citrus', 'Grape', 'Rose', 'Ficus', 'Houseplants', 'Orchid'],
  },
  {
    name: 'Fall Armyworm',
    type: 'Pest',
    severity: 'High',
    description:
      'A destructive caterpillar with an inverted Y on its head that feeds in masses, stripping leaves and boring into cobs.',
    symptomKeywords: ['holes', 'brown', 'blight', 'curled'],
    treatment: 'Spray Bt or spinosad at dusk, hand pick egg masses, trap moths.',
    prevention: 'Use pheromone traps, rotate crops, plant early.',
    affectedPlants: ['Corn', 'Maize', 'Rice', 'Sorghum', 'Tomato', 'Cotton'],
  },
  {
    name: 'Nitrogen Deficiency',
    type: 'Deficiency',
    severity: 'Low',
    description:
      'Uniform yellowing that starts on the oldest leaves and moves upward while the plant grows slowly.',
    symptomKeywords: ['yellow', 'old leaves', 'pale', 'stunted'],
    treatment:
      'Apply compost or balanced fertilizer high in nitrogen (e.g. blood meal, fish emulsion).',
    prevention: 'Feed with organic compost regularly, test soil annually.',
    affectedPlants: ['Heavy Feeders', 'Leafy Greens', 'Corn', 'Tomato'],
  },
  {
    name: 'Iron Deficiency (Chlorosis)',
    type: 'Deficiency',
    severity: 'Medium',
    description:
      'Yellow leaves with distinct green veins, appearing on the youngest leaves first, usually from alkaline soil.',
    symptomKeywords: ['yellow veins', 'young leaves', 'pale', 'yellow'],
    treatment:
      'Apply chelated iron to soil or foliage spray. Check and adjust soil pH (5.5-6.5).',
    prevention: 'Avoid overwatering, keep pH balanced, add compost.',
    affectedPlants: ['Citrus', 'Blueberry', 'Gardenia', 'Azalea'],
  },
  {
    name: 'Potassium Deficiency',
    type: 'Deficiency',
    severity: 'Medium',
    description:
      'Scorched, brown leaf edges and weak stems, starting on older leaves. Plants look burnt and yield drops.',
    symptomKeywords: ['brown edges', 'scorched', 'old leaves', 'yellow'],
    treatment:
      'Apply potassium-rich fertilizer like kelp meal or wood ash. Mulch to hold moisture.',
    prevention: 'Feed with balanced organic fertilizer each growing season.',
    affectedPlants: ['Tomato', 'Potato', 'Banana', 'Corn'],
  },
  {
    name: 'Phosphorus Deficiency',
    type: 'Deficiency',
    severity: 'Medium',
    description:
      'Leaves turn dull, dark green or purple, often with purple veins, and the plant stays small with poor flowering.',
    symptomKeywords: ['purple', 'dark', 'stunted', 'pale'],
    treatment: 'Apply bone meal or rock phosphate, warm the soil, correct pH.',
    prevention: 'Feed balanced compost, test soil annually, mulch to warm soil.',
    affectedPlants: ['Tomato', 'Corn', 'Strawberry', 'Lettuce', 'Rose', 'Leafy Greens'],
  },
  {
    name: 'Magnesium Deficiency',
    type: 'Deficiency',
    severity: 'Medium',
    description:
      'Yellowing between the veins of older leaves while the veins stay green, often with a purple tint.',
    symptomKeywords: ['yellow veins', 'old leaves', 'pale', 'yellow'],
    treatment: 'Spray Epsom salts, apply dolomite lime, feed a balanced fertilizer.',
    prevention: 'Feed balanced compost, test soil, avoid excess potassium.',
    affectedPlants: ['Tomato', 'Potato', 'Pepper', 'Rose', 'Cucumber', 'Citrus'],
  },
  {
    name: 'Calcium Deficiency (Blossom End Rot)',
    type: 'Deficiency',
    severity: 'Medium',
    description:
      'Dark, sunken, leathery patches on the blossom end of fruit, caused by calcium not reaching the growing fruit.',
    symptomKeywords: ['brown', 'spots', 'mushy', 'dark'],
    treatment:
      'Water consistently, apply calcium foliar spray, mulch the soil.',
    prevention: 'Water consistently, mulch to hold moisture, avoid nitrogen excess.',
    affectedPlants: ['Tomato', 'Pepper', 'Squash', 'Eggplant', 'Melon', 'Cabbage'],
  },
  {
    name: 'Zinc Deficiency',
    type: 'Deficiency',
    severity: 'Low',
    description:
      'New leaves grow small, narrow and bunched in a rosette, with yellowing between the veins.',
    symptomKeywords: ['yellow veins', 'young leaves', 'stunted', 'pale'],
    treatment: 'Apply zinc sulphate foliar spray, correct soil pH, feed balanced fertilizer.',
    prevention: 'Test soil, avoid over-liming, feed balanced fertiliser.',
    affectedPlants: ['Corn', 'Citrus', 'Grape', 'Onion', 'Bean', 'Apple'],
  },
  {
    name: 'Boron Deficiency',
    type: 'Deficiency',
    severity: 'Medium',
    description:
      'New growth dies back, stems crack and cork, and fruit develops hollow or discoloured tissue.',
    symptomKeywords: ['brown', 'spots', 'stunted', 'wilt'],
    treatment: 'Apply a small precise dose of borax, add compost, correct pH.',
    prevention: 'Test soil, mulch to hold moisture, avoid over-liming.',
    affectedPlants: ['Apple', 'Grape', 'Cauliflower', 'Tomato', 'Strawberry', 'Beet'],
  },
  {
    name: 'Sulfur Deficiency',
    type: 'Deficiency',
    severity: 'Low',
    description:
      'Uniform yellowing of new leaves first, with thin stems and slow growth. Common in sandy, low-organic soils.',
    symptomKeywords: ['yellow', 'young leaves', 'pale', 'stunted'],
    treatment: 'Apply gypsum or sulfur fertilizer, feed compost, foliar sulfur.',
    prevention: 'Feed compost, use gypsum, test soil.',
    affectedPlants: ['Brassicas', 'Onion', 'Garlic', 'Grape', 'Leafy Greens', 'Corn'],
  },
]

export const seedPlants = [
  {
    name: 'Tomato',
    family: 'Solanaceae',
    sunlight: 'Full sun (6-8h)',
    water: '1-2 in per week',
    care: 'Stake early, prune suckers, feed every 2 weeks with tomato fertilizer.',
    facts: 'There are over 10,000 tomato varieties. Botanically it is a fruit, legally it was ruled a vegetable in 1893!',
  },
  {
    name: 'Basil',
    family: 'Lamiaceae',
    sunlight: 'Full sun',
    water: 'Keep soil moist',
    care: 'Pinch flower buds, harvest from the top, plant in rich well-drained soil.',
    facts: 'Basil is a symbol of love in Italy and a symbol of mourning in Greece.',
  },
  {
    name: 'Peace Lily',
    family: 'Araceae',
    sunlight: 'Indirect light',
    water: 'Weekly, keep slightly moist',
    care: 'Wipe leaves monthly, fertilize every 6 weeks, keep away from cold drafts.',
    facts: 'Peace lilies are excellent air purifiers, removing benzene and formaldehyde.',
  },
  {
    name: 'Monstera',
    family: 'Araceae',
    sunlight: 'Bright indirect',
    water: 'Water when top 2 in is dry',
    care: 'Provide a moss pole, wipe leaves, fertilize monthly in growing season.',
    facts: 'The holes in monstera leaves (fenestrations) let wind pass through without tearing.',
  },
  {
    name: 'Rosemary',
    family: 'Lamiaceae',
    sunlight: 'Full sun',
    water: 'Let soil dry between waterings',
    care: 'Prune after flowering, grow in gritty soil, avoid wet feet.',
    facts: 'Rosemary has been used as a memory symbol since ancient Greece — it is also a great pest repellent.',
  },
  {
    name: 'Chili Pepper',
    family: 'Solanaceae',
    sunlight: 'Full sun (6-8h)',
    water: 'Moderate, consistent',
    care: 'Feed with high-phosphorus fertilizer, pinch first flowers for bushier plants.',
    facts: 'The capsaicin in chilies is measured in Scoville Heat Units (SHU).',
  },
  {
    name: 'Aloe Vera',
    family: 'Asphodelaceae',
    sunlight: 'Bright indirect to full sun',
    water: 'Water every 3 weeks, less in winter',
    care: 'Use sandy soil, shallow wide pot, allow soil to fully dry.',
    facts: 'Aloe vera gel has been used medicinally for over 6,000 years.',
  },
  {
    name: 'Snake Plant',
    family: 'Asparagaceae',
    sunlight: 'Low to bright indirect',
    water: 'Every 2-4 weeks',
    care: 'Tolerates neglect, use succulent soil, avoid overwatering at all costs.',
    facts: 'Snake plants convert CO2 to oxygen at night, making them ideal bedroom plants.',
  },
  {
    name: 'Marigold',
    family: 'Asteraceae',
    sunlight: 'Full sun',
    water: 'Weekly',
    care: 'Deadhead spent blooms, plant after last frost, pinch young plants.',
    facts: 'Marigolds are natural nematode repellents and are often planted with vegetables.',
  },
  {
    name: 'Orchid',
    family: 'Orchidaceae',
    sunlight: 'Bright indirect',
    water: 'Weekly ice-cube or soak method',
    care: 'Repot every 2 years, use orchid bark, provide humid air and airflow.',
    facts: 'Orchids are the largest family of flowering plants, with over 25,000 species.',
  },
]

/** Broad crop groups, mirroring the backend matcher. Keyed by lowercase group name. */
export const PLANT_GROUPS = {
  cucurbits: ['cucumber', 'squash', 'pumpkin', 'zucchini', 'melon', 'watermelon', 'gourd'],
  nightshades: ['tomato', 'potato', 'eggplant', 'pepper', 'chili', 'chilli', 'bell pepper'],
  'leafy greens': ['lettuce', 'spinach', 'cabbage', 'kale', 'broccoli', 'swiss chard', 'arugula'],
  brassicas: ['cabbage', 'broccoli', 'cauliflower', 'kale', 'brussels sprout', 'radish'],
  alliums: ['onion', 'garlic', 'leek', 'shallot', 'chive'],
  legumes: ['bean', 'pea', 'lentil', 'soybean', 'chickpea', 'cowpea'],
  houseplants: ['monstera', 'peace lily', 'snake plant', 'aloe vera', 'pothos', 'philodendron', 'orchid', 'spider plant'],
  herbs: ['basil', 'mint', 'rosemary', 'thyme', 'cilantro', 'parsley', 'sage', 'oregano'],
  'stone fruits': ['peach', 'plum', 'cherry', 'apricot', 'nectarine'],
  'pome fruits': ['apple', 'pear', 'quince'],
  citrus: ['orange', 'lemon', 'lime', 'grapefruit', 'mandarin', 'clementine'],
  berries: ['strawberry', 'blueberry', 'raspberry', 'blackberry', 'cranberry'],
  grains: ['wheat', 'corn', 'maize', 'rice', 'barley', 'oat'],
  ornamentals: ['rose', 'geranium', 'zinnia', 'petunia', 'marigold', 'gardenia', 'azalea', 'hydrangea'],
  'root vegetables': ['carrot', 'beet', 'radish', 'potato', 'turnip', 'onion'],
  'heavy feeders': ['tomato', 'corn', 'cabbage', 'potato', 'squash', 'pepper'],
}

/** Curated, searchable plant list for the detection plant selector. */
export const PLANT_OPTIONS = [
  {
    group: 'Vegetables',
    items: [
      'Tomato', 'Potato', 'Eggplant', 'Bell Pepper', 'Chili Pepper', 'Cucumber', 'Squash',
      'Pumpkin', 'Zucchini', 'Melon', 'Lettuce', 'Spinach', 'Cabbage', 'Broccoli',
      'Cauliflower', 'Kale', 'Radish', 'Carrot', 'Beet', 'Onion', 'Garlic', 'Beans',
      'Peas', 'Corn', 'Rice', 'Wheat', 'Okra',
    ],
  },
  {
    group: 'Fruits',
    items: [
      'Strawberry', 'Blueberry', 'Grape', 'Apple', 'Pear', 'Peach', 'Plum', 'Cherry',
      'Orange', 'Lemon', 'Banana', 'Papaya', 'Mango',
    ],
  },
  {
    group: 'Ornamentals',
    items: ['Rose', 'Marigold', 'Geranium', 'Zinnia', 'Gardenia', 'Azalea', 'Sunflower'],
  },
  {
    group: 'Herbs',
    items: ['Basil', 'Mint', 'Rosemary'],
  },
  {
    group: 'Houseplants',
    items: ['Monstera', 'Peace Lily', 'Snake Plant', 'Aloe Vera', 'Orchid', 'Pothos', 'Spider Plant'],
  },
]
