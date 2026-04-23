import { showToast } from "./toasts.js";

export function initJobStatus() {
  const form = document.querySelector("[data-status-form]");
  if (!form) return;
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submitter = event.submitter;
    const body = new FormData(form);
    if (submitter?.value) body.set("status", submitter.value);
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body,
        headers: { "X-Requested-With": "fetch" },
      });
      const payload = await response.json();
      if (!response.ok || !payload.success) {
        showToast(payload.message || "Status update failed.", "error");
        return;
      }
      updateStatusUI(payload.job);
      showToast(payload.message, "success");
    } catch {
      showToast("Status update failed.", "error");
    }
  });
}

function updateStatusUI(job) {
  const badge = document.querySelector("[data-status-badge]");
  const applied = document.querySelector("[data-applied-date]");
  const followUp = document.querySelector("[data-follow-up-date]");
  if (badge) {
    badge.className = `status-badge status-${job.status}`;
    badge.textContent = label(job.status);
  }
  if (applied) applied.textContent = formatDate(job.applied_date);
  if (followUp) followUp.textContent = formatDate(job.follow_up_date);
}

function formatDate(value) {
  if (!value) return "Not set";
  return new Intl.DateTimeFormat("en-GB", { dateStyle: "medium" }).format(new Date(value));
}

function label(value) {
  const labels = {
    interested: "Interested",
    applied: "Applied",
    interview: "Interview",
    offer: "Offer",
    rejected: "Rejected",
    ignored: "Ignored",
    new: "New",
  };
  return labels[value] || value;
}
