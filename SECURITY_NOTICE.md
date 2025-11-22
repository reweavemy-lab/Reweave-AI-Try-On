# ⚠️ SECURITY NOTICE - API Key Exposed

## What Happened
The Google Gemini API key was accidentally committed to the repository in documentation files. This has been fixed, but **you need to generate a new API key immediately**.

## Immediate Actions Required

### 1. Revoke the Old API Key
1. Go to: https://aistudio.google.com/app/apikey
2. Find the key: `AIzaSyDcp-qwhSQfaBzmftTlH4NfPcWHJNRQuoc`
3. **Delete/Revoke** it immediately

### 2. Generate a New API Key
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the new key (starts with `AIza...`)

### 3. Update Streamlit Cloud
1. Go to: https://share.streamlit.io/
2. Select your app: `reweave-ai-try-on-nwuappplx28vde2yqwhpilz`
3. Go to Settings → Secrets
4. Update `GOOGLE_API_KEY` with your **new** API key
5. Redeploy the app

### 4. Check API Usage
- Go to Google Cloud Console
- Check for any unauthorized usage
- Set up usage quotas/limits if needed

## Prevention
- ✅ API keys removed from all files
- ✅ `render.yaml` updated to not include keys
- ✅ Documentation updated with warnings
- ✅ `.env` file is in `.gitignore` (safe)

## Files Fixed
- `DEPLOYMENT.md` - API key removed
- `QUICK_DEPLOY.md` - API key removed  
- `render.yaml` - API key removed

**Never commit API keys to git repositories!**

