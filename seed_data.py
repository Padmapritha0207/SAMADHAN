"""
seed_data.py - Realistic seed data for SAMADHAN: Jharkhand Societal Innovation Platform
Includes 24 districts, HEIs, industries, government departments, trends, projects, solutions, and achievements.
"""

JHARKHAND_LOCATIONS = {
    "Ranchi": {
        "lat": 23.3441, "lng": 85.3096,
        "blocks": {
            "Kanke": ["Sukhurhutu", "Boreya", "Arsande", "Choreya", "Kanke Central"],
            "Namkum": ["Rajaulatu", "Hardag", "Sidroll", "Khelgaon", "Tatisilwai"],
            "Ormanjhi": ["Irba", "Daru", "Chutupalu", "Hesal", "Ormanjhi Town"],
            "Angara": ["Hesal", "Getalsud", "Gonda", "Silli Road", "Jonha"],
            "Ratu": ["Ratu Garh", "Pipar Toli", "Kamre", "Simlia"],
            "Burmu": ["Burmu", "Chakla", "Bhatbigha"]
        }
    },
    "Dhanbad": {
        "lat": 23.7957, "lng": 86.4304,
        "blocks": {
            "Jharia": ["Fatehpur", "Bhaga", "Lodna", "Tisra", "Kenduadih"],
            "Dhanbad Sadar": ["Saraidhela", "Hirapur", "Bank More", "Dhansar"],
            "Govindpur": ["Govindpur Central", "Kharni", "Saharpura"],
            "Baghmara": ["Katras", "Barora", "Mahuada"],
            "Nirsa": ["Nirsa North", "Chirkunda", "Mugma"],
            "Baliapur": ["Pradhankhanta", "Baliapur", "Sindri"]
        }
    },
    "East Singhbhum": {
        "lat": 22.8046, "lng": 86.2029,
        "blocks": {
            "Jamshedpur": ["Bistupur", "Kadma", "Sonari", "Sakchi", "Govindpur"],
            "Ghatshila": ["Ghatshila Town", "Dhalbhumgarh", "Kashida", "Rajstate"],
            "Potka": ["Haldipokhar", "Kowali", "Potka Central"],
            "Musabani": ["Badia", "Surda", "Musabani Mines"],
            "Baharagora": ["Baharagora Central", "Barasol", "Khandamouda"]
        }
    },
    "Bokaro": {
        "lat": 23.6693, "lng": 86.1511,
        "blocks": {
            "Chas": ["Chas North", "Pindrajora", "Kura", "Kala Pathar"],
            "Bermo": ["Phusro", "Bhandaridah", "Kargali"],
            "Gomia": ["Gomia Central", "Saram", "Kathara"],
            "Chandankiyari": ["Chandankiyari", "Batbinor", "Bhojudih"]
        }
    },
    "Hazaribagh": {
        "lat": 23.9925, "lng": 85.3637,
        "blocks": {
            "Sadar": ["Matwari", "Korrah", "Okni", "Cannary"],
            "Katkamsandi": ["Katkamsandi Central", "Kandaber", "Shahpur"],
            "Barhi": ["Barhi Bazar", "Kewal", "Konra"],
            "Barkagaon": ["Barkagaon", "Badam", "Urimari"]
        }
    },
    "Deoghar": {
        "lat": 24.4826, "lng": 86.7000,
        "blocks": {
            "Deoghar Sadar": ["Castairs Town", "Bilasipara", "Jasidih", "Rohini"],
            "Madhupur": ["Madhupur Central", "Bherwa", "Pathrol"],
            "Sarath": ["Sarath", "Kukraha", "Palojori Road"],
            "Mohanpur": ["Choupal", "Mohanpur", "Trikut"]
        }
    },
    "Palamu": {
        "lat": 24.0416, "lng": 84.0722,
        "blocks": {
            "Medininagar": ["Sua", "Shahpur", "Hamidganj", "Redma"],
            "Chainpur": ["Chainpur", "Bantara", "Kankari"],
            "Patan": ["Patan Central", "Kishunpur", "Naudiha"],
            "Chhatarpur": ["Chhatarpur", "Kutmu", "Mahuawan"]
        }
    },
    "Dumka": {
        "lat": 24.2676, "lng": 87.2486,
        "blocks": {
            "Dumka Sadar": ["Rasikpur", "Dudhani", "Gharbhanga"],
            "Jama": ["Jama", "Silanda", "Asanjor"],
            "Jarmundi": ["Basukinath", "Taljhari", "Sahana"],
            "Shikaripara": ["Shikaripara", "Harinsingha", "Pattabari"]
        }
    },
    "West Singhbhum": {
        "lat": 22.5697, "lng": 85.8078,
        "blocks": {
            "Chaibasa": ["Tambu", "Gutu", "Tungri", "Mahulsai"],
            "Chakradharpur": ["Chakradharpur Central", "Toklo", "Chainpur"],
            "Noamundi": ["Noamundi Iron Belt", "Gua", "Kiriburu"],
            "Jagannathpur": ["Jagannathpur", "Maluka", "Gitiilpi"]
        }
    },
    "Ramgarh": {
        "lat": 23.6334, "lng": 85.5149,
        "blocks": {
            "Ramgarh Sadar": ["Bijulia", "Chitarpur", "Giddi"],
            "Patratu": ["Patratu Dam Colony", "Bhurkunda", "Balkudra"],
            "Mandu": ["Kuju", "Mandu", "Karma"],
            "Gola": ["Gola Bazar", "Chitarpur", "Barlanga"]
        }
    },
    "Giridih": {
        "lat": 24.1856, "lng": 86.3093,
        "blocks": {
            "Giridih Sadar": ["Bhandaridih", "Makatpur", "Pachamba"],
            "Dumri": ["Dumri Bazar", "Isri", "Parasnath Foot"],
            "Jamua": ["Jamua Central", "Chitardi", "Remamba"],
            "Bagodar": ["Bagodar", "Atka", "Suriya Road"]
        }
    },
    "Khunti": {
        "lat": 23.0747, "lng": 85.2787,
        "blocks": {
            "Khunti Sadar": ["Birhu", "Kalamati", "Belwadag", "Saiko"],
            "Murhu": ["Murhu Bazar", "Panchghagh", "Ganaloya"],
            "Torpa": ["Torpa Central", "Tapkara", "Sundari"],
            "Karra": ["Karra", "Govindpur", "Lodhma"]
        }
    },
    "Gumla": {
        "lat": 23.0441, "lng": 84.5422,
        "blocks": {
            "Gumla Sadar": ["Palkot Road", "Sisai Road", "Karam Toli"],
            "Ghaghra": ["Ghaghra Bazar", "Dewaki", "Belagara"],
            "Chainpur": ["Chainpur Border", "Kurumgarh", "Barway"]
        }
    },
    "Simdega": {
        "lat": 22.6139, "lng": 84.5089,
        "blocks": {
            "Simdega Sadar": ["Saldega", "Bhelwadih", "Kolebira Gate"],
            "Kolebira": ["Kolebira", "Lachragarh", "Agharma"],
            "Bano": ["Bano Central", "Kanaroan", "Gerda"]
        }
    },
    "Lohardaga": {
        "lat": 23.4359, "lng": 84.6800,
        "blocks": {
            "Lohardaga Sadar": ["Nadia", "Karamtoli", "Kura"],
            "Kuru": ["Kuru Bazar", "Salgi", "Chando"],
            "Kisko": ["Kisko Mines", "Bhandra", "Peshrar"]
        }
    },
    "Latehar": {
        "lat": 23.7431, "lng": 84.5028,
        "blocks": {
            "Latehar Sadar": ["Dumar", "Chas", "Karamtoli"],
            "Chandwa": ["Chandwa Central", "Tori", "Chama"],
            "Mahuadanr": ["Netarhat Valley", "Mahuadanr", "Orsa"]
        }
    },
    "Garhwa": {
        "lat": 24.1611, "lng": 83.8078,
        "blocks": {
            "Garhwa Sadar": ["Tandia", "Sahijana", "Dipwa"],
            "Meral": ["Meral", "Banka", "Sangbarha"],
            "Nagar Untari": ["Shri Banshidhar", "Untari", "Chitvishram"]
        }
    },
    "Chatra": {
        "lat": 24.2081, "lng": 84.8717,
        "blocks": {
            "Chatra Sadar": ["Gudri Bazar", "Marwari Mohalla", "Dantar"],
            "Hunterganj": ["Hunterganj", "Koldhaiya", "Jabda"],
            "Tandwa": ["Tandwa Coal Belt", "Kalyanpur", "Garri"]
        }
    },
    "Koderma": {
        "lat": 24.4674, "lng": 85.5939,
        "blocks": {
            "Koderma Sadar": ["Lakhichatan", "Bekabar", "Domchanch"],
            "Jhumri Telaiya": ["Telaiya Dam", "Station Road", "Gumo"],
            "Markacho": ["Markacho", "Murkamnay", "Nawadih"]
        }
    },
    "Jamtara": {
        "lat": 23.9619, "lng": 86.8028,
        "blocks": {
            "Jamtara Sadar": ["Mihijam Border", "Court Road", "Nawadih"],
            "Karmatar": ["Vidyasagar Gram", "Karmatar Central", "Sitarampur"],
            "Narayanpur": ["Narayanpur", "Kashitand", "Dighari"]
        }
    },
    "Godda": {
        "lat": 24.8267, "lng": 87.2144,
        "blocks": {
            "Godda Sadar": ["Rautara", "Kalyanpur", "Asanbani"],
            "Mahagama": ["Mahagama", "Rajmahal Mines Gate", "Kachhua"],
            "Boarijor": ["Boarijor", "Lalmatia", "Bara Simra"]
        }
    },
    "Sahibganj": {
        "lat": 25.2444, "lng": 87.6433,
        "blocks": {
            "Sahibganj Sadar": ["Ganga Ghat", "Sakrigali", "Chowk"],
            "Rajmahal": ["Fossil Park Road", "Rajmahal Ghat", "Mangalhat"],
            "Barharwa": ["Barharwa Junction", "Kotra", "Bindudham"]
        }
    },
    "Pakur": {
        "lat": 24.6342, "lng": 87.8483,
        "blocks": {
            "Pakur Sadar": ["Harindanga", "Rani Jyotirmoyee", "Dhulian Road"],
            "Hiranpur": ["Hiranpur Bazar", "Sundarpahari Road", "Mohanpur"],
            "Litipara": ["Litipara Hills", "Dharampur", "Bichkora"]
        }
    },
    "Saraikela-Kharsawan": {
        "lat": 22.6994, "lng": 85.9317,
        "blocks": {
            "Gamharia": ["Adityapur Industrial Area", "Gamharia Town", "Kandra"],
            "Saraikela Sadar": ["Saraikela Palace", "Chhau Kendra", "Govindpur"],
            "Chandil": ["Chandil Dam Colony", "Chowka", "Ichagarh"]
        }
    }
}

