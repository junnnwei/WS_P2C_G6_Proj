let analysisMetrics = {
    sessionID: null,
    mouseMovements: 0,
    mouseDistance: 0,
    directionChanges: 0,
    keyPresses: 0,
    timeSpent: 0,
    formId: "",
    fieldInteractions: {},
    userInformation: "",
    keyPressIntervals: [], // Added key press interval tracking

    // comment this out first & we'll see if we actually need this; abit too difficult to analyze with ML
    // canvasFingerprint: "";
};

// generate sessionID as UID for backend processing across different records
if (!localStorage.getItem('sessionID')) {
    localStorage.setItem('sessionID', Math.random().toString(36).substr(2, 9));  // Store unique session ID
}

// Retrieve session ID for tracking
const sessionID = localStorage.getItem('sessionID');

/** This section tracks for user's mouse movements **/
let lastMouseX = null;
let lastMouseY = null;
let lastDirectionChange = null;
let totalDistance = 0;
// let directionChanges = 0;
// const MAX_DIRECTION_CHANGE_INTERVAL = 500; // 500ms max between direction changes
const DIRECTION_CHANGE_THRESHOLD = Math.PI / 4; // 45 degrees threshold for significant direction change

document.addEventListener('mousemove', (event) => {
    analysisMetrics.mouseMovements++;  // Update the mouseMovements inside analysisMetrics object

    const mouseX = event.clientX;
    const mouseY = event.clientY;

    if (lastMouseX !== null && lastMouseY !== null) {
        const deltaX = mouseX - lastMouseX;
        const deltaY = mouseY - lastMouseY;
        const distance = Math.sqrt(deltaX ** 2 + deltaY ** 2);

        totalDistance += distance;
        analysisMetrics.mouseDistance = totalDistance;
    }

    // Track direction changes
    if (lastMouseX !== null && lastMouseY !== null) {
        const deltaX = mouseX - lastMouseX;
        const deltaY = mouseY - lastMouseY;
        const direction = Math.atan2(deltaY, deltaX); // Direction in radians

        if (lastDirectionChange !== null) {
            let directionDifference = Math.abs(direction - lastDirectionChange);

            // Account for wrapping of angle between -π and π
            if (directionDifference > Math.PI) {
                directionDifference = 2 * Math.PI - directionDifference;
            }

            // Check if the direction change is significant enough
            if (directionDifference > DIRECTION_CHANGE_THRESHOLD) {
                analysisMetrics.directionChanges++;
                lastDirectionChange = direction;
            }

        } else {
            lastDirectionChange = direction; // set lastDirectionChange to initialized direction
        }
    }

    lastMouseX = mouseX;
    lastMouseY = mouseY;
});

/** This portion tracks how long a user spends on each field **/
// Key press tracking
let lastKeyPressTime = null;
let fieldFocusTimes = {};

document.addEventListener('focus', (event) => {
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        const fieldName = event.target.name || event.target.id;

        // Store the timestamp when the field is focused
        fieldFocusTimes[fieldName] = Date.now();
        // console.log(`Focus event for ${fieldName}:`, fieldFocusTimes); // Log the fieldFocusTimes to check
    }
}, true);

document.addEventListener('blur', (event) => {
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        const fieldName = event.target.name || event.target.id;

        // Check if the focus time exists for the field
        if (fieldFocusTimes[fieldName]) {
            const focusTime = fieldFocusTimes[fieldName];
            const blurTime = Date.now();
            const timeSpent = blurTime - focusTime; // Calculate the time spent on the field

            // Update the fieldInteractions with the time spent
            if (!analysisMetrics.fieldInteractions[fieldName]) {
                analysisMetrics.fieldInteractions[fieldName] = { keyPressCount: 0, timeSpent: 0 };
            }

            // Add the time spent to the fieldInteractions
            analysisMetrics.fieldInteractions[fieldName].timeSpent += timeSpent;

            delete fieldFocusTimes[fieldName];  // Clean up the fieldFocusTimes after processing
        }
    }
}, true);

