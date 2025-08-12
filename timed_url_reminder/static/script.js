function scheduleReminder() {
    const url = document.getElementById("urlInput").value.trim();
    const time = document.getElementById("timeInput").value;

    if (!url || !time) {
        document.getElementById("status").innerText = "Please enter both URL and time.";
        return;
    }

    fetch("/schedule", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url, time: time })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("status").innerText = data.message;
    })
    .catch(error => {
        document.getElementById("status").innerText = "Error scheduling reminder.";
    });
}
