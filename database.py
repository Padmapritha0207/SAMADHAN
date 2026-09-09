# -*- coding: utf-8 -*-
"""
database.py - SQLite storage and data access layer for SAMADHAN
Supports 3 dedicated stakeholder interfaces: HEI/Students, Industry, and Government.
"""

import sqlite3
import json
from datetime import datetime, timezone
import os
import hashlib
import seed_data
from ai_engine import engine

DB_PATH = os.path.join(os.path.dirname(__file__), "jharsolve.db")

DOMAIN_CODES = {
    "Water Management": "WTR",
    "Healthcare": "HLT",
    "Agriculture": "AGR",
    "Sanitation": "SAN",
    "Environment": "ENV",
    "Education": "EDU",
    "Rural Livelihoods": "RUR",
    "Accessibility": "ACC",
    "Urban Infrastructure": "URB",
    "Public Service Delivery": "PSD"
}

LIFECYCLE_STAGES = [
    "CITIZEN_PROBLEM",
    "AI_PROCESSING",
    "GOVT_VERIFICATION",
    "CHALLENGE_PUBLISHED",
    "HEI_INNOVATOR_PROPOSAL",
    "INDUSTRY_SCREENING",
    "FUNDING_ALLOCATED",
    "PROTOTYPE_DEVELOPMENT",
    "LAB_DEVELOPMENT",
    "TESTING_PILOT",
    "LEGAL_IP_CLEARANCE",
    "PROCUREMENT_READY",
    "GOVT_PROCUREMENT",
    "GROUND_DEPLOYMENT",
    "IMPACT_MONITORING_SCALING"
]

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_seed=False):
    conn = get_db()
    cursor = conn.cursor()

    if force_seed:
        cursor.execute("DROP TABLE IF EXISTS problems")
        cursor.execute("DROP TABLE IF EXISTS proposals")
        cursor.execute("DROP TABLE IF EXISTS notifications")
        cursor.execute("DROP TABLE IF EXISTS funding_pledges")
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS contact_inquiries")
        cursor.execute("DROP TABLE IF EXISTS audit_logs")
        cursor.execute("DROP TABLE IF EXISTS upvotes")
        conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        district TEXT NOT NULL,
        block TEXT,
        panchayat TEXT,
        locality TEXT,
        gps TEXT,
        domain TEXT NOT NULL,
        subdomain TEXT,
        urgency_score INTEGER DEFAULT 50,
        impact_level TEXT DEFAULT 'Medium',
        affected_population TEXT,
        citizen_suggestions TEXT,
        evidence_files TEXT,
        stage TEXT NOT NULL DEFAULT 'CITIZEN_PROBLEM',
        upvotes INTEGER DEFAULT 1,
        created_at TEXT NOT NULL,
        reporter_name TEXT,
        reporter_role TEXT DEFAULT 'Citizen',
        similar_count INTEGER DEFAULT 0,
        ai_analysis TEXT,
        govt_verification TEXT,
        funding_details TEXT,
        pilot_data TEXT,
        deployment_data TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proposals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id TEXT NOT NULL,
        hei_id TEXT,
        innovator_name TEXT NOT NULL,
        title TEXT NOT NULL,
        technical_abstract TEXT NOT NULL,
        proposed_budget REAL,
        timeline_months INTEGER,
        milestones TEXT,
        status TEXT DEFAULT 'SUBMITTED',
        funding_status TEXT DEFAULT 'PENDING_REVIEW',
        contact_name TEXT,
        contact_email TEXT,
        contact_phone TEXT,
        hei_institution TEXT,
        funding_industry_name TEXT,
        funding_decision_notes TEXT,
        decision_date TEXT,
        submitted_at TEXT NOT NULL,
        FOREIGN KEY (problem_id) REFERENCES problems(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient_role TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        problem_id TEXT,
        proposal_id INTEGER,
        created_at TEXT NOT NULL,
        is_read INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funding_pledges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id TEXT NOT NULL,
        industry_id TEXT,
        industry_name TEXT NOT NULL,
        pledge_amount REAL NOT NULL,
        funding_type TEXT DEFAULT 'CSR_GRANT',
        notes TEXT,
        pledged_at TEXT NOT NULL,
        FOREIGN KEY (problem_id) REFERENCES problems(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_type TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        organization TEXT,
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_inquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        actor_name TEXT NOT NULL,
        actor_role TEXT NOT NULL,
        action TEXT NOT NULL,
        problem_id TEXT,
        details TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS upvotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id TEXT NOT NULL,
        user_identifier TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(problem_id, user_identifier)
    )
    """)

    conn.commit()

    # Seed demo users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        demo_users = [
            ("STUDENT_HEI", "student_bit", "researcher@bitmesra.ac.in", hash_pw("samadhan123"), "BIT Mesra Ranchi"),
            ("INDUSTRY", "tatasteel_csr", "csr@tatasteel.com", hash_pw("samadhan123"), "Tata Steel Foundation"),
            ("GOVERNMENT", "officer_dwsd", "alok.sharma@jharkhand.gov.in", hash_pw("samadhan123"), "Dept of Drinking Water & Sanitation")
        ]
        cursor.executemany("""
        INSERT INTO users (user_type, username, email, password_hash, organization, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, demo_users)
        conn.commit()

    # Seed problems if empty or force_seed
    cursor.execute("SELECT COUNT(*) FROM problems")
    count = cursor.fetchone()[0]
    if count == 0 or force_seed:
        if force_seed:
            cursor.execute("DELETE FROM problems")
            cursor.execute("DELETE FROM proposals")
            cursor.execute("DELETE FROM notifications")
            cursor.execute("DELETE FROM funding_pledges")
            cursor.execute("DELETE FROM audit_logs")
            cursor.execute("DELETE FROM upvotes")

        for p in seed_data.SEED_PROBLEMS:
            cursor.execute("""
            INSERT INTO problems (
                id, title, description, district, block, panchayat, locality, gps,
                domain, subdomain, urgency_score, impact_level, affected_population,
                citizen_suggestions, evidence_files, stage, upvotes, created_at,
                reporter_name, reporter_role, similar_count, ai_analysis,
                govt_verification, funding_details, pilot_data, deployment_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"], p["title"], p["description"], p["district"],
                p.get("block"), p.get("panchayat"), p.get("locality"),
                json.dumps(p.get("gps", [23.3441, 85.3096])),
                p["domain"], p.get("subdomain"), p.get("urgency_score", 50),
                p.get("impact_level", "Medium"), p.get("affected_population"),
                p.get("citizen_suggestions"), json.dumps(p.get("evidence_files", [])),
                p["stage"], p.get("upvotes", 1), p.get("created_at", datetime.now(timezone.utc).isoformat()),
                p.get("reporter_name", "Concerned Citizen"), p.get("reporter_role", "Citizen"),
                p.get("similar_count", 0), json.dumps(p.get("ai_analysis", {})),
                json.dumps(p.get("govt_verification", {})), json.dumps(p.get("funding_details", {})),
                json.dumps(p.get("pilot_data", {})), json.dumps(p.get("deployment_data", {}))
            ))

        sample_proposals = [
            (
                "JH-ENV-2026-00045", "hei-iit-ism-dhanbad", "Prof. S. K. Roy",
                "Nitrogen-Foam Coal Seam Fire Infiltration System with IoT Thermal Probes",
                "Subsurface high-pressure injection of non-combustible nitrogen foam to extinguish subsurface seam fires combined with real-time solar particulate IoT nodes.",
                3500000, 6, json.dumps(["Phase 1: Lab Test Foam Expansion", "Phase 2: Borehole Injection Field Pilot"]),
                "UNDER_SCREENING", "PENDING_REVIEW",
                "Prof. S. K. Roy", "skroy.mining@iitism.ac.in", "+91 94311 28941",
                "Indian Institute of Technology (IIT-ISM), Dhanbad", None, None, None,
                "2026-09-01T10:00:00Z"
            ),
            (
                "JH-SAN-2026-00032", "hei-nit-jamshedpur", "Dr. Amitesh Kumar",
                "Decentralized Modular Constructed Wetland (DMCW) with Reed Beds",
                "Root-zone phytoremediation using Canna indica and Vetiver grass to purify domestic greywater before reservoir entry.",
                1200000, 4, json.dumps(["Phase 1: Soil Bed Filtration Setup", "Phase 2: Biological Testing"]),
                "APPROVED", "APPROVED",
                "Dr. Amitesh Kumar", "amitesh.env@nitjsr.ac.in", "+91 98351 44520",
                "National Institute of Technology (NIT), Jamshedpur", "Tata Steel Foundation",
                "Approved for CSR Grant under Rural Sanitation Mission.", "2026-08-25T11:00:00Z",
                "2026-08-15T14:30:00Z"
            ),
            (
                "JH-HLT-2026-00019", "hei-bit-mesra", "Prof. R. N. Mukherjee",
                "Phase-Change Material (PCM) Hybrid Solar Vaccine Backpack",
                "Portable thermal carrier with telemetry alarm maintaining 2C to 8C for 72 hours in forest sub-centers.",
                2800000, 5, json.dumps(["Phase 1: Thermal chamber design", "Phase 2: Field battery telemetry"]),
                "APPROVED", "APPROVED",
                "Prof. R. N. Mukherjee", "rnmukherjee@bitmesra.ac.in", "+91 94313 55201",
                "BIT Mesra Ranchi", "Social Alpha",
                "Approved under Tribal Healthcare Innovation Fund.", "2026-08-01T09:00:00Z",
                "2026-07-25T16:00:00Z"
            )
        ]

        for sp in sample_proposals:
            cursor.execute("""
            INSERT INTO proposals (
                problem_id, hei_id, innovator_name, title, technical_abstract,
                proposed_budget, timeline_months, milestones, status, funding_status,
                contact_name, contact_email, contact_phone, hei_institution,
                funding_industry_name, funding_decision_notes, decision_date, submitted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, sp)

        cursor.execute("""
        INSERT INTO notifications (recipient_role, title, message, problem_id, proposal_id, created_at, is_read)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "INDUSTRY",
            "New Proposal Received: Nitrogen-Foam Coal Seam Fire Infiltration",
            "IIT-ISM Dhanbad submitted a Rs 35.0 Lakhs solution proposal for Problem #JH-ENV-2026-00045 (Jharia). Review proposed solution and HEI contact details.",
            "JH-ENV-2026-00045", 1, datetime.now(timezone.utc).isoformat(), 0
        ))

        cursor.execute("""
        INSERT INTO audit_logs (timestamp, actor_name, actor_role, action, problem_id, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.now(timezone.utc).isoformat(), "System", "ADMIN", "PLATFORM_INITIALIZATION", None, "Initialized SAMADHAN database with 3 stakeholder interfaces support"))
        conn.commit()

    conn.close()

# --- Helper to deserialize problem row ---
def row_to_dict(row):
    if not row:
        return None
    d = dict(row)
    for field in ["gps", "evidence_files", "ai_analysis", "govt_verification", "funding_details", "pilot_data", "deployment_data", "milestones"]:
        if field in d and d[field]:
            try:
                d[field] = json.loads(d[field])
            except Exception:
                pass
    return d

def generate_problem_id(domain):
    code = DOMAIN_CODES.get(domain, "SOC")
    year = datetime.now(timezone.utc).year
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM problems WHERE domain = ?", (domain,))
    cnt = cursor.fetchone()[0] + 1
    conn.close()
    return f"JH-{code}-{year}-{cnt:05d}"

def create_problem(data):
    conn = get_db()
    cursor = conn.cursor()

    domain = data.get("domain") or data.get("suggested_domain") or "Water Management"
    problem_id = generate_problem_id(domain)
    created_at = datetime.now(timezone.utc).isoformat()

    ai_analysis = data.get("ai_analysis")
    if not ai_analysis:
        ai_analysis = engine.full_analyze_problem(
            title=data.get("title", ""),
            description=data.get("description", ""),
            district=data.get("district", "Ranchi"),
            block=data.get("block", ""),
            panchayat=data.get("panchayat", ""),
            locality=data.get("locality", ""),
            suggested_domain=domain,
            affected_pop=data.get("affected_population", "")
        )

    cursor.execute("""
    INSERT INTO problems (
        id, title, description, district, block, panchayat, locality, gps,
        domain, subdomain, urgency_score, impact_level, affected_population,
        citizen_suggestions, evidence_files, stage, upvotes, created_at,
        reporter_name, reporter_role, similar_count, ai_analysis,
        govt_verification, funding_details, pilot_data, deployment_data
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        problem_id, data.get("title"), data.get("description"), data.get("district"),
        data.get("block"), data.get("panchayat"), data.get("locality"),
        json.dumps(data.get("gps") or [23.3441, 85.3096]),
        domain, data.get("subdomain") or ai_analysis.get("subdomain"),
        data.get("urgency_score") or ai_analysis.get("urgency_score", 50),
        data.get("impact_level") or ai_analysis.get("impact_level", "Medium"),
        data.get("affected_population"), data.get("citizen_suggestions"),
        json.dumps(data.get("evidence_files", [])),
        "CITIZEN_PROBLEM", 1, created_at,
        data.get("reporter_name", "Concerned Citizen"),
        data.get("reporter_role", "Citizen"),
        ai_analysis.get("similar_problems_count", 0),
        json.dumps(ai_analysis),
        json.dumps({}), json.dumps({}), json.dumps({}), json.dumps({})
    ))

    cursor.execute("""
    INSERT INTO audit_logs (timestamp, actor_name, actor_role, action, problem_id, details)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (created_at, data.get("reporter_name", "Citizen"), "CITIZEN", "PROBLEM_SUBMITTED", problem_id, f"Logged problem: {data.get('title')}"))

    conn.commit()
    conn.close()
    return get_problem_by_id(problem_id)

def get_problem_by_id(problem_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM problems WHERE id = ?", (problem_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    prob = row_to_dict(row)

    # Attach proposals
    cursor.execute("SELECT * FROM proposals WHERE problem_id = ? ORDER BY id DESC", (problem_id,))
    prob["proposals"] = [row_to_dict(r) for r in cursor.fetchall()]

    # Attach funding pledges
    cursor.execute("SELECT * FROM funding_pledges WHERE problem_id = ? ORDER BY id DESC", (problem_id,))
    prob["funding_pledges"] = [row_to_dict(r) for r in cursor.fetchall()]

    conn.close()
    return prob

def get_all_problems(filters=None):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM problems WHERE 1=1"
    params = []

    if filters:
        if filters.get("domain") and filters["domain"] != "all":
            query += " AND domain = ?"
            params.append(filters["domain"])
        if filters.get("district") and filters["district"] != "all":
            query += " AND district = ?"
            params.append(filters["district"])
        if filters.get("stage") and filters["stage"] != "all":
            query += " AND stage = ?"
            params.append(filters["stage"])
        if filters.get("search"):
            query += " AND (title LIKE ? OR description LIKE ? OR block LIKE ?)"
            s = f"%{filters['search']}%"
            params.extend([s, s, s])

    query += " ORDER BY urgency_score DESC, created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    results = [row_to_dict(r) for r in rows]
    conn.close()
    return results

def toggle_upvote(problem_id, user_identifier):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM upvotes WHERE problem_id = ? AND user_identifier = ?", (problem_id, user_identifier))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM upvotes WHERE id = ?", (existing[0],))
        cursor.execute("UPDATE problems SET upvotes = MAX(1, upvotes - 1) WHERE id = ?", (problem_id,))
        upvoted = False
    else:
        cursor.execute("INSERT INTO upvotes (problem_id, user_identifier, created_at) VALUES (?, ?, ?)",
                       (problem_id, user_identifier, datetime.now(timezone.utc).isoformat()))
        cursor.execute("UPDATE problems SET upvotes = upvotes + 1 WHERE id = ?", (problem_id,))
        upvoted = True

    cursor.execute("SELECT upvotes FROM problems WHERE id = ?", (problem_id,))
    new_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"success": True, "upvoted": upvoted, "upvotes": new_count}

def transition_stage(problem_id, new_stage, actor_name, actor_role, details, extra_data=None):
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()

    updates = ["stage = ?"]
    params = [new_stage]

    if extra_data:
        if "govt_verification" in extra_data:
            updates.append("govt_verification = ?")
            params.append(json.dumps(extra_data["govt_verification"]))
        if "funding_details" in extra_data:
            updates.append("funding_details = ?")
            params.append(json.dumps(extra_data["funding_details"]))
        if "pilot_data" in extra_data:
            updates.append("pilot_data = ?")
            params.append(json.dumps(extra_data["pilot_data"]))
        if "deployment_data" in extra_data:
            updates.append("deployment_data = ?")
            params.append(json.dumps(extra_data["deployment_data"]))

    params.append(problem_id)
    cursor.execute(f"UPDATE problems SET {', '.join(updates)} WHERE id = ?", params)

    cursor.execute("""
    INSERT INTO audit_logs (timestamp, actor_name, actor_role, action, problem_id, details)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (now_str, actor_name, actor_role, f"STAGE_TRANSITION_{new_stage}", problem_id, details))

    conn.commit()
    conn.close()
    return get_problem_by_id(problem_id)

def add_proposal(problem_id, hei_id, innovator_name, title, technical_abstract,
                 proposed_budget=1000000, timeline_months=6, milestones=None,
                 contact_name=None, contact_email=None, contact_phone=None, hei_institution=None):
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()

    if milestones is None:
        milestones = ["Milestone 1: Design & Lab Validation", "Milestone 2: Field Prototyping"]

    cursor.execute("""
    INSERT INTO proposals (
        problem_id, hei_id, innovator_name, title, technical_abstract,
        proposed_budget, timeline_months, milestones, status, funding_status,
        contact_name, contact_email, contact_phone, hei_institution, submitted_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'SUBMITTED', 'PENDING_REVIEW', ?, ?, ?, ?, ?)
    """, (
        problem_id, hei_id, innovator_name, title, technical_abstract,
        proposed_budget, timeline_months, json.dumps(milestones),
        contact_name or innovator_name, contact_email, contact_phone,
        hei_institution or hei_id, now_str
    ))
    proposal_id = cursor.lastrowid

    # Emit notification to INDUSTRY funding partners
    budget_lakhs = (proposed_budget or 0) / 100000
    inst_display = hei_institution or innovator_name or "HEI Team"
    cursor.execute("""
    INSERT INTO notifications (recipient_role, title, message, problem_id, proposal_id, created_at, is_read)
    VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (
        "INDUSTRY",
        f"New Proposal Received: {title[:50]}",
        f"{inst_display} submitted a Rs {budget_lakhs:.1f} Lakhs solution proposal for Problem #{problem_id}. Review proposal & contact details.",
        problem_id, proposal_id, now_str
    ))

    # Advance problem stage to HEI_INNOVATOR_PROPOSAL if earlier
    cursor.execute("SELECT stage FROM problems WHERE id = ?", (problem_id,))
    cur_row = cursor.fetchone()
    if cur_row and cur_row[0] in ["CITIZEN_PROBLEM", "AI_PROCESSING", "GOVT_VERIFICATION", "CHALLENGE_PUBLISHED"]:
        cursor.execute("UPDATE problems SET stage = 'HEI_INNOVATOR_PROPOSAL' WHERE id = ?", (problem_id,))

    cursor.execute("""
    INSERT INTO audit_logs (timestamp, actor_name, actor_role, action, problem_id, details)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (now_str, innovator_name, "HEI", "PROPOSAL_SUBMITTED", problem_id, f"Submitted proposal #{proposal_id}: {title}"))

    conn.commit()
    conn.close()
    return get_problem_by_id(problem_id)

def approve_proposal_funding(proposal_id, industry_name="Tata Steel Foundation", notes=None):
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()

    cursor.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,))
    prop = cursor.fetchone()
    if not prop:
        conn.close()
        return {"success": False, "error": "Proposal not found"}

    prop_dict = dict(prop)
    problem_id = prop_dict["problem_id"]
    budget = prop_dict.get("proposed_budget") or 1000000
    notes_text = notes or f"Approved for full CSR grant funding by {industry_name}."

    # Update proposal
    cursor.execute("""
    UPDATE proposals
    SET funding_status = 'APPROVED', status = 'APPROVED',
        funding_industry_name = ?, funding_decision_notes = ?, decision_date = ?
    WHERE id = ?
    """, (industry_name, notes_text, now_str, proposal_id))

    # Update funding pledge
    cursor.execute("""
    INSERT INTO funding_pledges (problem_id, industry_id, industry_name, pledge_amount, funding_type, notes, pledged_at)
    VALUES (?, ?, ?, ?, 'CSR_GRANT', ?, ?)
    """, (problem_id, "ind-corporate", industry_name, budget, notes_text, now_str))

    # Advance problem stage to FUNDING_ALLOCATED and update funding details
    funding_info = {
        "status": "APPROVED",
        "industry_name": industry_name,
        "committed_amount": budget,
        "sanction_date": now_str,
        "decision_notes": notes_text,
        "proposal_id": proposal_id
    }
    cursor.execute("""
    UPDATE problems
    SET stage = 'FUNDING_ALLOCATED', funding_details = ?
    WHERE id = ?
    """, (json.dumps(funding_info), problem_id))

    # Notify HEI
    cursor.execute("""
    INSERT INTO notifications (recipient_role, title, message, problem_id, proposal_id, created_at, is_read)
    VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (
        "HEI",
        f"Proposal Approved for Funding: {prop_dict['title'][:45]}",
        f"Congratulations! {industry_name} has APPROVED CSR grant of Rs {budget/100000:.1f} Lakhs for your proposal '{prop_dict['title']}'.",
        problem_id, proposal_id, now_str
    ))

    # Notify Government
    cursor.execute("""
    INSERT INTO notifications (recipient_role, title, message, problem_id, proposal_id, created_at, is_read)
    VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (
        "GOVERNMENT",
        f"Funding Sanctioned for #{problem_id}",
        f"{industry_name} approved Rs {budget/100000:.1f} Lakhs for proposal '{prop_dict['title']}'. Problem advanced to FUNDING_ALLOCATED.",
        problem_id, proposal_id, now_str
    ))

    cursor.execute("""
    INSERT INTO audit_logs (timestamp, actor_name, actor_role, action, problem_id, details)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (now_str, industry_name, "INDUSTRY", "FUNDING_APPROVED", problem_id, f"Approved funding for proposal #{proposal_id} ({budget} INR)"))

    conn.commit()
    conn.close()
    return {"success": True, "message": f"Proposal #{proposal_id} approved for funding by {industry_name}."}

def disapprove_proposal_funding(proposal_id, industry_name="Tata Steel Foundation", reason=None):
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()

    cursor.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,))
    prop = cursor.fetchone()
    if not prop:
        conn.close()
        return {"success": False, "error": "Proposal not found"}

    prop_dict = dict(prop)
    problem_id = prop_dict["problem_id"]
    reason_text = reason or "Does not align with current CSR priority guidelines or technical readiness criteria."

    cursor.execute("""
    UPDATE proposals
    SET funding_status = 'DISAPPROVED', status = 'REJECTED',
        funding_industry_name = ?, funding_decision_notes = ?, decision_date = ?
    WHERE id = ?
    """, (industry_name, reason_text, now_str, proposal_id))

    cursor.execute("""
    INSERT INTO notifications (recipient_role, title, message, problem_id, proposal_id, created_at, is_read)
    VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (
        "HEI",
        f"Proposal Funding Decision: {prop_dict['title'][:45]}",
        f"{industry_name} has declined funding for proposal '{prop_dict['title']}'. Reason: {reason_text}",
        problem_id, proposal_id, now_str
    ))

    cursor.execute("""
    INSERT INTO audit_logs (timestamp, actor_name, actor_role, action, problem_id, details)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (now_str, industry_name, "INDUSTRY", "FUNDING_DISAPPROVED", problem_id, f"Disapproved proposal #{proposal_id}: {reason_text}"))

    conn.commit()
    conn.close()
    return {"success": True, "message": f"Proposal #{proposal_id} marked as disapproved."}

