# 🚀 DEPLOY NOW - Complete Deployment Guide

## Your Frontend is Already on Netlify! ✅

Now let's deploy the backend and connect everything together.

---

## 📋 Quick Overview

1. **Deploy Backend** → Railway (5-10 minutes)
2. **Get Backend URL** → Copy from Railway
3. **Update Frontend** → Add backend URL to `frontend/script.js`
4. **Redeploy Frontend** → Push to Netlify
5. **Test Everything** → Your app is live! 🎉

---

## Step 1: Deploy Backend to Railway

### Option A: Follow the Detailed Guide
Read: `deploy-backend-railway.md` for step-by-step instructions

### Option B: Quick Steps

1. **Go to [railway.app](https://railway.app)**
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - **Root Directory**: `backend` ⚠️ IMPORTANT!
   - **Build Command**: `pip install -r requirements.txt` (auto-detected)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT` (auto-detected)

4. **Get Your URL**
   - Go to Settings → Networking
   - Click "Generate Domain"
   - **Copy the URL** (e.g., `https://dermavision-api.up.railway.app`)

5. **Test Backend**
   - Visit: `https://your-url.railway.app/info`
   - Should see model information

---

## Step 2: Update Frontend with Backend URL

### Easy Method (Recommended):
```powershell
.\update-frontend-api.ps1
```
Enter your Railway URL when prompted.

### Manual Method:
1. Open `frontend/script.js`
2. Find line 19:
   ```javascript
   const PRODUCTION_API_URL = ""; // ⚠️ UPDATE THIS
   ```
3. Replace with:
   ```javascript
   const PRODUCTION_API_URL = "https://your-app.railway.app"; // Your Railway URL
   ```
4. Save

---

## Step 3: Redeploy Frontend to Netlify

### If Netlify is connected to Git (Auto-deploy):
```powershell
git add frontend/script.js
git commit -m "Connect frontend to backend API"
git push
```
Netlify will automatically redeploy in 1-2 minutes.

### If using Manual Upload:
```powershell
.\deploy-netlify.ps1
```
Then:
1. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag and drop `frontend-deploy.zip`
3. Wait for deployment

---

## Step 4: Test Your Live Application

1. **Visit your Netlify site**
2. **Upload a test image**
3. **Check if prediction works**
   - If it works: ✅ Success!
   - If errors: Check browser console and backend logs

---

## 🔧 Troubleshooting

### Backend Issues

**Backend not starting:**
- Check Railway logs
- Verify Root Directory is set to `backend`
- Check `requirements.txt` and `Procfile` exist

**Model not loading:**
- Check Railway logs for errors
- Verify model file is in `backend/models/skin_cancer_cnn.h5`
- Ensure model is committed to Git

**CORS errors:**
- Backend already has CORS enabled
- Verify backend URL is correct in frontend

### Frontend Issues

**Can't connect to backend:**
- Check backend URL in `frontend/script.js`
- Verify backend is running (test `/info` endpoint)
- Check browser console for errors

**Frontend not updating:**
- Clear browser cache
- Hard refresh (Ctrl+F5)
- Check Netlify deployment status

---

## ✅ Final Checklist

- [ ] Backend deployed to Railway
- [ ] Backend URL copied
- [ ] Backend tested (`/info` works)
- [ ] Frontend `script.js` updated with backend URL
- [ ] Frontend redeployed to Netlify
- [ ] Full application tested (upload image works)
- [ ] Everything working! 🎉

---

## 📞 Need Help?

- **Backend deployment**: See `deploy-backend-railway.md`
- **Frontend deployment**: See `NETLIFY_DEPLOY.md`
- **Full guide**: See `DEPLOYMENT.md`

---

**Once all steps are complete, your DermaVision app will be fully deployed and working online!** 🚀