JHARKHAND_HEIS = [
    {
        "id": "hei-bit-mesra",
        "name": "Birla Institute of Technology (BIT), Mesra, Ranchi",
        "type": "Deemed Technical University",
        "domains": ["Water Management", "Urban Infrastructure", "Energy", "IoT & Sensor Systems", "Environment"],
        "key_labs": ["Remote Sensing & GIS Lab", "Water Quality & Environmental Engg Lab", "Smart City & IoT Lab", "Space & Robotics Center"],
        "lead_contact": "Prof. R. N. Mukherjee, Dean Research & Societal Impact"
    },
    {
        "id": "hei-iit-dhanbad",
        "name": "Indian Institute of Technology (IIT-ISM), Dhanbad",
        "type": "Institute of National Importance",
        "domains": ["Mining Sustainability", "Water Management", "Environment", "Rural Livelihoods", "Energy"],
        "key_labs": ["Centre for Water Resource Management", "Mine Air Dust & Gas Control Lab", "Clean Coal & Energy Tech", "Geological Hazard Monitoring"],
        "lead_contact": "Prof. S. K. Roy, Faculty In-charge Innovation Cell"
    },
    {
        "id": "hei-nit-jamshedpur",
        "name": "National Institute of Technology (NIT), Jamshedpur",
        "type": "Institute of National Importance",
        "domains": ["Urban Infrastructure", "Sanitation", "Accessibility", "Education", "Manufacturing"],
        "key_labs": ["Advanced Materials & Waste Recycling", "Smart Rural Microgrid Lab", "Affordable Assistive Devices Center", "Hydraulic Structures Lab"],
        "lead_contact": "Dr. Amitesh Kumar, Head of Technology Transfer"
    },
    {
        "id": "hei-bau-ranchi",
        "name": "Birsa Agricultural University (BAU), Ranchi",
        "type": "State Agricultural University",
        "domains": ["Agriculture", "Rural Livelihoods", "Environment", "Water Management"],
        "key_labs": ["Drought-Resilient Seed Germplasm Bank", "Tribal Lac & Sericulture Tech Lab", "Integrated Pest & Soil Bio-clinic", "Agro-forestry Station"],
        "lead_contact": "Dr. Poonam Tirkey, Director of Extension Education"
    },
    {
        "id": "hei-aiims-deoghar",
        "name": "All India Institute of Medical Sciences (AIIMS), Deoghar",
        "type": "Apex Healthcare & Research Institution",
        "domains": ["Healthcare", "Sanitation", "Public Service Delivery"],
        "key_labs": ["Rural Community Epidemiology Unit", "Telemedicine & Digital Health Hub", "Maternal & Child Nutrition Clinic"],
        "lead_contact": "Dr. Saurabh Verma, Department of Community Medicine"
    },
    {
        "id": "hei-ranchi-univ",
        "name": "Ranchi University, Ranchi",
        "type": "State University",
        "domains": ["Rural Livelihoods", "Environment", "Education", "Accessibility"],
        "key_labs": ["Tribal Culture & Ethnobotany Center", "Environmental Impact Assessment Cell", "Rural Community Action Lab"],
        "lead_contact": "Prof. Smita Kujur, Dean of Sciences"
    }
]