def add_funding_pledge(problem_id, industry_id, industry_name, pledge_amount, funding_type="CSR_GRANT", notes=None):
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()

    cursor.execute("""
    INSERT INTO funding_pledges (problem_id, industry_id, industry_name, pledge_amount, funding_type, notes, pledged_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (problem_id, industry_id, industry_name, pledge_amount, funding_type, notes, now_str))

    cursor.execute("""
    UPDATE problems SET stage = 'FUNDING_ALLOCATED' WHERE id = ?
    """, (problem_id,))

    cursor.execute("""
    INSERT INTO audit_logs (timestamp, actor_name, actor_role, action, problem_id, details)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (now_str, industry_name, "INDUSTRY", "FUNDING_PLEDGED", problem_id, f"Pledged INR {pledge_amount} ({funding_type})"))

    conn.commit()
    conn.close()
    return get_problem_by_id(problem_id)

def get_all_proposals(funding_status=None, hei_id=None):
    conn = get_db()
    cursor = conn.cursor()
    query = """
    SELECT p.*, prob.title as problem_title, prob.domain as problem_domain,
           prob.district as problem_district, prob.stage as problem_stage
    FROM proposals p
    LEFT JOIN problems prob ON p.problem_id = prob.id
    WHERE 1=1
    """
    params = []
    if funding_status:
        query += " AND p.funding_status = ?"
        params.append(funding_status)
    if hei_id:
        query += " AND p.hei_id = ?"
        params.append(hei_id)
    query += " ORDER BY p.id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    results = [row_to_dict(r) for r in rows]
    conn.close()
    return results

