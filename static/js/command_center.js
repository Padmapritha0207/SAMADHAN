/**
 * command_center.js - Government Innovation Command Center
 * Features Leaflet GIS Jharkhand Map, AI Verification Queue, Analytics Charts, and Sanction Workflows.
 */

let jharkhandMap = null;
let mapMarkersGroup = null;
let domainChartInstance = null;
let urgencyChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  setupCommandCenterFilters();
});

function initCommandCenter() {
  setTimeout(() => {
    initLeafletMap();
    renderVerificationQueue();
    renderCommandCenterCharts();
  }, 100);
}

function initLeafletMap() {
  const mapContainer = document.getElementById("jharkhandMap");
  if (!mapContainer) return;

  if (jharkhandMap) {
    jharkhandMap.invalidateSize();
    return;
  }

  // Centered on Jharkhand
  jharkhandMap = L.map("jharkhandMap").setView([23.6102, 85.2799], 8);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors | GovTech Jharkhand'
  }).addTo(jharkhandMap);

  mapMarkersGroup = L.layerGroup().addTo(jharkhandMap);
  updateMapMarkers(AppState.problems);
}

function updateMapMarkers(problems) {
  if (!mapMarkersGroup || !jharkhandMap) return;

  mapMarkersGroup.clearLayers();

  // Add markers for problems with coordinates or district fallbacks
  problems.forEach(p => {
    let lat, lng;
    if (p.gps && p.gps.includes(",")) {
      const parts = p.gps.split(",").map(s => parseFloat(s.trim()));
      lat = parts[0];
      lng = parts[1];
    } else if (p.district && AppState.locations[p.district]) {
      lat = AppState.locations[p.district].lat;
      lng = AppState.locations[p.district].lng;
    }

    if (lat && lng) {
      const color = p.urgency_score >= 85 ? "#dc2626" :
                    p.urgency_score >= 65 ? "#d97706" : "#059669";

      const marker = L.circleMarker([lat, lng], {
        radius: p.urgency_score >= 85 ? 12 : 9,
        fillColor: color,
        color: "#ffffff",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85
      });

      const popupContent = `
        <div style="font-family: Inter, sans-serif; font-size: 12px; width: 220px;">
          <div style="font-size: 10px; font-weight: bold; color: #64748b;">${p.id}</div>
          <strong style="color: #0f172a; font-size: 13px;">${p.title}</strong>
          <div style="margin: 6px 0; color: #475569;">
            📍 ${p.locality ? p.locality + ', ' : ''}${p.district}<br/>
            🏷️ <strong>${p.domain}</strong><br/>
            ⚠️ Urgency: <strong style="color: ${color};">${p.urgency_score}/100</strong>
          </div>
          <button onclick="openProblemDetailModal('${p.id}')" style="background: #065f46; color: white; border: none; border-radius: 4px; padding: 4px 8px; font-size: 11px; cursor: pointer; width: 100%; font-weight: 600;">
            View Innovation Lifecycle
          </button>
        </div>
      `;

      marker.bindPopup(popupContent);
      mapMarkersGroup.addLayer(marker);
    }
  });
}

