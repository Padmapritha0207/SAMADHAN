"""
test_app.py - Automated Unit & Integration Test Suite for SAMADHAN
"""

import unittest
import json
import os
import sys

# Ensure scratch/jhar-solve is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database
import ai_engine
import i18n
import app

class TestSamadhanPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db(force_seed=True)
        cls.client = app.app.test_client()

    def test_i18n_completeness(self):
        """Verify that all keys in English exist in Hindi and app_name is SAMADHAN."""
        en_keys = set(i18n.TRANSLATIONS["en"].keys())
        hi_keys = set(i18n.TRANSLATIONS["hi"].keys())
        missing_in_hi = en_keys - hi_keys
        self.assertEqual(len(missing_in_hi), 0, f"Missing keys in Hindi: {missing_in_hi}")
        self.assertEqual(i18n.TRANSLATIONS["en"]["app_name"], "SAMADHAN")

    def test_ai_domain_classification(self):
        """Verify AI engine accurately classifies diverse societal domains."""
        test_cases = [
            ("Borewells drying up and severe fluoride poisoning in tubewells", "Water Management"),
            ("Tomato crops ruined by leaf curl virus and fungal blight in Ormanjhi", "Agriculture"),
            ("Toxic coal fire smoke and particulate dust engulfing settlement", "Environment"),
            ("Vaccine refrigerators fail due to 18 hour power cuts in tribal health subcenter", "Healthcare"),
            ("Open drainage and untreated sewage waste overflowing into village streets", "Sanitation"),
            ("Wheelchair ramp broken and stairs prevent disabled citizens accessing block office", "Accessibility")
        ]
        for text, expected_domain in test_cases:
            domain, subdomain, conf = ai_engine.engine.classify_domain(text, text)
            self.assertEqual(domain, expected_domain, f"Failed for '{text}': got {domain}, expected {expected_domain}")

    def test_ai_urgency_score(self):
        """Verify urgency score is high for life-critical hazards."""
        score_high, impact_high = ai_engine.engine.calculate_urgency_score(
            "Toxic contamination in tubewells causing child death and hospitalizations",
            "Emergency outbreak affecting 5000 families",
            "5000 families"
        )
        self.assertGreaterEqual(score_high, 80)
        self.assertEqual(impact_high, "High")

    def test_ai_hei_matching(self):
        """Verify HEI matching returns premier Jharkhand institutions."""
        match_wtr = ai_engine.engine.match_hei_expertise("Water Management")
        self.assertIn("Mesra", match_wtr["institution"])

        match_agr = ai_engine.engine.match_hei_expertise("Agriculture")
        self.assertIn("Birsa Agricultural University", match_agr["institution"])

        match_env = ai_engine.engine.match_hei_expertise("Environment")
        self.assertIn("IIT-ISM", match_env["institution"])

    def test_stakeholder_registration_and_login(self):
        """Test registration and login for Student & HEI, Industry, and Government."""
        categories = [
            ("STUDENT_HEI", "scholar_rahul", "rahul@bitmesra.ac.in", "pass1234", "BIT Mesra"),
            ("INDUSTRY", "tata_lead", "csrlead@tatasteel.com", "pass1234", "Tata Steel CSR"),
            ("GOVERNMENT", "dir_rural", "director.rural@jharkhand.gov.in", "pass1234", "Dept of Rural Dev")
        ]
        for user_type, uname, email, pwd, org in categories:
            # Register
            reg_res = self.client.post("/api/auth/register", json={
                "user_type": user_type,
                "username": uname,
                "email": email,
                "password": pwd,
                "organization": org
            })
            self.assertIn(reg_res.status_code, [201, 400]) # 201 created or 400 if exists

            # Login
            log_res = self.client.post("/api/auth/login", json={
                "user_type": user_type,
                "login_identifier": uname,
                "password": pwd
            })
            self.assertEqual(log_res.status_code, 200)
            data = log_res.get_json()
            self.assertTrue(data["success"])
            self.assertEqual(data["user"]["user_type"], user_type)

    def test_contact_inquiry_api(self):
        """Test Contact message logging."""
        res = self.client.post("/api/contact", json={
            "name": "Anil Kumar",
            "email": "anil@gmail.com",
            "message": "Interested in CSR funding for rural water projects in Khunti."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

    def test_trends_projects_solutions_achievements_apis(self):
        """Test new content APIs."""
        for endpoint, min_count in [("/api/trends", 4), ("/api/projects", 3), ("/api/solutions", 3), ("/api/achievements", 5)]:
            res = self.client.get(endpoint)
            self.assertEqual(res.status_code, 200)
            items = res.get_json()
            self.assertGreaterEqual(len(items), min_count)

    def test_create_problem_api(self):
        """Test POST /api/problems intake via 5-step wizard simulation."""
        payload = {
            "title": "Severe iron contamination in school drinking borewell",
            "description": "Children at Government Middle School are drinking reddish water with severe metallic taste and gastrointestinal distress.",
            "district": "Khunti",
            "block": "Murhu",
            "panchayat": "Panchghagh",
            "locality": "School Toli",
            "affected_population": "320 students and teachers",
            "suggested_domain": "Water Management"
        }
        res = self.client.post("/api/problems", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data["success"])
        prob = data["problem"]
        self.assertTrue(prob["id"].startswith("JH-WTR-2026-"))
        self.assertEqual(prob["domain"], "Water Management")
        self.assertGreaterEqual(prob["urgency_score"], 60)

    def test_government_verification_flow(self):
        """Test Government verification converts problem to official challenge."""
        res = self.client.post("/api/problems/JH-WTR-2026-00124/verify", json={
            "gov_notes": "Official State Water Challenge sanctioned with INR 20 Lakhs grant.",
            "challenge_grant_sanctioned": 2000000
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["problem"]["stage"], "CHALLENGE_PUBLISHED")

    def test_locations_api(self):
        """Verify 24 Jharkhand districts and cascading blocks."""
        res = self.client.get("/api/locations")
        self.assertEqual(res.status_code, 200)
        locs = res.get_json()
        self.assertEqual(len(locs), 24)

if __name__ == "__main__":
    unittest.main()