JHARKHAND_INDUSTRIES = [
    {
        "id": "ind-tata-steel",
        "name": "Tata Steel Foundation / Tata Steel CSR",
        "headquarters": "Jamshedpur",
        "csr_focus": ["Water Management", "Healthcare", "Education", "Tribal Livelihoods", "Sanitation"],
        "committed_grant_pool": 85000000,
        "active_partnerships": 18
    },
    {
        "id": "ind-bokaro-steel",
        "name": "Bokaro Steel Plant (SAIL CSR)",
        "headquarters": "Bokaro Steel City",
        "csr_focus": ["Urban Infrastructure", "Sanitation", "Water Management", "Education"],
        "committed_grant_pool": 42000000,
        "active_partnerships": 11
    },
    {
        "id": "ind-bccl-coal",
        "name": "Bharat Coking Coal Limited (CIL CSR)",
        "headquarters": "Dhanbad",
        "csr_focus": ["Environment", "Water Management", "Healthcare", "Community Safety"],
        "committed_grant_pool": 60000000,
        "active_partnerships": 14
    },
    {
        "id": "ind-jhar-innov-lab",
        "name": "Jharkhand Innovation Lab (Dept of IT & e-Gov)",
        "headquarters": "Ranchi",
        "csr_focus": ["Public Service Delivery", "Education", "Healthcare", "Accessibility", "Agriculture"],
        "committed_grant_pool": 35000000,
        "active_partnerships": 24
    },
    {
        "id": "ind-social-alpha",
        "name": "Social Alpha Societal Tech Fund",
        "headquarters": "Bengaluru / Ranchi Chapter",
        "csr_focus": ["Healthcare", "Water Management", "Agriculture", "Rural Livelihoods"],
        "committed_grant_pool": 50000000,
        "active_partnerships": 15
    }
]

