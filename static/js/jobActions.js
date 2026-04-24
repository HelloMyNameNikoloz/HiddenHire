export function initJobActions() {
  const modal = document.querySelector("[data-delete-modal]");
  const openButton = document.querySelector("[data-open-delete-modal]");
  if (!modal || !openButton) return;
  openButton.addEventListener("click", () => modal.showModal());
  modal.addEventListener("click", (event) => {
    if (event.target === modal) modal.close();
  });
}
