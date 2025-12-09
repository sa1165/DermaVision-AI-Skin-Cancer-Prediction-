#!/bin/bash
set -e

echo "🚀 Starting DermaVision Backend..."

# Check if model file is a Git LFS pointer
if [ -f "models/skin_cancer_cnn.h5" ]; then
    FILE_SIZE=$(stat -f%z "models/skin_cancer_cnn.h5" 2>/dev/null || stat -c%s "models/skin_cancer_cnn.h5" 2>/dev/null || echo "0")
    echo "📊 Model file size: $FILE_SIZE bytes"
    
    # If file is too small, it's likely a Git LFS pointer
    if [ "$FILE_SIZE" -lt 1000000 ]; then
        echo "⚠️ Model file appears to be a Git LFS pointer (too small)"
        echo "🔧 Attempting to pull Git LFS files..."
        
        # Try to install and pull Git LFS
        git lfs install 2>/dev/null || echo "Git LFS install failed"
        git lfs pull 2>/dev/null || echo "Git LFS pull failed"
        
        # Check size again
        FILE_SIZE=$(stat -f%z "models/skin_cancer_cnn.h5" 2>/dev/null || stat -c%s "models/skin_cancer_cnn.h5" 2>/dev/null || echo "0")
        echo "📊 Model file size after LFS pull: $FILE_SIZE bytes"
    fi
    
    if [ "$FILE_SIZE" -gt 100000000 ]; then
        echo "✅ Model file looks good (>100MB)"
    else
        echo "❌ Model file still too small - will run in DEMO mode"
    fi
else
    echo "❌ Model file not found - will run in DEMO mode"
fi

echo "🌐 Starting Uvicorn server..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT
