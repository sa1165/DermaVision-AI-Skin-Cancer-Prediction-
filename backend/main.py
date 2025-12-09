import os
import io
import time
import numpy as np
import random
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import requests
import shutil


# Try importing TensorFlow/Keras - handle version differences
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.layers import InputLayer
    from tensorflow.keras.utils import get_custom_objects
    
    # Register compatible classes for older model formats
    class CompatibleInputLayer(InputLayer):
        def __init__(self, *args, **kwargs):
            # Convert batch_shape to input_shape for compatibility
            if 'batch_shape' in kwargs:
                batch_shape = kwargs.pop('batch_shape')
                if batch_shape and len(batch_shape) > 1:
                    kwargs['input_shape'] = batch_shape[1:]
            super().__init__(*args, **kwargs)
    
    # Handle DTypePolicy compatibility (Keras 2.x vs 3.x)
    try:
        from tensorflow.keras.dtype_policies import DTypePolicy as TFDTypePolicy
        # Use the real DTypePolicy if available
        CompatibleDTypePolicy = TFDTypePolicy
    except ImportError:
        try:
            from keras.dtype_policies import DTypePolicy as KerasDTypePolicy
            CompatibleDTypePolicy = KerasDTypePolicy
        except ImportError:
            # Create a simple DTypePolicy wrapper for compatibility
            class CompatibleDTypePolicy:
                def __init__(self, name='float32'):
                    self.name = name
                    # Add required attributes
                    import numpy as np
                    self.compute_dtype = getattr(np, name, np.float32)
                    self.variable_dtype = getattr(np, name, np.float32)
                
                @classmethod
                def from_config(cls, config):
                    # Handle nested config structure
                    if isinstance(config, dict):
                        if 'config' in config:
                            # Nested structure: {'module': 'keras', 'class_name': 'DTypePolicy', 'config': {'name': 'float32'}}
                            return cls(config['config'].get('name', 'float32'))
                        else:
                            # Direct config: {'name': 'float32'}
                            return cls(config.get('name', 'float32'))
                    return cls('float32')
    
    # Register custom objects before any model loading
    custom_objs = get_custom_objects()
    custom_objs['InputLayer'] = CompatibleInputLayer
    custom_objs['DTypePolicy'] = CompatibleDTypePolicy
except ImportError:
    try:
        import keras
        tf = None
        InputLayer = None
        get_custom_objects = None
    except ImportError:
        tf = None
        keras = None
        InputLayer = None
        get_custom_objects = None

# ==================== INITIALIZATION ====================
app = FastAPI(
    title="DermaVision API",
    description="Research & Educational Skin Lesion Classifier",
    version="1.0.0"
)

