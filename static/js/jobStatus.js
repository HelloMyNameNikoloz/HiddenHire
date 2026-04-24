import { showToast } from "./toasts.js";

export function initJobStatus() {
  const form = document.querySelector("[data-status-form]");
  if (!form) return;
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submitter = event.submitter;
    const body = new FormData(form);
    if (submitter?.value) body.set("status", submitter.value);
    setPendingState(form, submitter?.value || "");
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body,
        headers: { "X-Requested-With": "fetch" },
      });
      const payload = await response.json();
      if (!response.ok || !payload.success) {
        showToast(payload.message || "Status update failed.", "error");
        clearPendingState(form);
        return;
      }
      updateStatusUI(form, payload.job);
      showToast(payload.message, "success");
    } catch {
      showToast("Status update failed.", "error");
    } finally {
      clearPendingState(form);
    }
  });
}

function updateStatusUI(form, job) {
  const badge = document.querySelector("[data-status-badge]");
  const applied = document.querySelector("[data-applied-date]");
  const followUp = document.querySelector("[data-follow-up-date]");
  const currentCopy = document.querySelector("[data-current-status-copy]");
  if (badge) {
    badge.className = `status-badge status-${job.status}`;
    badge.textContent = label(job.status);
  }
  if (currentCopy) currentCopy.textContent = label(job.status);
  if (applied) applied.textContent = formatDate(job.applied_date);
  if (followUp) followUp.textContent = formatDate(job.follow_up_date);
  form.querySelectorAll("[data-status-button]").forEach((button) => {
    button.classList.toggle("is-current", button.dataset.statusButton === job.status);
  });
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
    hidden: "Hidden",
    new: "New",
  };
  return labels[value] || value;
}

function setPendingState(form, status) {
  form.querySelectorAll("[data-status-button]").forEach((button) => {
    button.disabled = true;
    button.classList.toggle("is-pending", button.dataset.statusButton === status);
  });
}

function clearPendingState(form) {
  form.querySelectorAll("[data-status-button]").forEach((button) => {
    button.disabled = false;
    button.classList.remove("is-pending");
  });
}
