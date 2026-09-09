/**
 * citizen_wizard.js - 5-Step Citizen Reporting Wizard for JHAR-SOLVE
 * Includes cascading location selectors, file validation, live AI preview, and standard ID generation.
 */

let wizardCurrentStep = 1;
const wizardFormData = {
  title: "",
  description: "",
  suggested_domain: "",
  district: "",
  block: "",
  panchayat: "",
  locality: "",
  gps: "",
  affected_population: "",
  urgency_rationale: "",
  citizen_suggestions: "",
  evidence_files: []
};

document.addEventListener("DOMContentLoaded", () => {
  setupWizardLocationCascading();
  setupWizardNavigation();
  setupEvidenceUpload();
  setupLiveAIPreview();
});

function resetWizard() {
  wizardCurrentStep = 1;
  const form = document.getElementById("citizenWizardForm");
  if (form) form.reset();
  wizardFormData.evidence_files = [];
  updateFilePreviewList();
  updateWizardStepUI();
  const liveCard = document.getElementById("wizardLiveAiCard");
  if (liveCard) liveCard.classList.add("hidden");
}

function setupWizardLocationCascading() {
  const districtSelect = document.getElementById("wizardDistrict");
  const blockSelect = document.getElementById("wizardBlock");
  const panchayatSelect = document.getElementById("wizardPanchayat");

  if (!districtSelect || !blockSelect || !panchayatSelect) return;

  districtSelect.addEventListener("change", (e) => {
    const district = e.target.value;
    blockSelect.innerHTML = '<option value="">Select Block</option>';
    panchayatSelect.innerHTML = '<option value="">Select Panchayat</option>';
    panchayatSelect.disabled = true;

    if (district && AppState.locations[district]) {
      const blocks = Object.keys(AppState.locations[district].blocks).sort();
      blocks.forEach(b => {
        const opt = document.createElement("option");
        opt.value = b;
        opt.textContent = b;
        blockSelect.appendChild(opt);
      });
      blockSelect.disabled = false;

      // Auto set representative GPS coordinates
      const locData = AppState.locations[district];
      const gpsInput = document.getElementById("wizardGps");
      if (gpsInput && locData.lat && locData.lng) {
        gpsInput.value = `${locData.lat.toFixed(4)}, ${locData.lng.toFixed(4)}`;
      }
    } else {
      blockSelect.disabled = true;
    }
  });

  blockSelect.addEventListener("change", (e) => {
    const district = districtSelect.value;
    const block = e.target.value;
    panchayatSelect.innerHTML = '<option value="">Select Panchayat</option>';

    if (district && block && AppState.locations[district] && AppState.locations[district].blocks[block]) {
      const panchayats = AppState.locations[district].blocks[block];
      panchayats.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p;
        opt.textContent = p;
        panchayatSelect.appendChild(opt);
      });
      panchayatSelect.disabled = false;
    } else {
      panchayatSelect.disabled = true;
    }
  });
}

function setupWizardNavigation() {
  const btnNext = document.getElementById("wizardBtnNext");
  const btnBack = document.getElementById("wizardBtnBack");
  const btnSubmit = document.getElementById("wizardBtnSubmit");

  if (btnNext) {
    btnNext.addEventListener("click", () => {
      if (validateStep(wizardCurrentStep)) {
        saveStepData(wizardCurrentStep);
        if (wizardCurrentStep < 5) {
          wizardCurrentStep++;
          updateWizardStepUI();
        }
      }
    });
  }

  if (btnBack) {
    btnBack.addEventListener("click", () => {
      if (wizardCurrentStep > 1) {
        wizardCurrentStep--;
        updateWizardStepUI();
      }
    });
  }

  if (btnSubmit) {
    btnSubmit.addEventListener("click", handleWizardSubmit);
  }
}

