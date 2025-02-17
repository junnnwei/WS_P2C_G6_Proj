document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript Loaded!"); // Debugging

    let testButton = document.getElementById("test-captcha-btn");
    let modal = document.getElementById("recaptcha-modal");
    let overlay = document.getElementById("overlay");

    if (testButton) {
        console.log("Test button found!");

        testButton.addEventListener("click", function() {
            console.log("Test button clicked! Showing reCAPTCHA modal...");
            showRecaptchaModal();
        });
    } else {
        console.error("❌ Test button NOT found in the DOM!");
    }

    function showRecaptchaModal() {
        console.log("Showing modal..."); 
        overlay.style.display = "block";
        modal.style.display = "block";
    }

    function closeRecaptchaModal() {
        console.log("Closing modal..."); 
        overlay.style.display = "none";
        modal.style.display = "none";
    }
});

document.addEventListener("analysisMetricsReceived", function(event) {
    const analysisData = event.detail;
    console.log("Received data in recaptcha.js:", analysisData);

    fetch("/api/detect_bot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(analysisData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Bot Probability:", data.bot_probability);
        console.log("CAPTCHA Level:", data.captcha_level);

        let captchaContainer = document.getElementById("captcha-container");

        if (data.captcha_level === "easy") {
            captchaContainer.innerHTML = '<p>what is 2 + 1?.</p>';
        } else if (data.captcha_level === "medium") {
            captchaContainer.innerHTML = '<p>Is Wing keong Gay?.</p>';
        } else if (data.captcha_level === "hard") {
            captchaContainer.innerHTML = `<p>Maintain 5.0 GPA!.</p>`;
        } else {
            captchaContainer.innerHTML = "<p>Testing</p><div id='recaptcha-widget'></div>";
        
            // Wait a short delay, then render reCAPTCHA manually
            setTimeout(() => {
                grecaptcha.render('recaptcha-widget', {
                    'sitekey': '6LeUmNkqAAAAANBp8Po0WfjnkWEqS32W_mW2qc6m'
                });
            }, 100); // Small delay to ensure the DOM is updated
        }
        
    })
    .catch(error => console.error("Error in reCAPTCHA handling:", error));
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
