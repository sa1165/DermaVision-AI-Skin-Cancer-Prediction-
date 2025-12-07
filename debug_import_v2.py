import sys
print(f"Python: {sys.executable}")

try:
    import tensorflow as tf
    print(f"TensorFlow: {tf.__version__}")
except Exception as e:
    print(f"TensorFlow Import Error: {e}")

try:
    import keras
    print(f"Keras: {keras.__version__}")
except Exception as e:
    print(f"Keras Import Error: {e}")