def get_notifications(role=None, limit=20):
    conn = get_db()
    cursor = conn.cursor()
    if role:
        cursor.execute("""
        SELECT * FROM notifications
        WHERE recipient_role = ? OR recipient_role = 'ALL'
        ORDER BY created_at DESC LIMIT ?
        """, (role.upper(), limit))
    else:
        cursor.execute("SELECT * FROM notifications ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    results = [row_to_dict(r) for r in rows]
    conn.close()
    return results

def mark_notification_read(notif_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
    conn.commit()
    conn.close()
    return {"success": True}

# --- 3 Stakeholder Specialized Dashboards ---

def get_hei_dashboard(hei_id=None):
    conn = get_db()
    cursor = conn.cursor()

    # 1. Problem statements with raw citizen report + AI generated problem statement
    cursor.execute("""
    SELECT id, title, description, district, block, domain, urgency_score, impact_level,
           stage, ai_analysis, created_at
    FROM problems
    ORDER BY urgency_score DESC
    """)
    problem_rows = cursor.fetchall()
    problems_with_ai = []
    for r in problem_rows:
        item = row_to_dict(r)
        ai_data = item.get("ai_analysis") or {}
        item["ai_problem_statement"] = ai_data.get("structured_problem_statement") or (
            f"Develop a scalable {item.get('domain')} solution for {item.get('district')} tackling: {item.get('title')}."
        )
        item["ai_root_causes"] = ai_data.get("root_causes", [])
        item["ai_recommended_tech"] = ai_data.get("suggested_technologies", [])
        problems_with_ai.append(item)

    # 2. Proposals submitted by HEIs
    proposals_query = """
    SELECT p.*, prob.title as problem_title, prob.district as problem_district, prob.domain as problem_domain
    FROM proposals p
    LEFT JOIN problems prob ON p.problem_id = prob.id
    """
    if hei_id:
        proposals_query += " WHERE p.hei_id = ?"
        cursor.execute(proposals_query + " ORDER BY p.id DESC", (hei_id,))
    else:
        cursor.execute(proposals_query + " ORDER BY p.id DESC")
    proposals = [row_to_dict(r) for r in cursor.fetchall()]

    # 3. Project statuses for projects progressing through lifecycle
    cursor.execute("""
    SELECT id, title, domain, district, stage, funding_details, pilot_data, deployment_data
    FROM problems
    WHERE stage IN ('FUNDING_ALLOCATED', 'PROTOTYPE_DEVELOPMENT', 'LAB_DEVELOPMENT', 'TESTING_PILOT', 'LEGAL_IP_CLEARANCE', 'PROCUREMENT_READY', 'GOVT_PROCUREMENT', 'GROUND_DEPLOYMENT', 'IMPACT_MONITORING_SCALING')
    ORDER BY created_at DESC
    """)
    active_projects = [row_to_dict(r) for r in cursor.fetchall()]

    # Stats
    total_problems = len(problems_with_ai)
    total_proposals = len(proposals)
    approved_proposals = len([p for p in proposals if p.get("funding_status") == "APPROVED"])
    pending_proposals = len([p for p in proposals if p.get("funding_status") == "PENDING_REVIEW"])

    conn.close()
    return {
        "problem_statements": problems_with_ai,
        "proposals": proposals,
        "active_projects": active_projects,
        "stats": {
            "total_problem_statements": total_problems,
            "proposals_submitted": total_proposals,
            "approved_funded": approved_proposals,
            "pending_review": pending_proposals,
            "active_projects_count": len(active_projects)
        }
    }

def get_industry_dashboard(industry_name=None):
    conn = get_db()
    cursor = conn.cursor()

    # 1. Proposals for review (including complete HEI contact details)
    cursor.execute("""
    SELECT p.*, prob.title as problem_title, prob.domain as problem_domain,
           prob.district as problem_district, prob.urgency_score as problem_urgency,
           prob.stage as problem_stage, prob.description as problem_description
    FROM proposals p
    LEFT JOIN problems prob ON p.problem_id = prob.id
    ORDER BY p.funding_status ASC, p.id DESC
    """)
    all_proposals = [row_to_dict(r) for r in cursor.fetchall()]

    pending_proposals = [p for p in all_proposals if p.get("funding_status") == "PENDING_REVIEW"]
    funded_proposals = [p for p in all_proposals if p.get("funding_status") == "APPROVED"]
    disapproved_proposals = [p for p in all_proposals if p.get("funding_status") == "DISAPPROVED"]

    # 2. Notifications for industry (e.g., when new proposal arrives)
    cursor.execute("""
    SELECT * FROM notifications
    WHERE recipient_role IN ('INDUSTRY', 'ALL')
    ORDER BY created_at DESC LIMIT 15
    """)
    notifications = [row_to_dict(r) for r in cursor.fetchall()]

    total_committed = sum([p.get("proposed_budget", 0) for p in funded_proposals])

    conn.close()
    return {
        "pending_proposals": pending_proposals,
        "funded_proposals": funded_proposals,
        "disapproved_proposals": disapproved_proposals,
        "all_proposals": all_proposals,
        "notifications": notifications,
        "stats": {
            "pending_review_count": len(pending_proposals),
            "funded_count": len(funded_proposals),
            "disapproved_count": len(disapproved_proposals),
            "total_committed_funding": total_committed,
            "total_proposals": len(all_proposals)
        }
    }

def get_government_master_overview():
    conn = get_db()
    cursor = conn.cursor()

    # 1. All problem statements
    cursor.execute("""
    SELECT * FROM problems ORDER BY urgency_score DESC, created_at DESC
    """)
    all_problems = [row_to_dict(r) for r in cursor.fetchall()]

    # 2. All solutions (proposals)
    cursor.execute("""
    SELECT p.*, prob.title as problem_title, prob.domain as problem_domain,
           prob.district as problem_district, prob.stage as problem_stage
    FROM proposals p
    LEFT JOIN problems prob ON p.problem_id = prob.id
    ORDER BY p.id DESC
    """)
    all_solutions = [row_to_dict(r) for r in cursor.fetchall()]

    # 3. All project statuses
    cursor.execute("""
    SELECT id, title, domain, district, stage, urgency_score, affected_population,
           govt_verification, funding_details, pilot_data, deployment_data, created_at
    FROM problems
    ORDER BY stage ASC, created_at DESC
    """)
    all_project_statuses = [row_to_dict(r) for r in cursor.fetchall()]

    # Aggregate stats
    stage_counts = {}
    for p in all_problems:
        st = p.get("stage", "CITIZEN_PROBLEM")
        stage_counts[st] = stage_counts.get(st, 0) + 1

    total_budget_funded = sum([s.get("proposed_budget", 0) for s in all_solutions if s.get("funding_status") == "APPROVED"])

    conn.close()
    return {
        "all_problem_statements": all_problems,
        "all_solutions": all_solutions,
        "all_project_statuses": all_project_statuses,
        "stage_distribution": stage_counts,
        "stats": {
            "total_problems": len(all_problems),
            "total_solutions": len(all_solutions),
            "approved_funded_solutions": len([s for s in all_solutions if s.get("funding_status") == "APPROVED"]),
            "pending_solutions": len([s for s in all_solutions if s.get("funding_status") == "PENDING_REVIEW"]),
            "total_budget_funded": total_budget_funded,
            "active_pilots_count": stage_counts.get("TESTING_PILOT", 0),
            "ground_deployed_count": stage_counts.get("GROUND_DEPLOYMENT", 0)
        }
    }

# --- Stakeholder User Authentication ---

def register_user(user_type, username, email, password, organization=None):
    conn = get_db()
    cursor = conn.cursor()
    pw_hash = hash_pw(password)
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        cursor.execute("""
        INSERT INTO users (user_type, username, email, password_hash, organization, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_type, username, email, pw_hash, organization, created_at))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {
            "success": True,
            "message": "Registration successful",
            "user": {
                "id": user_id,
                "user_type": user_type,
                "username": username,
                "email": email,
                "organization": organization
            }
        }
    except sqlite3.IntegrityError as e:
        conn.close()
        err_msg = "Username or Email already registered." if "UNIQUE" in str(e) else str(e)
        return {"success": False, "error": err_msg}

def authenticate_user(user_type, login_identifier, password):
    conn = get_db()
    cursor = conn.cursor()
    pw_hash = hash_pw(password)

    cursor.execute("""
    SELECT * FROM users
    WHERE user_type = ? AND (username = ? OR email = ?) AND password_hash = ?
    """, (user_type, login_identifier, login_identifier, pw_hash))
    row = cursor.fetchone()
    conn.close()

    if row:
        user_dict = dict(row)
        user_dict.pop("password_hash", None)
        return {"success": True, "user": user_dict}
    return {"success": False, "error": "Invalid username/email or password for the selected role."}

def save_contact_inquiry(name, email, message):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO contact_inquiries (name, email, message, created_at)
    VALUES (?, ?, ?, ?)
    """, (name, email, message, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()
    return {"success": True}

def get_audit_trail(limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    results = [dict(r) for r in rows]
    conn.close()
    return results

def get_platform_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM problems")
    total_problems = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM problems WHERE stage != 'CITIZEN_PROBLEM'")
    verified_problems = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM proposals")
    total_proposals = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM proposals WHERE funding_status = 'APPROVED'")
    funded_solutions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM problems WHERE stage = 'TESTING_PILOT'")
    active_pilots = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM problems WHERE stage IN ('GROUND_DEPLOYMENT', 'IMPACT_MONITORING_SCALING')")
    deployed_count = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(proposed_budget) FROM proposals WHERE funding_status = 'APPROVED'")
    funded_sum = cursor.fetchone()[0] or 0.0

    conn.close()
    return {
        "total_problems": total_problems,
        "verified_problems": verified_problems,
        "total_proposals": total_proposals,
        "funded_solutions": funded_solutions,
        "active_pilots": active_pilots,
        "deployed_count": deployed_count,
        "total_committed_funding": funded_sum
    }
