#!/bin/bash
# Railway build script to ensure Git LFS files are downloaded

echo "🔧 Installing Git LFS..."
git lfs install --local

echo "📥 Pulling Git LFS files..."
git lfs pull

echo "✅ Git LFS files downloaded"
ls -lh models/

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Build complete!"
