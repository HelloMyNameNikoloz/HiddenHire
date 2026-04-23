import { showToast } from "./toasts.js";

export function initJobNotes() {
  const form = document.querySelector("[data-notes-form]");
  if (!form) return;
  const indicator = form.querySelector("[data-save-indicator]");
  const save = async () => {
    try {
      if (indicator) indicator.textContent = "Saving...";
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { "X-Requested-With": "fetch" },
      });
      const payload = await response.json();
      if (!response.ok || !payload.success) {
        if (indicator) indicator.textContent = "Save failed";
        showToast(payload.message || "Notes save failed.", "error");
        return false;
      }
      if (indicator) indicator.textContent = "Saved";
      return true;
    } catch {
      if (indicator) indicator.textContent = "Save failed";
      showToast("Notes save failed.", "error");
      return false;
    }
  };
  const debounced = debounce(save, 500);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (await save()) showToast("Notes saved.", "success");
  });
  form.querySelector("textarea")?.addEventListener("input", debounced);
}

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => fn(...args), delay);
  };
}
