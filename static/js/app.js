/**
 * app.js - Main Application Controller for SAMADHAN
 * Jharkhand Societal Innovation Lifecycle Platform
 * Supports 3 dedicated stakeholder interfaces:
 * 1. HEI / Students & Research Organizations
 * 2. Industry (Funding Partners)
 * 3. Government (Administration)
 */

const AppState = {
  currentLang: "en",
  currentUser: null,
  currentView: "home",
  i18nData: {},
  problems: [],
  locations: {},
  trends: [],
  projects: [],
  solutions: [],
  achievements: [],
  activeAuthCategory: "STUDENT_HEI", // STUDENT_HEI, INDUSTRY, GOVERNMENT
  heroSlideIndex: 0,
  heiData: null,
  industryData: null,
  govData: null,
  activeHeiTab: "problems",
  activeIndustryTab: "review",
  activeGovTab: "problems"
};

// --- Initialization ---
document.addEventListener("DOMContentLoaded", async () => {
  await loadCurrentUser();
  await loadLocations();
  await loadI18n(AppState.currentLang);
  await loadHomeContent();
  await loadProblems();

  setupEventListeners();
  initHeroSlider();
  initRouting();
});

// --- I18N Handling ---
async function loadI18n(lang) {
  try {
    const res = await fetch(`/api/i18n/${lang}`);
    const data = await res.json();
    AppState.currentLang = lang;
    AppState.i18nData = data.strings || {};
    applyTranslations();
  } catch (err) {
    console.error("Failed to load i18n:", err);
  }
}

function t(key, fallback = "") {
  return AppState.i18nData[key] || fallback || key;
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (AppState.i18nData[key]) {
      el.textContent = AppState.i18nData[key];
    }
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (AppState.i18nData[key]) {
      el.setAttribute("placeholder", AppState.i18nData[key]);
    }
  });

  document.querySelectorAll(".lang-btn").forEach(btn => {
    const lang = btn.getAttribute("data-lang");
    if (lang === AppState.currentLang) {
      btn.classList.add("bg-emerald-700", "text-white");
      btn.classList.remove("text-slate-300", "hover:text-white");
    } else {
      btn.classList.remove("bg-emerald-700", "text-white");
      btn.classList.add("text-slate-300", "hover:text-white");
    }
  });
}

function toggleLanguage(lang) {
  loadI18n(lang);
}

// --- Hero Slider Animation ---
function initHeroSlider() {
  const track = document.getElementById("heroTrack");
  if (!track) return;

  const totalSlides = 5;
  if (window.__heroInterval) clearInterval(window.__heroInterval);
  window.__heroInterval = setInterval(() => {
    AppState.heroSlideIndex = (AppState.heroSlideIndex + 1) % totalSlides;
    const shiftPercent = AppState.heroSlideIndex * (100 / totalSlides);
    track.style.transform = `translateX(-${shiftPercent}%)`;
  }, 4000);
}

// --- Home Content (Trends, Projects, Solutions, Achievements) ---
async function loadHomeContent() {
  try {
    const [trendsRes, projRes, solRes, achRes] = await Promise.all([
      fetch("/api/trends"),
      fetch("/api/projects"),
      fetch("/api/solutions"),
      fetch("/api/achievements")
    ]);

    AppState.trends = await trendsRes.json();
    AppState.projects = await projRes.json();
    AppState.solutions = await solRes.json();
    AppState.achievements = await achRes.json();

    renderTrendsSection();
    renderProjectsSection();
    renderSolutionsSection();
    renderAchievementsSection();
  } catch (err) {
    console.error("Error loading home content:", err);
  }
}

// --- Accessibility Font Size Controller (IIT Madras Standard) ---
function adjustFontSize(delta) {
  const root = document.documentElement;
  if (delta === 0) {
    root.style.fontSize = "16px";
  } else {
    const current = parseFloat(window.getComputedStyle(root).fontSize) || 16;
    root.style.fontSize = Math.min(20, Math.max(13, current + delta * 1.5)) + "px";
  }
}

// Helper: Crisp Vector Icons for Institutional Academic Cards
function getInstitutionalSvg(type) {
  switch (type) {
    case "water":
    case "Water Management":
      return `<svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>`;
    case "agriculture":
    case "Agriculture":
      return `<svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>`;
    case "environment":
    case "Environment":
      return `<svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>`;
    case "healthcare":
    case "Healthcare":
      return `<svg class="w-5 h-5 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>`;
    case "livelihoods":
    case "Rural Livelihoods":
      return `<svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>`;
    case "grant":
      return `<svg class="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
    case "certificate":
      return `<svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
    default:
      return `<svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>`;
  }
}

function renderTrendsSection() {
  const container = document.getElementById("trendsGrid");
  if (!container) return;

  container.innerHTML = AppState.trends.map((t, idx) => {
    const accentColors = [
      "border-t-emerald-700",
      "border-t-blue-700",
      "border-t-amber-700",
      "border-t-purple-700",
      "border-t-teal-700"
    ];
    const accent = accentColors[idx % accentColors.length];

    return `
      <div class="inst-card border-t-4 ${accent} p-6 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-3.5 pb-2 border-b border-slate-100">
            <div class="flex items-center space-x-2">
              <span class="p-1.5 rounded-md bg-slate-100 border border-slate-200">${getInstitutionalSvg(t.domain)}</span>
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-600">${t.domain || "Technological Domain"}</span>
            </div>
            <span class="inst-badge bg-emerald-50 text-emerald-800 border border-emerald-200">
              ${t.badge}
            </span>
          </div>

          <h3 class="font-serif-inst text-base sm:text-lg font-bold text-slate-900 mb-2 leading-snug">${t.title}</h3>
          <p class="text-xs text-slate-600 mb-4 leading-relaxed">${t.summary}</p>
        </div>

        <div class="pt-3 border-t border-slate-100 bg-slate-50/70 p-3 rounded-md border border-slate-200/60 text-xs">
          <div class="flex items-center space-x-1 text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1">
            <span>🎯 Verified Societal Impact:</span>
          </div>
          <div class="font-semibold text-emerald-950">${t.key_impact}</div>
        </div>
      </div>
    `;
  }).join("");
}