function renderVerificationQueue() {
  const container = document.getElementById("ccVerificationList");
  if (!container) return;

  // Filter problems pending government verification
  const pending = AppState.problems.filter(p =>
    p.stage === "CITIZEN_PROBLEM" || p.stage === "AI_PROCESSING"
  );

  if (pending.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center text-slate-500 bg-slate-50 rounded-xl border border-slate-200">
        <span class="text-3xl block mb-2">✅</span>
        <p class="font-semibold text-slate-700">Verification Queue Clear</p>
        <p class="text-xs text-slate-500 mt-1">All current AI-processed problems have been reviewed by Government Nodal Officers.</p>
      </div>`;
    return;
  }

  container.innerHTML = pending.map(p => `
    <div class="p-5 bg-white rounded-xl border border-slate-200 shadow-sm hover:border-emerald-300 transition duration-150">
      <div class="flex items-start justify-between mb-2">
        <div>
          <span class="text-xs font-mono font-bold text-slate-400 mr-2">${p.id}</span>
          <span class="text-xs font-semibold px-2 py-0.5 rounded border ${getDomainBadgeClass(p.domain)}">${p.domain}</span>
        </div>
        <span class="text-xs font-bold px-2 py-0.5 rounded bg-red-50 text-red-700 border border-red-200">
          Urgency: ${p.urgency_score}/100
        </span>
      </div>

      <h4 class="text-sm font-bold text-slate-900 mb-1 hover:text-emerald-700 cursor-pointer" onclick="openProblemDetailModal('${p.id}')">
        ${p.title}
      </h4>
      <p class="text-xs text-slate-600 mb-3 line-clamp-2">${p.description}</p>

      <div class="p-3 bg-emerald-50/60 rounded-lg border border-emerald-100 mb-3 text-xs">
        <div class="font-bold text-emerald-900 mb-1 flex items-center">
          <span class="mr-1">🤖</span> AI Assessment Summary:
        </div>
        <div class="text-slate-700 mb-1">
          <strong>Synthesized Statement:</strong> ${(p.ai_analysis && p.ai_analysis.generated_problem_statement) || p.title}
        </div>
        <div class="text-slate-700">
          <strong>Recommended Institution:</strong> ${(p.ai_analysis && p.ai_analysis.recommended_hei) || 'BIT Mesra / IIT Dhanbad'}
        </div>
      </div>

      <div class="flex items-center justify-between pt-2 border-t border-slate-100">
        <div class="text-[11px] text-slate-500">
          📍 ${p.locality || ''}, ${p.block || ''}, ${p.district}
        </div>
        <div class="flex space-x-2">
          <button onclick="rejectProblem('${p.id}')" class="px-3 py-1 text-xs font-medium text-slate-600 hover:text-red-700 border border-slate-200 rounded hover:bg-red-50">
            Reject
          </button>
          <button onclick="promptVerifyAndPublish('${p.id}')" class="px-3 py-1 text-xs font-bold text-white bg-emerald-700 hover:bg-emerald-800 rounded shadow-sm">
            ✓ Verify & Publish Challenge
          </button>
        </div>
      </div>
    </div>
  `).join("");
}

async function promptVerifyAndPublish(problemId) {
  const p = AppState.problems.find(item => item.id === problemId);
  if (!p) return;

  const notes = prompt(
    `Government Verification Note for ${problemId}:\n\nEnter departmental verification remarks and approve challenge release:`,
    "Verified on-ground community need. Approved as official State Innovation Challenge with initial R&D grant eligibility."
  );

  if (notes === null) return; // User cancelled

  try {
    const res = await fetch(`/api/problems/${problemId}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        gov_notes: notes,
        challenge_grant_sanctioned: 2500000
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Challenge successfully approved & published for ${problemId}!`, "success");
      await loadProblems();
      await loadStats();
      renderVerificationQueue();
    }
  } catch (err) {
    showToast("Error verifying problem", "error");
  }
}

async function rejectProblem(problemId) {
  if (!confirm(`Are you sure you want to mark ${problemId} as ineligible?`)) return;

  try {
    const res = await fetch(`/api/problems/${problemId}/transition`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        stage: "CITIZEN_PROBLEM",
        notes: "Marked ineligible for innovation grant by Departmental Audit."
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Updated status for ${problemId}`, "info");
      loadProblems();
    }
  } catch (err) {
    showToast("Action failed", "error");
  }
}

function renderCommandCenterCharts() {
  const domainCtx = document.getElementById("domainChart");
  const urgencyCtx = document.getElementById("urgencyChart");

  if (!domainCtx || !urgencyCtx || !window.Chart) return;

  // Domain Distribution Chart
  const domainData = AppState.stats.domain_counts || {};
  const labels = Object.keys(domainData);
  const values = Object.values(domainData);

  if (domainChartInstance) domainChartInstance.destroy();
  domainChartInstance = new Chart(domainCtx, {
    type: "doughnut",
    data: {
      labels: labels.length ? labels : ["Water", "Agri", "Health", "Env"],
      datasets: [{
        data: values.length ? values : [2, 1, 1, 1],
        backgroundColor: [
          "#0284c7", "#16a34a", "#dc2626", "#d97706", "#7c3aed",
          "#0d9488", "#ea580c", "#4f46e5", "#64748b", "#059669"
        ]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { font: { size: 10 } } }
      }
    }
  });

  // Urgency Distribution Chart
  let low = 0, med = 0, high = 0;
  AppState.problems.forEach(p => {
    if (p.urgency_score >= 80) high++;
    else if (p.urgency_score >= 50) med++;
    else low++;
  });

  if (urgencyChartInstance) urgencyChartInstance.destroy();
  urgencyChartInstance = new Chart(urgencyCtx, {
    type: "bar",
    data: {
      labels: ["Standard (<50)", "Moderate (50-79)", "Critical (80+)"],
      datasets: [{
        label: "Number of Problems",
        data: [low, med, high],
        backgroundColor: ["#10b981", "#f59e0b", "#ef4444"]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 1 } }
      }
    }
  });
}

function setupCommandCenterFilters() {
  const ccDistrict = document.getElementById("ccFilterDistrict");
  const ccDomain = document.getElementById("ccFilterDomain");

  const runCCFilter = () => {
    const filters = {};
    if (ccDistrict && ccDistrict.value) filters.district = ccDistrict.value;
    if (ccDomain && ccDomain.value) filters.domain = ccDomain.value;
    loadProblems(filters);
  };

  if (ccDistrict) ccDistrict.addEventListener("change", runCCFilter);
  if (ccDomain) ccDomain.addEventListener("change", runCCFilter);
}
