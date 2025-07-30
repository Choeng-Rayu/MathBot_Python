# 🔧 DigitalOcean Deployment Troubleshooting

## 🚨 Common Deployment Issues and Solutions

### Issue 1: Python Version Compatibility Error

**Error Message:**
```
-----> No Python version was specified. Using the buildpack default: Python 3.13
KeyError: '__version__'
```

**Solution:**
✅ **Fixed** - Added `.python-version` file with Python 3.11
✅ **Fixed** - Added `runtime.txt` with `python-3.11.9`
✅ **Fixed** - Updated dependencies to compatible versions

### Issue 2: Pillow Build Error

**Error Message:**
```
Getting requirements to build wheel did not run successfully.
KeyError: '__version__'
```

**Root Cause:** Pillow 10.1.0 is not compatible with Python 3.13

**Solution:**
✅ **Fixed** - Updated Pillow to version 10.2.0
✅ **Fixed** - Specified Python 3.11 for better compatibility

### Issue 3: Dependency Version Conflicts

**Solution:**
✅ **Fixed** - Updated all dependencies to compatible versions:
- matplotlib: 3.8.2 → 3.8.4
- reportlab: 4.0.7 → 4.0.9
- Pillow: 10.1.0 → 10.2.0
- numpy: 1.25.2 → 1.26.4
- aiohttp: 3.9.1 → 3.9.5

## 📋 Pre-Deployment Checklist

Before deploying to DigitalOcean, ensure:

### ✅ Files Created/Updated:
- [x] `.python-version` - Specifies Python 3.11
- [x] `runtime.txt` - Alternative Python version specification
- [x] `requirements.txt` - Updated with compatible versions
- [x] `Dockerfile` - Updated to Python 3.11.9
- [x] `deployment/digitalocean-app.yaml` - DigitalOcean configuration

### ✅ Environment Variables Required:
```env
ENVIRONMENT=production
TELEGRAM_BOT_TOKEN=your_bot_token
WEBHOOK_URL=https://your-app.ondigitalocean.app
WEBHOOK_SECRET=your_webhook_secret
MONGODB_URI=your_mongodb_uri
DEEPSEEK_API_KEY=your_deepseek_key
SECRET_KEY=your_secret_key
```

### ✅ GitHub Repository:
- [x] All files committed and pushed
- [x] Repository URL updated in `deployment/digitalocean-app.yaml`
- [x] Branch set to `main`

## 🚀 Deployment Steps

### Step 1: Update Repository URL
Edit `deployment/digitalocean-app.yaml`:
```yaml
github:
  repo: YOUR_ACTUAL_USERNAME/MathBot_Python  # Replace with your username
  branch: main
```

### Step 2: Commit and Push Changes
```bash
git add .
git commit -m "Fix Python compatibility and deployment issues"
git push origin main
```

### Step 3: Create DigitalOcean App
1. Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Choose "GitHub" as source
4. Select your repository
5. Choose `main` branch
6. Enable auto-deploy

### Step 4: Configure Environment Variables
In DigitalOcean dashboard, add these environment variables:

**Required:**
```
ENVIRONMENT=production
TELEGRAM_BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-app-name.ondigitalocean.app
MONGODB_URI=your_mongodb_connection_string
DEEPSEEK_API_KEY=your_deepseek_api_key
```

**Security:**
```
WEBHOOK_SECRET=generate_random_secret_here
SECRET_KEY=generate_random_key_here
ALLOWED_HOSTS=*
```

**Optional (for OCR):**
```
GOOGLE_CLOUD_CREDENTIALS_JSON=your_google_cloud_json_credentials
```

### Step 5: Deploy
1. Click "Create Resources"
2. Wait for deployment (5-10 minutes)
3. Check logs for any errors

### Step 6: Set Webhook
After successful deployment:
```bash
curl -X GET "https://your-app-name.ondigitalocean.app/set_webhook"
```

## 🔍 Monitoring Deployment

### Check Build Logs
Monitor the build process in DigitalOcean dashboard:
- Look for successful Python installation
- Verify all dependencies install correctly
- Check for any error messages

### Verify Health
After deployment:
```bash
curl https://your-app-name.ondigitalocean.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "telegram_bot": "running",
  "alarm_scheduler": "running",
  "environment": "production"
}
```

## 🐛 Common Runtime Issues

### Issue: Bot Not Responding
**Check:**
1. Environment variables are set correctly
2. Webhook URL matches your app URL
3. Telegram bot token is valid

**Solution:**
```bash
# Check webhook info
curl https://your-app-name.ondigitalocean.app/webhook_info

# Reset webhook
curl https://your-app-name.ondigitalocean.app/set_webhook
```

### Issue: Database Connection Failed
**Check:**
1. MongoDB URI is correct
2. Database user has proper permissions
3. Network access is configured in MongoDB Atlas

### Issue: OCR Not Working
**Check:**
1. `GOOGLE_CLOUD_CREDENTIALS_JSON` is set
2. JSON credentials are valid
3. Google Cloud Vision API is enabled

## 📊 Performance Optimization

### Resource Usage
- **Basic plan ($5/month)**: Suitable for small to medium usage
- **Monitor**: CPU and memory usage in dashboard
- **Scale**: Upgrade plan if needed

### Logging
- Set `LOG_LEVEL=INFO` for production
- Use `LOG_LEVEL=DEBUG` for troubleshooting
- Monitor logs in DigitalOcean dashboard

## 🆘 Getting Help

### Debug Information to Collect:
1. Build logs from DigitalOcean dashboard
2. Runtime logs from application
3. Environment variables (without sensitive values)
4. Error messages and stack traces

### Support Channels:
- 📚 Documentation: `docs/DIGITALOCEAN_DEPLOYMENT.md`
- 📧 Creator: choengrayu307@gmail.com
- 🐛 GitHub Issues: Create an issue in your repository

---

**Note:** All the issues mentioned above have been fixed in the current version. The deployment should now work successfully with Python 3.11 and compatible dependencies.
