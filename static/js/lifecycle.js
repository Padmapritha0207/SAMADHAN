/**
 * lifecycle.js - 15-Stage Innovation Lifecycle Controller & Specialized Stakeholder Hubs
 * Manages the complete lifecycle stepper, modal inspectors, HEI submissions, CSR pledges, and admin logs.
 */

const LIFECYCLE_STAGES_CONFIG = [
  { key: "CITIZEN_PROBLEM", name: "1. Citizen Problem", icon: "📢", desc: "Reported by community members with on-ground evidence." },
  { key: "AI_PROCESSING", name: "2. AI Processing", icon: "🤖", desc: "Domain classification, urgency scoring & duplicate detection." },
  { key: "GOVT_VERIFICATION", name: "3. Gov Verification", icon: "🏛️", desc: "Departmental nodal officer reviews AI insights & ground authenticity." },
  { key: "CHALLENGE_PUBLISHED", name: "4. Challenge Published", icon: "🚀", desc: "Formalized as official State Innovation Challenge with seed grant." },
  { key: "HEI_INNOVATOR_PROPOSAL", name: "5. HEI/Innovator Proposal", icon: "🎓", desc: "Academic researchers & startups submit technical R&D proposals." },
  { key: "INDUSTRY_SCREENING", name: "6. Industry Screening", icon: "🏭", desc: "CSR partners & venture committees screen for viability." },
  { key: "FUNDING_ALLOCATED", name: "7. Funding Allocated", icon: "💰", desc: "CSR grants or state matching funds formally released." },
  { key: "PROTOTYPE_DEVELOPMENT", name: "8. Prototype Dev", icon: "⚙️", desc: "Hardware/software lab prototype under active engineering." },
  { key: "LAB_DEVELOPMENT", name: "9. Lab Bench Testing", icon: "🔬", desc: "Standardized laboratory safety and efficacy verification." },
  { key: "TESTING_PILOT", name: "10. Testing & Pilot", icon: "🧪", desc: "Field deployment pilot in target Jharkhand community." },
  { key: "LEGAL_IP_CLEARANCE", name: "11. Legal/IP Clearance", icon: "⚖️", desc: "Patent disclosure, safety compliance & regulatory approvals." },
  { key: "PROCUREMENT_READY", name: "12. Procurement Ready", icon: "📋", desc: "Technical specifications ready for government tender." },
  { key: "GOVT_PROCUREMENT", name: "13. Govt Procurement", icon: "📑", desc: "Official purchase order / GeM portal tender awarded." },
  { key: "GROUND_DEPLOYMENT", name: "14. Ground Deployment", icon: "🌍", desc: "Permanent public installation and commissioning." },
  { key: "IMPACT_MONITORING_SCALING", name: "15. Impact & Scaling", icon: "📈", desc: "Real-time IoT telemetry, beneficiary impact tracking & statewide scaling." }
];

let activeProblemModal = null;

// --- Modal Inspection & Stepper ---
async function openProblemDetailModal(problemId) {
  try {
    const res = await fetch(`/api/problems/${problemId}`);
    if (!res.ok) throw new Error("Problem not found");
    const problem = await res.json();
    activeProblemModal = problem;
    renderProblemDetailModal(problem);
  } catch (err) {
    showToast("Failed to load problem details", "error");
  }
}

function closeProblemDetailModal() {
  const modal = document.getElementById("problemDetailModal");
  if (modal) modal.classList.add("hidden");
  activeProblemModal = null;
}