function renderProjectsSection() {
  const container = document.getElementById("projectsGrid");
  if (!container) return;

  container.innerHTML = AppState.projects.map(p => `
    <div class="inst-card p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
      <div>
        <div class="flex flex-wrap items-center justify-between gap-2 mb-3 pb-2.5 border-b border-slate-100">
          <div class="flex items-center space-x-2">
            <span class="font-mono text-[11px] font-bold text-slate-800 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
              REF: ${p.id}
            </span>
            <span class="text-[11px] font-semibold text-slate-500">📍 ${p.district}</span>
          </div>
          <span class="inst-badge bg-blue-50 text-blue-800 border border-blue-200 font-semibold">
            ${p.status}
          </span>
        </div>

        <h3 class="font-serif-inst text-base sm:text-lg font-bold text-slate-900 mb-2 leading-snug">${p.title}</h3>
        <p class="text-xs text-slate-600 mb-4 leading-relaxed">${p.desc}</p>

        <!-- Institutional Stakeholder & Outlay Metadata -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs bg-slate-50 p-3 rounded-md border border-slate-200/70 mb-4">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">Lead R&D Institution</span>
            <span class="font-semibold text-slate-800">${p.lead_institution}</span>
          </div>
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">Sponsoring CSR Partner</span>
            <span class="font-semibold text-slate-800">${p.funding_partner}</span>
          </div>
          <div class="sm:col-span-2 pt-1 border-t border-slate-200/60 flex items-center justify-between">
            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500">Approved Grant Sanction</span>
            <span class="font-mono font-bold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">${p.grant}</span>
          </div>
        </div>
      </div>

      <div>
        <div class="flex justify-between text-[11px] font-semibold text-slate-600 mb-1.5">
          <span>Implementation Progress</span>
          <span class="font-mono font-bold text-emerald-800">${p.progress_percent}%</span>
        </div>
        <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
          <div class="bg-emerald-700 h-full rounded-full transition-all duration-500" style="width: ${p.progress_percent}%"></div>
        </div>
      </div>
    </div>
  `).join("");
}

function renderSolutionsSection() {
  const container = document.getElementById("solutionsGrid");
  if (!container) return;

  container.innerHTML = AppState.solutions.map(s => `
    <div class="inst-card p-6 flex flex-col justify-between border-t-4 border-t-purple-700 shadow-sm">
      <div>
        <div class="flex items-center justify-between mb-3 pb-2 border-b border-slate-100">
          <span class="font-mono text-[10px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
            ${s.id}
          </span>
          <span class="inst-badge bg-purple-50 text-purple-900 border border-purple-200">
            STATE CERTIFIED
          </span>
        </div>

        <h3 class="font-serif-inst text-base font-bold text-slate-900 mb-2.5 leading-snug">${s.title}</h3>

        <div class="space-y-1 text-xs text-slate-600 mb-4">
          <div><strong class="text-slate-700">Innovating Lab:</strong> ${s.developed_by}</div>
          <div><strong class="text-slate-700">Deployment Belt:</strong> ${s.deployed_at}</div>
        </div>
      </div>

      <div class="pt-3 border-t border-slate-100 bg-emerald-50/60 p-3 rounded-md border border-emerald-200/80 text-xs">
        <div class="text-[10px] font-bold uppercase tracking-wider text-emerald-900 mb-1">Audited Societal Reach:</div>
        <div class="text-emerald-950 font-semibold mb-1">${s.impact_metric}</div>
        <div class="text-[10px] text-slate-500 border-t border-emerald-100 pt-1">
          Procured by: <span class="font-medium text-slate-700">${s.procured_by}</span>
        </div>
      </div>
    </div>
  `).join("");
}

function renderAchievementsSection() {
  const container = document.getElementById("achievementsGrid");
  if (!container) return;

  container.innerHTML = AppState.achievements.map((a, idx) => {
    const borders = ["border-t-amber-400", "border-t-emerald-400", "border-t-blue-400", "border-t-purple-400", "border-t-teal-400"];
    const borderAccent = borders[idx % borders.length];

    return `
      <div class="bg-slate-900/90 rounded-lg p-6 border border-slate-800 border-t-4 ${borderAccent} text-center flex flex-col justify-between hover:bg-slate-850 transition">
        <div>
          <div class="font-serif-inst text-3xl sm:text-4xl font-black text-white tracking-tight mb-2">
            ${a.stat}
          </div>
          <h4 class="text-sm font-bold text-amber-300 uppercase tracking-wide mb-2.5">${a.label}</h4>
          <p class="text-xs text-slate-300 leading-relaxed mb-4">${a.desc}</p>
        </div>
        <div class="pt-2 border-t border-slate-800/80 text-[10px] font-mono text-emerald-400">
          ✓ Verified by State Nodal Directorate
        </div>
      </div>
    `;
  }).join("");
}

// --- Auth Modal & Stakeholder Category Switching ---
function openLoginModal(defaultCat = "STUDENT_HEI") {
  AppState.activeAuthCategory = defaultCat;
  updateAuthModalCategoryTabs("login");
  const modal = document.getElementById("loginModal");
  if (modal) modal.classList.remove("hidden");
}

function closeLoginModal() {
  const modal = document.getElementById("loginModal");
  if (modal) modal.classList.add("hidden");
}

function openRegisterModal(defaultCat = "STUDENT_HEI") {
  AppState.activeAuthCategory = defaultCat;
  updateAuthModalCategoryTabs("register");
  const modal = document.getElementById("registerModal");
  if (modal) modal.classList.remove("hidden");
}

function closeRegisterModal() {
  const modal = document.getElementById("registerModal");
  if (modal) modal.classList.add("hidden");
}

function selectAuthCategory(category, formType = "login") {
  AppState.activeAuthCategory = category;
  updateAuthModalCategoryTabs(formType);
}

function updateAuthModalCategoryTabs(formType) {
  const prefix = formType === "login" ? "loginTab" : "regTab";
  const cats = ["STUDENT_HEI", "INDUSTRY", "GOVERNMENT"];

  cats.forEach(c => {
    const btn = document.getElementById(`${prefix}-${c}`);
    if (!btn) return;
    if (c === AppState.activeAuthCategory) {
      btn.className = "flex-1 py-2 text-center text-xs font-bold rounded-lg bg-emerald-700 text-white shadow-sm transition";
    } else {
      btn.className = "flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-600 hover:bg-slate-100 transition";
    }
  });

  if (formType === "register") {
    const orgLabel = document.getElementById("regOrgLabel");
    if (orgLabel) {
      if (AppState.activeAuthCategory === "STUDENT_HEI") orgLabel.textContent = "Institution / College Name *";
      else if (AppState.activeAuthCategory === "INDUSTRY") orgLabel.textContent = "Company / Foundation Name *";
      else orgLabel.textContent = "Government Department / Office *";
    }
  }
}