GOVT_DEPARTMENTS = [
    {"code": "WTR", "name": "Department of Drinking Water & Sanitation", "nodal_officer": "Er. Alok Sharma, Chief Engineer"},
    {"code": "HLT", "name": "Department of Health, Medical Education & Family Welfare", "nodal_officer": "Dr. S. K. Pandey, Addl Director"},
    {"code": "AGR", "name": "Department of Agriculture, Animal Husbandry & Cooperative", "nodal_officer": "Shri B. N. Ram, Director Agriculture"},
    {"code": "EDU", "name": "Department of School Education & Literacy", "nodal_officer": "Smt. Vandana Dadel, Secretary"},
    {"code": "RUR", "name": "Department of Rural Development", "nodal_officer": "Shri Manoj Kumar, State Program Officer"},
    {"code": "URB", "name": "Urban Development & Housing Department", "nodal_officer": "Shri Ravi Shankar, Joint Secretary"},
    {"code": "ENV", "name": "Department of Forest, Environment & Climate Change", "nodal_officer": "Dr. Pradeep Kumar, PCCF"},
    {"code": "ACC", "name": "Department of Women, Child Dev & Social Security", "nodal_officer": "Smt. Kiran Singh, State Commissioner"}
]

# CURRENT TRENDS IN JHARKHAND
JHARKHAND_TRENDS = [
    {
        "id": "trend-1",
        "title": "Groundwater Arsenic & Fluoride Removal",
        "domain": "Water Management",
        "badge": "High Priority",
        "icon": "💧",
        "summary": "Rapid deployment of catalytic iron-oxidation and activated alumina filtration skids in Sahibganj, Ranchi, and Palamu deep aquifer zones.",
        "key_impact": "Lowering waterborne dental fluorosis & skin keratosis across 240+ rural hamlets."
    },
    {
        "id": "trend-2",
        "title": "Smart AgroTech & Early Pest Warning",
        "domain": "Agriculture",
        "badge": "Rapid Adoption",
        "icon": "🌾",
        "summary": "Smartphone edge-AI crop leaf scanners combined with Trichoderma bio-fungicides protecting vegetable harvest yields across Ormanjhi and Kanke.",
        "key_impact": "Saving 350+ smallholder tomato and paddy farmers up to 45% crop loss."
    },
    {
        "id": "trend-3",
        "title": "Clean Mining & Air Dust Abatement",
        "domain": "Environment",
        "badge": "Technological R&D",
        "icon": "🏭",
        "summary": "Nitrogen-foam mine fire seam inertization coupled with low-cost solar IoT particulate monitors (PM2.5 & CO) in Jharia and Bokaro coal belts.",
        "key_impact": "Mitigating noxious fumes around 12 schools and peri-urban settlements."
    },
    {
        "id": "trend-4",
        "title": "Solar Cold-Chain for Tribal Healthcare",
        "domain": "Healthcare",
        "badge": "Life Critical",
        "icon": "🏥",
        "summary": "Phase Change Material (PCM) hybrid solar-thermal vaccine carriers securing 72-hour thermal integrity during grid outages in remote forested PHCs.",
        "key_impact": "Protecting childhood immunization drives for over 6,200 infants in West Singhbhum."
    },
    {
        "id": "trend-5",
        "title": "Forest Produce (Lac & Silk) Mechanization",
        "domain": "Rural Livelihoods",
        "badge": "Economic Empowerment",
        "icon": "🌿",
        "summary": "Decentralized solar lac scrapers and tussar silk reeling machines developed by BAU & RU providing high value addition for tribal SHGs.",
        "key_impact": "Increasing monthly incomes of indigenous women artisans by 3.2x in Khunti."
    }
]

