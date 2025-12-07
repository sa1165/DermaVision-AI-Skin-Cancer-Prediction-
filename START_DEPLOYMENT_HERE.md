# 🚀 START HERE - Deploy Your Backend & Connect to Frontend

## Current Status
- ✅ **Frontend**: Already deployed on Netlify
- ⏳ **Backend**: Needs to be deployed
- ⏳ **Connection**: Frontend needs backend URL

---

## Quick Start (3 Steps)

### Step 1: Deploy Backend to Railway (5-10 minutes)

1. **Go to [railway.app](https://railway.app)**
   - Sign up/login with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure (IMPORTANT!)**
   - Click on your service
   - Go to **Settings** tab
   - Set **Root Directory** to: `backend` ⚠️
   - Build and Start commands are auto-detected (should be correct)

4. **Get Your Backend URL**
   - In Settings → **Networking**
   - Click **"Generate Domain"**
   - **Copy the URL** (e.g., `https://dermavision-api.up.railway.app`)
   - ⭐ **SAVE THIS URL!**

5. **Test Backend**
   - Visit: `https://your-url.railway.app/info`
   - Should see: `{"model_loaded": true, ...}`

---

### Step 2: Update Frontend with Backend URL

**Easy Method:**
```powershell
.\update-frontend-api.ps1
```
Enter your Railway URL when prompted.

**Or Manual:**
1. Open `frontend/script.js`
2. Find line 19: `const PRODUCTION_API_URL = "";`
3. Replace with: `const PRODUCTION_API_URL = "https://your-app.railway.app";`
4. Save

---

### Step 3: Redeploy Frontend to Netlify

**If Netlify is connected to Git:**
```powershell
git add frontend/script.js
git commit -m "Connect to backend API"
git push
```
Netlify will auto-deploy in 1-2 minutes.

**If using manual upload:**
```powershell
.\deploy-netlify.ps1
```
Then drag `frontend-deploy.zip` to [app.netlify.com/drop](https://app.netlify.com/drop)

---

## ✅ Test Your Live App

1. Visit your Netlify site
2. Upload a test image
3. Check if prediction works
4. **Success!** 🎉

---

## 📚 Detailed Guides

- **Full deployment guide**: `DEPLOY_NOW.md`
- **Railway step-by-step**: `deploy-backend-railway.md`
- **Backend checklist**: `BACKEND_DEPLOYMENT_CHECKLIST.md`
- **General deployment**: `DEPLOYMENT.md`

---

## 🆘 Troubleshooting

**Backend not starting?**
- Check Railway logs
- Verify Root Directory is `backend`
- Check `Procfile` exists

**Can't connect frontend to backend?**
- Verify backend URL is correct
- Test backend: `https://your-url.railway.app/info`
- Check browser console for errors

**Need more help?**
- See `DEPLOY_NOW.md` for detailed troubleshooting

---

## 🎯 What You'll Have After Deployment

- ✅ Frontend on Netlify (already done)
- ✅ Backend on Railway
- ✅ Full working application online
- ✅ Users can upload images and get predictions

---

**Ready? Start with Step 1 above!** 🚀