function renderProblemDetailModal(p) {
  const modal = document.getElementById("problemDetailModal");
  if (!modal) return;

  // Header Data
  document.getElementById("modalProblemId").textContent = p.id;
  document.getElementById("modalProblemTitle").textContent = p.title;
  document.getElementById("modalDomainBadge").textContent = p.domain;
  document.getElementById("modalDomainBadge").className = `text-xs font-semibold px-2.5 py-1 rounded-md border ${getDomainBadgeClass(p.domain)}`;

  const urgencyEl = document.getElementById("modalUrgencyBadge");
  urgencyEl.textContent = `Urgency: ${p.urgency_score}/100`;
  urgencyEl.className = `text-xs font-bold px-2 py-0.5 rounded border ${
    p.urgency_score >= 85 ? "bg-red-50 text-red-700 border-red-200" :
    p.urgency_score >= 65 ? "bg-amber-50 text-amber-700 border-amber-200" :
    "bg-emerald-50 text-emerald-700 border-emerald-200"
  }`;

  document.getElementById("modalLocation").textContent = `${p.locality ? p.locality + ', ' : ''}${p.block ? p.block + ', ' : ''}${p.district}`;
  document.getElementById("modalCreated").textContent = new Date(p.created_at).toLocaleDateString();
  document.getElementById("modalReporter").textContent = `${p.reporter_name} (${p.reporter_role || 'Citizen'})`;

  // Render Stepper
  renderHorizontalStepper(p.stage);

  // Render Tabs
  switchModalTab("journey");
  renderModalJourneyTab(p);
  renderModalSpecsTab(p);
  renderModalProposalsTab(p);
  renderModalFundingTab(p);
  renderModalImpactTab(p);

  // Render Role-specific action bar
  renderModalActionBar(p);

  modal.classList.remove("hidden");
}

function renderHorizontalStepper(currentStageKey) {
  const stepperContainer = document.getElementById("modalStepperScroll");
  if (!stepperContainer) return;

  let currentFound = false;
  let currentIndex = LIFECYCLE_STAGES_CONFIG.findIndex(s => s.key === currentStageKey);
  if (currentIndex === -1) currentIndex = 0;

  stepperContainer.innerHTML = LIFECYCLE_STAGES_CONFIG.map((stage, idx) => {
    const isPassed = idx < currentIndex;
    const isCurrent = idx === currentIndex;

    const nodeClass = isPassed ? "passed" : isCurrent ? "current" : "future";
    const circleBg = isPassed ? "bg-emerald-600 text-white" :
                     isCurrent ? "bg-amber-500 text-white ring-4 ring-amber-200 animate-pulse" :
                     "bg-slate-200 text-slate-500";

    return `
      <div class="lifecycle-node ${nodeClass} flex flex-col items-center">
        <div class="w-10 h-10 rounded-full ${circleBg} flex items-center justify-center font-bold text-sm mb-1.5 shadow-sm relative z-10">
          ${isPassed ? '✓' : stage.icon}
        </div>
        <div class="text-[11px] font-bold ${isCurrent ? 'text-amber-700' : isPassed ? 'text-emerald-800' : 'text-slate-400'} leading-tight">
          ${stage.name}
        </div>
        <div class="text-[9px] text-slate-400 mt-0.5 line-clamp-1">${stage.key}</div>
      </div>
    `;
  }).join("");

  // Auto-scroll stepper to current node
  setTimeout(() => {
    const currentNode = stepperContainer.querySelector(".lifecycle-node.current");
    if (currentNode) {
      stepperContainer.scrollLeft = currentNode.offsetLeft - (stepperContainer.clientWidth / 2) + 70;
    }
  }, 100);
}

function switchModalTab(tabId) {
  document.querySelectorAll(".modal-tab-pane").forEach(pane => pane.classList.add("hidden"));
  document.querySelectorAll(".modal-tab-btn").forEach(btn => {
    btn.classList.remove("border-emerald-600", "text-emerald-700", "font-bold");
    btn.classList.add("text-slate-500", "border-transparent");
  });

  const targetPane = document.getElementById(`modalTabPane-${tabId}`);
  const targetBtn = document.getElementById(`modalTabBtn-${tabId}`);

  if (targetPane) targetPane.classList.remove("hidden");
  if (targetBtn) {
    targetBtn.classList.add("border-emerald-600", "text-emerald-700", "font-bold");
    targetBtn.classList.remove("text-slate-500", "border-transparent");
  }
}

