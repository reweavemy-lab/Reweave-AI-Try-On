# Deployment Guide for Reweave AI Try-On

## Option 1: Streamlit Cloud (Recommended - Free)

1. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `reweavemy-lab/Reweave-AI-Try-On`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Set Environment Variables**:
   - In Streamlit Cloud dashboard, go to Settings → Secrets
   - Add: `GOOGLE_API_KEY=your_new_api_key_here`
   - **IMPORTANT**: Never commit API keys to git. Always use secrets/environment variables.

4. **Custom Domain** (Optional):
   - In Streamlit Cloud settings, add custom domain: `ai.reweave.shop`
   - Update DNS records as instructed

## Option 2: Render (Alternative)

1. **Create render.yaml**:
   ```yaml
   services:
     - type: web
       name: reweave-ai-tryon
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
       envVars:
         - key: GOOGLE_API_KEY
           value: [SET_IN_RENDER_DASHBOARD]  # Never commit API keys to git!
   ```

2. **Deploy**:
   - Connect GitHub repo to Render
   - Render will auto-detect and deploy

## Option 3: Railway

1. **Create railway.json**:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"
     }
   }
   ```

2. **Deploy**:
   - Connect GitHub repo to Railway
   - Add environment variable: `GOOGLE_API_KEY`
   - Railway will auto-deploy

## Environment Variables Required:
- `GOOGLE_API_KEY`: Your Google Gemini API key

