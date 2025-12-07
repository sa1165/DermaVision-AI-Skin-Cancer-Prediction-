📌 Overview

DermaVision is an end-to-end machine learning application built to classify skin lesions as Benign or Malignant based on dermoscopic images.

The system is designed strictly for educational and research purposes, demonstrating how AI can assist in dermatology workflows — while including strong ethical disclaimers and safety protections.

The project includes:

🧠 A trained CNN model (TensorFlow/Keras) using Kaggle dataset

⚙️ A production-ready FastAPI backend for real-time inference

💻 A modern responsive frontend UI (HTML/CSS/JS)

📊 Confidence scoring (High / Medium / Low)

📝 Skin lesion learning guide (Benign & Malignant categories)

🔐 Safety modal requiring user acknowledgment before use



🚀 Features
🧠 1. Deep Learning Model

Trained on a binary classification task:

Benign

Malignant

Architecture:

Custom CNN with convolutional, pooling, dense, and dropout layers

Image size: 224×224

Activation: Sigmoid

Loss: Binary Crossentropy

📈 2. Confidence Bands

Prediction is categorized as:

Confidence	Range	Meaning
High	≥ 80%	Strong model agreement
Medium	60–79%	Acceptable but not strong
Low	< 60%	Do NOT rely on this result
🖼️ 3. Modern Frontend

Image upload

Preview display

Analyze button

Dark/light theme toggle

Session history

Learn section with lesion explanations

⚙️ 4. FastAPI Backend

The backend exposes:

POST /predict


Returns:

{
  "predicted_class": "Benign",
  "confidence": 0.94,
  "confidence_band": "High",
  "inference_time_ms": 42.5
}

🛡️ 5. Safety Modal

User MUST acknowledge:

“This is NOT a medical device.”

📊 Model Training Summary

The deep learning model was trained on Kaggle using:

CNN model with ~1M parameters

Data augmentation

Early stopping

Learning rate scheduling

Adam optimizer

Dataset used:
Melanoma Cancer Dataset (Binary: Benign vs Malignant)

Final model saved as:

dermavision_binary.keras

⚙️ Backend Installation & Running (Local)
1️⃣ Navigate to backend folder
cd backend

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run FastAPI server
uvicorn main:app --reload


Server will start at:

👉 http://127.0.0.1:8000

Swagger Docs:
👉 http://127.0.0.1:8000/docs

💻 Frontend Setup

If using VS Code Live Server:

Go to frontend/ folder

Open index.html

Right-click → Open with Live Server

OR manually open:

frontend/index.html


Update the backend URL inside script.js:

const API_URL = "https://your-backend-url.com/predict";

🌐 Deployment Guide
✔ Frontend

Deploy on:

Netlify

Vercel

GitHub Pages

✔ Backend (FastAPI)

Deploy on:

Render.com (recommended)

Railway.app

Fly.io

Azure App Service

AWS EC2

Required:

Expose port 8000

Install requirements.txt

Add CORS permissions for frontend domain

Example Render start command:

uvicorn main:app --host 0.0.0.0 --port 8000

🔍 API Spec
Request:

POST /predict
Form-data:

file: <image file>

Response:
{
  "predicted_class": "Malignant",
  "confidence": 0.81,
  "confidence_band": "High",
  "inference_time_ms": 34.5
}

📚 Learn Section

Includes concise explanations of:

Benign:

BKL — Benign Keratosis

DF — Dermatofibroma

NV — Melanocytic Nevus

VASC — Vascular Lesion

Malignant / Serious:

MEL — Melanoma

BCC — Basal Cell Carcinoma

AKIEC — Actinic Keratosis

⚠️ Medical Disclaimer

DermaVision is NOT a medical device.
It must not be used for diagnosis, treatment, or clinical decision-making.
Always consult a qualified healthcare professional for real medical concerns.

🤝 Contributing

Pull requests are welcome.
For major changes, open an issue first to discuss what you would like to change.

📜 License

This project is for research and educational purposes only.