function renderModalJourneyTab(p) {
  const el = document.getElementById("modalTabPane-journey");
  if (!el) return;

  const currentCfg = LIFECYCLE_STAGES_CONFIG.find(s => s.key === p.stage) || LIFECYCLE_STAGES_CONFIG[0];

  el.innerHTML = `
    <div class="space-y-4 text-xs">
      <div class="p-4 bg-amber-50 rounded-xl border border-amber-200">
        <div class="flex items-center space-x-2 text-amber-900 font-bold text-sm mb-1">
          <span>${currentCfg.icon}</span>
          <span>Current Active Stage: ${currentCfg.name}</span>
        </div>
        <p class="text-slate-700 leading-relaxed">${currentCfg.desc}</p>
      </div>

      <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
        <h5 class="font-bold text-slate-900 mb-2">Stage Milestone Details:</h5>
        <div class="space-y-2">
          ${p.govt_verification && p.govt_verification.verified_by ? `
            <div class="p-2.5 bg-white rounded border border-slate-200">
              <span class="font-bold text-emerald-800">🏛️ Government Verification Completed:</span>
              <p class="text-slate-600 mt-1">${p.govt_verification.gov_notes}</p>
              <div class="text-[10px] text-slate-400 mt-1">Verified by: ${p.govt_verification.verified_by} on ${new Date(p.govt_verification.verified_date).toLocaleDateString()}</div>
            </div>
          ` : ''}

          ${p.funding_details && p.funding_details.sanctioned_amount ? `
            <div class="p-2.5 bg-white rounded border border-slate-200">
              <span class="font-bold text-purple-800">💰 CSR / Grant Funding Sanctioned:</span>
              <p class="text-slate-600 mt-1">Amount: <strong>₹${(p.funding_details.sanctioned_amount / 100000).toFixed(1)} Lakhs</strong> by ${p.funding_details.sponsor}</p>
            </div>
          ` : ''}

          ${p.pilot_data && p.pilot_data.pilot_location ? `
            <div class="p-2.5 bg-white rounded border border-slate-200">
              <span class="font-bold text-blue-800">🧪 Active Field Pilot:</span>
              <p class="text-slate-600 mt-1">Location: ${p.pilot_data.pilot_location} | User Satisfaction: ${p.pilot_data.satisfaction_rate || '90%+'}</p>
            </div>
          ` : ''}

          ${p.deployment_data && p.deployment_data.deployed_date ? `
            <div class="p-2.5 bg-white rounded border border-emerald-200 bg-emerald-50">
              <span class="font-bold text-emerald-900">🌍 Ground Deployment Commissioned:</span>
              <p class="text-slate-700 mt-1">Procured by: ${p.deployment_data.procuring_agency}</p>
            </div>
          ` : ''}
        </div>
      </div>
    </div>
  `;
}