# EXISTING PROJECTS IN PROGRESS
JHARKHAND_EXISTING_PROJECTS = [
    {
        "id": "PROJ-WTR-2026",
        "title": "JharJal Community Arsenic Filtration Skid",
        "district": "Sahibganj (Rajmahal)",
        "lead_institution": "BIT Mesra Environmental Engineering Lab",
        "funding_partner": "Tata Steel Foundation & Social Alpha",
        "progress_percent": 85,
        "status": "Testing & Field Pilot",
        "grant": "₹25.0 Lakhs",
        "desc": "Modular solar-powered water filtration skid purifying 35,000 L/day for 800+ Ganga basin households."
    },
    {
        "id": "PROJ-HLT-2026",
        "title": "ColdShield Solar Vaccine Carrier Pack",
        "district": "West Singhbhum (Chaibasa)",
        "lead_institution": "AIIMS Deoghar Community Medicine & BIT Mesra",
        "funding_partner": "Social Alpha Societal Tech Fund",
        "progress_percent": 70,
        "status": "Prototype In Progress",
        "grant": "₹32.0 Lakhs",
        "desc": "Portable PCM backpack maintaining 2°C to 8°C vaccine cold-chain for 72 hours across 14 forest sub-centers."
    },
    {
        "id": "PROJ-ENV-2026",
        "title": "Subsurface Mine Fire Smoke & Dust Barrier",
        "district": "Dhanbad (Jharia)",
        "lead_institution": "IIT (ISM) Dhanbad Clean Coal Center",
        "funding_partner": "Bharat Coking Coal Limited (CIL CSR)",
        "progress_percent": 60,
        "status": "Lab Bench Verification",
        "grant": "₹45.0 Lakhs",
        "desc": "Continuous nitrogen foam barrier and solar IoT air telemetry preventing gas seepage near residential schools."
    },
    {
        "id": "PROJ-AGR-2026",
        "title": "Edge-AI Crop Disease Diagnostic & Bio-Dip",
        "district": "Ranchi (Ormanjhi)",
        "lead_institution": "Birsa Agricultural University (BAU)",
        "funding_partner": "NABARD Jharkhand Innovation Grant",
        "progress_percent": 90,
        "status": "Field Pilot Deployed",
        "grant": "₹18.0 Lakhs",
        "desc": "Vernacular mobile pest diagnostic assistant coupled with indigenous organic biocontrol formulations."
    }
]

