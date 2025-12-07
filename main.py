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
    "http://localhost:5500",                      # Local development (VS Code Live Server)
    "http://127.0.0.1:5500",                      # Local development
    "http://localhost:8000",                     # Local backend testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODEL LOADING ====================
# Load the trained Keras model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "skin_cancer_cnn.h5")

model = None
try:
    # Try to load the actual model
    if keras is not None:
        # Handle compatibility issues with older model formats
        try:
            # First, try standard loading (custom objects already registered)
            model = keras.models.load_model(MODEL_PATH, compile=False)
            print(f"[OK] Model loaded successfully from {MODEL_PATH}")
        except Exception as e1:
            # Custom objects should already be registered, but try explicit custom_objects
            try:
                custom_objs = get_custom_objects()
                model = keras.models.load_model(MODEL_PATH, compile=False, custom_objects=custom_objs)
                print(f"[OK] Model loaded successfully from {MODEL_PATH} (with compatibility fixes)")
            except Exception as e2:
                print(f"[ERROR] Model loading failed: {str(e2)[:200]}")
                print("[INFO] This model was saved with an older Keras version.")
                print("[INFO] Consider retraining the model with TensorFlow 2.14+ or using TensorFlow 2.8-2.10")
                raise e1  # Raise original error for demo mode
    else:
        print("[WARN] Keras not available")
except FileNotFoundError:
    print(f"[ERROR] Model file not found at {MODEL_PATH}")
    print("[WARN] Using DEMO mode with simulated predictions")
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")
    print("[WARN] Using DEMO mode with simulated predictions")

# If model fails to load, use a simple mock predictor for demo purposes
if model is None:
    print("[NOTE] Note: Running in DEMO mode - predictions are simulated")
    print("   To use real predictions, place a valid .h5 model file in: models/Dermavision_cnn.h5")

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
        
        # Use actual model if available, otherwise use demo prediction
        if model is not None:
            prediction = model.predict(img_array, verbose=0)
            
            # Handle different model output formats
            pred_output = prediction[0]
            
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
            
            mode = "production"
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
        "model_path": MODEL_PATH,
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
    print(f"Model Path: {MODEL_PATH}")
    print(f"Model Loaded: {'[OK]' if model else '[ERROR]'}")
    print("Start with: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("="*60 + "\n")
