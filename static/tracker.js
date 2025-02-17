let analysisMetrics = {
    sessionID: null,
    movementData: [], // Tracks mouse movement, clicks, and scroll events
    totalKeyInputs: 0,
    totalTimeSpentOnPage: 0,
    averageTimePerField: 0,
    formId: "",
    fieldInteractions: {},
    width: 0,
    height: 0,
    pixelRatio: 0,
    userAgent: "",
    platform: "",
    language: "",
    timezone: "",
    keyPressIntervals: [],
};

// Generate sessionID as UID for backend processing across different records
if (!localStorage.getItem('sessionID')) {
    localStorage.setItem('sessionID', Math.random().toString(36).substr(2, 9));
}
const sessionID = localStorage.getItem('sessionID');

// Utility function for throttling
function throttle(callback, delay) {
    let lastExecutionTime = 0;
    return function (...args) {
        const now = Date.now();
        if (now - lastExecutionTime >= delay) {
            lastExecutionTime = now;
            callback(...args);
        }
    };
}

// Throttled version of logEvent for movementData
const throttledLogEvent = throttle((action, x, y) => {
    const timestamp = Date.now();
    const roundedX = Math.round(x / 10) * 10; // Reduce data precision
    const roundedY = Math.round(y / 10) * 10; // Reduce data precision
    analysisMetrics.movementData.push(`${action}-${roundedX}-${roundedY}-${timestamp}`);
}, 100); // Throttle movementData to once every 100ms

// /** This section tracks for user's mouse movements **/
let lastMouseX = null;
let lastMouseY = null;
document.addEventListener('mousemove', (event) => {
    const mouseX = event.clientX;
    const mouseY = event.clientY;
    // Log only movementData with throttling
    throttledLogEvent('move', mouseX, mouseY);

    lastMouseX = mouseX;
    lastMouseY = mouseY;
});

/** This portion tracks how long a user spends on each field **/
// Key press tracking
let fieldFocusTimes = {};

document.addEventListener('focus', (event) => {
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        const fieldName = event.target.name || event.target.id;
        const fieldType = event.target.type || 'text'; // Default to 'text' if type is not specified

         // Initialize field interaction if not already done
        if (!analysisMetrics.fieldInteractions[fieldName]) {
            analysisMetrics.fieldInteractions[fieldName] = { keyPressCount: 0, timeSpent: 0, inputType: fieldType };
        }

        // Store the timestamp when the field is focused
        fieldFocusTimes[fieldName] = Date.now();
        // console.log(`Focus event for ${fieldName}:`, fieldFocusTimes); // Log the fieldFocusTimes to check
    }
}, true);

document.addEventListener('blur', (event) => {
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        const fieldName = event.target.name || event.target.id;
        const fieldType = event.target.type || 'text'; // Default to 'text' if type is not specified

        // Check if the focus time exists for the field
        if (fieldFocusTimes[fieldName]) {
            const focusTime = fieldFocusTimes[fieldName];
            const blurTime = Date.now();
            const timeSpent = blurTime - focusTime; // Calculate the time spent on the field

            // Update the fieldInteractions with the time spent
            if (!analysisMetrics.fieldInteractions[fieldName]) {
                analysisMetrics.fieldInteractions[fieldName] = { keyPressCount: 0, timeSpent: 0, inputType: fieldType};
            }

            // Add the time spent to the fieldInteractions
            analysisMetrics.fieldInteractions[fieldName].timeSpent += timeSpent;

            delete fieldFocusTimes[fieldName];  // Clean up the fieldFocusTimes after processing
        }
    }
}, true);
// Click listener for capturing clicks
document.addEventListener('click', (event) => {
    const { clientX: x, clientY: y } = event;
    const timestamp = Date.now();
    analysisMetrics.movementData.push(`click-${x}-${y}-${timestamp}`); // Log clicks without throttling
});

/** This portion tracks the duration between each key input **/
let lastKeyPressTime = null;

