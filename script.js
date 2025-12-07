// ==================== CONFIGURATION ====================
// API Base URL configuration
// For production: Update this with your backend URL (e.g., "https://your-backend.railway.app")
// For local development: Leave as is (will auto-detect localhost)
const getApiBaseUrl = () => {
    const hostname = window.location.hostname;
    const port = window.location.port;
    
    // Local development - auto-detect
    if (hostname === "localhost" || hostname === "127.0.0.1") {
        if (port === "3000" || port === "5500" || port === "") {
            return "http://localhost:8000";
        }
    }
    
    // Production - UPDATE THIS with your backend URL
    // Example: "https://dermavision-api.railway.app"
    // Or set via Netlify environment variable and use build-time replacement
    const PRODUCTION_API_URL = ""; // ⚠️ UPDATE THIS with your backend URL
    
    if (PRODUCTION_API_URL) {
        return PRODUCTION_API_URL;
    }
    
    // Fallback: empty string (relative path - only works if backend is on same domain)
    return "";
};

const API_BASE_URL = getApiBaseUrl();
const ENDPOINTS = {
    predict: `${API_BASE_URL}/predict`,
    info: `${API_BASE_URL}/info`,
};

// Class information for the Learn tab
const LESION_INFO = {
    Benign: {
        title: "Benign Lesion",
        description: "This lesion appears to be benign. Benign lesions are non-cancerous and generally safe.",
        details: [
            "Benign lesions are non-cancerous growths",
            "They typically have regular borders and consistent coloring",
            "Most are harmless and don't require medical treatment",
            "However, always monitor for any changes and consult a dermatologist if needed"
        ]
    },
    Malignant: {
        title: "Malignant Lesion",
        description: "This lesion shows characteristics of malignancy. Medical consultation is recommended.",
        details: [
            "Malignant lesions are potentially cancerous",
            "Look for asymmetry, irregular borders, and color variation",
            "Early detection and treatment significantly improve outcomes",
            "CONSULT A DERMATOLOGIST IMMEDIATELY for professional evaluation"
        ]
    }
};

// ==================== DOM ELEMENTS ====================
const modal = document.getElementById("safetyModal");
const acceptCheckbox = document.getElementById("acceptCheckbox");
const continueBtn = document.getElementById("continueBtn");
const mainApp = document.getElementById("mainApp");