async function handleLoginSubmit(e) {
  e.preventDefault();
  const loginId = document.getElementById("loginIdentifier").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_type: AppState.activeAuthCategory,
        login_identifier: loginId,
        password: password
      })
    });
    const data = await res.json();
    if (data.success) {
      AppState.currentUser = data.active_user;
      updateUserUI();
      closeLoginModal();
      showToast(`Welcome back, ${data.user.username}! Signed in as ${data.user.user_type.replace('_', ' ')}`, "success");

      // Auto-navigate to respective interface
      if (data.user.user_type === "STUDENT_HEI") navigateTo("hei-portal");
      else if (data.user.user_type === "INDUSTRY") navigateTo("industry-portal");
      else if (data.user.user_type === "GOVERNMENT") navigateTo("gov-portal");
    } else {
      showToast(data.error || "Login failed", "error");
    }
  } catch (err) {
    showToast("Server connection error", "error");
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  const username = document.getElementById("regUsername").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const password = document.getElementById("regPassword").value.trim();
  const org = document.getElementById("regOrg").value.trim();

  try {
    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_type: AppState.activeAuthCategory,
        username,
        email,
        password,
        organization: org
      })
    });
    const data = await res.json();
    if (data.success) {
      AppState.currentUser = data.active_user;
      updateUserUI();
      closeRegisterModal();
      showToast(`Account successfully created for ${username}!`, "success");

      if (data.user.user_type === "STUDENT_HEI") navigateTo("hei-portal");
      else if (data.user.user_type === "INDUSTRY") navigateTo("industry-portal");
      else if (data.user.user_type === "GOVERNMENT") navigateTo("gov-portal");
    } else {
      showToast(data.error || "Registration failed", "error");
    }
  } catch (err) {
    showToast("Registration error", "error");
  }
}

// --- Contact Form Submission ---
async function handleContactSubmit(e) {
  e.preventDefault();
  const name = document.getElementById("contactName").value.trim();
  const email = document.getElementById("contactEmail").value.trim();
  const message = document.getElementById("contactMessage").value.trim();

  try {
    const res = await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, message })
    });
    const data = await res.json();
    if (data.success) {
      showToast("Thank you! Your inquiry has been sent to the State Innovation Mission.", "success");
      document.getElementById("contactForm").reset();
    } else {
      showToast(data.error || "Could not send message", "error");
    }
  } catch (err) {
    showToast("Error sending message", "error");
  }
}

// --- Persona / Role Switcher ---
async function loadCurrentUser() {
  try {
    const res = await fetch("/api/auth/current-user");
    const data = await res.json();
    AppState.currentUser = data.user;
    updateUserUI();
  } catch (err) {
    console.error("Failed to load user:", err);
  }
}

async function switchPersona(roleKey) {
  try {
    const res = await fetch("/api/auth/switch-role", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role_key: roleKey })
    });
    const data = await res.json();
    if (data.success) {
      AppState.currentUser = data.user;
      updateUserUI();
      showToast(`Switched persona to: ${data.user.name} (${data.user.role})`, "success");

      if (data.user.role === "GOVERNMENT") navigateTo("gov-portal");
      else if (data.user.role === "HEI" || data.user.role === "INNOVATOR") navigateTo("hei-portal");
      else if (data.user.role === "INDUSTRY") navigateTo("industry-portal");
      else if (data.user.role === "ADMIN") navigateTo("gov-portal");
      else navigateTo("home");
    }
  } catch (err) {
    showToast("Error switching role", "error");
  }
}

function updateUserUI() {
  const u = AppState.currentUser;
  if (!u) return;
  updateUserRoleNav();
}

function updateUserRoleNav() {
  const u = AppState.currentUser;
  const role = (u && u.role) ? u.role.toUpperCase() : "CITIZEN";

  const heiLink = document.getElementById("navLinkHeiPortal");
  const indLink = document.getElementById("navLinkIndustryPortal");
  const govLink = document.getElementById("navLinkGovPortal");

  const userBadge = document.getElementById("navUserBadge");
  const userName = document.getElementById("navUserName");
  const userIcon = document.getElementById("navUserIcon");
  const authButtons = document.getElementById("navAuthButtons");

  // Reset: hide all 3 portals by default
  if (heiLink) { heiLink.classList.add("hidden"); heiLink.classList.remove("flex"); }
  if (indLink) { indLink.classList.add("hidden"); indLink.classList.remove("flex"); }
  if (govLink) { govLink.classList.add("hidden"); govLink.classList.remove("flex"); }

  // STRICT REQUIREMENT: Only show the portal matching the logged-in stakeholder
  if (role === "HEI" || role === "INNOVATOR" || role === "STUDENT_HEI") {
    if (heiLink) {
      heiLink.classList.remove("hidden");
      heiLink.classList.add("flex");
    }
  } else if (role === "INDUSTRY") {
    if (indLink) {
      indLink.classList.remove("hidden");
      indLink.classList.add("flex");
    }
  } else if (role === "GOVERNMENT" || role === "ADMIN") {
    if (govLink) {
      govLink.classList.remove("hidden");
      govLink.classList.add("flex");
    }
  }

  // Update Auth / User chip in top bar
  if (u && role !== "CITIZEN") {
    if (userBadge) {
      userBadge.classList.remove("hidden");
      userBadge.classList.add("flex");
    }
    if (userName) userName.textContent = `${u.name}`;
    if (userIcon) {
      userIcon.textContent = (role === "HEI" || role === "INNOVATOR" || role === "STUDENT_HEI") ? "🎓" :
                             role === "INDUSTRY" ? "🏭" : "🏛️";
    }
    if (authButtons) {
      authButtons.classList.add("hidden");
    }
  } else {
    if (userBadge) {
      userBadge.classList.add("hidden");
      userBadge.classList.remove("flex");
    }
    if (authButtons) {
      authButtons.classList.remove("hidden");
    }
  }
}

async function handleLogout() {
  try {
    const res = await fetch("/api/auth/logout", { method: "POST" });
    const data = await res.json();
    AppState.currentUser = data.user;
    updateUserUI();
    updateUserRoleNav();
    showToast("Signed out successfully. Returned to Home.", "info");
    navigateTo("home");
  } catch (err) {
    console.error("Logout error:", err);
  }
}

// --- Locations & Master Data ---
async function loadLocations() {
  try {
    const res = await fetch("/api/locations");
    AppState.locations = await res.json();
    populateDistrictDropdowns();
  } catch (err) {
    console.error("Failed to load locations:", err);
  }
}

function populateDistrictDropdowns() {
  const districtSelects = document.querySelectorAll(".district-select");
  const districts = Object.keys(AppState.locations).sort();

  districtSelects.forEach(select => {
    const firstOption = select.firstElementChild ? select.firstElementChild.outerHTML : "";
    select.innerHTML = firstOption;
    districts.forEach(d => {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = d;
      select.appendChild(opt);
    });
  });
}

// --- Problems Listing ---
async function loadProblems(filters = {}) {
  try {
    const params = new URLSearchParams(filters);
    const res = await fetch(`/api/problems?${params}`);
    const data = await res.json();
    AppState.problems = data.problems || [];
    if (window.updateMapMarkers) {
      window.updateMapMarkers(AppState.problems);
    }
  } catch (err) {
    console.error("Failed to load problems:", err);
  }
}

// =========================================================================
// 1. HEI / STUDENT & RESEARCH ORGANIZATIONS PORTAL CONTROLLER
// =========================================================================