function renderModalSpecsTab(p) {
  const el = document.getElementById("modalTabPane-specs");
  if (!el) return;

  const ai = p.ai_analysis || {};

  el.innerHTML = `
    <div class="space-y-4 text-xs">
      <div class="p-4 bg-white rounded-xl border border-slate-200">
        <h5 class="font-bold text-slate-900 mb-2">Original Citizen Problem Description</h5>
        <p class="text-slate-700 leading-relaxed whitespace-pre-wrap">${p.description}</p>
        ${p.citizen_suggestions ? `
          <div class="mt-3 p-2 bg-slate-50 rounded border border-slate-100 text-slate-600">
            <strong>Citizen's Suggested Solution:</strong> ${p.citizen_suggestions}
          </div>
        ` : ''}
      </div>

      <div class="p-4 bg-emerald-50 rounded-xl border border-emerald-200">
        <h5 class="font-bold text-emerald-900 mb-2 flex items-center">
          <span class="mr-1">🤖</span> AI Problem Engine Processing Output
        </h5>
        <div class="space-y-2 text-slate-800">
          <div><strong>Synthesized GovTech Problem Statement:</strong><br/>
            <span class="italic text-slate-900">"${ai.generated_problem_statement || p.title}"</span>
          </div>
          <div class="grid grid-cols-2 gap-2 pt-2">
            <div><strong>Sub-domain:</strong> ${p.subdomain || ai.subdomain || 'General'}</div>
            <div><strong>Urgency Classification:</strong> ${p.urgency_score}/100 (${p.impact_level} Impact)</div>
            <div><strong>Recommended Academic Lab:</strong> ${ai.recommended_hei || 'BIT Mesra / IIT Dhanbad'}</div>
            <div><strong>Recommended Solution Tech:</strong> ${ai.recommended_tech || 'Hardware / IoT Solution'}</div>
            <div><strong>Geographic Cluster ID:</strong> ${ai.geographic_cluster_id || 'JH-CLUSTER-RNC-01'}</div>
            <div><strong>Similar Community Reports:</strong> ${p.similar_count || 12} incidents nearby</div>
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderModalProposalsTab(p) {
  const el = document.getElementById("modalTabPane-proposals");
  if (!el) return;

  const proposals = p.proposals || [];

  el.innerHTML = `
    <div class="space-y-3 text-xs">
      <div class="flex items-center justify-between">
        <h5 class="font-bold text-slate-900">Academic & Startup Solutions (${proposals.length})</h5>
        <button onclick="openSubmitProposalModal('${p.id}')" class="px-3 py-1 bg-emerald-700 text-white rounded font-bold hover:bg-emerald-800">
          + Submit Solution Proposal
        </button>
      </div>

      ${proposals.length === 0 ? `
        <div class="p-6 text-center text-slate-400 bg-slate-50 rounded-xl border border-slate-200">
          No proposals submitted yet. Higher Education Institutions (HEIs) and Innovators are invited to propose R&D solutions.
        </div>
      ` : proposals.map(pr => `
        <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-start justify-between">
            <div>
              <h6 class="font-bold text-slate-900 text-sm">${pr.title}</h6>
              <div class="text-slate-500 mt-0.5">Submitted by: <strong>${pr.innovator_name}</strong></div>
            </div>
            <span class="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-semibold border border-blue-200">
              ${pr.status || 'SUBMITTED'}
            </span>
          </div>
          <p class="text-slate-600 mt-2">${pr.technical_abstract}</p>
          <div class="flex items-center space-x-4 mt-3 pt-2 border-t border-slate-100 text-slate-500">
            <span>Proposed Budget: <strong>₹${(pr.proposed_budget / 100000).toFixed(1)} Lakhs</strong></span>
            <span>Timeline: <strong>${pr.timeline_months} months</strong></span>
          </div>
        </div>
      `).join("")}
    </div>
  `;
}

function renderModalFundingTab(p) {
  const el = document.getElementById("modalTabPane-funding");
  if (!el) return;

  const pledges = p.funding_pledges || [];

  el.innerHTML = `
    <div class="space-y-3 text-xs">
      <div class="flex items-center justify-between">
        <h5 class="font-bold text-slate-900">Committed CSR & Grant Funding (${pledges.length})</h5>
        <button onclick="openPledgeFundingModal('${p.id}')" class="px-3 py-1 bg-amber-600 text-white rounded font-bold hover:bg-amber-700">
          + Pledge CSR / Grant
        </button>
      </div>

      ${pledges.length === 0 ? `
        <div class="p-6 text-center text-slate-400 bg-slate-50 rounded-xl border border-slate-200">
          No CSR or grant commitments yet. Industry partners and funding bodies can pledge support to accelerate this prototype.
        </div>
      ` : pledges.map(f => `
        <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-start justify-between">
            <div>
              <h6 class="font-bold text-slate-900 text-sm">${f.industry_name}</h6>
              <div class="text-slate-500 mt-0.5">Type: <strong>${f.funding_type}</strong></div>
            </div>
            <span class="text-sm font-bold text-emerald-700">
              ₹${(f.pledge_amount / 100000).toFixed(1)} Lakhs
            </span>
          </div>
          <p class="text-slate-600 mt-2">${f.notes || 'Committed under Jharkhand Sustainable Tech CSR pool.'}</p>
        </div>
      `).join("")}
    </div>
  `;
}

function renderModalImpactTab(p) {
  const el = document.getElementById("modalTabPane-impact");
  if (!el) return;

  const dep = p.deployment_data || {};
  const metrics = dep.impact_metrics || {};

  el.innerHTML = `
    <div class="space-y-4 text-xs">
      <div class="p-4 bg-white rounded-xl border border-slate-200">
        <h5 class="font-bold text-slate-900 mb-2">Target Community Impact Metrics</h5>
        <div class="grid grid-cols-2 gap-3 text-slate-700">
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
            <span class="text-slate-500">Estimated Beneficiaries:</span>
            <div class="text-base font-bold text-slate-900 mt-1">${metrics.beneficiaries || p.affected_population || '2,500+ citizens'}</div>
          </div>
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
            <span class="text-slate-500">Target Location:</span>
            <div class="text-base font-bold text-slate-900 mt-1">${p.district}, ${p.block || 'Block'}</div>
          </div>
        </div>

        ${dep.deployed_date ? `
          <div class="mt-4 p-3 bg-emerald-50 rounded-lg border border-emerald-200">
            <h6 class="font-bold text-emerald-900 mb-2">Live Real-World Operational Data</h6>
            <div class="grid grid-cols-2 gap-2">
              <div><strong>Daily Output:</strong> ${metrics.daily_liters_purified || 'Operational'}</div>
              <div><strong>System Uptime:</strong> ${metrics.uptime_percentage || '99%'}</div>
              <div><strong>Safe Quality Benchmark:</strong> ${metrics.fluoride_level_post_filter || 'Compliant'}</div>
              <div><strong>Deployed On:</strong> ${dep.deployed_date}</div>
            </div>
          </div>
        ` : `
          <div class="mt-4 p-4 text-center bg-slate-50 rounded-lg text-slate-500 border border-slate-200">
            Deployment impact metrics will be logged via IoT sensors and field verification once this solution reaches Stage 14 (Ground Deployment).
          </div>
        `}
      </div>
    </div>
  `;
}

function renderModalActionBar(p) {
  const container = document.getElementById("modalActionBar");
  if (!container) return;

  const user = AppState.currentUser || {};
  const role = user.role || "CITIZEN";

  if (role === "GOVERNMENT" || role === "ADMIN") {
    container.innerHTML = `
      <div class="flex items-center justify-between w-full">
        <div class="text-xs text-slate-600 font-medium">
          🏛️ <strong>Government Nodal Officer Controls:</strong>
        </div>
        <div class="flex items-center space-x-2">
          <select id="stageAdvanceSelect" class="text-xs border border-slate-300 rounded px-2 py-1 bg-white">
            ${LIFECYCLE_STAGES_CONFIG.map(s => `
              <option value="${s.key}" ${s.key === p.stage ? 'selected' : ''}>${s.name}</option>
            `).join("")}
          </select>
          <button onclick="advanceStageFromModal('${p.id}')" class="px-3 py-1 bg-emerald-700 text-white rounded text-xs font-bold hover:bg-emerald-800">
            Update Stage
          </button>
        </div>
      </div>
    `;
  } else if (role === "HEI" || role === "INNOVATOR") {
    container.innerHTML = `
      <div class="flex items-center justify-between w-full">
        <div class="text-xs text-slate-600">
          🎓 <strong>Academic / Innovator Actions:</strong> Submit your technical proposal or prototype test logs.
        </div>
        <button onclick="openSubmitProposalModal('${p.id}')" class="px-4 py-1.5 bg-emerald-700 text-white rounded text-xs font-bold hover:bg-emerald-800 shadow-sm">
          Submit Solution Proposal
        </button>
      </div>
    `;
  } else if (role === "INDUSTRY") {
    container.innerHTML = `
      <div class="flex items-center justify-between w-full">
        <div class="text-xs text-slate-600">
          🏭 <strong>Industry CSR Actions:</strong> Fund this societal prototype to scale ground impact.
        </div>
        <button onclick="openPledgeFundingModal('${p.id}')" class="px-4 py-1.5 bg-amber-600 text-white rounded text-xs font-bold hover:bg-amber-700 shadow-sm">
          Pledge CSR / Grant Funding
        </button>
      </div>
    `;
  } else {
    // Citizen
    container.innerHTML = `
      <div class="flex items-center justify-between w-full">
        <button onclick="toggleUpvote('${p.id}'); openProblemDetailModal('${p.id}');" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-xs font-bold">
          👍 Upvote (${p.upvotes || 1})
        </button>
        <button onclick="closeProblemDetailModal()" class="px-4 py-1.5 bg-slate-800 text-white rounded text-xs font-bold hover:bg-slate-900">
          Done
        </button>
      </div>
    `;
  }
}

async function advanceStageFromModal(problemId) {
  const select = document.getElementById("stageAdvanceSelect");
  if (!select) return;
  const newStage = select.value;

  try {
    const res = await fetch(`/api/problems/${problemId}/transition`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        stage: newStage,
        notes: `Advanced to ${newStage} by Authorized Government Officer.`
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Problem advanced to ${newStage}`, "success");
      await loadProblems();
      await loadStats();
      openProblemDetailModal(problemId);
    }
  } catch (err) {
    showToast("Failed to transition stage", "error");
  }
}

