document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("open-sidebar").onclick = function() {
        document.getElementById("sidebar").classList.add("open");
    };
    document.getElementById("close-sidebar").onclick = function() {
        document.getElementById("sidebar").classList.remove("open");
    };
});