// Add: Reset time tracking when window out of focus
window.addEventListener("blur", () => {
    lastKeyPressTime = null; // Reset key tracking when page loses focus
});

document.addEventListener('keydown', (event) => {
    analysisMetrics.totalKeyInputs++;

    const currentKeyPressTime = Date.now();

    // if (lastKeyPressTime !== null) {
    //     const interval = currentKeyPressTime - lastKeyPressTime;
    //     analysisMetrics.keyPressIntervals.push(interval);
    // }

    if (lastKeyPressTime === null) {
        lastKeyPressTime = currentKeyPressTime; // Reset without recording a long interval
    } else {
        const interval = currentKeyPressTime - lastKeyPressTime;
        analysisMetrics.keyPressIntervals.push(interval);
        lastKeyPressTime = currentKeyPressTime;
    }

    const activeElement = document.activeElement;
    if (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA') {
        const fieldName = activeElement.name || activeElement.id;
        if (!analysisMetrics.fieldInteractions[fieldName]) {
            analysisMetrics.fieldInteractions[fieldName] = { keyPressCount: 0, timeSpent: 0 };
        }
        analysisMetrics.fieldInteractions[fieldName].keyPressCount++;
    }

    lastKeyPressTime = currentKeyPressTime;
});

/** This tracks how long a user spends per page **/
let startTime = Date.now();
window.addEventListener('load', () => {
    analysisMetrics.formId = document.querySelector('form')?.id || "unknown-form";
    analysisMetrics.width = window.innerWidth;
    analysisMetrics.height = window.innerHeight;
    analysisMetrics.pixelRatio = window.devicePixelRatio;
    analysisMetrics.userAgent = navigator.userAgent;
    analysisMetrics.platform = navigator.platform;
    analysisMetrics.language = navigator.language;

    const timezoneOffset = new Date().getTimezoneOffset();
    const timezone = timezoneOffset < 0 ? `GMT+${-timezoneOffset / 60}` : `GMT-${timezoneOffset / 60}`;
    analysisMetrics.timezone = timezone;
});

document.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent form submission for testing

    analysisMetrics.totalTimeSpentOnPage = Date.now() - startTime;

    // Send the data to the backend
    analysisMetrics.sessionID = sessionID;

     // Subtract 1 for the submit button
    const numberOfFields = Object.keys(analysisMetrics.fieldInteractions).length - 1;
    if (numberOfFields > 0) {
        analysisMetrics.averageTimePerField = analysisMetrics.totalTimeSpentOnPage / numberOfFields;
    } else {
        analysisMetrics.averageTimePerField = 0.0;
    }

    sendAnalysisMetrics();
});

/** Sends the data to the backend **/
function sendAnalysisMetrics() {
    console.log("Sending data:", analysisMetrics);

    fetch('http://127.0.0.1:5000/api/analysis-metrics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(analysisMetrics),
    })
        .then((response) => response.json())
        .then((data) => {console.log("Response from server:", data)

            let userMetrics = {
                totalTimeSpentOnPage: analysisMetrics.totalTimeSpentOnPage,
                averageTimePerField: analysisMetrics.averageTimePerField,
                mousespeed_sd: data.mousespeed_sd,
                keystroke_sd: data.keystroke_sd,
                user_agent: navigator.userAgent
            };
            // Dispatch event to send user data to the recaptcha.js for detection and other shit
            document.dispatchEvent(new CustomEvent('analysisMetricsReceived', { detail: userMetrics }));
        })
        .catch((error) => console.error("Error:", error));

    // send information to bot detection 
    
}

// Form submission event to clear input fields
document.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent actual form submission
    event.target.reset(); // Clear input fields and textarea
    
    // Reset analysis metrics for new session
    analysisMetrics.totalKeyInputs = 0;
    averageTimePerField = 0;
    analysisMetrics.keyPressIntervals = [];
    analysisMetrics.fieldInteractions = {};
    lastKeyPressTime = null;
    analysisMetrics.movementData = [];
    
    console.log("Form submitted and inputs cleared.");
});