# PROVEN & DEPLOYED SOLUTIONS
JHARKHAND_SOLUTIONS = [
    {
        "id": "SOL-01",
        "title": "Community Fluoride-Removal Filter Skid (45,000 L/Day)",
        "developed_by": "Birla Institute of Technology (BIT) Mesra",
        "deployed_at": "Kanke Block, Ranchi",
        "impact_metric": "3,850 citizens served daily with water fluoride <0.4 mg/L",
        "procured_by": "Dept of Drinking Water & Sanitation",
        "icon": "💧"
    },
    {
        "id": "SOL-02",
        "title": "AgroBlit Vernacular Smartphone Disease Classifier",
        "developed_by": "Birsa Agricultural University (BAU) Ranchi",
        "deployed_at": "Ormanjhi, Ratu, and Angara vegetable clusters",
        "impact_metric": "1,450 farmers active; chemical pesticide usage reduced by 38%",
        "procured_by": "Dept of Agriculture & Cooperative",
        "icon": "📱"
    },
    {
        "id": "SOL-03",
        "title": "Modular Lightweight Carbon-Fiber Accessibility Ramps",
        "developed_by": "NIT Jamshedpur Assistive Devices Center",
        "deployed_at": "Ranchi Sadar Hospital, Kanke & Chas Block Collectorates",
        "impact_metric": "Assisting 2,500+ differently-abled and senior citizens monthly",
        "procured_by": "Urban Development & Social Security Dept",
        "icon": "♿"
    },
    {
        "id": "SOL-04",
        "title": "Solar-Powered Decentralized Lac & Silk Processing Machine",
        "developed_by": "Ranchi University & BAU Joint Lab",
        "deployed_at": "Khunti & Chaibasa Tribal SHG Clusters",
        "impact_metric": "420 indigenous women artisan livelihoods empowered",
        "procured_by": "Dept of Rural Development (JSLPS)",
        "icon": "🧵"
    }
]

# STATE ACHIEVEMENTS & MILESTONES
JHARKHAND_ACHIEVEMENTS = [
    {
        "stat": "150,000+",
        "label": "Citizens Impacted",
        "desc": "Access to safe potable water, cold-chain immunization, and accessible public facilities.",
        "icon": "👥"
    },
    {
        "stat": "42",
        "label": "Innovations Incubated",
        "desc": "Grassroots hardware and software prototypes developed by Jharkhand HEIs and startups.",
        "icon": "💡"
    },
    {
        "stat": "₹18.5 Cr",
        "label": "CSR & Grants Mobilized",
        "desc": "Committed by Tata Steel, SAIL, Coal India, and state innovation matching funds.",
        "icon": "💰"
    },
    {
        "stat": "24 / 24",
        "label": "Districts Covered",
        "desc": "100% geographic coverage mapping localized societal challenges across Jharkhand.",
        "icon": "📍"
    },
    {
        "stat": "99.4%",
        "label": "Deployment Uptime",
        "desc": "IoT telemetry monitoring ground installations ensuring uninterrupted public utility.",
        "icon": "⚡"
    },
    {
        "stat": "National Award",
        "label": "GovTech Excellence 2026",
        "desc": "Conferred by Ministry of Electronics & IT for pioneering societal lifecycle innovation.",
        "icon": "🏆"
    }
]