function switchHeiTab(tabName) {
  AppState.activeHeiTab = tabName;
  const tabs = ["problems", "submit", "account", "projects"];

  tabs.forEach(t => {
    const btn = document.getElementById(`heiTabBtn-${t}`);
    const pane = document.getElementById(`heiTabPane-${t}`);
    if (btn) {
      if (t === tabName) {
        btn.className = "hei-tab-btn px-4 py-2.5 rounded-xl bg-emerald-700 text-white shadow-sm transition font-bold";
      } else {
        btn.className = "hei-tab-btn px-4 py-2.5 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 transition font-bold";
      }
    }
    if (pane) {
      pane.classList.toggle("hidden", t !== tabName);
    }
  });

  if (tabName === "submit") {
    populateHeiProposalDropdown();
  }
}

async function loadHeiDashboard() {
  try {
    const res = await fetch("/api/hei/dashboard");
    const data = await res.json();
    AppState.heiData = data;

    // 1. Account Stats
    const stats = data.stats || {};
    const pCount = document.getElementById("heiStatAvailableProblems");
    const sCount = document.getElementById("heiStatSubmittedProposals");
    const aCount = document.getElementById("heiStatApprovedProposals");
    const actCount = document.getElementById("heiStatActiveProjects");

    if (pCount) pCount.textContent = stats.total_problem_statements || 0;
    if (sCount) sCount.textContent = stats.proposals_submitted || 0;
    if (aCount) aCount.textContent = stats.approved_funded || 0;
    if (actCount) actCount.textContent = stats.active_projects_count || 0;

    // 2. Render Problem Statements & AI Generated Statements
    renderHeiProblems(data.problem_statements || []);

    // 3. Render My Proposals in Account Dashboard
    renderHeiAccountProposals(data.proposals || []);

    // 4. Render In-Flight Projects Status
    renderHeiProjectsStatus(data.active_projects || []);

    // 5. Populate problem dropdown
    populateHeiProposalDropdown();
  } catch (err) {
    console.error("Error loading HEI dashboard:", err);
  }
}

function renderHeiProblems(problems) {
  const grid = document.getElementById("heiProblemsGrid");
  if (!grid) return;

  if (problems.length === 0) {
    grid.innerHTML = `<div class="col-span-2 text-center p-8 bg-white rounded-2xl border border-slate-200 text-slate-500 text-xs">No problem statements available currently.</div>`;
    return;
  }

  grid.innerHTML = problems.map(p => `
    <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center space-x-2">
            <span class="font-mono text-xs font-bold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">${p.id}</span>
            <span class="text-[11px] font-bold px-2 py-0.5 rounded ${getDomainBadgeClass(p.domain)}">${p.domain}</span>
          </div>
          <span class="text-xs font-bold px-2 py-0.5 rounded ${p.urgency_score >= 80 ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-amber-50 text-amber-800 border border-amber-200'}">
            Urgency: ${p.urgency_score}/100
          </span>
        </div>

        <h4 class="text-base font-bold text-slate-900 mb-1 leading-snug">${p.title}</h4>
        <div class="text-xs text-slate-500 mb-3 flex items-center space-x-2">
          <span>📍 ${p.district}${p.block ? ', ' + p.block : ''}</span>
          <span>•</span>
          <span class="font-semibold text-slate-700">Stage: ${formatStageLabel(p.stage)}</span>
        </div>

        <!-- Citizen Original Report Snippet -->
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100 mb-3 text-xs text-slate-600">
          <span class="font-bold text-slate-700 block mb-0.5">Citizen Community Report:</span>
          ${p.description.substring(0, 140)}...
        </div>

        <!-- AI GENERATED PROBLEM STATEMENT (Core Requirement) -->
        <div class="bg-gradient-to-r from-emerald-50 to-teal-50/70 p-4 rounded-xl border border-emerald-200 mb-4 text-xs text-slate-800">
          <div class="flex items-center space-x-1.5 font-bold text-emerald-900 mb-1">
            <span>🤖</span>
            <span>AI-Generated Problem Statement (from citizen report):</span>
          </div>
          <p class="font-medium leading-relaxed text-emerald-950">${p.ai_problem_statement || "Develop a scalable engineered solution addressing this challenge."}</p>
          
          ${p.ai_root_causes && p.ai_root_causes.length > 0 ? `
            <div class="mt-2 text-[11px] text-slate-600">
              <strong>Key Root Causes:</strong> ${p.ai_root_causes.slice(0, 2).join('; ')}
            </div>
          ` : ''}
        </div>
      </div>

      <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
        <button onclick="inspectProblemDetails('${p.id}')" class="text-xs text-slate-600 hover:text-slate-900 font-bold underline">
          View 15-Stage Details
        </button>
        <button onclick="openHeiSubmitForProblem('${p.id}', '${escapeQuotes(p.title)}')" class="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-xl shadow-sm transition flex items-center space-x-1">
          <span>🚀 Submit Solution Proposal</span>
        </button>
      </div>
    </div>
  `).join("");
}

function filterHeiProblems() {
  const sel = document.getElementById("heiDomainFilter");
  if (!sel || !AppState.heiData) return;
  const domain = sel.value;
  const list = AppState.heiData.problem_statements || [];
  if (domain === "all") {
    renderHeiProblems(list);
  } else {
    renderHeiProblems(list.filter(p => p.domain === domain));
  }
}

function populateHeiProposalDropdown() {
  const sel = document.getElementById("heiPropProblemId");
  if (!sel) return;

  const probs = (AppState.heiData && AppState.heiData.problem_statements) || AppState.problems || [];
  const currentVal = sel.value;
  sel.innerHTML = `<option value="">Select the Problem Statement you are solving</option>` +
    probs.map(p => `<option value="${p.id}">${p.id} - ${p.title.substring(0, 60)}...</option>`).join("");

  if (currentVal) sel.value = currentVal;

  // Auto-fill user contact info if logged in
  if (AppState.currentUser) {
    const u = AppState.currentUser;
    const nameInput = document.getElementById("heiPropContactName");
    const emailInput = document.getElementById("heiPropContactEmail");
    const instInput = document.getElementById("heiPropInstitution");

    if (nameInput && !nameInput.value) nameInput.value = u.name || "";
    if (emailInput && !emailInput.value) emailInput.value = u.email || "";
    if (instInput && !instInput.value) instInput.value = u.org || "";
  }
}

function openHeiSubmitForProblem(problemId, problemTitle) {
  switchHeiTab("submit");
  const sel = document.getElementById("heiPropProblemId");
  if (sel) {
    sel.value = problemId;
  }
}

