export function initToasts() {
  document.querySelectorAll("[data-toast]").forEach((toast) => dismissLater(toast));
  window.HiddenHireToast = showToast;
}

export function showToast(message, tone = "success") {
  const stack = document.querySelector("[data-toast-stack]");
  if (!stack) return;
  const toast = document.createElement("div");
  toast.className = `toast toast-${tone}`;
  toast.dataset.toast = "true";
  toast.textContent = message;
  stack.appendChild(toast);
  dismissLater(toast);
}

function dismissLater(toast) {
  window.setTimeout(() => toast.remove(), 3200);
}
