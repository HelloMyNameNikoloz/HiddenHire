export function initTheme() {
  const button = document.querySelector("[data-theme-toggle]");
  if (!button) return;
  const label = button.querySelector("[data-theme-label]");
  const applyTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    localStorage.setItem("hiddenhire.theme", theme);
    if (label) label.textContent = theme === "dark" ? "Dark mode" : "Light mode";
  };
  applyTheme(document.documentElement.dataset.theme || "light");
  button.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(next);
  });
}
