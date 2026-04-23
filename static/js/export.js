export function initExport() {
  const form = document.querySelector("[data-filter-form]");
  if (!form) return;
  const sync = () => {
    const params = new URLSearchParams(new FormData(form));
    document.querySelectorAll("[data-export-link]").forEach((link) => {
      link.href = `/export?${params.toString()}`;
    });
  };
  sync();
  document.addEventListener("filters:updated", sync);
  form.addEventListener("change", sync);
}
