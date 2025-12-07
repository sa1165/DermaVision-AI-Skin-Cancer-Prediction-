import os
import sys

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    import tensorflow as tf
    print("TensorFlow imported successfully")
    print(f"TensorFlow version: {tf.__version__}")
except ImportError as e:
    print(f"Error importing TensorFlow: {e}")
except Exception as e:
    print(f"Unexpected error importing TensorFlow: {e}")

try:
    import keras
    print("Keras imported successfully")
    print(f"Keras version: {keras.__version__}")
except ImportError as e:
    print(f"Error importing Keras: {e}")
except Exception as e:
    print(f"Unexpected error importing Keras: {e}")
