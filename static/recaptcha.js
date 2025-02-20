document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript Loaded!"); // Debugging

    let testButton = document.getElementById("test-captcha-btn");
    let modal = document.getElementById("recaptcha-modal");
    let overlay = document.getElementById("overlay");
});

document.addEventListener("analysisMetricsReceived", function(event) {
    const analysisData = event.detail;
    console.log("📥 Received data in recaptcha.js:", analysisData);

    fetch("/api/detect_bot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(analysisData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("🤖 Bot Probability:", data.bot_probability);
        console.log("🛡️ CAPTCHA Level:", data.captcha_level);

        let captchaContainer = document.getElementById("captcha-container");
        captchaContainer.innerHTML = ""; // Clear previous CAPTCHA
        
        const level = data.captcha_level; // Get the difficulty level (e.g., "easy")
        const url = `static/captcha_templates/${level}.html`; // Dynamically construct the correct URL
        
        console.log("Fetching CAPTCHA from:", url); // Debugging - Check if URL is correct
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                document.getElementById("captcha-container").innerHTML = html;
            })
            .catch(error => console.error("❌ Error in loading CAPTCHA template:", error));
        
        showRecaptchaModal();
    })
    .catch(error => console.error("❌ Error in reCAPTCHA handling:", error));
});


function showRecaptchaModal() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("recaptcha-modal").style.display = "block";
}

function closeRecaptchaModal() {
    console.log("Closing modal...");  // Debugging
    document.getElementById("overlay").style.display = "none";
    document.getElementById("recaptcha-modal").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function() {
    let closeBtn = document.querySelector(".close-btn");
    if (closeBtn) {
        closeBtn.addEventListener("click", closeRecaptchaModal);
    } else {
        console.error("❌ Close button not found!");
    }
});
