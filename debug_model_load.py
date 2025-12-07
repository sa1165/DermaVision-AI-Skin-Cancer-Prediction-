import os
import sys

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "Dermavision_cnn.h5")
print(f"Checking model at: {MODEL_PATH}")

if not os.path.exists(MODEL_PATH):
    print("File does not exist")
    sys.exit(1)

print(f"File size: {os.path.getsize(MODEL_PATH)} bytes")

print("--- Trying h5py ---")
try:
    import h5py
    with h5py.File(MODEL_PATH, 'r') as f:
        print("h5py opened file successfully")
        print("Keys:", list(f.keys()))
except ImportError:
    print("h5py not installed")
except Exception as e:
    print(f"h5py failed: {e}")

print("--- Trying tensorflow ---")
try:
    import tensorflow as tf
    print(f"TensorFlow version: {tf.__version__}")
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("tf.keras.models.load_model success")
    except Exception as e:
        print(f"tf.keras.models.load_model failed: {e}")
except ImportError:
    print("TensorFlow not installed")
