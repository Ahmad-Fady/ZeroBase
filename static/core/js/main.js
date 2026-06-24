// import internshipData from "./data.json" with { type: "json" };
let internshipData = {};
const trackData = [
  "Frontend",
  "Backend",
  "Full Stack",
  "Mobile",
  "DevOps",
  "Cloud",
  "Cybersecurity",
  "QA",
  "DSA",
  "System Design",
  "Database",
  "Embedded",
  "Game Dev",
  "AI Engineering",
];

const jobsData = [
  { id: 1, title: "Junior Frontend Engineer", company: "Shopify", level: "Junior", location: "Remote" },
  { id: 2, title: "Backend Engineer", company: "Notion", level: "Entry", location: "San Francisco, CA" },
  { id: 3, title: "Cloud Engineer", company: "AWS", level: "Mid", location: "Seattle, WA" },
  { id: 4, title: "QA Automation Engineer", company: "Atlassian", level: "Entry", location: "Remote" },
  { id: 5, title: "Cybersecurity Analyst", company: "CrowdStrike", level: "Junior", location: "Austin, TX" },
  { id: 6, title: "AI Engineer", company: "OpenAI", level: "Mid", location: "San Francisco, CA" },
];

const THEME_KEY = "gradjobs-theme";

function setTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem(THEME_KEY, theme);
  const icon = document.querySelector(".theme-toggle__icon");
  const text = document.querySelector(".theme-toggle__text");
  if (icon) icon.textContent = theme === "dark" ? "☀️" : "🌙";
  if (text) text.textContent = theme === "dark" ? "Light" : "Dark";
}

function setupTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  const preferredDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(saved || (preferredDark ? "dark" : "light"));

  const btn = document.getElementById("theme-toggle");
  btn?.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    setTheme(current === "light" ? "dark" : "light");
  });
}

function markActiveNav() {
  const page = document.body.dataset.page || "home";
  document.querySelectorAll("[data-nav]").forEach((link) => {
    if (link.dataset.nav === page) link.classList.add("active");
  });
}

function renderEmpty(container, message) {
  container.innerHTML = `<article class="empty-state"><p>${message}</p></article>`;
}

function initLearningPage() {
  const grid = document.getElementById("track-grid");
  const search = document.getElementById("track-search");
  if (!grid || !search) return;

  const render = () => {
    const q = search.value.trim().toLowerCase();
    const list = trackData.filter((t) => t.toLowerCase().includes(q));
    if (!list.length) return renderEmpty(grid, "No track matched your search.");

    grid.innerHTML = list
      .map(
        (track) => `
          <article class="feature-card">
            <h3>${track}</h3>
            <p>Focused roadmap, curated resources, and practical milestones.</p>
          </article>
        `,
      )
      .join("");
  };

  search.addEventListener("input", render);
  render();
}

function initInternshipsPage() {
  const grid = document.getElementById("internship-grid");
  const search = document.getElementById("internship-search");
  const location = document.getElementById("internship-location");
  if (!grid || !search || !location) return;

  const render = () => {
    const q = search.value.trim().toLowerCase();
    const loc = location.value.trim().toLowerCase();

    const list = internshipData.filter((item) => {
      const roleMatch =
        item.title.toLowerCase().includes(q) || item.company.toLowerCase().includes(q);
      const locationMatch = !loc || item.location.toLowerCase().includes(loc);
      return roleMatch && locationMatch;
    });

    if (!list.length) return renderEmpty(grid, "No internships found. Try different filters.");

    grid.innerHTML = list
      .map(
        (item) => `
          <article class="listing-card">
            <div class="listing-top">
              <h3>${item.title}</h3>
              <span class="badge ${item.stipend > 0 ? "badge-paid" : "badge-unpaid"}">
                ${item.stipend > 0 ? "Paid" : "Unpaid"}
              </span>
            </div>
            <p class="meta">${item.company} • ${item.location}</p>
            <p class="meta">Posted ${new Date(item.postedDate).toLocaleDateString()}</p>
            <div class="listing-actions">
              <button class="btn">Apply</button>
            </div>
          </article>
        `,
      )
      .join("");
  };

  search.addEventListener("input", render);
  location.addEventListener("input", render);
  render();
}

function initJobsPage() {
  const grid = document.getElementById("jobs-grid");
  const roleInput = document.getElementById("job-role-search");
  const levelFilter = document.getElementById("job-level-filter");
  const locationInput = document.getElementById("job-location-search");
  if (!grid || !roleInput || !levelFilter || !locationInput) return;

  const render = () => {
    const role = roleInput.value.trim().toLowerCase();
    const level = levelFilter.value;
    const location = locationInput.value.trim().toLowerCase();

    const list = jobsData.filter((job) => {
      const roleMatch = !role || job.title.toLowerCase().includes(role);
      const levelMatch = !level || job.level === level;
      const locMatch = !location || job.location.toLowerCase().includes(location);
      return roleMatch && levelMatch && locMatch;
    });

    if (!list.length) return renderEmpty(grid, "No jobs found. Try changing filters.");

    grid.innerHTML = list
      .map(
        (job) => `
          <article class="listing-card">
            <div class="listing-top">
              <h3>${job.title}</h3>
              <span class="pill">${job.level}</span>
            </div>
            <p class="meta">${job.company} • ${job.location}</p>
            <div class="listing-actions">
              <button class="btn btn-secondary">View details</button>
            </div>
          </article>
        `,
      )
      .join("");
  };

  roleInput.addEventListener("input", render);
  levelFilter.addEventListener("change", render);
  locationInput.addEventListener("input", render);
  render();
}

function boot() {
  setupTheme();
  markActiveNav();
  const page = document.body.dataset.page;
  if (page === "learn") initLearningPage();
  if (page === "internships") initInternshipsPage();
  if (page === "jobs") initJobsPage();
}

boot();
