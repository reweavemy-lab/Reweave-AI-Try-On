# Quick Deployment Instructions

## 🚀 Fastest Way: Streamlit Cloud (5 minutes)

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click**: "New app"
4. **Fill in**:
   - Repository: `reweavemy-lab/Reweave-AI-Try-On`
   - Branch: `main`
   - Main file: `app.py`
5. **Click**: "Deploy"
6. **After deployment**, go to Settings → Secrets
7. **Add secret**: 
   - Key: `GOOGLE_API_KEY`
   - Value: `[YOUR_NEW_API_KEY]` ⚠️ **Generate a new key - the old one was exposed!**
8. **Redeploy** the app (it will pick up the secret)

Your app will be live at: `https://[your-app-name].streamlit.app`

## 🌐 To Use Custom Domain `ai.reweave.shop`:

1. In Streamlit Cloud Settings → Custom Domain
2. Add domain: `ai.reweave.shop`
3. Follow DNS instructions to add CNAME record

---

## Alternative: Render (Also Free)

1. **Go to**: https://render.com/
2. **Sign up** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect** repository: `reweavemy-lab/Reweave-AI-Try-On`
5. **Render will auto-detect** `render.yaml` configuration
6. **Click**: "Create Web Service"
7. **Add environment variable**:
   - Key: `GOOGLE_API_KEY`
   - Value: `[YOUR_NEW_API_KEY]` ⚠️ **Generate a new key - the old one was exposed!**

Your app will be live at: `https://[your-app-name].onrender.com`

---

**Note**: The repository is already prepared with all necessary files:
- ✅ `requirements.txt` - Dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `render.yaml` - Render configuration
- ✅ `Procfile` - For Heroku/Railway compatibility

