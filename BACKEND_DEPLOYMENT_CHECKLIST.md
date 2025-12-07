# ✅ Backend Deployment Checklist

## Pre-Deployment Verification

### Files Required ✅
- [x] `backend/main.py` - FastAPI application
- [x] `backend/requirements.txt` - Dependencies
- [x] `backend/Procfile` - Start command (for Heroku/Railway)
- [x] `backend/runtime.txt` - Python version
- [x] `backend/models/skin_cancer_cnn.h5` - Model file

### Configuration Check ✅

**Procfile:**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```
✅ Correct - Uses `$PORT` environment variable

**Runtime:**
```
python-3.10
```
✅ Correct - Python 3.10 specified

**Requirements:**
- fastapi==0.104.1 ✅
- uvicorn[standard]==0.24.0 ✅
- tensorflow==2.14.0 ✅
- keras==2.14.0 ✅
- pillow==10.1.0 ✅
- numpy==1.24.3 ✅
- python-multipart==0.0.6 ✅

**CORS Configuration:**
- ✅ CORS enabled for all origins in `main.py`
- ✅ Allows all methods and headers

**Model Path:**
- ✅ Model path: `backend/models/skin_cancer_cnn.h5`
- ✅ Model file exists and is in repository

---

## Deployment Platforms

### Railway (Recommended)
- ✅ Root Directory: `backend`
- ✅ Build Command: `pip install -r requirements.txt`
- ✅ Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- ✅ Auto-detects Python from `runtime.txt`

### Render
- ✅ Environment: Python 3
- ✅ Build Command: `pip install -r backend/requirements.txt`
- ✅ Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- ✅ Root Directory: `backend`

### Heroku
- ✅ Procfile exists: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- ✅ Requirements.txt present
- ✅ Runtime.txt present

---

## Post-Deployment Verification

After deploying, test these endpoints:

1. **Root Endpoint:**
   ```
   GET https://your-backend-url.com/
   ```
   Expected: `{"status": "running", "model": "loaded", ...}`

2. **Info Endpoint:**
   ```
   GET https://your-backend-url.com/info
   ```
   Expected: Model information with `"model_loaded": true`

3. **Predict Endpoint:**
   ```
   POST https://your-backend-url.com/predict
   Content-Type: multipart/form-data
   Body: image file
   ```
   Expected: Prediction JSON response

---

## Common Issues & Solutions

### Issue: Model Not Loading
**Solution:**
- Verify model file is committed to Git
- Check file path in logs
- Ensure model file size is within platform limits
- Use Git LFS if file > 100MB

### Issue: Build Fails
**Solution:**
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Check build logs for specific errors
- Ensure runtime.txt specifies correct Python version

### Issue: App Crashes on Start
**Solution:**
- Verify Procfile command is correct
- Check that PORT environment variable is used
- Review startup logs for errors
- Ensure all dependencies installed correctly

### Issue: CORS Errors
**Solution:**
- Backend already has CORS enabled
- Verify frontend URL matches (if restricted)
- Check browser console for specific errors

---

## Model File Size

**Current Model:** `backend/models/skin_cancer_cnn.h5`
- Check size: Should be reasonable for Git
- If > 100MB: Consider Git LFS
- Railway/Render: Usually handles files up to 500MB

---

## Environment Variables (Optional)

No environment variables required for basic deployment.

Optional variables you might add later:
- `MODEL_PATH` - Custom model path
- `LOG_LEVEL` - Logging level
- `MAX_FILE_SIZE` - Max upload size

---

## Ready to Deploy! ✅

All files are in place and configured correctly. Follow `DEPLOY_NOW.md` for step-by-step deployment instructions.

