import allJobs from "./data.json" with { type: "json" };

const root = document.getElementById("job-board-root");
const jobListEl = document.getElementById("job-list");
const listPanelEl = document.getElementById("job-list-panel");
const detailShell = document.getElementById("job-detail-shell");
const jobDetailContent = document.getElementById("job-detail-content");
const searchInput = document.getElementById("job-search");
const sortSelect = document.getElementById("sort");

/** Selected job object, or null when browsing the full-width list */
let selectedJob = null;

const LIST_BOARD =
  "job-board-root mx-auto mt-8 w-full max-w-7xl flex flex-col gap-4 transition-all duration-300 ease-out lg:mt-10";

const SPLIT_BOARD =
  "job-board-root mx-auto mt-8 w-full max-w-7xl flex min-h-[50vh] flex-col gap-4 transition-all duration-300 ease-out lg:mt-10 lg:min-h-[calc(100vh-11rem)] lg:flex-row lg:items-stretch lg:gap-6";

const LIST_PANEL =
  "job-list-panel w-full border-0 bg-transparent shadow-none transition-all duration-300 ease-out";

const SPLIT_PANEL =
  "job-list-panel w-full max-lg:order-last flex-shrink-0 border border-gray-200 bg-white shadow-sm transition-all duration-300 ease-out lg:w-2/5 lg:rounded-2xl";

const LIST_JOBLIST =
  "flex flex-col gap-4 sm:gap-5 transition-all duration-300 ease-out";

const SPLIT_JOBLIST =
  "flex max-h-[55vh] flex-col gap-3 overflow-y-auto p-3 transition-all duration-300 ease-out sm:p-4 lg:max-h-[min(100vh-8rem,900px)]";

const LIST_DETAIL =
  "job-detail-shell min-h-0 min-w-0 transition-all duration-300 ease-out";

const SPLIT_DETAIL =
  "job-detail-shell min-h-[280px] min-w-0 flex-1 transition-all duration-300 ease-out max-lg:order-first lg:sticky lg:top-4 lg:self-start lg:w-3/5";

function formatDate(iso) {
  try {
    return new Intl.DateTimeFormat(undefined, {
      dateStyle: "medium",
    }).format(new Date(iso));
  } catch {
    return iso;
  }
}

function buildDescription(job) {
  if (job.description && String(job.description).trim()) {
    return job.description.trim();
  }
  const pay =
    job.stipend > 0
      ? `This internship offers a stipend of $${job.stipend.toLocaleString()}.`
      : "Compensation for this role is listed as unpaid; confirm details with the employer.";
  return [
    `${job.company} is looking for a **${job.title}** based in ${job.location}. ${pay}`,
    "",
    "You will collaborate with the team on real projects, learn tooling used in production, and participate in reviews and mentorship. Strong communication and curiosity are valued alongside core technical skills.",
    "",
    `Posted on ${formatDate(job.postedDate)}. Apply early—roles may close when capacity is reached.`,
  ].join("\n");
}

function markdownLite(text) {
  return text
    .split("\n")
    .map((line) => {
      const trimmed = line.trim();
      if (!trimmed) return "";
      const escaped = trimmed
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
      return `<p>${escaped.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")}</p>`;
    })
    .filter(Boolean)
    .join("");
}

function filterJobs(jobs, query) {
  const q = query.trim().toLowerCase();
  if (!q) return jobs;
  return jobs.filter(
    (j) =>
      j.title.toLowerCase().includes(q) ||
      j.company.toLowerCase().includes(q) ||
      (j.location && j.location.toLowerCase().includes(q)),
  );
}

function sortJobs(jobs, key) {
  const copy = [...jobs];
  switch (key) {
    case "money-high":
      return copy.sort((a, b) => b.stipend - a.stipend);
    case "money-low":
      return copy.sort((a, b) => a.stipend - b.stipend);
    case "company":
      return copy.sort((a, b) => a.company.localeCompare(b.company));
    case "newest":
    default:
      return copy.sort(
        (a, b) => new Date(b.postedDate) - new Date(a.postedDate),
      );
  }
}

function getVisibleJobs() {
  const q = searchInput?.value ?? "";
  const sortKey = sortSelect?.value ?? "newest";
  return sortJobs(filterJobs(allJobs, q), sortKey);
}

function syncLayout() {
  if (!root || !listPanelEl || !jobListEl || !detailShell) return;

  const hasSelection = selectedJob != null;

  if (hasSelection) {
    root.dataset.layout = "split";
    root.className = SPLIT_BOARD;
    listPanelEl.className = SPLIT_PANEL;
    jobListEl.className = SPLIT_JOBLIST;
    detailShell.className = SPLIT_DETAIL;
    detailShell.removeAttribute("hidden");
    detailShell.setAttribute("aria-hidden", "false");
  } else {
    root.dataset.layout = "list";
    root.className = LIST_BOARD;
    listPanelEl.className = LIST_PANEL;
    jobListEl.className = LIST_JOBLIST;
    detailShell.className = LIST_DETAIL;
    detailShell.setAttribute("hidden", "");
    detailShell.setAttribute("aria-hidden", "true");
  }
}

function clearList() {
  jobListEl.replaceChildren();
}

