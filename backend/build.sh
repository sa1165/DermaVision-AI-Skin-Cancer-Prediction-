#!/bin/bash
set -e

echo "🔍 Checking Git LFS status..."
git lfs version || echo "⚠️ Git LFS not found"

echo "🔧 Installing Git LFS..."
git lfs install

echo "📥 Fetching Git LFS files..."
git lfs fetch --all

echo "📥 Pulling Git LFS files..."
git lfs pull

echo "📊 Checking model file..."
ls -lh models/ || echo "⚠️ models/ directory not found"

if [ -f "models/skin_cancer_cnn.h5" ]; then
    echo "✅ Model file found"
    file models/skin_cancer_cnn.h5
    head -n 5 models/skin_cancer_cnn.h5
else
    echo "❌ Model file not found!"
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Build complete!"