async function handleHeiProposalSubmit(e) {
  e.preventDefault();
  const problemId = document.getElementById("heiPropProblemId").value;
  const title = document.getElementById("heiPropTitle").value.trim();
  const technicalAbstract = document.getElementById("heiPropAbstract").value.trim();
  const budget = parseFloat(document.getElementById("heiPropBudget").value);
  const timeline = parseInt(document.getElementById("heiPropTimeline").value);
  const milestonesText = document.getElementById("heiPropMilestones").value.trim();
  const milestones = milestonesText ? milestonesText.split("\n").map(s => s.trim()).filter(Boolean) : [];

  const contactName = document.getElementById("heiPropContactName").value.trim();
  const contactEmail = document.getElementById("heiPropContactEmail").value.trim();
  const contactPhone = document.getElementById("heiPropContactPhone").value.trim();
  const heiInstitution = document.getElementById("heiPropInstitution").value.trim();

  if (!problemId) {
    showToast("Please select a target problem statement.", "error");
    return;
  }

  try {
    const res = await fetch("/api/proposals", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        problem_id: problemId,
        title,
        technical_abstract: technicalAbstract,
        proposed_budget: budget,
        timeline_months: timeline,
        milestones,
        innovator_name: contactName,
        contact_name: contactName,
        contact_email: contactEmail,
        contact_phone: contactPhone,
        hei_institution: heiInstitution
      })
    });

    const data = await res.json();
    if (data.success) {
      showToast("Solution proposal successfully submitted! Industry partners have received a live alert.", "success");
      document.getElementById("heiProposalForm").reset();
      await loadHeiDashboard();
      switchHeiTab("account");
    } else {
      showToast(data.error || "Submission failed", "error");
    }
  } catch (err) {
    showToast("Server connection error during proposal submission.", "error");
  }
}

