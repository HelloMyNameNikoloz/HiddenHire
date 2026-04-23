export function initUpload() {
  const form = document.querySelector("[data-upload-form]");
  const dropzone = document.querySelector("[data-dropzone]");
  const input = document.querySelector("[data-file-input]");
  const fileName = document.querySelector("[data-file-name]");
  if (!form || !dropzone || !input || !fileName) return;
  const updateName = () => {
    fileName.textContent = input.files?.[0]?.name || "No file selected";
  };
  ["dragenter", "dragover"].forEach((name) =>
    dropzone.addEventListener(name, (event) => {
      event.preventDefault();
      dropzone.classList.add("is-dragover");
    }),
  );
  ["dragleave", "drop"].forEach((name) =>
    dropzone.addEventListener(name, (event) => {
      event.preventDefault();
      dropzone.classList.remove("is-dragover");
    }),
  );
  dropzone.addEventListener("drop", (event) => {
    input.files = event.dataTransfer.files;
    updateName();
  });
  input.addEventListener("change", updateName);
}
