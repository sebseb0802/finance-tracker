function showSuccessToast(message, duration=3000) {
    var success_toast = document.getElementById("success-toast");
    var success_toast_text = document.getElementById("success-toast-text");
    success_toast_text.textContent = message;
    success_toast.className = "success-toast show";
    setTimeout(function() {
        success_toast.className = "success-toast"
    }, duration);
}

document.addEventListener("DOMContentLoaded", function() {
    var message = document.getElementById("success-message")?.dataset.message;
    if (message) {
        showSuccessToast(message);
    }
});