function renderHeiAccountProposals(proposals) {
  const tbody = document.getElementById("heiAccountProposalsList");
  if (!tbody) return;

  if (proposals.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="p-6 text-center text-slate-500 text-xs">No proposals submitted yet. Browse problem statements and submit your first proposal!</td></tr>`;
    return;
  }

  tbody.innerHTML = proposals.map(p => {
    const statusClass = p.funding_status === "APPROVED" ? "bg-emerald-100 text-emerald-800" :
                        p.funding_status === "DISAPPROVED" ? "bg-red-100 text-red-800" :
                        "bg-amber-100 text-amber-800";
    return `
      <tr class="hover:bg-slate-50">
        <td class="p-3.5 font-bold text-slate-900">${p.title}</td>
        <td class="p-3.5 font-mono text-emerald-800">${p.problem_id}</td>
        <td class="p-3.5 font-bold text-slate-800">₹ ${(p.proposed_budget / 100000).toFixed(1)} Lakhs</td>
        <td class="p-3.5 text-slate-600">${p.timeline_months} Months</td>
        <td class="p-3.5"><span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold ${statusClass}">${p.funding_status}</span></td>
        <td class="p-3.5 text-slate-600 text-[11px]">${p.funding_industry_name || p.funding_decision_notes || 'Under Industry Review'}</td>
        <td class="p-3.5 text-slate-500 text-[11px]">${p.submitted_at ? p.submitted_at.substring(0, 10) : ''}</td>
      </tr>
    `;
  }).join("");
}

function renderHeiProjectsStatus(projects) {
  const grid = document.getElementById("heiProjectsList");
  if (!grid) return;

  if (projects.length === 0) {
    grid.innerHTML = `<div class="col-span-2 text-center p-8 bg-white rounded-2xl border border-slate-200 text-slate-500 text-xs">No funded projects currently in development. Proposals will appear here once approved for funding.</div>`;
    return;
  }

  grid.innerHTML = projects.map(p => `
    <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
      <div class="flex items-center justify-between mb-3">
        <span class="font-mono text-xs font-bold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded">${p.id}</span>
        <span class="text-xs font-bold px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-800 border border-blue-200">
          ${formatStageLabel(p.stage)}
        </span>
      </div>

      <h4 class="text-base font-bold text-slate-900 mb-1">${p.title}</h4>
      <div class="text-xs text-slate-500 mb-4">📍 ${p.district} • Domain: ${p.domain}</div>

      <div class="bg-slate-50 rounded-xl p-3 border border-slate-100 text-xs space-y-1 mb-4">
        <div><strong>Funding Partner:</strong> ${p.funding_details ? p.funding_details.industry_name || 'Committed CSR Partner' : 'Sanctioned Pool'}</div>
        <div><strong>Committed Grant:</strong> <span class="text-emerald-800 font-bold">₹ ${p.funding_details && p.funding_details.committed_amount ? (p.funding_details.committed_amount/100000).toFixed(1) + ' Lakhs' : 'Under Allocation'}</span></div>
      </div>

      <div class="pt-2">
        <button onclick="inspectProblemDetails('${p.id}')" class="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold rounded-xl transition">
          View Complete 15-Stage Lifecycle Journey →
        </button>
      </div>
    </div>
  `).join("");
}

// =========================================================================
// 2. INDUSTRY & CSR FUNDING PARTNERS PORTAL CONTROLLER
// =========================================================================

function switchIndustryTab(tabName) {
  AppState.activeIndustryTab = tabName;
  const tabs = ["review", "funded", "notifications"];

  tabs.forEach(t => {
    const btn = document.getElementById(`indTabBtn-${t}`);
    const pane = document.getElementById(`indTabPane-${t}`);
    if (btn) {
      if (t === tabName) {
        btn.className = "ind-tab-btn px-4 py-2.5 rounded-xl bg-blue-800 text-white shadow-sm transition font-bold";
      } else {
        btn.className = "ind-tab-btn px-4 py-2.5 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 transition font-bold";
      }
    }
    if (pane) {
      pane.classList.toggle("hidden", t !== tabName);
    }
  });
}

async function loadIndustryDashboard() {
  try {
    const res = await fetch("/api/industry/dashboard");
    const data = await res.json();
    AppState.industryData = data;

    // 1. Account Stats
    const stats = data.stats || {};
    const pCount = document.getElementById("indStatPendingCount");
    const fCount = document.getElementById("indStatFundedCount");
    const cFund = document.getElementById("indStatCommittedFunding");
    const dCount = document.getElementById("indStatDisapprovedCount");

    if (pCount) pCount.textContent = stats.pending_review_count || 0;
    if (fCount) fCount.textContent = stats.funded_count || 0;
    if (cFund) cFund.textContent = `₹ ${((stats.total_committed_funding || 0) / 100000).toFixed(1)} L`;
    if (dCount) dCount.textContent = stats.disapproved_count || 0;

    // 2. Notifications Badge & Ticker
    const notifs = data.notifications || [];
    const badge = document.getElementById("indNotifBadge");
    const ticker = document.getElementById("indLatestNotifText");

    if (badge) badge.textContent = `${notifs.filter(n => !n.is_read).length} NEW`;
    if (ticker && notifs.length > 0) {
      ticker.textContent = notifs[0].title + " - " + notifs[0].message;
    }

    // 3. Render Proposals Awaiting Review (WITH HEI CONTACT DETAILS)
    renderIndustryReviewProposals(data.pending_proposals || []);

    // 4. Render Funded Proposals
    renderIndustryFundedProposals(data.funded_proposals || []);

    // 5. Render Notifications Log
    renderIndustryNotifications(notifs);
  } catch (err) {
    console.error("Error loading Industry dashboard:", err);
  }
}

function renderIndustryReviewProposals(proposals) {
  const grid = document.getElementById("indReviewProposalsGrid");
  if (!grid) return;

  if (proposals.length === 0) {
    grid.innerHTML = `<div class="p-8 bg-white rounded-2xl border border-slate-200 text-center text-slate-500 text-xs">No pending proposals awaiting review. All current submissions have been evaluated.</div>`;
    return;
  }

  grid.innerHTML = proposals.map(p => `
    <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-md flex flex-col md:flex-row justify-between gap-6 hover:border-blue-400 transition">
      <!-- Left Column: Proposal & Problem Details -->
      <div class="flex-grow space-y-4">
        <div class="flex items-center space-x-2">
          <span class="font-mono text-xs font-bold text-blue-800 bg-blue-50 px-2.5 py-1 rounded-lg border border-blue-200">Proposal #${p.id}</span>
          <span class="font-mono text-xs text-slate-500">Problem: ${p.problem_id}</span>
          <span class="text-[11px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-300">Pending Review</span>
        </div>

        <div>
          <h4 class="text-lg font-bold text-slate-900 leading-snug">${p.title}</h4>
          <p class="text-xs text-slate-600 mt-2 leading-relaxed">${p.technical_abstract}</p>
        </div>

        <!-- Budget & Timeline Metrics -->
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 bg-slate-50 p-3 rounded-2xl border border-slate-200 text-xs">
          <div>
            <span class="text-slate-500 block text-[11px]">Requested Budget</span>
            <span class="font-black text-emerald-800 text-sm">₹ ${(p.proposed_budget / 100000).toFixed(1)} Lakhs</span>
          </div>
          <div>
            <span class="text-slate-500 block text-[11px]">Timeline</span>
            <span class="font-bold text-slate-800 text-sm">${p.timeline_months} Months</span>
          </div>
          <div>
            <span class="text-slate-500 block text-[11px]">Submitted Date</span>
            <span class="font-medium text-slate-700 text-xs">${p.submitted_at ? p.submitted_at.substring(0, 10) : 'Recent'}</span>
          </div>
        </div>

        <!-- Associated Problem Context -->
        <div class="text-xs text-slate-700">
          <span class="font-bold">Targeted Citizen Problem:</span> ${p.problem_title || p.problem_id} (📍 ${p.problem_district || 'Jharkhand'})
        </div>
      </div>

      <!-- Right Column: HEI Lead Contact Details + Funding Action Buttons -->
      <div class="w-full md:w-80 shrink-0 flex flex-col justify-between bg-blue-50/50 p-5 rounded-2xl border border-blue-200">
        <div>
          <div class="flex items-center space-x-1.5 font-bold text-blue-950 text-xs mb-3">
            <span>🎓</span>
            <span>HEI Investigator Contact Details</span>
          </div>

          <div class="space-y-2 text-xs text-slate-700">
            <div>
              <span class="text-[11px] text-slate-500 block">Lead Scientist / Scholar:</span>
              <span class="font-bold text-slate-900">${p.contact_name || p.innovator_name}</span>
            </div>
            <div>
              <span class="text-[11px] text-slate-500 block">Institution / College:</span>
              <span class="font-semibold text-blue-900">${p.hei_institution || 'BIT Mesra / IIT-ISM'}</span>
            </div>
            <div>
              <span class="text-[11px] text-slate-500 block">Official Email:</span>
              <a href="mailto:${p.contact_email}" class="font-mono text-emerald-800 hover:underline font-semibold text-[11px] break-all">
                ✉️ ${p.contact_email || 'contact@hei.ac.in'}
              </a>
            </div>
            <div>
              <span class="text-[11px] text-slate-500 block">Contact Phone:</span>
              <a href="tel:${p.contact_phone}" class="font-mono text-slate-800 font-semibold text-[11px]">
                📞 ${p.contact_phone || '+91 94311 00000'}
              </a>
            </div>
          </div>
        </div>

        <!-- Direct Approve or Disapprove Buttons (Core Requirement) -->
        <div class="pt-5 border-t border-blue-200/80 space-y-2">
          <button onclick="openFundingDecisionModal(${p.id}, 'APPROVE', ${escapeJsonForHtml(p)})" class="w-full py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-black rounded-xl text-xs shadow-md transition flex items-center justify-center space-x-1.5">
            <span>✓</span><span>Approve Funding (CSR Grant)</span>
          </button>
          <button onclick="openFundingDecisionModal(${p.id}, 'DISAPPROVE', ${escapeJsonForHtml(p)})" class="w-full py-2 bg-white hover:bg-red-50 text-red-700 hover:text-red-800 border border-red-300 font-bold rounded-xl text-xs transition flex items-center justify-center space-x-1.5">
            <span>✕</span><span>Disapprove Funding</span>
          </button>
        </div>
      </div>
    </div>
  `).join("");
}

function renderIndustryFundedProposals(proposals) {
  const tbody = document.getElementById("indFundedProposalsList");
  if (!tbody) return;

  if (proposals.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="p-6 text-center text-slate-500 text-xs">No funded proposals yet. Review pending submissions to allocate CSR funding.</td></tr>`;
    return;
  }

  tbody.innerHTML = proposals.map(p => `
    <tr class="hover:bg-slate-50">
      <td class="p-3.5 font-bold text-slate-900">${p.title}</td>
      <td class="p-3.5 text-blue-900 font-semibold">${p.hei_institution || p.contact_name}</td>
      <td class="p-3.5 font-black text-emerald-800">₹ ${(p.proposed_budget / 100000).toFixed(1)} Lakhs</td>
      <td class="p-3.5 text-slate-700 font-medium">${p.funding_industry_name || 'Tata Steel Foundation'}</td>
      <td class="p-3.5 text-slate-500">${p.decision_date ? p.decision_date.substring(0, 10) : 'Recent'}</td>
      <td class="p-3.5"><span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-100 text-blue-800">${formatStageLabel(p.problem_stage || 'FUNDING_ALLOCATED')}</span></td>
      <td class="p-3.5 text-slate-600 text-[11px]">${p.funding_decision_notes || 'Approved for CSR Grant.'}</td>
    </tr>
  `).join("");
}

