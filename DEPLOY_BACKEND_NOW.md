# 🚀 Deploy Backend to Make It Accessible from Netlify

Your backend works locally but needs to be deployed to the cloud so your Netlify frontend can access it.

## Quick Deploy to Railway (5 minutes)

### Step 1: Prepare Your Repository

Make sure your code is on GitHub:

```bash
# If not already on GitHub
git add .
git commit -m "Ready for backend deployment"
git push origin main
```

### Step 2: Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
   - Sign up with GitHub (easiest)

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Deployment**
   - Railway auto-detects Python, but verify:
   - **Root Directory**: `backend` (important!)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Model File**
   - The model file `skin_cancer_cnn.h5` should be in your repo at `backend/models/`
   - If it's not committed (too large), you can:
     - Use Git LFS, OR
     - Upload it via Railway's file system after deployment

5. **Get Your Backend URL**
   - Wait for deployment to complete
   - Click on your service
   - Go to Settings → Generate Domain
   - **Copy the URL**: `https://your-app.railway.app` ⭐

### Step 3: Update Frontend

1. **Open** `frontend/script.js`
2. **Find line 19**:
   ```javascript
   const PRODUCTION_API_URL = ""; // ⚠️ UPDATE THIS
   ```
3. **Replace with your Railway URL**:
   ```javascript
   const PRODUCTION_API_URL = "https://your-app.railway.app"; // Your Railway URL
   ```
4. **Save**

### Step 4: Redeploy Frontend

**Option A: Quick Redeploy**
```powershell
.\deploy-netlify.ps1
```
Then upload new zip to Netlify

**Option B: Git Push (Auto-deploy)**
```bash
git add frontend/script.js
git commit -m "Add backend API URL"
git push
```
Netlify will auto-deploy if connected to Git

### Step 5: Test

1. Visit your Netlify site
2. Upload an image
3. Should work! ✅

---

## Alternative: Deploy to Render

1. **Go to [render.com](https://render.com)**
2. **New** → **Web Service**
3. **Connect** your GitHub repository
4. **Configure**:
   - **Name**: `dermavision-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`
5. **Deploy** and copy URL

---

## Verify Backend is Working

After deployment, test your backend:

1. Visit: `https://your-backend-url.com/info`
2. Should see:
   ```json
   {
     "app_name": "DermaVision",
     "model_loaded": true,
     ...
   }
   ```

If you see this, backend is working! ✅

---

## Troubleshooting

### Model Not Loading

If backend deploys but model doesn't load:

1. **Check model file is in repo**:
   - Should be at: `backend/models/skin_cancer_cnn.h5`
   - If file is too large for Git:
     - Use Git LFS, OR
     - Upload via Railway file system

2. **Check backend logs**:
   - Railway: Click on service → View logs
   - Look for model loading messages

### CORS Errors

CORS is already configured for all origins. If you still get errors:
- Check backend logs
- Verify backend URL is correct in frontend

### Backend Not Starting

Check:
- `requirements.txt` is in `backend/` folder
- Python version is compatible (3.8+)
- Port uses `$PORT` environment variable
- Check deployment logs for errors

---

## Quick Checklist

- [ ] Backend code pushed to GitHub
- [ ] Deployed to Railway/Render
- [ ] Backend URL copied
- [ ] Frontend `script.js` updated with backend URL
- [ ] Frontend redeployed to Netlify
- [ ] Tested: Backend `/info` endpoint works
- [ ] Tested: Frontend can upload images

---

**Once backend is deployed and frontend URL is updated, everything will work!** 🎉