# Pre-populated problem seeds
SEED_PROBLEMS = [
    {
        "id": "JH-WTR-2026-00124",
        "title": "Recurring seasonal shortage of potable drinking water affecting households in Hesal locality",
        "description": "Every summer between February and June, the underground borewells dry up due to declining water tables. Over 420 tribal and rural households have to walk 3.5 km daily to fetch unfiltered stream water, leading to seasonal waterborne illnesses among children and elderly.",
        "district": "Ranchi",
        "block": "Angara",
        "panchayat": "Hesal",
        "locality": "Hesal Toli",
        "gps": "23.4121, 85.4981",
        "domain": "Water Management",
        "subdomain": "Potable Drinking Water Availability & Groundwater Depletion",
        "urgency_score": 91,
        "impact_level": "High",
        "affected_population": "420 households (~2,100 people)",
        "citizen_suggestions": "Community solar powered deep aquifer pump connected to a community storage tank and gravity fed taps.",
        "evidence_files": ["water_scarcity_well.jpg", "field_survey_note.pdf"],
        "stage": "CITIZEN_PROBLEM",
        "upvotes": 68,
        "created_at": "2026-09-08T10:15:00Z",
        "reporter_name": "Ramesh Soren",
        "reporter_role": "Citizen",
        "similar_count": 43,
        "ai_analysis": {
            "confidence": 0.96,
            "generated_problem_statement": "Recurring seasonal shortage of potable drinking water caused by rapid aquifer depletion, forcing marginalized households to rely on contaminated surface streams.",
            "recommended_hei": "Birla Institute of Technology (BIT), Mesra, Ranchi",
            "recommended_tech": "Solar-driven Submersible Micro-Pumping & Electro-coagulation Filtration Unit",
            "cluster_id": "JH-CLUSTER-RNC-WTR-01"
        }
    },
    {
        "id": "JH-AGR-2026-00087",
        "title": "Early blight fungal infestation destroying vegetable crops in tomato belt",
        "description": "Fungal wilt and early blight disease are wiping out over 60% of winter tomato and brinjal harvests across Ormanjhi. Smallholder farmers lack early detection diagnostic tools and are resorting to excess unbranded chemical sprays that contaminate soil and runoff.",
        "district": "Ranchi",
        "block": "Ormanjhi",
        "panchayat": "Irba",
        "locality": "Kisan Tola",
        "gps": "23.4812, 85.4601",
        "domain": "Agriculture",
        "subdomain": "Crop Pest Surveillance & Bio-organic Control",
        "urgency_score": 84,
        "impact_level": "High",
        "affected_population": "350 smallholder farmers",
        "citizen_suggestions": "Need mobile leaf scanner app or bio-fungicide that does not require expensive spray equipment.",
        "evidence_files": ["infected_tomato_leaves.jpg"],
        "stage": "AI_PROCESSING",
        "upvotes": 52,
        "created_at": "2026-09-05T14:20:00Z",
        "reporter_name": "Sunita Devi",
        "reporter_role": "Citizen",
        "similar_count": 27,
        "ai_analysis": {
            "confidence": 0.93,
            "generated_problem_statement": "Severe pre-harvest tomato fungal blight causing economic distress to smallholders due to absence of rapid optical disease diagnostic tools and organic bio-control formulations.",
            "recommended_hei": "Birsa Agricultural University (BAU), Ranchi",
            "recommended_tech": "Smartphone Edge-AI Crop Disease Classifier + Trichoderma-based Bio-fungicide Seedling Dip",
            "cluster_id": "JH-CLUSTER-RNC-AGR-02"
        }
    },
    {
        "id": "JH-ENV-2026-00045",
        "title": "Subsurface coal mine fire gaseous emissions and fugitive dust in Jharia settlements",
        "description": "Continuous toxic fumes containing carbon monoxide, sulfur dioxide and particulate matter PM2.5 exceeding 380 ug/m3 engulfing primary schools and settlements adjacent to old coal seams.",
        "district": "Dhanbad",
        "block": "Jharia",
        "panchayat": "Lodna",
        "locality": "Lodna Basti",
        "gps": "23.7410, 86.4180",
        "domain": "Environment",
        "subdomain": "Toxic Fugitive Gas & Dust Abatement",
        "urgency_score": 95,
        "impact_level": "High",
        "affected_population": "8,500 residents & 3 government schools",
        "citizen_suggestions": "Continuous particulate barriers and community air quality warning sirens.",
        "evidence_files": ["smoke_seep_fissures.jpg", "air_quality_handheld_readings.pdf"],
        "stage": "CHALLENGE_PUBLISHED",
        "upvotes": 142,
        "created_at": "2026-08-20T09:30:00Z",
        "reporter_name": "Binod Mahato",
        "reporter_role": "Citizen",
        "similar_count": 89,
        "ai_analysis": {
            "confidence": 0.98,
            "generated_problem_statement": "Chronic ambient exposure to toxic coal mine gaseous seepage and particulate matter endangering school children in Jharia mining peri-urban belt.",
            "recommended_hei": "Indian Institute of Technology (IIT-ISM), Dhanbad",
            "recommended_tech": "Nitrogen-Foam Seam Inertization & Low-Cost Solar IoT Gas Sensor Network",
            "cluster_id": "JH-CLUSTER-DHN-ENV-01"
        },
        "govt_verification": {
            "verified_by": "Er. Alok Sharma, Chief Engineer, Dept of Drinking Water & Sanitation",
            "verified_date": "2026-08-24T11:00:00Z",
            "challenge_grant_sanctioned": 2500000,
            "gov_notes": "Official State Innovation Challenge #JH-CHG-2026-045 approved under Clean Mining & Air Quality Mission."
        }
    },
    {
        "id": "JH-WTR-2025-00003",
        "title": "High iron and fluoride contamination in drinking tubewells in Kanke tribal hamlets",
        "description": "Over 3,800 residents consuming tubewell water containing 4.8 mg/L Iron and 2.4 mg/L Fluoride. Children were exhibiting dental fluorosis and skeletal stiffness.",
        "district": "Ranchi",
        "block": "Kanke",
        "panchayat": "Sukhurhutu",
        "locality": "Sukhurhutu Munda Toli",
        "gps": "23.4412, 85.3341",
        "domain": "Water Management",
        "subdomain": "Arsenic, Iron & Fluoride Removal from Deep Tubewells",
        "urgency_score": 96,
        "impact_level": "High",
        "affected_population": "3,800 residents across 3 hamlets",
        "citizen_suggestions": "Community filter plant with regular chemical testing.",
        "evidence_files": ["discolored_water_sample.jpg", "lab_fluoride_report.pdf"],
        "stage": "GROUND_DEPLOYMENT",
        "upvotes": 245,
        "created_at": "2025-10-04T09:00:00Z",
        "reporter_name": "Birsa Munda (Gram Pradhan)",
        "reporter_role": "Citizen",
        "similar_count": 62,
        "ai_analysis": {
            "confidence": 0.99,
            "generated_problem_statement": "Excessive groundwater geochemical fluorosis and ferruginous contamination inflicting permanent bone/dental pathology on indigenous population.",
            "recommended_hei": "BIT Mesra Environmental Engineering Dept",
            "recommended_tech": "Adsorptive Activated Alumina & Catalytic Iron-Oxidation Filtration Skids with IoT TDS/Turbidity Telemetry",
            "cluster_id": "JH-CLUSTER-RNC-WTR-02"
        },
        "deployment_data": {
            "deployed_date": "2026-03-15",
            "procuring_agency": "Jharkhand Drinking Water & Sanitation Dept (Tender #DWSD-2026-FL-08)",
            "contractor_innovator": "JharJal CleanTech Pvt Ltd (BIT Mesra Incubation)",
            "impact_metrics": {
                "daily_liters_purified": "45,000 Liters/Day",
                "fluoride_level_post_filter": "0.4 mg/L (Safe limit < 1.0)",
                "iron_level_post_filter": "0.1 mg/L (Safe limit < 0.3)",
                "beneficiaries": 3850,
                "uptime_percentage": "99.4%"
            }
        }
    }
]