function renderIndustryNotifications(notifs) {
  const feed = document.getElementById("indNotificationsFeed");
  if (!feed) return;

  if (notifs.length === 0) {
    feed.innerHTML = `<div class="p-6 bg-white rounded-2xl border border-slate-200 text-center text-slate-500 text-xs">No notifications logged.</div>`;
    return;
  }

  feed.innerHTML = notifs.map(n => `
    <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm flex items-start justify-between">
      <div class="flex items-start space-x-3">
        <span class="text-xl">🔔</span>
        <div>
          <div class="font-bold text-slate-900 text-xs">${n.title}</div>
          <div class="text-xs text-slate-600 mt-0.5">${n.message}</div>
          <div class="text-[10px] text-slate-400 mt-1">${n.created_at ? n.created_at.substring(0, 19).replace('T', ' ') : ''}</div>
        </div>
      </div>
      <span class="px-2 py-0.5 text-[10px] font-bold rounded ${n.is_read ? 'bg-slate-100 text-slate-500' : 'bg-amber-100 text-amber-800'}">
        ${n.is_read ? 'Read' : 'New'}
      </span>
    </div>
  `).join("");
}

// Funding Decision Modal Logic
function openFundingDecisionModal(proposalId, action, proposal) {
  const modal = document.getElementById("fundingDecisionModal");
  if (!modal) return;

  document.getElementById("decProposalId").value = proposalId;
  document.getElementById("decAction").value = action;
  document.getElementById("decProposalName").textContent = proposal.title;
  document.getElementById("decHeiDetails").textContent = `${proposal.hei_institution || 'HEI Team'} • Lead: ${proposal.contact_name || proposal.innovator_name}`;

  const approveFields = document.getElementById("decApproveFields");
  const disapproveFields = document.getElementById("decDisapproveFields");
  const submitBtn = document.getElementById("decSubmitBtn");
  const title = document.getElementById("fundingDecisionTitle");

  if (action === "APPROVE") {
    title.textContent = "Approve CSR Grant Funding";
    approveFields.classList.remove("hidden");
    disapproveFields.classList.add("hidden");
    submitBtn.textContent = "Confirm & Sanction Funding";
    submitBtn.className = "px-5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl font-bold transition";
  } else {
    title.textContent = "Disapprove Proposal Funding";
    approveFields.classList.add("hidden");
    disapproveFields.classList.remove("hidden");
    submitBtn.textContent = "Confirm Disapproval";
    submitBtn.className = "px-5 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl font-bold transition";
  }

  modal.classList.remove("hidden");
}

function closeFundingDecisionModal() {
  const modal = document.getElementById("fundingDecisionModal");
  if (modal) modal.classList.add("hidden");
}

async function handleFundingDecisionSubmit(e) {
  e.preventDefault();
  const proposalId = document.getElementById("decProposalId").value;
  const action = document.getElementById("decAction").value;

  let url, payload;
  if (action === "APPROVE") {
    url = `/api/proposals/${proposalId}/approve`;
    payload = {
      industry_name: document.getElementById("decIndustryName").value.trim() || "Tata Steel Foundation",
      notes: document.getElementById("decNotes").value.trim() || "Approved under CSR Innovation Grant."
    };
  } else {
    url = `/api/proposals/${proposalId}/disapprove`;
    payload = {
      industry_name: "Tata Steel Foundation",
      reason: document.getElementById("decReason").value.trim() || "Does not align with current corporate CSR guidelines."
    };
  }

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      showToast(action === "APPROVE" ? "Funding Sanctioned successfully! Problem stage moved to FUNDING_ALLOCATED." : "Proposal marked as disapproved.", "success");
      closeFundingDecisionModal();
      await loadIndustryDashboard();
      await loadProblems();
    } else {
      showToast(data.error || "Decision processing failed", "error");
    }
  } catch (err) {
    showToast("Server error during decision submission", "error");
  }
}

// =========================================================================
// 3. GOVERNMENT OVERSIGHT & ADMINISTRATIVE MASTER INTERFACE
// =========================================================================

function switchGovTab(tabName) {
  AppState.activeGovTab = tabName;
  const tabs = ["problems", "solutions", "projects"];

  tabs.forEach(t => {
    const btn = document.getElementById(`govTabBtn-${t}`);
    const pane = document.getElementById(`govTabPane-${t}`);
    if (btn) {
      if (t === tabName) {
        btn.className = "gov-tab-btn px-4 py-2.5 rounded-xl bg-amber-700 text-white shadow-sm transition font-bold";
      } else {
        btn.className = "gov-tab-btn px-4 py-2.5 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 transition font-bold";
      }
    }
    if (pane) {
      pane.classList.toggle("hidden", t !== tabName);
    }
  });
}

async function loadGovMaster() {
  try {
    const res = await fetch("/api/government/master");
    const data = await res.json();
    AppState.govData = data;

    // 1. KPIs
    const stats = data.stats || {};
    const tp = document.getElementById("govStatTotalProblems");
    const ts = document.getElementById("govStatTotalSolutions");
    const fs = document.getElementById("govStatFundedSolutions");
    const ap = document.getElementById("govStatActivePilots");

    if (tp) tp.textContent = stats.total_problems || 0;
    if (ts) ts.textContent = stats.total_solutions || 0;
    if (fs) fs.textContent = stats.approved_funded_solutions || 0;
    if (ap) ap.textContent = stats.active_pilots_count || 0;

    // 2. All Problem Statements
    renderGovProblems(data.all_problem_statements || []);

    // 3. All Solutions
    renderGovSolutions(data.all_solutions || []);

    // 4. All Project Statuses
    renderGovProjectStatuses(data.all_project_statuses || []);
  } catch (err) {
    console.error("Error loading Government master data:", err);
  }
}

function renderGovProblems(problems) {
  const tbody = document.getElementById("govMasterProblemsList");
  if (!tbody) return;

  tbody.innerHTML = problems.map(p => `
    <tr class="hover:bg-slate-50">
      <td class="p-3.5">
        <span class="font-mono font-bold text-amber-900 block">${p.id}</span>
        <span class="font-bold text-slate-900">${p.title}</span>
      </td>
      <td class="p-3.5 text-slate-700">📍 ${p.district}${p.block ? ', ' + p.block : ''}</td>
      <td class="p-3.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${getDomainBadgeClass(p.domain)}">${p.domain}</span></td>
      <td class="p-3.5 font-bold ${p.urgency_score >= 80 ? 'text-red-700' : 'text-amber-800'}">${p.urgency_score}/100</td>
      <td class="p-3.5"><span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-800">${formatStageLabel(p.stage)}</span></td>
      <td class="p-3.5 text-slate-600">${p.reporter_name || 'Citizen'}</td>
      <td class="p-3.5">
        ${p.stage === 'CITIZEN_PROBLEM' ? `
          <button onclick="verifyProblemAsGov('${p.id}')" class="px-3 py-1 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-[11px] font-bold shadow-sm transition">
            Verify & Sanction Challenge
          </button>
        ` : `
          <button onclick="inspectProblemDetails('${p.id}')" class="text-xs font-bold text-emerald-800 hover:underline">
            Inspect Lifecycle →
          </button>
        `}
      </td>
    </tr>
  `).join("");
}