// --- Proposal Submission Modal ---
function openSubmitProposalModal(problemId) {
  const modal = document.getElementById("proposalSubmitModal");
  if (!modal) return;
  document.getElementById("propProblemId").value = problemId;
  modal.classList.remove("hidden");
}

function closeProposalModal() {
  const modal = document.getElementById("proposalSubmitModal");
  if (modal) modal.classList.add("hidden");
}

async function handleProposalSubmit(e) {
  e.preventDefault();
  const problemId = document.getElementById("propProblemId").value;
  const title = document.getElementById("propTitle").value.trim();
  const technical_abstract = document.getElementById("propAbstract").value.trim();
  const proposed_budget = document.getElementById("propBudget").value;
  const timeline_months = document.getElementById("propTimeline").value;

  try {
    const res = await fetch(`/api/problems/${problemId}/proposals`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        technical_abstract,
        proposed_budget: parseFloat(proposed_budget),
        timeline_months: parseInt(timeline_months)
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast("Solution proposal successfully submitted to JHAR-SOLVE!", "success");
      closeProposalModal();
      await loadProblems();
      await loadStats();
      openProblemDetailModal(problemId);
    } else {
      showToast(data.error || "Submission failed", "error");
    }
  } catch (err) {
    showToast("Error submitting proposal", "error");
  }
}

