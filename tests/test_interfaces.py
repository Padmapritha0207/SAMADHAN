"""
test_interfaces.py - Tests for HEI, Industry, and Government dedicated interfaces
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database
import app

class TestStakeholderInterfaces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db(force_seed=True)
        cls.client = app.app.test_client()

    def test_hei_dashboard(self):
        """Verify HEI dashboard returns problem statements, AI generated problem statements, submitted proposals, and project status."""
        res = self.client.get("/api/hei/dashboard")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("problem_statements", data)
        self.assertIn("proposals", data)
        self.assertIn("active_projects", data)
        self.assertIn("stats", data)

        # Verify AI generated problem statement is present on problem statements
        self.assertGreater(len(data["problem_statements"]), 0)
        first_prob = data["problem_statements"][0]
        self.assertIn("ai_problem_statement", first_prob)
        self.assertTrue(len(first_prob["ai_problem_statement"]) > 10)

    def test_proposal_submission_with_contact_details(self):
        """Verify submitting solution proposal with HEI contact details and industry notification."""
        payload = {
            "problem_id": "JH-WTR-2026-00124",
            "title": "Solar-Powered Electrochemical Fluoride Removal Unit",
            "technical_abstract": "Continuous flow capacitive deionization skid powered by 2kW solar PV array with activated carbon electrodes.",
            "proposed_budget": 2400000,
            "timeline_months": 5,
            "innovator_name": "Dr. Sunita Murmu",
            "hei_id": "hei-bit-mesra",
            "contact_name": "Dr. Sunita Murmu",
            "contact_email": "sunita.murmu@bitmesra.ac.in",
            "contact_phone": "+91 94311 77889",
            "hei_institution": "BIT Mesra Ranchi - Centre for Environmental Tech"
        }
        res = self.client.post("/api/proposals", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data["success"])

        # Check industry notification was emitted
        notifs_res = self.client.get("/api/notifications?role=INDUSTRY")
        self.assertEqual(notifs_res.status_code, 200)
        notifs = notifs_res.get_json()
        self.assertTrue(any("Solar-Powered Electrochemical" in n["title"] for n in notifs))

    def test_industry_dashboard_and_review(self):
        """Verify Industry dashboard has proposals to review, HEI contact details, and funded status."""
        res = self.client.get("/api/industry/dashboard")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("pending_proposals", data)
        self.assertIn("funded_proposals", data)
        self.assertIn("notifications", data)
        self.assertIn("stats", data)

        # Check that proposals include HEI contact details
        for prop in data["pending_proposals"]:
            self.assertIn("contact_name", prop)
            self.assertIn("contact_email", prop)
            self.assertIn("contact_phone", prop)
            self.assertIn("hei_institution", prop)

    def test_industry_funding_approval_and_disapproval(self):
        """Verify Industry Approve and Disapprove actions."""
        # 1. Approve proposal 1
        app_res = self.client.post("/api/proposals/1/approve", json={
            "industry_name": "Tata Steel Foundation",
            "notes": "Sanctioned full CSR grant of Rs 35 Lakhs for coal fire foam infiltration."
        })
        self.assertEqual(app_res.status_code, 200)
        self.assertTrue(app_res.get_json()["success"])

        # 2. Check problem stage advanced to FUNDING_ALLOCATED
        prob_res = self.client.get("/api/problems/JH-ENV-2026-00045")
        self.assertEqual(prob_res.status_code, 200)
        self.assertEqual(prob_res.get_json()["stage"], "FUNDING_ALLOCATED")

        # 3. Disapprove another proposal
        # Submit a temporary proposal to disapprove
        temp_prop_res = self.client.post("/api/proposals", json={
            "problem_id": "JH-WTR-2026-00124",
            "title": "Preliminary Ceramic Filter Mockup",
            "technical_abstract": "Basic clay pot filtration test that requires further thermal validation.",
            "proposed_budget": 500000,
            "timeline_months": 3,
            "contact_name": "Test Innovator",
            "contact_email": "test@innovator.org",
            "contact_phone": "+91 99999 88888",
            "hei_institution": "Ranchi University"
        })
        self.assertEqual(temp_prop_res.status_code, 201)

        # Get the ID of the new proposal
        ind_dash = self.client.get("/api/industry/dashboard").get_json()
        new_prop = [p for p in ind_dash["pending_proposals"] if "Ceramic Filter" in p["title"]][0]
        prop_id = new_prop["id"]

        dis_res = self.client.post(f"/api/proposals/{prop_id}/disapprove", json={
            "industry_name": "Tata Steel Foundation",
            "reason": "Does not meet scale requirement for 2026 CSR framework."
        })
        self.assertEqual(dis_res.status_code, 200)
        self.assertTrue(dis_res.get_json()["success"])

    def test_government_master_overview(self):
        """Verify Government master overview returns all problems, all solutions, and all project statuses."""
        res = self.client.get("/api/government/master")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("all_problem_statements", data)
        self.assertIn("all_solutions", data)
        self.assertIn("all_project_statuses", data)
        self.assertIn("stage_distribution", data)
        self.assertIn("stats", data)

        self.assertGreater(len(data["all_problem_statements"]), 0)
        self.assertGreater(len(data["all_solutions"]), 0)
        self.assertGreater(len(data["all_project_statuses"]), 0)

if __name__ == "__main__":
    unittest.main()
