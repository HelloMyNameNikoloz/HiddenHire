import { showToast } from "./toasts.js";

const debounce = (fn, delay = 250) => {
  let timer;
  return (...args) => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => fn(...args), delay);
  };
};

export function initFilters() {
  const form = document.querySelector("[data-filter-form]");
  const results = document.querySelector("#dashboard-results");
  if (!form || !results) return;
  const refresh = debounce(async () => {
    try {
      const params = new URLSearchParams(new FormData(form));
      params.set("partial", "1");
      const response = await fetch(`/?${params.toString()}`, { headers: { "X-Requested-With": "fetch" } });
      if (!response.ok) throw new Error();
      results.innerHTML = await response.text();
      const url = new URL(window.location.href);
      url.search = new URLSearchParams(new FormData(form)).toString();
      window.history.replaceState({}, "", url);
      document.dispatchEvent(new CustomEvent("filters:updated"));
    } catch {
      showToast("Dashboard refresh failed.", "error");
    }
  }, 220);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    refresh();
  });
  form.addEventListener("change", refresh);
  form.addEventListener("input", (event) => {
    if (["search", "text", "number"].includes(event.target.type)) refresh();
  });
}
