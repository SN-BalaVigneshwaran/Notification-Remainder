document.addEventListener("DOMContentLoaded", function () {
    // Ask for permission to show notifications
    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }

    // Check every 5 seconds for a match
    setInterval(checkReminder, 5000);
});

// Intercept form submission
document.addEventListener("submit", function (e) {
    e.preventDefault(); // Stop form from redirecting

    const url = document.getElementById("url").value;
    const time = document.getElementById("time").value;

    if (!url || !time) {
        alert("Please fill both URL and time!");
        return;
    }

    // Save reminder locally
    localStorage.setItem("reminderData", JSON.stringify({
        url: url,
        time: time
    }));

    alert("Reminder set! Keep this tab open.");
});

// Checks if it's time to show notification
function checkReminder() {
    const data = JSON.parse(localStorage.getItem("reminderData"));
    if (!data) return;

    const now = new Date();
    const reminderTime = new Date(data.time);

    // Match up to minute
    if (
        now.getFullYear() === reminderTime.getFullYear() &&
        now.getMonth() === reminderTime.getMonth() &&
        now.getDate() === reminderTime.getDate() &&
        now.getHours() === reminderTime.getHours() &&
        now.getMinutes() === reminderTime.getMinutes()
    ) {
        localStorage.removeItem("reminderData");

        // Show browser notification
        if (Notification.permission === "granted") {
            const notification = new Notification("🔔 Time for your reminder!", {
                body: "Click to open: " + data.url,
                icon: "https://cdn-icons-png.flaticon.com/512/565/565340.png"
            });

            notification.onclick = () => {
                window.open(data.url, "_blank");
            };
        } else {
            // Fallback: redirect
            window.location.href = data.url;
        }
    }
}
