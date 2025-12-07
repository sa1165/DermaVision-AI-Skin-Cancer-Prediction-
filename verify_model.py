import os
import tensorflow as tf
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "skin_cancer_cnn.h5")
print(f"Loading model from: {MODEL_PATH}")

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.")
    
    print(f"Model Output Shape: {model.output_shape}")
    
    # Check last layer activation if possible
    last_layer = model.layers[-1]
    print(f"Last Layer Config: {last_layer.get_config()}")
    
    # Sanity check prediction on random data
    dummy_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
    prediction = model.predict(dummy_input)
    print(f"Dummy Prediction Shape: {prediction.shape}")
    print(f"Dummy Prediction Value: {prediction}")

except Exception as e:
    print(f"Error: {e}")