async function verifyProblemAsGov(problemId) {
  try {
    const res = await fetch(`/api/problems/${problemId}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        gov_notes: "Verified by State Departmental Nodal Committee. Sanctioned as official State Innovation Challenge.",
        challenge_grant_sanctioned: 2000000
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Problem #${problemId} verified and published as Official State Challenge!`, "success");
      await loadGovMaster();
      await loadProblems();
    }
  } catch (err) {
    showToast("Error verifying problem", "error");
  }
}

function renderGovSolutions(solutions) {
  const tbody = document.getElementById("govMasterSolutionsList");
  if (!tbody) return;

  tbody.innerHTML = solutions.map(s => {
    const statusClass = s.funding_status === "APPROVED" ? "bg-emerald-100 text-emerald-800" :
                        s.funding_status === "DISAPPROVED" ? "bg-red-100 text-red-800" :
                        "bg-amber-100 text-amber-800";
    return `
      <tr class="hover:bg-slate-50">
        <td class="p-3.5 font-bold text-slate-900">${s.title}</td>
        <td class="p-3.5 font-mono text-amber-900">${s.problem_id}</td>
        <td class="p-3.5 font-semibold text-blue-900">${s.hei_institution || s.innovator_name}</td>
        <td class="p-3.5 text-slate-700 text-[11px]">${s.contact_name} (${s.contact_email || 'N/A'})</td>
        <td class="p-3.5 font-black text-emerald-800">₹ ${(s.proposed_budget / 100000).toFixed(1)} Lakhs</td>
        <td class="p-3.5"><span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold ${statusClass}">${s.funding_status}</span></td>
        <td class="p-3.5 text-slate-600 text-[11px]">${s.funding_industry_name || 'Pending Review'}</td>
      </tr>
    `;
  }).join("");
}

function renderGovProjectStatuses(projects) {
  const grid = document.getElementById("govMasterProjectsGrid");
  if (!grid) return;

  grid.innerHTML = projects.map(p => `
    <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:shadow-md transition">
      <div class="flex items-center justify-between mb-2">
        <span class="font-mono text-xs font-bold text-amber-900">${p.id}</span>
        <span class="text-[11px] font-extrabold px-2 py-0.5 rounded-full bg-slate-100 text-slate-800">${formatStageLabel(p.stage)}</span>
      </div>
      <h4 class="text-sm font-bold text-slate-900 mb-1 leading-snug">${p.title}</h4>
      <div class="text-[11px] text-slate-500 mb-3">📍 ${p.district} • Domain: ${p.domain}</div>

      <div class="bg-slate-50 rounded-xl p-2.5 text-xs space-y-1 mb-3">
        <div><strong>Urgency Score:</strong> ${p.urgency_score}/100</div>
        <div><strong>Affected:</strong> ${p.affected_population || 'Community'}</div>
      </div>

      <button onclick="inspectProblemDetails('${p.id}')" class="w-full py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-900 font-bold rounded-lg text-xs transition">
        Manage 15-Stage Lifecycle
      </button>
    </div>
  `).join("");
}

// =========================================================================
// VIEW ROUTING & GENERAL HELPERS
// =========================================================================

function navigateTo(viewName) {
  const u = AppState.currentUser;
  const role = (u && u.role) ? u.role.toUpperCase() : "CITIZEN";

  // STRICT ACCESS GUARDS: Only allow users into their authorized portal
  if (viewName === "hei-portal") {
    if (role !== "HEI" && role !== "INNOVATOR" && role !== "STUDENT_HEI") {
      showToast("🔒 Access Restricted: Please log in with your Student & Higher Education Institution account to access this portal.", "error");
      openLoginModal("STUDENT_HEI");
      return;
    }
  } else if (viewName === "industry-portal") {
    if (role !== "INDUSTRY") {
      showToast("🔒 Access Restricted: Please log in with your Industry / CSR Partner account to access this portal.", "error");
      openLoginModal("INDUSTRY");
      return;
    }
  } else if (viewName === "gov-portal") {
    if (role !== "GOVERNMENT" && role !== "ADMIN") {
      showToast("🔒 Access Restricted: Please log in with an authorized Government account to access this portal.", "error");
      openLoginModal("GOVERNMENT");
      return;
    }
  }

  AppState.currentView = viewName;

  document.querySelectorAll(".view-section").forEach(sec => {
    sec.classList.add("hidden");
  });

  const target = document.getElementById(`view-${viewName}`);
  if (target) {
    target.classList.remove("hidden");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  document.querySelectorAll(".nav-link").forEach(link => {
    if (link.getAttribute("data-target") === viewName) {
      link.classList.add("text-amber-400", "font-bold");
      link.classList.remove("text-slate-200");
    } else {
      link.classList.remove("text-amber-400", "font-bold");
      link.classList.add("text-slate-200");
    }
  });

  if (viewName === "hei-portal") {
    loadHeiDashboard();
  } else if (viewName === "industry-portal") {
    loadIndustryDashboard();
  } else if (viewName === "gov-portal") {
    loadGovMaster();
  } else if (viewName === "command") {
    if (window.initCommandCenter) window.initCommandCenter();
  } else if (viewName === "wizard") {
    if (window.resetWizard) window.resetWizard();
  }
}

function scrollToSection(sectionId) {
  if (AppState.currentView !== "home") {
    navigateTo("home");
    setTimeout(() => {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }, 150);
  } else {
    const el = document.getElementById(sectionId);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  }
}

function getDomainBadgeClass(domain) {
  const map = {
    "Water Management": "badge-water",
    "Healthcare": "badge-health",
    "Agriculture": "badge-agri",
    "Environment": "badge-env",
    "Sanitation": "badge-san",
    "Education": "badge-edu",
    "Accessibility": "badge-acc"
  };
  return map[domain] || "bg-slate-100 text-slate-800 border-slate-200";
}

function formatStageLabel(stage) {
  return (stage || "").replace(/_/g, " ");
}

function escapeQuotes(str) {
  return (str || "").replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

function escapeJsonForHtml(obj) {
  return JSON.stringify(obj).replace(/'/g, "&apos;").replace(/"/g, "&quot;");
}

function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  const bgClass = type === "success" ? "bg-emerald-600 text-white" :
                  type === "error" ? "bg-red-600 text-white" :
                  "bg-slate-800 text-white";

  toast.className = `toast px-4 py-3 rounded-lg shadow-lg text-sm font-medium flex items-center space-x-2 ${bgClass}`;
  toast.innerHTML = `
    <span>${type === "success" ? "✓" : type === "error" ? "⚠" : "ℹ"}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function setupEventListeners() {
  document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const target = link.getAttribute("data-target");
      if (target) navigateTo(target);
    });
  });
}

function initRouting() {
  navigateTo("home");
}

function inspectProblemDetails(problemId) {
  if (window.openProblemDetailModal) {
    window.openProblemDetailModal(problemId);
  } else {
    console.log("Viewing problem details for:", problemId);
  }
}