# Enable CORS to allow frontend requests
origins = [
    "https://resonant-choux-319363.netlify.app",  # Live Netlify frontend
    "https://jovial-longma-e0ee2e.netlify.app",  # Live Netlify frontend (current deployment)
    "http://localhost:5500",                      # Local development (VS Code Live Server)
    "http://127.0.0.1:5500",                      # Local development
    "http://localhost:8000",                     # Local backend testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    print("="*60)
    print("🚀 DermaVision API Starting...")
    print(f"📊 Model Loading: Lazy (on first request)")
    print(f"🌐 CORS Enabled for: {len(origins)} origins")
    print("="*60)


# ==================== MODEL LOADING ====================
# Paths
BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")
TFLITE_MODEL_PATH = os.path.join(MODELS_DIR, "skin_cancer_cnn.tflite")
H5_MODEL_PATH = os.path.join(MODELS_DIR, "skin_cancer_cnn.h5")

# GitHub LFS download URL (fallback for H5)
MODEL_DOWNLOAD_URL = "https://github.com/sa1165/DermaVision-AI-Skin-Cancer-Prediction-/raw/main/models/skin_cancer_cnn.h5"

# Global model variables
model = None
is_tflite = False
model_loading_attempted = False

def is_git_lfs_pointer(filepath):
    """Check if a file is a Git LFS pointer file."""
    try:
        if not os.path.exists(filepath):
            return False
        
        # Git LFS pointer files are small (< 1KB) and start with "version https://git-lfs.github.com"
        file_size = os.path.getsize(filepath)
        if file_size < 1024:  # Less than 1KB
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline()
                if 'git-lfs' in first_line or 'version https' in first_line:
                    return True
        return False
    except Exception:
        return False

def download_model_from_url(url, destination):
    """Download model file from URL with progress."""
    try:
        print(f"[INFO] Downloading model from {url}...")
        print(f"[INFO] This may take a few minutes (model is ~500MB)...")
        
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        if downloaded % (10 * 1024 * 1024) == 0:  # Log every 10MB
                            print(f"[INFO] Downloaded {downloaded / (1024*1024):.1f}MB / {total_size / (1024*1024):.1f}MB ({percent:.1f}%)")
        
        print(f"[OK] Model downloaded successfully to {destination}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to download model: {e}")
        return False

def load_model_lazy():
    """Load model lazily on first request (Prioritizes TFLite)."""
    global model, is_tflite, model_loading_attempted
    
    if model is not None:
        return model
    
    if model_loading_attempted:
        return None
    
    model_loading_attempted = True
    
    print(f"[INFO] lazy_load triggered. Checking for models...")
    
    # 1. Try Loading TFLite Model (Preferred for Memory)
    if os.path.exists(TFLITE_MODEL_PATH):
        try:
            print(f"[INFO] Found TFLite model at {TFLITE_MODEL_PATH}")
            # Initialize TFLite Interpreter
            interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
            interpreter.allocate_tensors()
            
            model = interpreter
            is_tflite = True
            print(f"[OK] TFLite Model loaded successfully!")
            print(f"[INFO] Memory usage should be minimal (~100MB)")
            return model
        except Exception as e:
            print(f"[ERROR] Failed to load TFLite model: {e}")
            print(f"[INFO] Falling back to H5 model...")
            is_tflite = False
    else:
        print(f"[INFO] TFLite model not found at {TFLITE_MODEL_PATH}")

    # 2. Fallback to H5 Model (Original Logic)
    try:
        # Check if model file exists and is not a Git LFS pointer
        if os.path.exists(H5_MODEL_PATH):
            if is_git_lfs_pointer(H5_MODEL_PATH):
                print(f"[WARN] H5 Model file is a Git LFS pointer")
                print(f"[INFO] Attempting to download H5 model from GitHub...")
                
                if download_model_from_url(MODEL_DOWNLOAD_URL, H5_MODEL_PATH):
                    print(f"[OK] Download complete, attempting to load...")
                else:
                    return None
        
        # Load H5
        if keras is not None:
            try:
                model = keras.models.load_model(H5_MODEL_PATH, compile=False)
                print(f"[OK] H5 Model loaded successfully")
                return model
            except Exception as e1:
                try:
                    custom_objs = get_custom_objects()
                    model = keras.models.load_model(H5_MODEL_PATH, compile=False, custom_objects=custom_objs)
                    print(f"[OK] H5 Model loaded with custom objects")
                    return model
                except Exception as e2:
                    print(f"[ERROR] H5 Model loading failed: {e2}")
                    return None
        else:
            print("[WARN] Keras not available")
            return None
            
    except Exception as e:
        print(f"[ERROR] Error loading H5 model: {e}")
        return None



# ==================== CONFIGURATION ====================
INPUT_SIZE = 224
CLASS_NAMES = {0: "Benign", 1: "Malignant"}
CONFIDENCE_THRESHOLDS = {
    "High": 0.80,
    "Medium": 0.60,
    "Low": 0.00
}

# ==================== DISCLAIMER ====================
DISCLAIMER = (
    "⚠️ RESEARCH & EDUCATIONAL TOOL ONLY\n"
    "DermaVision is NOT a medical device and cannot be used for medical diagnosis or treatment decisions.\n"
    "Results are ML model predictions, NOT medical advice.\n"
    "Always consult a qualified dermatologist for skin concerns."
)

# ==================== UTILITY FUNCTIONS ====================
def preprocess_image(image_file) -> np.ndarray:
    """
    Load and preprocess image from UploadFile.
    
    - Converts to RGB
    - Resizes to 224x224
    - Normalizes to [0, 1] range
    """
    try:
        # Read image from uploaded file
        img = Image.open(io.BytesIO(image_file))
        
        # Convert RGBA/grayscale to RGB
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # Resize to model input size
        img = img.resize((INPUT_SIZE, INPUT_SIZE), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img, dtype=np.float32)
        
        # Normalize to [0, 1]
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    except Exception as e:
        raise ValueError(f"Image preprocessing failed: {str(e)}")

def calculate_confidence_band(confidence: float) -> str:
    """
    Calculate confidence band based on confidence score.
    
    - High: >= 0.80
    - Medium: >= 0.60 and < 0.80
    - Low: < 0.60
    """
    if confidence >= CONFIDENCE_THRESHOLDS["High"]:
        return "High"
    elif confidence >= CONFIDENCE_THRESHOLDS["Medium"]:
        return "Medium"
    else:
        return "Low"

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "model": "loaded" if model else "not_loaded",
        "app": "DermaVision API"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Make a skin lesion prediction.
    
    Input: An uploaded image file (JPG, PNG, WebP)
    Output: JSON with prediction, confidence, and metadata
    """
    
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload JPG, PNG, or WebP."
        )
    
    try:
        # Read file content
        contents = await file.read()
        
        # Preprocess image
        img_array = preprocess_image(contents)
        
        # Record inference time
        start_time = time.time()
        
        # Load model lazily on first request
        current_model = load_model_lazy()
        
        # Use actual model if available, otherwise use demo prediction
        if current_model is not None:
            # === PREDICTION LOGIC ===
            if is_tflite:
                # TFLite Inference
                input_details = current_model.get_input_details()
                output_details = current_model.get_output_details()
                
                # Set input tensor
                current_model.set_tensor(input_details[0]['index'], img_array)
                
                # Run inference
                current_model.invoke()
                
                # Get output tensor
                result = current_model.get_tensor(output_details[0]['index'])
                pred_output = result[0] # Single batch
                
            else:
                # Keras Inference
                prediction = current_model.predict(img_array, verbose=0)
                pred_output = prediction[0]
            
            # === PROCESS OUTPUT ===
            # Check if model outputs sigmoid (single value) or softmax (2 values)
            if len(pred_output) == 1:
                # SIGMOID output: single value represents probability of Malignant (class 1)
                malignant_prob = float(pred_output[0])
                benign_prob = 1.0 - malignant_prob
                
                # Class prediction: >= 0.5 = Malignant (1), < 0.5 = Benign (0)
                predicted_class = 1 if malignant_prob >= 0.5 else 0
                
                # Confidence is the probability of the predicted class
                confidence_score = malignant_prob if predicted_class == 1 else benign_prob
            else:
                # SOFTMAX output: 2 values [benign_prob, malignant_prob]
                benign_prob = float(pred_output[0])
                malignant_prob = float(pred_output[1])
                
                # Class prediction: argmax
                predicted_class = int(np.argmax(pred_output))
                
                # Confidence is the probability of the predicted class
                confidence_score = malignant_prob if predicted_class == 1 else benign_prob
            
            mode = "production (TFLite)" if is_tflite else "production (Keras)"
        else:
            # Demo mode: Generate random realistic prediction
            malignant_prob = round(random.uniform(0.0, 1.0), 4)
            benign_prob = 1.0 - malignant_prob
            predicted_class = 1 if malignant_prob >= 0.5 else 0
            confidence_score = malignant_prob if predicted_class == 1 else benign_prob
            mode = "demo"
        
        inference_time = (time.time() - start_time) * 1000  # Convert to ms
        confidence_band = calculate_confidence_band(confidence_score)
        class_name = CLASS_NAMES[predicted_class]
        
        # Prepare response
        response = {
            "predicted_class": class_name,
            "class_index": predicted_class,
            "confidence": round(confidence_score, 4),
            "confidence_percentage": round(confidence_score * 100, 2),
            "confidence_band": confidence_band,
            "probabilities": {
                "Benign": round(float(benign_prob), 4),
                "Malignant": round(float(malignant_prob), 4)
            },
            "inference_time_ms": round(inference_time, 2),
            "disclaimer": DISCLAIMER,
            "mode": mode,
            "timestamp": time.time()
        }
        
        return response
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/info")
async def info():
    """Get API and model information."""
    return {
        "app_name": "DermaVision",
        "version": "1.0.0",
        "description": "Binary Skin Lesion Classifier (Benign vs Malignant)",
        "model_input_size": INPUT_SIZE,
        "classes": CLASS_NAMES,
        "confidence_thresholds": CONFIDENCE_THRESHOLDS,
        "model_type": "TFLite" if is_tflite else "Keras H5",
        "model_loaded": model is not None,
        "disclaimer": DISCLAIMER
    }

# ==================== ERROR HANDLERS ====================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)}
    )

# ==================== SERVER INFO ====================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("DermaVision Backend Server")
    print("="*60)
    print(f"TFLite Path: {TFLITE_MODEL_PATH}")
    print(f"H5 Path: {H5_MODEL_PATH}")
    print(f"Model Loaded: {'[OK]' if model else '[NO]'}")
    print("Start with: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("="*60 + "\n")