const themeToggle = document.getElementById("themeToggle");
const uploadBox = document.getElementById("uploadBox");
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const previewImg = document.getElementById("previewImg");
const removeImageBtn = document.getElementById("removeImageBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const loadingSpinner = document.getElementById("loadingSpinner");

const predictionResult = document.getElementById("predictionResult");
const resultClass = document.getElementById("resultClass");
const confidenceText = document.getElementById("confidenceText");
const confidenceFill = document.getElementById("confidenceFill");
const confidenceBand = document.getElementById("confidenceBand");
const probBenign = document.getElementById("probBenign");
const probMalignant = document.getElementById("probMalignant");
const probBenignValue = document.getElementById("probBenignValue");
const probMalignantValue = document.getElementById("probMalignantValue");
const infoCard = document.getElementById("infoCard");
const inferenceTime = document.getElementById("inferenceTime");
const closeResult = document.querySelector(".close-result");
const historyList = document.getElementById("historyList");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");

const navTabs = document.querySelectorAll(".nav-tab");
const tabContents = document.querySelectorAll(".tab-content");

// ==================== STATE ====================
let currentImage = null;
let sessionHistory = JSON.parse(localStorage.getItem("dermavision_history")) || [];

// ==================== INITIALIZATION ====================
window.addEventListener("DOMContentLoaded", () => {
    initTheme();
    loadSessionHistory();
    attachEventListeners();
    console.log("✓ DermaVision app initialized");
});

// ==================== THEME MANAGEMENT ====================
function initTheme() {
    const savedTheme = localStorage.getItem("dermavision_theme") || "dark-mode";
    document.body.className = savedTheme;
    updateThemeIcon();
}

function updateThemeIcon() {
    const isDarkMode = document.body.classList.contains("dark-mode");
    themeToggle.textContent = isDarkMode ? "☀️" : "🌙";
}

themeToggle.addEventListener("click", () => {
    const isDarkMode = document.body.classList.contains("dark-mode");

    if (isDarkMode) {
        document.body.classList.remove("dark-mode");
        document.body.classList.add("light-mode");
        localStorage.setItem("dermavision_theme", "light-mode");
    } else {
        document.body.classList.remove("light-mode");
        document.body.classList.add("dark-mode");
        localStorage.setItem("dermavision_theme", "dark-mode");
    }

    updateThemeIcon();
});

// ==================== MODAL MANAGEMENT ====================
acceptCheckbox.addEventListener("change", () => {
    continueBtn.disabled = !acceptCheckbox.checked;
});

continueBtn.addEventListener("click", () => {
    modal.classList.remove("modal-active");
    mainApp.style.display = "flex";
    localStorage.setItem("dermavision_modal_accepted", "true");
});

// Check if user already accepted
window.addEventListener("load", () => {
    const accepted = localStorage.getItem("dermavision_modal_accepted");
    if (accepted) {
        modal.classList.remove("modal-active");
    }
});

// ==================== EVENT LISTENERS ====================
function attachEventListeners() {
    // File upload
    uploadBox.addEventListener("click", () => imageInput.click());
    imageInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) displayImagePreview(file);
    });

    // Drag and drop
    uploadBox.addEventListener("dragover", (e) => {
        e.preventDefault();
        uploadBox.classList.add("dragover");
    });
    uploadBox.addEventListener("dragleave", () => {
        uploadBox.classList.remove("dragover");
    });
    uploadBox.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadBox.classList.remove("dragover");
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            imageInput.files = files;
            const file = files[0];
            if (file) displayImagePreview(file);
        }
    });

    // Buttons
    removeImageBtn.addEventListener("click", removeImage);
    analyzeBtn.addEventListener("click", () => {
        if (!currentImage) {
            showNotification("Please upload an image first.", "error");
            return;
        }
        makePrediction(currentImage);
    });
    clearBtn.addEventListener("click", clearAll);
    closeResult.addEventListener("click", () => {
        predictionResult.classList.add("hidden");
    });
    clearHistoryBtn.addEventListener("click", clearHistory);

    // Tab navigation
    navTabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            const tabName = tab.dataset.tab;
            navTabs.forEach((t) => t.classList.remove("active"));
            tab.classList.add("active");
            tabContents.forEach((content) => content.classList.remove("active"));
            document.getElementById(`${tabName}Tab`).classList.add("active");
        });
    });

    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "k") {
            e.preventDefault();
            imageInput.click();
        }
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            if (!analyzeBtn.disabled) analyzeBtn.click();
        }
    });
}

// ==================== FILE UPLOAD HANDLING ====================
function displayImagePreview(file) {
    const validTypes = ["image/jpeg", "image/png", "image/webp"];
    if (!validTypes.includes(file.type)) {
        showNotification("Invalid file type. Please upload JPG, PNG, or WebP.", "error");
        return;
    }

    if (file.size > 5 * 1024 * 1024) {
        showNotification("File too large. Maximum size is 5MB.", "error");
        return;
    }

    currentImage = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        imagePreview.classList.remove("hidden");
        uploadBox.style.display = "none";
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    currentImage = null;
    imageInput.value = "";
    imagePreview.classList.add("hidden");
    uploadBox.style.display = "block";
    analyzeBtn.disabled = true;
    predictionResult.classList.add("hidden");
}

function clearAll() {
    removeImage();
    showNotification("Cleared all", "success");
}

// ==================== PREDICTION ====================
async function makePrediction(file) {
    loadingSpinner.classList.remove("hidden");
    analyzeBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(ENDPOINTS.predict, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Prediction failed");
        }

        const data = await response.json();
        displayPredictionResult(data);
        addToHistory(data);

    } catch (error) {
        console.error("Prediction error:", error);
        showNotification(`Error: ${error.message}`, "error");
    } finally {
        loadingSpinner.classList.add("hidden");
        analyzeBtn.disabled = false;
    }
}