function validateStep(step) {
  if (step === 1) {
    const title = document.getElementById("wizardTitle").value.trim();
    const desc = document.getElementById("wizardDesc").value.trim();
    if (title.length < 5) {
      showToast("Please provide a descriptive problem title (min 5 characters).", "error");
      document.getElementById("wizardTitle").focus();
      return false;
    }
    if (desc.length < 10) {
      showToast("Please provide a detailed description (min 10 characters).", "error");
      document.getElementById("wizardDesc").focus();
      return false;
    }
    return true;
  } else if (step === 2) {
    const dist = document.getElementById("wizardDistrict").value;
    if (!dist) {
      showToast("Please select a Jharkhand district.", "error");
      return false;
    }
    return true;
  }
  return true;
}

function saveStepData(step) {
  if (step === 1) {
    wizardFormData.title = document.getElementById("wizardTitle").value.trim();
    wizardFormData.description = document.getElementById("wizardDesc").value.trim();
    wizardFormData.suggested_domain = document.getElementById("wizardDomain").value;
  } else if (step === 2) {
    wizardFormData.district = document.getElementById("wizardDistrict").value;
    wizardFormData.block = document.getElementById("wizardBlock").value;
    wizardFormData.panchayat = document.getElementById("wizardPanchayat").value;
    wizardFormData.locality = document.getElementById("wizardLocality").value.trim();
    wizardFormData.gps = document.getElementById("wizardGps").value.trim();
  } else if (step === 4) {
    wizardFormData.affected_population = document.getElementById("wizardAffected").value.trim();
    wizardFormData.urgency_rationale = document.getElementById("wizardUrgency").value.trim();
    wizardFormData.citizen_suggestions = document.getElementById("wizardSuggestions").value.trim();
  }

  if (wizardCurrentStep === 4) {
    // Populate review step
    populateReviewStep();
  }
}

function updateWizardStepUI() {
  // Update step indicators
  for (let i = 1; i <= 5; i++) {
    const stepNode = document.getElementById(`stepperNode${i}`);
    const stepPane = document.getElementById(`wizardStepPane${i}`);

    if (stepNode) {
      stepNode.classList.remove("active", "completed");
      if (i < wizardCurrentStep) {
        stepNode.classList.add("completed");
      } else if (i === wizardCurrentStep) {
        stepNode.classList.add("active");
      }
    }

    if (stepPane) {
      if (i === wizardCurrentStep) {
        stepPane.classList.remove("hidden");
      } else {
        stepPane.classList.add("hidden");
      }
    }
  }

  // Navigation button controls
  const btnBack = document.getElementById("wizardBtnBack");
  const btnNext = document.getElementById("wizardBtnNext");
  const btnSubmit = document.getElementById("wizardBtnSubmit");

  if (btnBack) {
    if (wizardCurrentStep === 1) {
      btnBack.classList.add("hidden");
    } else {
      btnBack.classList.remove("hidden");
    }
  }

  if (btnNext && btnSubmit) {
    if (wizardCurrentStep === 5) {
      btnNext.classList.add("hidden");
      btnSubmit.classList.remove("hidden");
    } else {
      btnNext.classList.remove("hidden");
      btnSubmit.classList.add("hidden");
    }
  }

  window.scrollTo({ top: 120, behavior: "smooth" });
}

function setupEvidenceUpload() {
  const fileInput = document.getElementById("wizardFileInput");
  const dropZone = document.getElementById("wizardDropZone");

  if (!fileInput || !dropZone) return;

  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("border-emerald-500", "bg-emerald-50");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("border-emerald-500", "bg-emerald-50");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("border-emerald-500", "bg-emerald-50");
    handleSelectedFiles(e.dataTransfer.files);
  });

  fileInput.addEventListener("change", (e) => {
    handleSelectedFiles(e.target.files);
  });
}

function handleSelectedFiles(files) {
  const maxSizeBytes = 25 * 1024 * 1024;
  const allowedExtensions = ["jpg", "jpeg", "png", "pdf", "mp4"];

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const ext = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(ext)) {
      showToast(`File type .${ext} is not allowed. (Use JPG, PNG, PDF, or MP4)`, "error");
      continue;
    }

    if (file.size > maxSizeBytes) {
      showToast(`File ${file.name} exceeds max limit of 25MB.`, "error");
      continue;
    }

    wizardFormData.evidence_files.push(file);
  }

  updateFilePreviewList();
}