// --- Funding Pledge Modal ---
function openPledgeFundingModal(problemId) {
  const modal = document.getElementById("fundingPledgeModal");
  if (!modal) return;
  document.getElementById("fundProblemId").value = problemId;
  modal.classList.remove("hidden");
}

function closeFundingModal() {
  const modal = document.getElementById("fundingPledgeModal");
  if (modal) modal.classList.add("hidden");
}

async function handleFundingSubmit(e) {
  e.preventDefault();
  const problemId = document.getElementById("fundProblemId").value;
  const industry_name = document.getElementById("fundIndustryName").value.trim();
  const pledge_amount = document.getElementById("fundAmount").value;
  const funding_type = document.getElementById("fundType").value;
  const notes = document.getElementById("fundNotes").value.trim();

  try {
    const res = await fetch(`/api/problems/${problemId}/fund`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        industry_name,
        pledge_amount: parseFloat(pledge_amount),
        funding_type,
        notes
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast("CSR / Grant funding committed successfully!", "success");
      closeFundingModal();
      await loadProblems();
      await loadStats();
      openProblemDetailModal(problemId);
    } else {
      showToast(data.error || "Pledge failed", "error");
    }
  } catch (err) {
    showToast("Error committing funds", "error");
  }
}

// --- Dedicated Hub Renderers ---
function renderHEIHub() {
  const container = document.getElementById("heiChallengesList");
  if (!container) return;

  const challenges = AppState.problems.filter(p =>
    p.stage === "CHALLENGE_PUBLISHED" || p.stage === "HEI_INNOVATOR_PROPOSAL" || p.stage === "INDUSTRY_SCREENING"
  );

  container.innerHTML = challenges.length === 0 ? `
    <div class="col-span-full p-8 text-center bg-slate-50 rounded-xl text-slate-500">
      No open academic challenges right now.
    </div>
  ` : challenges.map(p => `
    <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold px-2 py-0.5 rounded border ${getDomainBadgeClass(p.domain)}">${p.domain}</span>
          <span class="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">R&D Grant Eligible</span>
        </div>
        <h4 class="text-sm font-bold text-slate-900 mb-1 cursor-pointer hover:text-emerald-700" onclick="openProblemDetailModal('${p.id}')">
          ${p.title}
        </h4>
        <p class="text-xs text-slate-600 mb-3 line-clamp-3">${p.description}</p>
        <div class="p-2.5 bg-slate-50 rounded-lg text-xs text-slate-700 mb-3">
          <strong>Recommended Lab:</strong> ${(p.ai_analysis && p.ai_analysis.recommended_lab) || 'Engineering R&D'}<br/>
          <strong>Key Tech:</strong> ${(p.ai_analysis && p.ai_analysis.recommended_tech) || 'CleanTech / IoT'}
        </div>
      </div>
      <div class="flex items-center justify-between pt-2 border-t border-slate-100">
        <span class="text-xs text-slate-500">Proposals: ${p.proposals ? p.proposals.length : 0}</span>
        <button onclick="openSubmitProposalModal('${p.id}')" class="px-3 py-1 bg-emerald-700 text-white rounded text-xs font-bold hover:bg-emerald-800">
          Propose Solution
        </button>
      </div>
    </div>
  `).join("");
}

