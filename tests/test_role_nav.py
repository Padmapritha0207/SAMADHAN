"""
test_role_nav.py - Verify role authentication mapping and session isolation
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database
import app

class TestRoleNavigation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db(force_seed=True)
        cls.client = app.app.test_client()

    def test_student_hei_login_role(self):
        """Verify Student & HEI login returns HEI role."""
        res = self.client.post("/api/auth/login", json={
            "user_type": "STUDENT_HEI",
            "login_identifier": "student_bit",
            "password": "samadhan123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["user"]["user_type"], "STUDENT_HEI")
        self.assertEqual(data["active_user"]["role"], "HEI")

    def test_industry_login_role(self):
        """Verify Industry login returns INDUSTRY role."""
        res = self.client.post("/api/auth/login", json={
            "user_type": "INDUSTRY",
            "login_identifier": "tatasteel_csr",
            "password": "samadhan123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["user"]["user_type"], "INDUSTRY")
        self.assertEqual(data["active_user"]["role"], "INDUSTRY")

    def test_government_login_role(self):
        """Verify Government login returns GOVERNMENT role."""
        res = self.client.post("/api/auth/login", json={
            "user_type": "GOVERNMENT",
            "login_identifier": "officer_dwsd",
            "password": "samadhan123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["user"]["user_type"], "GOVERNMENT")
        self.assertEqual(data["active_user"]["role"], "GOVERNMENT")

    def test_logout_resets_to_citizen(self):
        """Verify logout returns citizen persona."""
        res = self.client.post("/api/auth/logout")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["user"]["role"], "CITIZEN")

if __name__ == "__main__":
    unittest.main()
