window.captchaPassed = false;

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

        const level = data.captcha_level; // Get the difficulty level (e.g., "easy")

        if (level === "none") {
            console.log("✅ No CAPTCHA required.");
            return; // Skip CAPTCHA rendering
        }

        if (data.redirect) {
            window.location.href = data.redirect; // Redirect to the blocked page
        }

        captchaContainer.innerHTML = ""; // Clear previous CAPTCHA
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
                executeCaptchaScript(level);
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


function executeCaptchaScript(level) {
    if (level === "easy") {
        generateMathCaptcha();
    }
}

/** ✅ Math CAPTCHA Logic */
function generateMathCaptcha() {
    let num1 = Math.floor(Math.random() * 10);
    let num2 = Math.floor(Math.random() * 10);
    document.getElementById("math-problem").textContent = `${num1} + ${num2} = ?`;
    window.mathCaptchaAnswer = num1 + num2;
    
}

function checkMathCaptcha() {
    let userAnswer = parseInt(document.getElementById("math-answer").value);
    if (userAnswer === window.mathCaptchaAnswer) {
        alert("Correct! Submitting form...");
        window.captchaPassed = true;
        closeRecaptchaModal();
        //document.getElementById("login-form").submit();
    } else {
        alert("❌ Incorrect! Try again.");
        //window.captchaPassed = false;
    }
}

function checkImageCaptcha() {
    let userAnswer = document.getElementById("image-answer")?.value.trim().toLowerCase();
    let correctAnswer = "ben tan";
    if (userAnswer === correctAnswer) {
        alert("Correct! Submitting form...");
        window.captchaPassed = true;
        closeRecaptchaModal();
        //document.getElementById("login-form").submit();
    } else {
        alert("Incorrect! Try again.");
        //window.captchaPassed = false;
    }
}
function checkTextCaptcha(isCorrect) {
    //Prevent multiple button clicks from interfering
    document.querySelectorAll("button[onclick^='checkTextCaptcha']").forEach(btn => btn.disabled = true);

    if (isCorrect) {
        alert("Correct! Submitting form...");
        window.captchaPassed = true;
        closeRecaptchaModal();

    } else {
        alert("Incorrect! Try again.");
        
        //Re-enable buttons after incorrect attempt
        document.querySelectorAll("button[onclick^='checkTextCaptcha']").forEach(btn => btn.disabled = false);
    }
}