function updateFilePreviewList() {
  const listEl = document.getElementById("wizardFilesList");
  if (!listEl) return;

  if (wizardFormData.evidence_files.length === 0) {
    listEl.innerHTML = `<span class="text-xs text-slate-400">No files uploaded yet.</span>`;
    return;
  }

  listEl.innerHTML = wizardFormData.evidence_files.map((f, idx) => `
    <div class="flex items-center justify-between p-2 bg-slate-50 rounded-md border border-slate-200 text-xs">
      <div class="flex items-center truncate">
        <span class="mr-2">📎</span>
        <span class="font-medium text-slate-800 truncate">${f.name}</span>
        <span class="ml-2 text-slate-400">(${(f.size / 1024).toFixed(0)} KB)</span>
      </div>
      <button type="button" onclick="removeEvidenceFile(${idx})" class="text-red-500 hover:text-red-700 ml-2 font-bold">×</button>
    </div>
  `).join("");
}

function removeEvidenceFile(idx) {
  wizardFormData.evidence_files.splice(idx, 1);
  updateFilePreviewList();
}

function setupLiveAIPreview() {
  const btnAnalyze = document.getElementById("btnLiveAiPreview");
  if (!btnAnalyze) return;

  btnAnalyze.addEventListener("click", async () => {
    const title = document.getElementById("wizardTitle").value.trim();
    const desc = document.getElementById("wizardDesc").value.trim();
    const dist = document.getElementById("wizardDistrict").value;
    const suggested = document.getElementById("wizardDomain").value;

    if (!title && !desc) {
      showToast("Please write a problem title or description first to preview AI analysis.", "info");
      return;
    }

    btnAnalyze.disabled = true;
    btnAnalyze.innerHTML = `<span>Analyzing with AI Engine...</span>`;

    try {
      const res = await fetch("/api/ai/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          description: desc,
          district: dist || "Ranchi",
          suggested_domain: suggested
        })
      });
      const data = await res.json();
      renderLiveAiPreviewCard(data);
    } catch (err) {
      showToast("AI preview service unavailable", "error");
    } finally {
      btnAnalyze.disabled = false;
      btnAnalyze.innerHTML = `<span>✨ Live AI Preview</span>`;
    }
  });
}

function renderLiveAiPreviewCard(ai) {
  const card = document.getElementById("wizardLiveAiCard");
  if (!card) return;

  card.classList.remove("hidden");
  card.innerHTML = `
    <div class="p-4 bg-emerald-50 rounded-xl border border-emerald-200 text-xs">
      <div class="flex items-center justify-between mb-2">
        <span class="font-bold text-emerald-900 flex items-center">
          <span class="mr-1">🤖</span> AI Problem Classification Preview
        </span>
        <span class="bg-emerald-200 text-emerald-900 px-2 py-0.5 rounded font-semibold">
          Confidence: ${(ai.confidence * 100).toFixed(0)}%
        </span>
      </div>
      <div class="grid grid-cols-2 gap-2 text-slate-700 mb-2">
        <div><strong>Domain:</strong> ${ai.domain}</div>
        <div><strong>Subdomain:</strong> ${ai.subdomain}</div>
        <div><strong>Urgency Score:</strong> <span class="font-bold text-red-600">${ai.urgency_score}/100</span> (${ai.impact_level} Impact)</div>
        <div><strong>Recommended HEI:</strong> ${ai.recommended_hei}</div>
      </div>
      <div class="p-2 bg-white rounded border border-emerald-100 mb-2">
        <strong>Formalized GovTech Problem Statement:</strong><br/>
        <span class="italic text-slate-800">"${ai.generated_problem_statement}"</span>
      </div>
      <div class="text-[11px] text-emerald-800 font-medium">
        🛡️ ${ai.ai_governance_notice}
      </div>
    </div>
  `;
}