function renderList(jobs) {
  if (selectedJob) {
    const fresh = jobs.find((j) => j.id === selectedJob.id);
    if (!fresh) {
      selectedJob = null;
    } else {
      selectedJob = fresh;
    }
  }

  syncLayout();
  clearList();

  if (jobs.length === 0) {
    const empty = document.createElement("div");
    empty.className = "no-results !py-8 !shadow-none";
    empty.innerHTML =
      "<h3 class=\"!mb-2\">No matches</h3><p class=\"!mb-0\">Try a different search or sort option.</p>";
    jobListEl.append(empty);
    selectedJob = null;
    syncLayout();
    jobDetailContent?.replaceChildren();
    return;
  }

  const inSplit = selectedJob != null;

  jobs.forEach((job) => {
    const isPaid = job.stipend > 0;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = inSplit
      ? "job-card job-card--list"
      : "job-card job-card--browse";
    btn.dataset.jobId = String(job.id);

    const isActive = inSplit && selectedJob && job.id === selectedJob.id;
    btn.setAttribute("aria-pressed", isActive ? "true" : "false");
    if (isActive) btn.classList.add("is-active");

    const title = document.createElement("h2");
    title.className = "job-title";
    title.textContent = job.title;

    const company = document.createElement("div");
    company.className = "company-name";
    company.textContent = job.company;

    const details = document.createElement("div");
    details.className = "details";
    details.textContent = `${job.location} • ${formatDate(job.postedDate)}`;

    const stipend = document.createElement("div");
    stipend.className = `stipend${isPaid ? "" : " stipend--unpaid"}`;
    stipend.textContent = isPaid ? `$${job.stipend.toLocaleString()}` : "Unpaid";

    const badge = document.createElement("span");
    badge.className = `badge ${isPaid ? "badge-paid" : "badge-unpaid"}`;
    badge.textContent = isPaid ? "Paid" : "Unpaid";

    btn.append(title, company, details, stipend, badge);
    btn.addEventListener("click", () => selectJob(job.id));
    jobListEl.append(btn);
  });

  if (selectedJob) {
    renderDetail(selectedJob);
  } else {
    jobDetailContent?.replaceChildren();
  }
}

function selectJob(id) {
  const jobs = getVisibleJobs();
  const job = jobs.find((j) => j.id === id);
  if (!job) return;
  selectedJob = job;
  renderList(jobs);
}

function closeDetail() {
  selectedJob = null;
  renderList(getVisibleJobs());
}

function renderDetail(job) {
  if (!jobDetailContent) return;

  jobDetailContent.replaceChildren();

  const isPaid = job.stipend > 0;

  const closeRow = document.createElement("div");
  closeRow.className =
    "mb-4 flex items-start justify-end gap-3 sm:absolute sm:right-4 sm:top-4 sm:z-10 sm:mb-0";

  const closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.className =
    "inline-flex h-10 items-center justify-center rounded-xl border border-gray-200 bg-white px-3 text-sm font-semibold text-gray-600 shadow-sm transition hover:border-gray-300 hover:bg-gray-50 hover:text-gray-900";
  closeBtn.setAttribute("aria-label", "Close job details and return to list");
  closeBtn.innerHTML =
    "<span aria-hidden=\"true\" class=\"text-lg leading-none\">×</span><span class=\"ml-1.5 hidden sm:inline\">Close</span>";
  closeBtn.addEventListener("click", closeDetail);
  closeRow.append(closeBtn);

  const header = document.createElement("header");
  header.className = "job-detail-header sm:pr-24";

  const h = document.createElement("h2");
  h.className = "job-detail-title";
  h.textContent = job.title;

  const meta = document.createElement("div");
  meta.className = "job-detail-meta";
  meta.innerHTML = `
    <span class="job-detail-company">${escapeHtml(job.company)}</span>
    <span class="job-detail-dot" aria-hidden="true">·</span>
    <span class="job-detail-location">${escapeHtml(job.location)}</span>
    <span class="job-detail-dot" aria-hidden="true">·</span>
    <span class="job-detail-posted">Posted ${escapeHtml(formatDate(job.postedDate))}</span>
  `;

  const stipRow = document.createElement("div");
  stipRow.className = "job-detail-stipend-row";
  const stip = document.createElement("span");
  stip.className = `job-detail-stipend${isPaid ? "" : " job-detail-stipend--muted"}`;
  stip.textContent = isPaid
    ? `$${job.stipend.toLocaleString()} stipend`
    : "Unpaid position";
  const badge = document.createElement("span");
  badge.className = `badge ${isPaid ? "badge-paid" : "badge-unpaid"}`;
  badge.textContent = isPaid ? "Paid" : "Unpaid";
  stipRow.append(stip, badge);

  header.append(h, meta, stipRow);

  const actions = document.createElement("div");
  actions.className = "job-detail-actions";
  const applyBtn = document.createElement("a");
  applyBtn.className = "btn btn-apply";
  applyBtn.textContent = "Apply now";
  applyBtn.href = job.applyUrl || "#";
  if (!job.applyUrl) {
    applyBtn.addEventListener("click", (e) => e.preventDefault());
    applyBtn.title = "Application URL not set for this listing (demo)";
  }
  applyBtn.rel = "noopener noreferrer";
  actions.append(applyBtn);

  const body = document.createElement("div");
  body.className = "job-detail-body";
  const h3 = document.createElement("h3");
  h3.className = "job-detail-section-title";
  h3.textContent = "Job description";
  const desc = document.createElement("div");
  desc.className = "job-detail-description prose-flow";
  desc.innerHTML = markdownLite(buildDescription(job));
  body.append(h3, desc);

  jobDetailContent.append(closeRow, header, actions, body);
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function refresh() {
  renderList(getVisibleJobs());
}

searchInput?.addEventListener("input", () => {
  refresh();
});

sortSelect?.addEventListener("change", () => {
  refresh();
});

refresh();
