# 🚀 Deployment Guide - DermaVision

This guide explains how to deploy DermaVision to production.

## 📋 Overview

DermaVision consists of two parts:
1. **Frontend** (Static HTML/CSS/JS) → Deploy to **Netlify**
2. **Backend** (FastAPI/Python) → Deploy to **Railway, Render, or Heroku**

---

## 🌐 Frontend Deployment (Netlify)

### Option 1: Deploy via Netlify Dashboard

1. **Prepare your repository**
   - Push your code to GitHub/GitLab/Bitbucket
   - Make sure `frontend/` folder contains all frontend files

2. **Deploy to Netlify**
   - Go to [netlify.com](https://netlify.com) and sign up/login
   - Click "Add new site" → "Import an existing project"
   - Connect your Git repository
   - Configure build settings:
     - **Base directory**: `frontend` (or leave empty if root)
     - **Build command**: (leave empty - no build needed)
     - **Publish directory**: `frontend` (or `.` if frontend is root)
   - Click "Deploy site"

3. **Set Environment Variables** (Important!)
   - Go to Site settings → Environment variables
   - Add: `VITE_API_BASE_URL` = `https://your-backend-url.com`
   - Or update `frontend/script.js` with your backend URL

### Option 2: Deploy via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy
cd frontend
netlify deploy --prod

# Or for draft deployment
netlify deploy
```

### Option 3: Drag & Drop

1. Zip the `frontend/` folder
2. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
3. Drag and drop the zip file
4. Your site will be live in seconds!

---

## 🔧 Backend Deployment Options

### Option 1: Railway (Recommended - Easy & Free)

1. **Sign up** at [railway.app](https://railway.app)
2. **Create new project** → "Deploy from GitHub repo"
3. **Select your repository**
4. **Configure**:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Add environment variables** (if needed)
6. **Deploy!** Railway will give you a URL like `https://your-app.railway.app`

### Option 2: Render

1. **Sign up** at [render.com](https://render.com)
2. **Create new Web Service**
3. **Connect your repository**
4. **Configure**:
   - Environment: Python 3
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Deploy!**

### Option 3: Heroku

1. **Install Heroku CLI** and login
2. **Create `Procfile`** in `backend/`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. **Deploy**:
   ```bash
   cd backend
   heroku create your-app-name
   git push heroku main
   ```

### Option 4: PythonAnywhere

1. **Sign up** at [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload your backend files**
3. **Configure WSGI file** to point to `main:app`
4. **Install dependencies** via Bash console

---

## 🔗 Connecting Frontend to Backend

After deploying both:

1. **Get your backend URL** (e.g., `https://dermavision-api.railway.app`)

2. **Update frontend API URL**:
   - **Option A**: Set Netlify environment variable
     - Go to Netlify → Site settings → Environment variables
     - Add: `VITE_API_BASE_URL` = `https://your-backend-url.com`
   
   - **Option B**: Update `frontend/script.js` directly
     ```javascript
     const API_BASE_URL = "https://your-backend-url.com";
     ```

3. **Enable CORS** (if not already enabled)
   - Your backend already has CORS enabled for all origins
   - If you want to restrict, update `backend/main.py`:
     ```python
     allow_origins=["https://your-netlify-site.netlify.app"]
     ```

---

## 📝 Pre-Deployment Checklist

### Frontend
- [ ] All files in `frontend/` folder
- [ ] `netlify.toml` configured
- [ ] `_redirects` file in `frontend/` (for SPA routing)
- [ ] API URL configured (environment variable or hardcoded)
- [ ] Test locally with production API URL

### Backend
- [ ] `requirements.txt` includes all dependencies
- [ ] Model file (`skin_cancer_cnn.h5`) is included or accessible
- [ ] CORS configured for frontend domain
- [ ] Environment variables set (if needed)
- [ ] Port uses `$PORT` environment variable (for cloud platforms)

---

## 🧪 Testing Deployment

1. **Test Frontend**: Visit your Netlify URL
2. **Test Backend**: Visit `https://your-backend-url.com/info`
3. **Test Connection**: Upload an image in the frontend
4. **Check Logs**: Monitor both Netlify and backend logs for errors

---

## 🔒 Security Considerations

1. **CORS**: Restrict CORS to your frontend domain in production
2. **Rate Limiting**: Add rate limiting to backend API
3. **HTTPS**: Both Netlify and most backend platforms provide HTTPS
4. **API Keys**: If you add authentication, use environment variables

---

## 📊 Monitoring

- **Netlify**: Built-in analytics and logs
- **Railway/Render**: Built-in logs and metrics
- **Uptime**: Monitor your API with services like UptimeRobot

---

## 🆘 Troubleshooting

### Frontend can't connect to backend
- Check CORS settings in backend
- Verify API URL in frontend
- Check browser console for errors
- Verify backend is running and accessible

### Backend deployment fails
- Check `requirements.txt` is correct
- Verify Python version compatibility
- Check build logs for specific errors
- Ensure model file is included or accessible

### Model not loading
- Verify model file path is correct
- Check file permissions
- Ensure model file is in the deployment

---

## 🎉 Quick Start (Netlify + Railway)

1. **Backend (Railway)**:
   ```bash
   # Push to GitHub
   git push origin main
   
   # Deploy on Railway (via dashboard)
   # Get URL: https://your-app.railway.app
   ```

2. **Frontend (Netlify)**:
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Deploy
   cd frontend
   netlify deploy --prod
   
   # Set environment variable
   # VITE_API_BASE_URL = https://your-app.railway.app
   ```

3. **Update Frontend API URL** in Netlify dashboard

4. **Done!** Your app is live! 🎊

---

## 📞 Support

For issues:
- Check deployment logs
- Verify environment variables
- Test API endpoints directly
- Review CORS configuration

---

**Last Updated**: December 2025



