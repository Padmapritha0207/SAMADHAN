# SAMADHAN: Jharkhand Societal Innovation Lifecycle Platform

> **Official Name**: SAMADHAN (समाधान)  
> **Tagline**: From Citizen Problems to Government-Deployed Solutions  
> **Motto**: Problem → Innovation → Impact  
> **Jurisdiction**: State Innovation & Technology Mission, Department of Higher & Technical Education, Government of Jharkhand  
> **Academic Consortium**: BIT Mesra · IIT (ISM) Dhanbad · NIT Jamshedpur · Birsa Agricultural University · AIIMS Deoghar · Ranchi University  

---

## 1. Product Vision & Architecture

**SAMADHAN** is an institutional GovTech and societal innovation collaboration platform engineered for Jharkhand. Unlike conventional complaint/grievance portals that merely record and close complaints, SAMADHAN transforms verified real-world community problems into structured innovation opportunities and manages their complete 15-stage lifecycle.

### The 15-Stage Innovation Lifecycle:
```
1. Citizen Problem
   ↓
2. AI Processing (Domain, Urgency, Duplicate Detection)
   ↓
3. Government Verification (Human-in-the-loop Governance)
   ↓
4. Challenge Published (Official State Innovation Challenge)
   ↓
5. HEI / Innovator Proposal (Academic & Startup Solutions)
   ↓
6. Industry Screening (Feasibility, ESG & SDG alignment)
   ↓
7. Funding Allocated (CSR Grants & State Matching Funds)
   ↓
8. Prototype Development (Hardware/Software Engineering)
   ↓
9. Lab Bench Development (Standardized Testing)
   ↓
10. Testing & Pilot (Field Trials in Jharkhand Districts)
   ↓
11. Legal / IP Clearance (Patents, Safety & Regulatory Clearances)
   ↓
12. Procurement Readiness (GeM Specifications & BOM)
   ↓
13. Government Procurement (Tender Awarded)
   ↓
14. Ground Deployment (Permanent Public Installation)
   ↓
15. Impact Monitoring & Scaling (IoT Telemetry & Statewide Expansion)
```

---

## 2. Four Stakeholder Ecosystems & 6 Roles

1. **Citizens**: Mobile-first 5-step wizard, community upvoting, real-time lifecycle tracking (`JH-[DOM]-2026-XXXXX`).
2. **Government Departments**: Innovation Command Center, AI verification queue, Leaflet GIS heatmap across 24 Jharkhand districts, pilot sanctions, tender awards.
3. **Higher Education Institutions (HEIs)**: BIT Mesra, IIT (ISM) Dhanbad, NIT Jamshedpur, Birsa Agricultural University, AIIMS Deoghar, Ranchi University.
4. **Innovators & Grassroots Startups**: Prototyping hardware, lab bench testing, field pilots.
5. **Industry & CSR Funding Partners**: Tata Steel Foundation, Bokaro Steel (SAIL CSR), Coal India / BCCL, Social Alpha, Jharkhand Innovation Lab.
6. **Platform Administrators**: Audit logs, KYC verification, master data management, system health.

---

## 3. Citizen Experience & 5-Step Reporting Wizard

- **Step 1 — Problem**: Title, detailed description, suggested category, **"✨ Live AI Preview"** button.
- **Step 2 — Location**: Cascading dropdowns across all **24 Jharkhand Districts** → Blocks → Panchayats → Localities with GPS coordinate capture.
- **Step 3 — Evidence**: Photos, documents (PDF), and videos (MP4) with client and server file validation (<10MB photos/docs, <25MB video).
- **Step 4 — Feedback & Context**: Estimated affected population, urgency rationale, citizen suggestions.
- **Step 5 — Review & Confirmation**: Summary verification, terms confirmation, and instant ID generation (e.g., `JH-WTR-2026-00124`).

---

## 4. AI Problem Engine & Governance Guardrails

- **10 GovTech Domains**: Water Management, Healthcare, Agriculture, Sanitation, Environment, Education, Accessibility, Urban Infrastructure, Rural Livelihoods, Public Service Delivery.
- **Automated Capabilities**:
  - Domain & Sub-domain classification with confidence scoring
  - GovTech Problem Statement synthesis
  - Vector TF-IDF cosine similarity duplicate & cluster detection
  - Urgency scoring (0–100) based on vulnerability and population scale
  - Automated HEI expertise and research lab matching
- **Assisted Intelligence Governance**: AI assists decision-making, but all official challenge publications, grant sanctions, and procurement decisions require authorized departmental human approvals.

---

## 5. Bilingual i18n Architecture

- Native English & Hindi (`हिन्दी`) translation dictionaries.
- Instant toggle with zero UI flicker.
- Extensible architecture ready for regional tribal languages (Santali, Ho, Bengali, Mundari).

---

## 6. How to Run

### Requirements:
- Python 3.10+ (Tested on Python 3.14)
- Dependencies installed: `Flask`, `scikit-learn`, `pandas`, `numpy`, `scipy`

### Starting the Server:
```powershell
cd C:\Users\oviya\.gemini\antigravity\scratch\jhar-solve
python app.py
```
Open your browser at: `http://127.0.0.1:5000`

### Running the Test Suite:
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```