function displayPredictionResult(data) {
    const classInfo = LESION_INFO[data.predicted_class];

    resultClass.innerHTML = `<div class="result-class-name ${data.predicted_class.toLowerCase()}">${data.predicted_class}</div>`;
    confidenceText.textContent = `Confidence: ${data.confidence_percentage}%`;
    confidenceFill.style.width = `${data.confidence_percentage}%`;

    confidenceBand.textContent = `${data.confidence_band} Confidence`;
    confidenceBand.className = `${data.confidence_band.toLowerCase()}`;

    const benignProb = data.probabilities.Benign * 100;
    const malignantProb = data.probabilities.Malignant * 100;

    probBenign.style.width = `${benignProb}%`;
    probMalignant.style.width = `${malignantProb}%`;
    probBenignValue.textContent = `${benignProb.toFixed(1)}%`;
    probMalignantValue.textContent = `${malignantProb.toFixed(1)}%`;

    infoCard.className = `info-card ${data.predicted_class.toLowerCase()}`;
    infoCard.innerHTML = `<h3>ℹ️ ${classInfo.title}</h3><p>${classInfo.description}</p><ul>${classInfo.details.map(detail => `<li>${detail}</li>`).join("")}</ul>`;

    inferenceTime.textContent = data.inference_time_ms;
    predictionResult.classList.remove("hidden");
}

// ==================== SESSION HISTORY ====================
function addToHistory(prediction) {
    const historyItem = {
        id: Date.now(),
        class: prediction.predicted_class,
        confidence: prediction.confidence_percentage,
        band: prediction.confidence_band,
        timestamp: new Date().toLocaleTimeString(),
        probabilities: prediction.probabilities
    };

    sessionHistory.unshift(historyItem);
    if (sessionHistory.length > 20) sessionHistory = sessionHistory.slice(0, 20);

    localStorage.setItem("dermavision_history", JSON.stringify(sessionHistory));
    renderSessionHistory();
}

function loadSessionHistory() {
    sessionHistory = JSON.parse(localStorage.getItem("dermavision_history")) || [];
    renderSessionHistory();
}

function renderSessionHistory() {
    if (sessionHistory.length === 0) {
        historyList.innerHTML = '<p class="history-empty">No predictions yet. Upload an image to get started.</p>';
        clearHistoryBtn.style.display = "none";
        return;
    }

    historyList.innerHTML = sessionHistory.map((item) => `
        <div class="history-item" onclick="loadHistoryItem(${item.id})">
            <div class="history-item-class">
                <div class="history-item-label">Prediction</div>
                <div class="history-item-name">${item.class}</div>
            </div>
            <span class="history-item-badge ${item.class.toLowerCase()}">${item.confidence.toFixed(1)}%</span>
        </div>
    `).join("");

    clearHistoryBtn.style.display = "block";
}

function loadHistoryItem(id) {
    const item = sessionHistory.find(h => h.id === id);
    if (item) {
        const prediction = {
            predicted_class: item.class,
            confidence_percentage: item.confidence,
            confidence_band: item.band,
            probabilities: item.probabilities,
            inference_time_ms: 0
        };
        displayPredictionResult(prediction);
        predictionResult.classList.remove("hidden");
    }
}

function clearHistory() {
    if (confirm("Are you sure you want to clear all history?")) {
        sessionHistory = [];
        localStorage.removeItem("dermavision_history");
        renderSessionHistory();
        showNotification("History cleared", "success");
    }
}

// ==================== UTILITIES ====================
function showNotification(message, type = "info") {
    console.log(`[${type.toUpperCase()}] ${message}`);
    if (type === "error") {
        alert(message);
    }
}

// ==================== API HEALTH CHECK ====================
async function checkAPIHealth() {
    try {
        const response = await fetch(ENDPOINTS.info);
        if (response.ok) {
            console.log("✓ Backend API is healthy");
            return true;
        }
    } catch (error) {
        console.warn("⚠️ Backend API is not responding. Make sure it's running on port 8000");
    }
    return false;
}

// Check API on load
window.addEventListener("load", () => {
    setTimeout(checkAPIHealth, 500);
});

// ==================== EXPORT FUNCTIONS ====================
window.loadHistoryItem = loadHistoryItem;