function renderIndustryHub() {
  const container = document.getElementById("industryProjectsList");
  if (!container) return;

  const projects = AppState.problems.filter(p =>
    p.stage === "INDUSTRY_SCREENING" || p.stage === "FUNDING_ALLOCATED" || p.stage === "PROTOTYPE_DEVELOPMENT"
  );

  container.innerHTML = projects.length === 0 ? `
    <div class="col-span-full p-8 text-center bg-slate-50 rounded-xl text-slate-500">
      No projects under CSR screening right now.
    </div>
  ` : projects.map(p => `
    <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold px-2 py-0.5 rounded border ${getDomainBadgeClass(p.domain)}">${p.domain}</span>
          <span class="text-xs font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded">CSR Match Eligible</span>
        </div>
        <h4 class="text-sm font-bold text-slate-900 mb-1 cursor-pointer hover:text-emerald-700" onclick="openProblemDetailModal('${p.id}')">
          ${p.title}
        </h4>
        <p class="text-xs text-slate-600 mb-3 line-clamp-3">${p.description}</p>
        <div class="p-2.5 bg-purple-50/60 rounded-lg text-xs text-slate-700 mb-3 border border-purple-100">
          <strong>Target Beneficiaries:</strong> ${p.affected_population || '1,000+ citizens'}<br/>
          <strong>SDG Goals:</strong> SDG 3 (Health), SDG 6 (Clean Water), SDG 9 (Innovation)
        </div>
      </div>
      <div class="flex items-center justify-between pt-2 border-t border-slate-100">
        <span class="text-xs text-slate-500">Pledged: ₹${p.funding_details && p.funding_details.sanctioned_amount ? (p.funding_details.sanctioned_amount/100000).toFixed(1) + ' L' : '0'}</span>
        <button onclick="openPledgeFundingModal('${p.id}')" class="px-3 py-1 bg-amber-600 text-white rounded text-xs font-bold hover:bg-amber-700">
          Pledge CSR Fund
        </button>
      </div>
    </div>
  `).join("");
}

async function renderAdminCenter() {
  const container = document.getElementById("adminAuditList");
  if (!container) return;

  try {
    const res = await fetch("/api/audit-trail?limit=25");
    const data = await res.json();
    const logs = data.logs || [];

    container.innerHTML = logs.map(l => `
      <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
        <td class="p-3 text-slate-500 font-mono">${new Date(l.timestamp).toLocaleTimeString()}</td>
        <td class="p-3 font-semibold text-slate-800">${l.actor_name} (${l.actor_role})</td>
        <td class="p-3"><span class="px-2 py-0.5 rounded bg-slate-100 text-slate-800 font-mono text-[11px]">${l.action}</span></td>
        <td class="p-3 font-mono text-emerald-700">${l.problem_id || '—'}</td>
        <td class="p-3 text-slate-600 truncate max-w-xs">${l.details}</td>
      </tr>
    `).join("");
  } catch (err) {
    console.error("Failed to load audit trail:", err);
  }
}
