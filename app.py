"""
app.py - SAMADHAN Flask Application Entrypoint & REST API
Jharkhand Societal Innovation Lifecycle Platform
"""

import os
import json
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template, session, send_from_directory
from werkzeug.utils import secure_filename

import database
import seed_data
from ai_engine import engine
from i18n import TRANSLATIONS, get_text

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "samadhan-govtech-innov-jharkhand-2026-secret-key"

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "mp4"}
MAX_CONTENT_LENGTH = 25 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure database is initialized with tables and seeds on server start
database.init_db()

# Demo User Personas
PERSONAS = {
    "citizen": {
        "id": "usr-cit-01",
        "name": "Ramesh Soren",
        "role": "CITIZEN",
        "org": "Hesal Gram Panchayat, Angara",
        "district": "Ranchi",
        "badge": "Community Reporter"
    },
    "government": {
        "id": "usr-gov-01",
        "name": "Er. Alok Sharma",
        "role": "GOVERNMENT",
        "org": "Dept. of Drinking Water & Sanitation",
        "district": "Statewide / Ranchi HQ",
        "badge": "Chief Engineer & Nodal Officer"
    },
    "hei": {
        "id": "usr-hei-01",
        "name": "Prof. R. N. Mukherjee",
        "role": "HEI",
        "org": "BIT Mesra, Ranchi",
        "district": "Ranchi",
        "badge": "Dean R&D / Innovation Lead"
    },
    "innovator": {
        "id": "usr-inn-01",
        "name": "Pooja Besra",
        "role": "INNOVATOR",
        "org": "JharJal CleanTech Startup",
        "district": "Ranchi / Bokaro",
        "badge": "Grassroots Hardware Innovator"
    },
    "industry": {
        "id": "usr-ind-01",
        "name": "Rajeev Singhal",
        "role": "INDUSTRY",
        "org": "Tata Steel Foundation (CSR)",
        "district": "East Singhbhum (Jamshedpur)",
        "badge": "CSR Head - Impact Investments"
    },
    "admin": {
        "id": "usr-adm-01",
        "name": "State Mission Director",
        "role": "ADMIN",
        "org": "Jharkhand State Technology Mission",
        "district": "Government Secretariat, Ranchi",
        "badge": "State Super Administrator"
    }
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def setup_session_user():
    if "user" not in session:
        session["user"] = PERSONAS["citizen"]
    if "lang" not in session:
        session["lang"] = "en"

# --- Frontend Page ---
@app.route("/")
def index():
    return render_template("index.html")

# --- I18N API ---
@app.route("/api/i18n/<lang>")
def get_i18n(lang):
    if lang not in TRANSLATIONS:
        lang = "en"
    session["lang"] = lang
    return jsonify({
        "lang": lang,
        "strings": TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    })

# --- User Persona Switcher & Current User ---
@app.route("/api/auth/current-user", methods=["GET"])
def current_user():
    return jsonify({
        "user": session.get("user", PERSONAS["citizen"]),
        "personas": PERSONAS
    })

@app.route("/api/auth/switch-role", methods=["POST"])
def switch_role():
    data = request.get_json() or {}
    role_key = data.get("role_key", "citizen").lower()
    if role_key in PERSONAS:
        session["user"] = PERSONAS[role_key]
        return jsonify({"success": True, "user": session["user"]})
    return jsonify({"error": "Invalid persona key"}), 400

# --- Stakeholder Register & Login APIs ---
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    user_type = data.get("user_type", "STUDENT_HEI") # STUDENT_HEI, INDUSTRY, GOVERNMENT
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    org = data.get("organization", "").strip()

    if not username or len(username) < 3:
        return jsonify({"success": False, "error": "Username must be at least 3 characters."}), 400
    if not email or "@" not in email:
        return jsonify({"success": False, "error": "A valid email address is required."}), 400
    if not password or len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters."}), 400

    res = database.register_user(user_type, username, email, password, org)
    if res["success"]:
        # Map user type to persona role
        role_map = {
            "STUDENT_HEI": ("HEI", "Research Scholar / Faculty"),
            "INDUSTRY": ("INDUSTRY", "Corporate CSR Partner"),
            "GOVERNMENT": ("GOVERNMENT", "Government Officer")
        }
        role, badge = role_map.get(user_type, ("CITIZEN", "Registered Member"))
        session["user"] = {
            "id": f"usr-{res['user']['id']}",
            "name": username,
            "role": role,
            "org": org or "SAMADHAN Stakeholder Network",
            "district": "Jharkhand",
            "badge": badge
        }
        res["active_user"] = session["user"]
        return jsonify(res), 201
    return jsonify(res), 400

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    user_type = data.get("user_type", "STUDENT_HEI")
    login_id = data.get("login_identifier", "").strip()
    password = data.get("password", "").strip()

    if not login_id or not password:
        return jsonify({"success": False, "error": "Username/Email and Password are required."}), 400

    res = database.authenticate_user(user_type, login_id, password)
    if res["success"]:
        role_map = {
            "STUDENT_HEI": ("HEI", "Research Scholar / Faculty"),
            "INDUSTRY": ("INDUSTRY", "Corporate CSR Partner"),
            "GOVERNMENT": ("GOVERNMENT", "Government Officer")
        }
        role, badge = role_map.get(user_type, ("CITIZEN", "Registered Member"))
        session["user"] = {
            "id": f"usr-{res['user']['id']}",
            "name": res["user"]["username"],
            "role": role,
            "org": res["user"]["organization"] or "SAMADHAN Stakeholder",
            "district": "Jharkhand",
            "badge": badge
        }
        res["active_user"] = session["user"]
        return jsonify(res)
    return jsonify(res), 401

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session["user"] = PERSONAS["citizen"]
    return jsonify({"success": True, "user": session["user"]})

# --- Contact Inquiry API ---
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Please provide your name, email, and message."}), 400

    database.save_contact_inquiry(name, email, message)
    return jsonify({"success": True, "message": "Your inquiry has been logged. Our nodal team will get back to you shortly."})

# --- Trends, Projects, Solutions & Achievements APIs ---
@app.route("/api/trends", methods=["GET"])
def get_trends():
    return jsonify(seed_data.JHARKHAND_TRENDS)

@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify(seed_data.JHARKHAND_EXISTING_PROJECTS)

@app.route("/api/solutions", methods=["GET"])
def get_solutions():
    return jsonify(seed_data.JHARKHAND_SOLUTIONS)

@app.route("/api/achievements", methods=["GET"])
def get_achievements():
    return jsonify(seed_data.JHARKHAND_ACHIEVEMENTS)

# --- Locations Cascading API ---
@app.route("/api/locations", methods=["GET"])
def get_locations():
    return jsonify(seed_data.JHARKHAND_LOCATIONS)

@app.route("/api/heis", methods=["GET"])
def get_heis():
    return jsonify(seed_data.JHARKHAND_HEIS)

@app.route("/api/industries", methods=["GET"])
def get_industries():
    return jsonify(seed_data.JHARKHAND_INDUSTRIES)

# --- AI Live Preview Endpoint ---
@app.route("/api/ai/analyze", methods=["POST"])
def live_ai_analyze():
    data = request.get_json() or {}
    title = data.get("title", "")
    description = data.get("description", "")
    district = data.get("district", "Ranchi")
    block = data.get("block", "")
    panchayat = data.get("panchayat", "")
    locality = data.get("locality", "")
    suggested_domain = data.get("suggested_domain", "")
    affected_pop = data.get("affected_population", "")

    if not title and not description:
        return jsonify({"error": "Title or description required"}), 400

    analysis = engine.full_analyze_problem(
        title=title,
        description=description,
        district=district,
        block=block,
        panchayat=panchayat,
        locality=locality,
        suggested_domain=suggested_domain,
        affected_pop=affected_pop
    )
    return jsonify(analysis)

# --- Problems CRUD & Filtering ---
@app.route("/api/problems", methods=["GET"])
def list_problems():
    filters = {
        "district": request.args.get("district"),
        "domain": request.args.get("domain"),
        "stage": request.args.get("stage"),
        "search": request.args.get("search")
    }
    problems = database.get_all_problems(filters)
    return jsonify({"count": len(problems), "problems": problems})

@app.route("/api/problems/<problem_id>", methods=["GET"])
def get_single_problem(problem_id):
    problem = database.get_problem_by_id(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404
    return jsonify(problem)

@app.route("/api/problems", methods=["POST"])
def report_problem():
    if request.is_json:
        data = request.get_json()
        evidence_files = []
    else:
        data = request.form.to_dict()
        evidence_files = []
        if "evidence_files" in request.files:
            files = request.files.getlist("evidence_files")
            for f in files:
                if f and allowed_file(f.filename):
                    fname = secure_filename(f.filename)
                    timestamp_prefix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
                    stored_name = f"{timestamp_prefix}_{fname}"
                    f.save(os.path.join(app.config["UPLOAD_FOLDER"], stored_name))
                    evidence_files.append(stored_name)

    if not data.get("title") or len(data.get("title", "").strip()) < 5:
        return jsonify({"error": "Problem title must be at least 5 characters long."}), 400
    if not data.get("description") or len(data.get("description", "").strip()) < 10:
        return jsonify({"error": "Detailed description must be at least 10 characters long."}), 400
    if not data.get("district"):
        return jsonify({"error": "Please select a Jharkhand district."}), 400

    cur_user = session.get("user", PERSONAS["citizen"])
    data["evidence_files"] = evidence_files
    data["reporter_name"] = cur_user.get("name", "Concerned Citizen")
    data["reporter_role"] = cur_user.get("role", "CITIZEN")

    new_problem = database.create_problem(data)
    all_problems = database.get_all_problems()
    engine.update_corpus(all_problems)

    return jsonify({
        "success": True,
        "message": f"Problem successfully logged under ID {new_problem['id']}",
        "problem": new_problem
    }), 201

@app.route("/api/problems/<problem_id>/upvote", methods=["POST"])
def upvote_problem(problem_id):
    user_id = session.get("user", {}).get("id", request.remote_addr or "anon")
    res = database.toggle_upvote(problem_id, user_id)
    return jsonify(res)

@app.route("/api/problems/<problem_id>/verify", methods=["POST"])
def verify_problem(problem_id):
    cur_user = session.get("user", {})
    if cur_user.get("role") not in ["GOVERNMENT", "ADMIN"]:
        actor_name = cur_user.get("name", "Er. Alok Sharma (Acting Officer)")
        actor_role = "GOVERNMENT"
    else:
        actor_name = cur_user.get("name")
        actor_role = cur_user.get("role")

    data = request.get_json() or {}
    notes = data.get("gov_notes", "Verified on-ground validity by Departmental Committee. Approved as official State Innovation Challenge.")
    grant_amount = float(data.get("challenge_grant_sanctioned", 2000000))

    extra_data = {
        "govt_verification": {
            "verified_by": actor_name,
            "verified_role": actor_role,
            "verified_date": datetime.now(timezone.utc).isoformat(),
            "challenge_grant_sanctioned": grant_amount,
            "gov_notes": notes
        }
    }

    updated = database.transition_stage(
        problem_id=problem_id,
        new_stage="CHALLENGE_PUBLISHED",
        actor_name=actor_name,
        actor_role=actor_role,
        details=notes,
        extra_data=extra_data
    )
    return jsonify({"success": True, "problem": updated})

@app.route("/api/problems/<problem_id>/transition", methods=["POST"])
def transition_problem_stage(problem_id):
    cur_user = session.get("user", PERSONAS["government"])
    data = request.get_json() or {}
    new_stage = data.get("stage")
    notes = data.get("notes", f"Advanced to {new_stage}")
    extra_data = data.get("extra_data", {})

    if not new_stage:
        return jsonify({"error": "New stage is required"}), 400

    try:
        updated = database.transition_stage(
            problem_id=problem_id,
            new_stage=new_stage,
            actor_name=cur_user.get("name", "Authorized Officer"),
            actor_role=cur_user.get("role", "GOVERNMENT"),
            details=notes,
            extra_data=extra_data
        )
        return jsonify({"success": True, "problem": updated})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/problems/<problem_id>/proposals", methods=["POST"])
def submit_proposal(problem_id):
    cur_user = session.get("user", PERSONAS["hei"])
    data = request.get_json() or {}

    title = data.get("title")
    technical_abstract = data.get("technical_abstract", "")
    proposed_budget = float(data.get("proposed_budget", 1000000))
    timeline_months = int(data.get("timeline_months", 6))
    innovator_name = data.get("innovator_name") or cur_user.get("name", "HEI Research Team")
    hei_id = data.get("hei_id", "hei-bit-mesra")
    contact_name = data.get("contact_name") or innovator_name
    contact_email = data.get("contact_email") or cur_user.get("email", "contact@hei.ac.in")
    contact_phone = data.get("contact_phone", "+91 94311 00000")
    hei_institution = data.get("hei_institution") or cur_user.get("org", "Higher Education Institution")
    milestones = data.get("milestones")

    if not title or len(title.strip()) < 5:
        return jsonify({"error": "Proposal title is required (min 5 chars)"}), 400

    updated = database.add_proposal(
        problem_id=problem_id,
        hei_id=hei_id,
        innovator_name=innovator_name,
        title=title,
        technical_abstract=technical_abstract,
        proposed_budget=proposed_budget,
        timeline_months=timeline_months,
        milestones=milestones,
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
        hei_institution=hei_institution
    )
    return jsonify({"success": True, "message": "Proposal submitted successfully! Industry partners have been notified.", "problem": updated})

@app.route("/api/proposals", methods=["POST"])
def create_proposal():
    cur_user = session.get("user", PERSONAS["hei"])
    data = request.get_json() or {}

    problem_id = data.get("problem_id")
    if not problem_id:
        return jsonify({"error": "problem_id is required"}), 400

    title = data.get("title", "").strip()
    if not title or len(title) < 5:
        return jsonify({"error": "Proposal title must be at least 5 characters long."}), 400

    technical_abstract = data.get("technical_abstract", "").strip()
    if not technical_abstract or len(technical_abstract) < 10:
        return jsonify({"error": "Technical abstract must be at least 10 characters."}), 400

    proposed_budget = float(data.get("proposed_budget", 1000000))
    timeline_months = int(data.get("timeline_months", 6))
    innovator_name = data.get("innovator_name") or cur_user.get("name", "HEI Research Lead")
    hei_id = data.get("hei_id", "hei-bit-mesra")
    contact_name = data.get("contact_name") or innovator_name
    contact_email = data.get("contact_email") or cur_user.get("email", "contact@hei.ac.in")
    contact_phone = data.get("contact_phone", "+91 94311 00000")
    hei_institution = data.get("hei_institution") or cur_user.get("org", "Higher Education Institution")
    milestones = data.get("milestones")

    updated = database.add_proposal(
        problem_id=problem_id,
        hei_id=hei_id,
        innovator_name=innovator_name,
        title=title,
        technical_abstract=technical_abstract,
        proposed_budget=proposed_budget,
        timeline_months=timeline_months,
        milestones=milestones,
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
        hei_institution=hei_institution
    )
    return jsonify({
        "success": True,
        "message": f"Proposal '{title}' submitted successfully! Industry partners have been notified.",
        "problem": updated
    }), 201

# --- HEI Interface API ---
@app.route("/api/hei/dashboard", methods=["GET"])
def hei_dashboard():
    cur_user = session.get("user", {})
    hei_id = request.args.get("hei_id") or (cur_user.get("id") if cur_user.get("role") == "HEI" else None)
    data = database.get_hei_dashboard(hei_id)
    return jsonify(data)

# --- Industry Interface APIs ---
@app.route("/api/industry/dashboard", methods=["GET"])
def industry_dashboard():
    cur_user = session.get("user", {})
    industry_name = request.args.get("industry_name") or (cur_user.get("org") if cur_user.get("role") == "INDUSTRY" else "Tata Steel Foundation")
    data = database.get_industry_dashboard(industry_name)
    return jsonify(data)

@app.route("/api/proposals/<int:proposal_id>/approve", methods=["POST"])
def approve_proposal(proposal_id):
    cur_user = session.get("user", PERSONAS["industry"])
    data = request.get_json() or {}
    industry_name = data.get("industry_name") or cur_user.get("org", "Tata Steel Foundation")
    notes = data.get("notes", "Funding approved under CSR Innovation Grant.")

    res = database.approve_proposal_funding(proposal_id, industry_name, notes)
    if res.get("success"):
        return jsonify(res)
    return jsonify(res), 400

@app.route("/api/proposals/<int:proposal_id>/disapprove", methods=["POST"])
def disapprove_proposal(proposal_id):
    cur_user = session.get("user", PERSONAS["industry"])
    data = request.get_json() or {}
    industry_name = data.get("industry_name") or cur_user.get("org", "Tata Steel Foundation")
    reason = data.get("reason", "Proposal does not align with current corporate CSR guidelines.")

    res = database.disapprove_proposal_funding(proposal_id, industry_name, reason)
    if res.get("success"):
        return jsonify(res)
    return jsonify(res), 400

# --- Notifications API ---
@app.route("/api/notifications", methods=["GET"])
def list_notifications():
    role = request.args.get("role")
    notifs = database.get_notifications(role)
    return jsonify(notifs)

@app.route("/api/notifications/<int:notif_id>/read", methods=["POST"])
def mark_notification_read(notif_id):
    res = database.mark_notification_read(notif_id)
    return jsonify(res)

# --- Government Interface API ---
@app.route("/api/government/master", methods=["GET"])
def government_master():
    data = database.get_government_master_overview()
    return jsonify(data)

@app.route("/api/problems/<problem_id>/fund", methods=["POST"])
def pledge_funding(problem_id):
    cur_user = session.get("user", PERSONAS["industry"])
    data = request.get_json() or {}

    industry_name = data.get("industry_name") or cur_user.get("org", "Tata Steel Foundation")
    industry_id = data.get("industry_id", "ind-tata-steel")
    amount = float(data.get("pledge_amount", 1500000))
    funding_type = data.get("funding_type", "CSR_GRANT")
    notes = data.get("notes", "Pledge committed under FY2026 CSR Sustainable Development Grant pool.")

    updated = database.add_funding_pledge(
        problem_id=problem_id,
        industry_id=industry_id,
        industry_name=industry_name,
        pledge_amount=amount,
        funding_type=funding_type,
        notes=notes
    )
    return jsonify({"success": True, "problem": updated})

@app.route("/api/stats", methods=["GET"])
def platform_stats():
    stats = database.get_platform_stats()
    return jsonify(stats)

@app.route("/api/audit-trail", methods=["GET"])
def audit_trail():
    limit = int(request.args.get("limit", 50))
    logs = database.get_audit_trail(limit)
    return jsonify({"count": len(logs), "logs": logs})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting SAMADHAN on http://0.0.0.0:{port} ...")
    app.run(host="0.0.0.0", port=port, debug=False)
