# 🔬 DermaVision - Skin Lesion Classifier

A **research and educational** web application for binary skin lesion classification (Benign vs Malignant) using a trained CNN model.

> ⚠️ **IMPORTANT DISCLAIMER**: DermaVision is **NOT a medical device** and cannot be used for medical diagnosis or treatment decisions. Always consult a qualified dermatologist for any skin concerns.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Usage Guide](#-usage-guide)
- [Model Information](#-model-information)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📌 Project Overview

DermaVision is a full-stack web application that combines:
- **Backend**: FastAPI server for image processing and ML predictions
- **Frontend**: Modern responsive UI with dark/light mode support
- **Model**: Trained binary CNN classifier for skin lesion analysis

The application features a safety modal, image upload/preview, confidence scoring, session history, and an educational learning section.

### Key Features:
- ✅ Binary classification (Benign vs Malignant)
- ✅ Confidence scoring and bands (High/Medium/Low)
- ✅ Real-time prediction with inference timing
- ✅ Session history tracking
- ✅ Educational learning tab with ABCDE melanoma detection guide
- ✅ Dark/Light theme support
- ✅ Responsive mobile-friendly design
- ✅ Safety notice modal with legal disclaimers

---

## 🎨 Features

### Frontend Features
- **Safety Modal**: Mandatory disclaimer before app access
- **Image Upload**: Drag-and-drop or file picker
- **Image Preview**: Visual confirmation before analysis
- **Real-time Predictions**: Instant ML model inference
- **Confidence Visualization**: Progress bars and confidence bands
- **Probability Display**: Benign/Malignant probability distribution
- **Session History**: Track all predictions in current session
- **Learning Tab**: Educational information about skin lesions
- **ABCDE Rule**: Melanoma detection guidelines
- **Theme Toggle**: Dark/Light mode switching
- **Responsive Design**: Works on desktop, tablet, and mobile

### Backend Features
- **FastAPI Server**: Modern async web framework
- **Image Preprocessing**: Automatic resizing to 224×224
- **Model Loading**: Keras model integration
- **Confidence Calculation**: Intelligent confidence banding
- **Error Handling**: Comprehensive error responses
- **CORS Support**: Cross-origin requests enabled
- **API Documentation**: Auto-generated Swagger UI at `/docs`

---

## 🛠️ Tech Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom styling with CSS variables, Glass Morphism, animations
- **JavaScript (Vanilla)**: No frameworks, pure DOM manipulation
- **Local Storage**: Session persistence

### Backend
- **Python 3.8+**
- **FastAPI**: Async web framework
- **Uvicorn**: ASGI server
- **TensorFlow/Keras**: ML model loading and inference
- **Pillow**: Image processing
- **NumPy**: Numerical operations

### Model
- **Architecture**: CNN (Convolutional Neural Network)
- **Input Size**: 224×224 pixels
- **Output**: Binary classification (Benign/Malignant)
- **Format**: H5 (Keras) or KERAS format

---

## 📁 Project Structure

```
DERMAVISION_CNN/
│
├── backend/
│   ├── main.py                  # FastAPI application
│   ├── requirements.txt          # Python dependencies
│   └── models/
│       └── Dermavision_cnn.h5    # Trained model (place here)
│
├── frontend/
│   ├── index.html               # Main HTML
│   ├── styles.css               # Styling & theming
│   ├── script.js                # JavaScript logic
│
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda
- Modern web browser
- Your trained `Dermavision_cnn.h5` model file

### Step 1: Clone/Download Project
```bash
cd DERMAVISION_CNN
```

### Step 2: Set Up Backend

#### Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r backend/requirements.txt
```

This will install:
- fastapi==0.104.1
- uvicorn==0.24.0
- tensorflow==2.14.0
- keras==2.14.0
- pillow==10.1.0
- numpy==1.24.3
- python-multipart==0.0.6

### Step 3: Verify Model File
Ensure your trained model is at:
```
backend/models/Dermavision_cnn.h5
```

If the file has a different name or is elsewhere, update the `MODEL_PATH` in `backend/main.py`:
```python
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "YOUR_MODEL_NAME.h5")
```

### Step 4: Frontend Setup
No installation needed! The frontend runs directly in the browser. Simply open `frontend/index.html` in any modern browser, or serve it with a simple HTTP server:

```bash
# Python 3
python -m http.server 5500 --directory frontend

# Or using Node.js (if installed)
npx http-server frontend -p 5500
```

---

## 🎯 Running the Application

### Step 1: Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**API Documentation** is available at: `http://localhost:8000/docs`

### Step 2: Open Frontend

#### Option A: Direct Browser
Open `frontend/index.html` directly in your browser (file:// protocol).

#### Option B: Local Server (Recommended for CORS)
```bash
# In a new terminal
cd frontend
python -m http.server 5500 --directory .
```

Then visit: `http://localhost:5500`

### Step 3: Test the Application

1. Open `http://localhost:5500` in your browser
2. Read and accept the safety notice modal
3. Upload a skin lesion image (JPG, PNG, or WebP)
4. Click "Analyze Lesion"
5. View the prediction result and confidence score
6. Check the session history
7. Visit the "Learn" tab for educational information

---

## 📡 API Documentation

### Endpoints

#### 1. **POST /predict**
Make a prediction on an uploaded image.

**Request:**
```
POST /predict
Content-Type: multipart/form-data

file: <binary image data>
```

**Supported File Types:** JPG, PNG, WebP  
**Max File Size:** No hard limit (handled by FastAPI defaults)

**Response (200 OK):**
```json
{
  "predicted_class": "Benign",
  "class_index": 0,
  "confidence": 0.9234,
  "confidence_percentage": 92.34,
  "confidence_band": "High",
  "probabilities": {
    "Benign": 0.9234,
    "Malignant": 0.0766
  },
  "inference_time_ms": 145.23,
  "disclaimer": "⚠️ RESEARCH & EDUCATIONAL TOOL ONLY...",
  "timestamp": 1702000000.123
}
```

**Error Response (400/500):**
```json
{
  "detail": "Error message describing the issue"
}
```

#### 2. **GET /info**
Get API and model information.

**Response:**
```json
{
  "app_name": "DermaVision",
  "version": "1.0.0",
  "description": "Binary Skin Lesion Classifier (Benign vs Malignant)",
  "model_input_size": 224,
  "classes": {
    "0": "Benign",
    "1": "Malignant"
  },
  "confidence_thresholds": {
    "High": 0.8,
    "Medium": 0.6,
    "Low": 0.0
  },
  "model_path": "models/Dermavision_cnn.h5",
  "model_loaded": true,
  "disclaimer": "⚠️ RESEARCH & EDUCATIONAL TOOL ONLY..."
}
```

#### 3. **GET /**
Health check endpoint.

**Response:**
```json
{
  "status": "running",
  "model": "loaded",
  "app": "DermaVision API"
}
```

---

## 👤 Usage Guide

### For Users

1. **Initial Setup**
   - Ensure both backend and frontend are running
   - Open the frontend in your browser
   - Read and accept the safety notice

2. **Making Predictions**
   - Upload a skin lesion image (JPG, PNG, WebP)
   - Click "Analyze Lesion" button
   - Wait for the inference to complete
   - View the prediction and confidence score

3. **Understanding Results**
   - **Confidence Band**: Shows reliability of prediction
     - 🟢 **High** (≥80%): More reliable
     - 🟡 **Medium** (60-79%): Moderate reliability
     - 🔴 **Low** (<60%): Less reliable
   - **Probability Bars**: Visual representation of Benign vs Malignant scores

4. **Session History**
   - View all predictions made in current session
   - Click history items to revisit results
   - Clear history if needed

5. **Learning**
   - Click "Learn" tab to view educational content
   - Learn about different skin lesion types
   - Study the ABCDE melanoma detection rule

6. **Theme Toggle**
   - Click the sun/moon icon in the header
   - Switch between dark and light modes
   - Preference is saved locally

### For Developers

#### Customizing Model Path
Edit `backend/main.py`:
```python
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "your_model.h5")
```

#### Changing API Port
```bash
uvicorn main:app --port 9000
```

Update `API_BASE_URL` in `frontend/script.js`:
```javascript
const API_BASE_URL = "http://localhost:9000";
```

#### Adjusting Confidence Thresholds
Edit `backend/main.py`:
```python
CONFIDENCE_THRESHOLDS = {
    "High": 0.85,    # Adjust as needed
    "Medium": 0.65,
    "Low": 0.00
}
```

#### Adding More Classes
Modify `CLASS_NAMES` in `backend/main.py`:
```python
CLASS_NAMES = {0: "Benign", 1: "Malignant", 2: "Other"}
```

---

## 🧠 Model Information

### Model Architecture
- **Type**: Convolutional Neural Network (CNN)
- **Input Size**: 224 × 224 pixels (RGB)
- **Output**: Binary classification (Benign or Malignant)
- **Framework**: TensorFlow/Keras

### Training Details
- **Dataset**: HAM10000 or similar skin lesion dataset
- **Preprocessing**: Images resized to 224×224, normalized to [0, 1]
- **Augmentation**: Likely used during training
- **Validation**: Binary cross-entropy loss

### Inference
- **Preprocessing**: Image → 224×224 RGB → Normalized [0, 1]
- **Output**: Probability score [0, 1]
  - Values < 0.5 → Benign
  - Values ≥ 0.5 → Malignant

### Performance Notes
- Inference time typically 50-200ms (depending on hardware)
- Accuracy depends on training data quality
- Always validate with professional dermatologists

---

## 🆘 Troubleshooting

### Backend Issues

#### "Model not loaded" Error
```
✗ Model file not found at backend/models/Dermavision_cnn.h5
```

**Solution:**
- Verify model file exists at `backend/models/Dermavision_cnn.h5`
- Check file path in `backend/main.py`
- Ensure file extension is correct (.h5 or .keras)

#### Port Already in Use
```
ERROR: Address already in use: ('0.0.0.0', 8000)
```

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

#### TensorFlow/Keras Issues
```
ModuleNotFoundError: No module named 'tensorflow'
```

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade tensorflow keras
```

### Frontend Issues

#### Backend Not Responding
```
⚠️ Backend API is not responding. Make sure it's running on port 8000
```

**Solution:**
- Ensure backend server is running: `uvicorn main:app --reload`
- Check that port 8000 is not blocked
- Verify `API_BASE_URL` in `script.js` is correct

#### CORS Errors
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
- Backend already has CORS enabled
- Ensure frontend is not running on restricted domain
- Check browser console for detailed error

#### Image Upload Not Working
**Solution:**
- Verify file size is under 5MB
- Ensure file type is JPG, PNG, or WebP
- Check browser's file upload permissions

### General Issues

#### Application Won't Load
1. Clear browser cache: `Ctrl+Shift+Delete`
2. Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
3. Try incognito/private window
4. Check browser console for errors: `F12`

#### Performance Issues
- Large images may take longer to process
- Reduce image resolution before upload
- Check system resources (CPU, RAM)
- Update to latest Python/TensorFlow versions

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more classification categories
- Implement multi-image batch processing
- Add data augmentation preprocessing
- Integrate confidence calibration
- Add explainability features (Grad-CAM)
- Performance optimizations
- Unit tests

---

## 📄 License

This project is for **research and educational purposes only**. Use at your own risk.

---

## ⚠️ Legal Disclaimer

**DermaVision is NOT a medical device and cannot be used for:**
- Medical diagnosis
- Treatment recommendations
- Clinical decision-making

**Always:**
- Consult a qualified dermatologist
- Seek professional medical advice for any skin concerns
- Do not delay medical treatment based on DermaVision results

---

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review API documentation at `http://localhost:8000/docs`
3. Check browser console for error messages
4. Verify backend logs for detailed error information

---

## 🙏 Acknowledgments

- Built with **FastAPI**, **TensorFlow/Keras**, and **modern web technologies**
- Inspired by medical AI research
- Trained on skin lesion datasets (HAM10000, ISIC, etc.)

---

**Last Updated**: December 2025  
**Version**: 1.0.0

ACCESS THE APPLICATION FROM HERE:
https://jovial-longma-e0ee2e.netlify.app/

