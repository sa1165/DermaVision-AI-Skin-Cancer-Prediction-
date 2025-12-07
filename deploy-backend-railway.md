# 🚀 Deploy Backend to Railway - Step by Step

## Quick Deployment Guide

### Prerequisites
- ✅ Your code is on GitHub (or GitLab/Bitbucket)
- ✅ Model file exists at `backend/models/skin_cancer_cnn.h5`
- ✅ Backend files are ready

---

## Step 1: Push Code to GitHub (if not already done)

```powershell
# Check if you have a git repository
git status

# If not initialized, initialize it:
git init
git add .
git commit -m "Ready for Railway deployment"

# Push to GitHub
git remote add origin <your-github-repo-url>
git push -u origin main
```

---

## Step 2: Deploy to Railway

### 2.1 Sign Up / Login
1. Go to **[railway.app](https://railway.app)**
2. Click **"Start a New Project"** or **"Login"**
3. Sign up with **GitHub** (easiest method)

### 2.2 Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub
4. Select your repository: `DERMAVISION_CNN`

### 2.3 Configure Deployment
Railway will auto-detect Python, but verify these settings:

1. **Click on your service** (the deployed app)
2. Go to **Settings** tab
3. Configure:

   **Root Directory:**
   - Set to: `backend`
   - This tells Railway where your Python app is

   **Build Command:**
   - Should be: `pip install -r requirements.txt`
   - Railway usually auto-detects this

   **Start Command:**
   - Should be: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Railway uses `$PORT` environment variable

### 2.4 Generate Domain
1. In your service, go to **Settings**
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. **Copy the URL** - it will look like: `https://your-app-name.up.railway.app` ⭐
   - **SAVE THIS URL!** You'll need it for the frontend

### 2.5 Verify Model File
- The model file `backend/models/skin_cancer_cnn.h5` should be in your repository
- Railway will include it automatically if it's committed to Git
- If the file is too large for Git, you may need to use Git LFS

---

## Step 3: Test Your Backend

After deployment completes (usually 2-5 minutes):

1. **Test the root endpoint:**
   ```
   https://your-app-name.up.railway.app/
   ```
   Should return: `{"status": "running", "model": "loaded", ...}`

2. **Test the info endpoint:**
   ```
   https://your-app-name.up.railway.app/info
   ```
   Should return model information

3. **Check logs:**
   - In Railway dashboard, click on your service
   - Go to **"Deployments"** tab
   - Click on the latest deployment
   - View **"Logs"** to see if model loaded successfully

---

## Step 4: Update Frontend with Backend URL

Once you have your Railway URL, update the frontend:

### Option A: Use the Helper Script
```powershell
.\update-frontend-api.ps1
```
Then enter your Railway URL when prompted.

### Option B: Manual Update
1. Open `frontend/script.js`
2. Find line 19:
   ```javascript
   const PRODUCTION_API_URL = ""; // ⚠️ UPDATE THIS
   ```
3. Replace with:
   ```javascript
   const PRODUCTION_API_URL = "https://your-app-name.up.railway.app"; // Your Railway URL
   ```
4. Save the file

---

## Step 5: Redeploy Frontend to Netlify

After updating the frontend:

### If using Git (Auto-deploy):
```powershell
git add frontend/script.js
git commit -m "Update backend API URL"
git push
```
Netlify will automatically redeploy.

### If using Manual Upload:
```powershell
.\deploy-netlify.ps1
```
Then upload the new zip to Netlify.

---

## Troubleshooting

### Backend Not Starting
- Check Railway logs for errors
- Verify `requirements.txt` is correct
- Ensure Python version is compatible (3.10+)
- Check that `Procfile` exists in `backend/` folder

### Model Not Loading
- Check Railway logs for model loading errors
- Verify model file path: `backend/models/skin_cancer_cnn.h5`
- Ensure model file is committed to Git
- Check file size (if > 100MB, may need Git LFS)

### CORS Errors
- Backend already has CORS enabled for all origins
- If issues persist, check Railway logs
- Verify backend URL is correct in frontend

### Build Fails
- Check Railway build logs
- Verify all dependencies in `requirements.txt`
- Ensure `runtime.txt` specifies Python 3.10

---

## Quick Checklist

- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Project created and connected to GitHub repo
- [ ] Root directory set to `backend`
- [ ] Domain generated and URL copied
- [ ] Backend tested (`/info` endpoint works)
- [ ] Frontend `script.js` updated with backend URL
- [ ] Frontend redeployed to Netlify
- [ ] Full application tested end-to-end

---

## Alternative: Deploy to Render

If Railway doesn't work, you can use Render:

1. Go to **[render.com](https://render.com)**
2. Sign up with GitHub
3. **New** → **Web Service**
4. Connect your repository
5. Configure:
   - **Name**: `dermavision-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`
6. Deploy and copy the URL

---

**Once backend is deployed and frontend is updated, your full application will be live!** 🎉