/** This portion tracks the duration between each key input **/
// Track key press intervals
document.addEventListener('keydown', (event) => {
    analysisMetrics.keyPresses++;

    const currentKeyPressTime = Date.now();
    
    // Track key press intervals
    if (lastKeyPressTime !== null) {
        const interval = currentKeyPressTime - lastKeyPressTime;
        analysisMetrics.keyPressIntervals.push(interval);
    }
    
    // Track interaction with specific field types
    const activeElement = document.activeElement;
    if (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA') {
        const fieldName = activeElement.name || activeElement.id;
        if (!analysisMetrics.fieldInteractions[fieldName]) {
            // fix: 25/1/25 - initialize timeSpent to 0 here first since it's called first
            // excluding it will result in NaN timeSpent for focus & blur events
            analysisMetrics.fieldInteractions[fieldName] = { keyPressCount: 0, timeSpent: 0 };
        }
        analysisMetrics.fieldInteractions[fieldName].keyPressCount++;
    }
    
    lastKeyPressTime = currentKeyPressTime;
});

/** This tracks how long a user spends per page **/
// Start a timer when the page loads
let startTime = Date.now();
window.addEventListener('load', () => {
    analysisMetrics.formId = document.querySelector('form')?.id || "unknown-form";
    // same thing; we'll see how the progress goes
    // analysisMetrics.canvasFingerprint = getCanvasFingerprint();
    analysisMetrics.userInformation = getUserInformation();
});

// Stop the timer and send data when the form is submitted
document.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent form submission for testing
    analysisMetrics.timeSpent = Math.floor((Date.now() - startTime) / 1000);

    // Send the data to the backend
    analysisMetrics.sessionID = sessionID;
    sendAnalysisMetrics();
});

/** This section attempts to obtain a canvas fingerprint // commented out first due to complexity **/
// function getCanvasFingerprint() {
//     const canvas = document.createElement('canvas');
//     const ctx = canvas.getContext('2d');
//
//     // Set canvas dimensions
//     canvas.width = 200;
//     canvas.height = 100;
//
//     // Draw text with specific styles
//     ctx.textBaseline = "alphabetic";
//     ctx.font = "16px 'Times New Roman'";
//     ctx.fillStyle = "black";
//     ctx.fillText("Canvas Tracker", 20, 50);
//
//     // Draw shapes
//     ctx.fillStyle = "blue";
//     ctx.fillRect(20, 20, 80, 40);
//     ctx.strokeStyle = "green";
//     ctx.beginPath();
//     ctx.arc(150, 50, 30, 0, Math.PI * 2, true);
//     ctx.stroke();
//
//     // Get the canvas content as a data URL
//     const dataURL = canvas.toDataURL();
//
//     return dataURL;
// }

/** This section retrieves further information that may be useful, but spoofable **/
function getUserInformation() {
    const timezoneOffset = new Date().getTimezoneOffset();
    let timezone = "";

    if (timezoneOffset === -480) {
        timezone = "GMT+8";
    }

    else {
        const hoursOffset = Math.abs(timezoneOffset / 60);
        const sign = timezoneOffset < 0 ? '+' : '-';
        timezone = `GMT${sign}${hoursOffset}`;
    }

    const extraData = [
        `width:${window.innerWidth}`,
        `height:${window.innerHeight}`,
        `pixelRatio:${window.devicePixelRatio}`,
        `userAgent:${navigator.userAgent}`,
        `platform:${navigator.platform}`,
        `language:${navigator.language}`,
        `timezone:${timezone}`,
    ].join(';');

    return extraData;
}


/** This section sends the information from frontend to backend to conduct further processing **/
function sendAnalysisMetrics() {
    console.log("Sending data:", analysisMetrics);

    fetch('http://127.0.0.1:5000/api/analysis-metrics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(analysisMetrics)
    })
    .then(response => response.json())
    .then(data => console.log("Response from server:", data))
    .catch(error => console.error("Error:", error));
}