"""
i18n.py - Bilingual (English & Hindi) Internationalization Dictionary for SAMADHAN
Jharkhand Societal Innovation Lifecycle Platform
"""

TRANSLATIONS = {
    "en": {
        # App Branding
        "app_name": "SAMADHAN",
        "app_subtitle": "Jharkhand Societal Innovation Lifecycle Platform",
        "tagline_sub": "From Citizen Problems to Government-Deployed Solutions",
        "tagline_motto": "Problem -> Innovation -> Impact",
        "state_govt": "Government of Jharkhand",
        "govtech_initiative": "State Innovation & Technology Mission",

        # Auth & Top Nav
        "btn_login": "Login",
        "btn_register": "Register",
        "tab_student_hei": "Student & Higher Education Institution",
        "tab_industry": "Industry",
        "tab_government": "Government",
        "lbl_username": "Username",
        "lbl_email": "Email Address",
        "lbl_password": "Password",
        "lbl_confirm_password": "Confirm Password",
        "lbl_institution": "Institution / College Name",
        "lbl_company": "Company / Foundation Name",
        "lbl_department": "Government Department",
        "btn_signin": "Sign In to SAMADHAN",
        "btn_create_account": "Create Account",

        # Navigation & Roles
        "nav_home": "Home",
        "nav_report": "Report Problem",
        "nav_trends": "Current Trends",
        "nav_projects": "Existing Projects",
        "nav_solutions": "Solutions",
        "nav_achievements": "Achievements",
        "nav_command": "Gov Command Center",
        "nav_proposals": "HEI Hub",
        "nav_funding": "Industry CSR",
        "nav_contact": "Contact",
        "nav_admin": "Admin Center",
        "active_role": "Active Persona",
        "switch_role": "Switch Persona",

        # Hero Section
        "hero_title": "Your Problem Can Become a Solution.",
        "hero_subtitle": "Report a real problem. Help innovators build a solution. Track its journey to the ground.",
        "hero_cta_report": "REPORT A PROBLEM",

        # Lifecycle Banner & Notice
        "ai_notice_title": "Assisted Intelligence with Human Governance",
        "ai_notice_body": "AI classifies, detects duplicates, and estimates urgency, but all decisions and challenge publications require human government verification.",

        # Sections
        "sec_trends_title": "Current Trends in Jharkhand",
        "sec_trends_sub": "Key technological and societal transitions driving grassroots innovation across the state",
        "sec_projects_title": "Existing Projects in Progress",
        "sec_projects_sub": "Active multi-stakeholder initiatives under R&D, prototype validation, and pilot testing",
        "sec_solutions_title": "Deployed & Proven Solutions",
        "sec_solutions_sub": "Tested technological innovations ready for procurement, scaling, and public benefit",
        "sec_achievements_title": "State Achievements & Impact",
        "sec_achievements_sub": "Measurable outcomes delivered through citizen-academia-industry-government collaboration",

        # Contact & Footer
        "contact_title": "Contact State Innovation Mission",
        "contact_sub": "Have questions or want to partner with SAMADHAN? Reach our nodal coordination team.",
        "contact_address_lbl": "Office Address",
        "contact_address_val": "State Innovation & Technology Mission, 3rd Floor, Project Building, Dhurwa, Ranchi - 834004, Jharkhand",
        "contact_phone_lbl": "Toll-Free Helpline",
        "contact_phone_val": "1800-345-7658 / 0651-2400124",
        "contact_email_lbl": "Official Email",
        "contact_email_val": "contact@samadhan.jharkhand.gov.in",
        "contact_social_lbl": "Connect on Social Media",
        "lbl_full_name": "Full Name",
        "lbl_message": "Message / Inquiry",
        "btn_send_message": "Send Message",

        # 15-Stage Lifecycle
        "stage_1": "Citizen Problem",
        "stage_2": "AI Processing",
        "stage_3": "Government Verification",
        "stage_4": "Challenge Published",
        "stage_5": "HEI/Innovator Proposal",
        "stage_6": "Industry Screening",
        "stage_7": "Funding Allocated",
        "stage_8": "Prototype Development",
        "stage_9": "Lab Development",
        "stage_10": "Testing & Pilot",
        "stage_11": "Legal/IP Clearance",
        "stage_12": "Procurement Readiness",
        "stage_13": "Govt Procurement",
        "stage_14": "Ground Deployment",
        "stage_15": "Impact Monitoring & Scaling",

        # Domains
        "domain_water_management": "Water Management",
        "domain_healthcare": "Healthcare",
        "domain_agriculture": "Agriculture",
        "domain_sanitation": "Sanitation",
        "domain_environment": "Environment",
        "domain_education": "Education",
        "domain_rural_livelihoods": "Rural Livelihoods",
        "domain_accessibility": "Accessibility",
        "domain_urban_infrastructure": "Urban Infrastructure",
        "domain_public_service_delivery": "Public Service Delivery",

        # 5-Step Wizard
        "wizard_step1_title": "Problem Details",
        "wizard_step1_desc": "What challenge is your community facing?",
        "wizard_step2_title": "Location",
        "wizard_step2_desc": "Where is this problem located in Jharkhand?",
        "wizard_step3_title": "Evidence Upload",
        "wizard_step3_desc": "Add photos, documents, or video clips",
        "wizard_step4_title": "Impact & Context",
        "wizard_step4_desc": "Who is affected and your suggested solutions",
        "wizard_step5_title": "Review & Submit",
        "wizard_step5_desc": "Verify all details before generating your Problem ID",

        # Form Fields
        "lbl_problem_title": "Problem Title",
        "lbl_problem_desc": "Detailed Description",
        "lbl_suggested_domain": "Suggested Category (Optional)",
        "lbl_district": "District",
        "lbl_block": "Block",
        "lbl_panchayat": "Panchayat",
        "lbl_locality": "Locality / Village / Ward",
        "lbl_gps": "GPS Coordinates",
        "lbl_affected_population": "Estimated Affected People / Families",
        "lbl_urgency_rationale": "Why is this urgent?",
        "lbl_citizen_suggestions": "Your Suggested Solution (Optional)",
        "btn_next": "Next Step",
        "btn_back": "Back",
        "btn_submit": "Submit to SAMADHAN",
        "btn_cancel": "Cancel",
        "btn_live_ai_preview": "Analyze with AI Engine",

        # Command Center
        "cmd_title": "Government Innovation Command Center",
        "cmd_subtitle": "Real-time AI Problem Clustering, Verification & Sanctions across Jharkhand",
        "cmd_pending_verification": "Pending Gov Verification",
        "cmd_active_challenges": "Published Challenges",
        "cmd_pilots_in_flight": "Pilots in Field",
        "cmd_procurement_ready": "Procurement Ready",
        "cmd_filter_district": "All Districts",
        "cmd_filter_domain": "All Domains",
        "cmd_btn_verify": "Verify & Publish Challenge",
        "cmd_btn_reject": "Reject / Mark Ineligible",

        # HEI & Innovator Portal
        "hei_title": "HEI & Innovator Solution Hub",
        "hei_subtitle": "Turn verified societal challenges into research breakthroughs and funded prototypes",
        "hei_btn_submit_proposal": "Submit Solution Proposal",

        # Industry & CSR Portal
        "industry_title": "Industry & CSR Innovation Marketplace",
        "industry_subtitle": "Fund high-impact grassroots innovations with measurable SDG and CSR impact",
        "industry_pledge_grant": "Pledge CSR / Grant Funding"
    },
    "hi": {
        # App Branding
        "app_name": "समाधान (SAMADHAN)",
        "app_subtitle": "झारखंड सामाजिक नवाचार जीवनचक्र मंच",
        "tagline_sub": "नागरिक समस्याओं से सरकार द्वारा क्रियान्वित समाधान तक",
        "tagline_motto": "समस्या -> नवाचार -> प्रभाव",
        "state_govt": "झारखंड सरकार",
        "govtech_initiative": "राज्य नवाचार एवं प्रौद्योगिकी मिशन",

        # Auth & Top Nav
        "btn_login": "लॉग इन",
        "btn_register": "पंजीकरण",
        "tab_student_hei": "छात्र एवं उच्च शिक्षण संस्थान",
        "tab_industry": "उद्योग",
        "tab_government": "सरकार",
        "lbl_username": "उपयोगकर्ता नाम",
        "lbl_email": "ईमेल पता",
        "lbl_password": "पासवर्ड",
        "lbl_confirm_password": "पासवर्ड की पुष्टि करें",
        "lbl_institution": "संस्थान / कॉलेज का नाम",
        "lbl_company": "कंपनी / फाउंडेशन का नाम",
        "lbl_department": "सरकारी विभाग",
        "btn_signin": "समाधान में साइन इन करें",
        "btn_create_account": "खाता बनाएं",

        # Navigation & Roles
        "nav_home": "मुख्य पृष्ठ",
        "nav_report": "समस्या दर्ज करें",
        "nav_trends": "वर्तमान रुझान",
        "nav_projects": "सक्रिय परियोजनाएं",
        "nav_solutions": "समाधान",
        "nav_achievements": "उपलब्धियां",
        "nav_command": "सरकारी कमांड सेंटर",
        "nav_proposals": "संस्थान केंद्र",
        "nav_funding": "उद्योग सीएसआर",
        "nav_contact": "संपर्क करें",
        "nav_admin": "प्रशासन केंद्र",
        "active_role": "सक्रिय भूमिका",
        "switch_role": "भूमिका बदलें",

        # Hero Section
        "hero_title": "आपकी समस्या एक समाधान बन सकती है।",
        "hero_subtitle": "वास्तविक समस्या दर्ज करें। नवाचारियों को समाधान बनाने में मदद करें। इसे जमीन पर लागू होते देखें।",
        "hero_cta_report": "समस्या दर्ज करें",

        # Lifecycle Banner & Notice
        "ai_notice_title": "सहायक एआई और मानवीय सरकारी अनुमोदन",
        "ai_notice_body": "एआई वर्गीकरण करता है, डुप्लिकेट खोजता है और तात्कालिकता का अनुमान लगाता है, लेकिन चुनौती प्रकाशित करने के लिए अधिकृत सरकारी अधिकारी का सत्यापन अनिवार्य है।",

        # Sections
        "sec_trends_title": "झारखंड में वर्तमान रुझान",
        "sec_trends_sub": "राज्य भर में जमीनी नवाचार को गति देने वाले प्रमुख तकनीकी और सामाजिक बदलाव",
        "sec_projects_title": "प्रगति पर वर्तमान परियोजनाएं",
        "sec_projects_sub": "अनुसंधान, प्रोटोटाइप और पायलट परीक्षण के तहत सक्रिय बहु-हितधारक पहल",
        "sec_solutions_title": "तैनात और सिद्ध समाधान",
        "sec_solutions_sub": "खरीद, विस्तार और सार्वजनिक उपयोग के लिए तैयार प्रमाणित तकनीकी नवाचार",
        "sec_achievements_title": "राज्य की उपलब्धियां और प्रभाव",
        "sec_achievements_sub": "नागरिक, शिक्षा, उद्योग और सरकार के सहयोग से प्राप्त ठोस परिणाम",

        # Contact & Footer
        "contact_title": "राज्य नवाचार मिशन से संपर्क करें",
        "contact_sub": "कोई प्रश्न है या समाधान से जुड़ना चाहते हैं? हमारी नोडल टीम से संपर्क करें।",
        "contact_address_lbl": "कार्यालय का पता",
        "contact_address_val": "राज्य नवाचार एवं प्रौद्योगिकी मिशन, तृतीय तल, प्रोजेक्ट भवन, धुर्वा, रांची - 834004, झारखंड",
        "contact_phone_lbl": "टोल-फ्री हेल्पलाइन",
        "contact_phone_val": "1800-345-7658 / 0651-2400124",
        "contact_email_lbl": "आधिकारिक ईमेल",
        "contact_email_val": "contact@samadhan.jharkhand.gov.in",
        "contact_social_lbl": "सोशल मीडिया पर जुड़ें",
        "lbl_full_name": "पूरा नाम",
        "lbl_message": "संदेश / पूछताछ",
        "btn_send_message": "संदेश भेजें",

        # 15-Stage Lifecycle
        "stage_1": "नागरिक समस्या",
        "stage_2": "एआई प्रसंस्करण",
        "stage_3": "सरकारी सत्यापन",
        "stage_4": "चुनौती प्रकाशित",
        "stage_5": "संस्थान/नवाचारी प्रस्ताव",
        "stage_6": "उद्योग स्क्रीनिंग",
        "stage_7": "अनुदान आवंटित",
        "stage_8": "प्रोटोटाइप विकास",
        "stage_9": "प्रयोगशाला विकास",
        "stage_10": "परीक्षण एवं पायलट",
        "stage_11": "कानूनी/आईपी अनापत्ति",
        "stage_12": "खरीद तत्परता",
        "stage_13": "सरकारी खरीद",
        "stage_14": "जमीनी तैनाती",
        "stage_15": "प्रभाव निगरानी एवं विस्तार",

        # Domains
        "domain_water_management": "जल प्रबंधन",
        "domain_healthcare": "स्वास्थ्य सेवा",
        "domain_agriculture": "कृषि",
        "domain_sanitation": "स्वच्छता",
        "domain_environment": "पर्यावरण",
        "domain_education": "शिक्षा",
        "domain_rural_livelihoods": "ग्रामीण आजीविका",
        "domain_accessibility": "सुलभता",
        "domain_urban_infrastructure": "शहरी अवसंरचना",
        "domain_public_service_delivery": "लोक सेवा वितरण",

        # 5-Step Wizard
        "wizard_step1_title": "समस्या विवरण",
        "wizard_step1_desc": "आपके समुदाय में क्या मुख्य चुनौती है?",
        "wizard_step2_title": "स्थान",
        "wizard_step2_desc": "झारखंड में यह समस्या कहाँ स्थित है?",
        "wizard_step3_title": "साक्ष्य अपलोड",
        "wizard_step3_desc": "फ़ोटो, दस्तावेज़ या वीडियो क्लिप जोड़ें",
        "wizard_step4_title": "प्रभाव एवं संदर्भ",
        "wizard_step4_desc": "कौन प्रभावित है और आपके सुझाव",
        "wizard_step5_title": "पुनरीक्षण एवं सबमिट",
        "wizard_step5_desc": "समस्या आईडी उत्पन्न करने से पहले विवरण जांचें",

        # Form Fields
        "lbl_problem_title": "समस्या का शीर्षक",
        "lbl_problem_desc": "विस्तृत विवरण",
        "lbl_suggested_domain": "सुझावित श्रेणी (वैकल्पिक)",
        "lbl_district": "जिला",
        "lbl_block": "प्रखंड (ब्लॉक)",
        "lbl_panchayat": "पंचायत",
        "lbl_locality": "इलाका / गाँव / वार्ड",
        "lbl_gps": "जीपीएस निर्देशांक",
        "lbl_affected_population": "अनुमानित प्रभावित लोग / परिवार",
        "lbl_urgency_rationale": "यह समस्या कितनी जरूरी क्यों है?",
        "lbl_citizen_suggestions": "आपका सुझाया गया समाधान (वैकल्पिक)",
        "btn_next": "अगला कदम",
        "btn_back": "पीछे",
        "btn_submit": "समाधान में जमा करें",
        "btn_cancel": "रद्द करें",
        "btn_live_ai_preview": "एआई इंजन से विश्लेषण करें",

        # Command Center
        "cmd_title": "सरकारी नवाचार कमांड सेंटर",
        "cmd_subtitle": "झारखंड भर में रीयल-टाइम एआई समस्या क्लस्टरिंग, सत्यापन और स्वीकृति",
        "cmd_pending_verification": "सत्यापन लंबित",
        "cmd_active_challenges": "प्रकाशित चुनौतियां",
        "cmd_pilots_in_flight": "मैदान में सक्रिय पायलट",
        "cmd_procurement_ready": "खरीद हेतु तैयार",
        "cmd_filter_district": "सभी जिले",
        "cmd_filter_domain": "सभी क्षेत्र",
        "cmd_btn_verify": "सत्यापित करें व चुनौती बनाएं",
        "cmd_btn_reject": "अमान्य घोषित करें",

        # HEI & Innovator Portal
        "hei_title": "संस्थान एवं नवाचारी समाधान केंद्र",
        "hei_subtitle": "सत्यापित सामाजिक चुनौतियों को अनुसंधान और वित्तपोषित प्रोटोटाइप में बदलें",
        "hei_btn_submit_proposal": "समाधान प्रस्ताव जमा करें",

        # Industry & CSR Portal
        "industry_title": "उद्योग एवं सीएसआर नवाचार बाज़ार",
        "industry_subtitle": "मापने योग्य सामाजिक प्रभाव वाले जमीनी नवाचारों को वित्तपोषित करें",
        "industry_pledge_grant": "सीएसआर / अनुदान सहयोग दें"
    }
}

def get_text(key: str, lang: str = "en") -> str:
    dict_for_lang = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return dict_for_lang.get(key, TRANSLATIONS["en"].get(key, key))
