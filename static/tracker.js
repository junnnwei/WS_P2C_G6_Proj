let analysisMetrics = {
    sessionID: null,
    movementData: [], // Tracks mouse movement, clicks, and scroll events
    mouseMovements: 0,
    mouseDistance: 0,
    directionChanges: 0,
    keyPresses: 0,
    timeSpent: 0,
    formId: "",
    fieldInteractions: {},
    userInformation: "",
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

/** This section tracks for user's mouse movements **/
let lastMouseX = null;
let lastMouseY = null;
let lastDirectionChange = null;
let totalDistance = 0;
const DIRECTION_CHANGE_THRESHOLD = Math.PI / 4; // 45 degrees threshold for direction changes

document.addEventListener('mousemove', (event) => {
    const mouseX = event.clientX;
    const mouseY = event.clientY;

    // Log only movementData with throttling
    throttledLogEvent('move', mouseX, mouseY);

    // Update mouse movements
    analysisMetrics.mouseMovements++;

    // Calculate distance traveled
    if (lastMouseX !== null && lastMouseY !== null) {
        const deltaX = mouseX - lastMouseX;
        const deltaY = mouseY - lastMouseY;
        const distance = Math.sqrt(deltaX ** 2 + deltaY ** 2);
        totalDistance += distance;
        analysisMetrics.mouseDistance = totalDistance;
    }

    // Track direction changes
    const deltaX = mouseX - lastMouseX;
    const deltaY = mouseY - lastMouseY;
    const direction = Math.atan2(deltaY, deltaX);
    if (lastDirectionChange !== null) {
        let directionDifference = Math.abs(direction - lastDirectionChange);
        if (directionDifference > Math.PI) {
            directionDifference = 2 * Math.PI - directionDifference;
        }
        if (directionDifference > DIRECTION_CHANGE_THRESHOLD) {
            analysisMetrics.directionChanges++;
            lastDirectionChange = direction;
        }
    } else {
        lastDirectionChange = direction;
    }

    lastMouseX = mouseX;
    lastMouseY = mouseY;
});

// Click listener for capturing clicks
document.addEventListener('click', (event) => {
    const { clientX: x, clientY: y } = event;
    const timestamp = Date.now();
    analysisMetrics.movementData.push(`click-${x}-${y}-${timestamp}`); // Log clicks without throttling
});

/** This portion tracks the duration between each key input **/
let lastKeyPressTime = null;

document.addEventListener('keydown', (event) => {
    analysisMetrics.keyPresses++;
    const currentKeyPressTime = Date.now();

    if (lastKeyPressTime !== null) {
        const interval = currentKeyPressTime - lastKeyPressTime;
        analysisMetrics.keyPressIntervals.push(interval);
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
    analysisMetrics.userInformation = getUserInformation();
});

document.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent form submission for testing
    analysisMetrics.timeSpent = Math.floor((Date.now() - startTime) / 1000);
    analysisMetrics.sessionID = sessionID;
    sendAnalysisMetrics();
});

/** Retrieves additional user information **/
function getUserInformation() {
    const timezoneOffset = new Date().getTimezoneOffset();
    const timezone = timezoneOffset < 0 ? `GMT+${-timezoneOffset / 60}` : `GMT-${timezoneOffset / 60}`;

    return [
        `width:${window.innerWidth}`,
        `height:${window.innerHeight}`,
        `pixelRatio:${window.devicePixelRatio}`,
        `userAgent:${navigator.userAgent}`,
        `platform:${navigator.platform}`,
        `language:${navigator.language}`,
        `timezone:${timezone}`,
    ].join(';');
}

/** Sends the data to the backend **/
function sendAnalysisMetrics() {
    console.log("Sending data:", analysisMetrics);

    fetch('http://127.0.0.1:5000/api/analysis-metrics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(analysisMetrics),
    })
        .then((response) => response.json())
        .then((data) => console.log("Response from server:", data))
        .catch((error) => console.error("Error:", error));
}