function populateReviewStep() {
  document.getElementById("reviewTitle").textContent = wizardFormData.title || "—";
  document.getElementById("reviewDesc").textContent = wizardFormData.description || "—";
  document.getElementById("reviewDomain").textContent = wizardFormData.suggested_domain || "Will be AI-classified";
  document.getElementById("reviewLocation").textContent = `${wizardFormData.locality || ''}, ${wizardFormData.panchayat || ''}, ${wizardFormData.block || ''}, ${wizardFormData.district || ''}`.replace(/^[ ,]+|[ ,]+$/g, '') || "—";
  document.getElementById("reviewGps").textContent = wizardFormData.gps || "Auto-mapped";
  document.getElementById("reviewAffected").textContent = wizardFormData.affected_population || "Community";
  document.getElementById("reviewUrgency").textContent = wizardFormData.urgency_rationale || "Standard priority";
  document.getElementById("reviewSuggestions").textContent = wizardFormData.citizen_suggestions || "Open to academic R&D";
  document.getElementById("reviewFilesCount").textContent = `${wizardFormData.evidence_files.length} file(s) attached`;
}

async function handleWizardSubmit() {
  const termsCheckbox = document.getElementById("wizardAgreeTerms");
  if (termsCheckbox && !termsCheckbox.checked) {
    showToast("Please confirm that the information provided is true and accurate.", "error");
    return;
  }

  const btnSubmit = document.getElementById("wizardBtnSubmit");
  btnSubmit.disabled = true;
  btnSubmit.innerHTML = `<span>Processing with AI Engine...</span>`;

  try {
    const formData = new FormData();
    formData.append("title", wizardFormData.title);
    formData.append("description", wizardFormData.description);
    formData.append("suggested_domain", wizardFormData.suggested_domain);
    formData.append("district", wizardFormData.district);
    formData.append("block", wizardFormData.block);
    formData.append("panchayat", wizardFormData.panchayat);
    formData.append("locality", wizardFormData.locality);
    formData.append("gps", wizardFormData.gps);
    formData.append("affected_population", wizardFormData.affected_population);
    formData.append("urgency_rationale", wizardFormData.urgency_rationale);
    formData.append("citizen_suggestions", wizardFormData.citizen_suggestions);

    wizardFormData.evidence_files.forEach(f => {
      formData.append("evidence_files", f);
    });

    const res = await fetch("/api/problems", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    if (res.ok && data.success) {
      showSubmissionSuccessModal(data.problem);
      resetWizard();
      loadStats();
      loadProblems();
    } else {
      showToast(data.error || "Failed to submit problem", "error");
    }
  } catch (err) {
    showToast("Server connection error during submission", "error");
  } finally {
    btnSubmit.disabled = false;
    btnSubmit.innerHTML = `<span>Submit to JHAR-SOLVE</span>`;
  }
}

function showSubmissionSuccessModal(problem) {
  const modal = document.getElementById("wizardSuccessModal");
  if (!modal) return;

  document.getElementById("successProblemId").textContent = problem.id;
  document.getElementById("successDomain").textContent = problem.domain;
  document.getElementById("successUrgency").textContent = `${problem.urgency_score}/100`;
  document.getElementById("successHei").textContent = (problem.ai_analysis && problem.ai_analysis.recommended_hei) || "BIT Mesra / IIT Dhanbad";
  document.getElementById("successStatement").textContent = (problem.ai_analysis && problem.ai_analysis.generated_problem_statement) || problem.title;

  modal.classList.remove("hidden");
}

function closeSuccessModal() {
  const modal = document.getElementById("wizardSuccessModal");
  if (modal) modal.classList.add("hidden");
}

function trackFromSuccessModal() {
  const pid = document.getElementById("successProblemId").textContent;
  closeSuccessModal();
  openProblemDetailModal(pid);
}
