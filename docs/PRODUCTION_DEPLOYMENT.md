# 🚀 Production Deployment Guide

## Quick Deployment to DigitalOcean

Your app URL: **https://hybridcoffee-za9sy.ondigitalocean.app**

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Deploy MathBot with AI model selection to DigitalOcean"
git push origin main
```

### Step 2: DigitalOcean Environment Variables

Copy and paste these **EXACT** environment variables into DigitalOcean App Platform:

#### **Required Environment Variables:**

| Variable Name | Value |
|---------------|-------|
| `ENVIRONMENT` | `production` |
| `HOST` | `0.0.0.0` |
| `PORT` | `8000` |
| `LOG_LEVEL` | `INFO` |
| `TELEGRAM_BOT_TOKEN` | `7659640601:AAHvuGO4r1esUjG3HYqkdcKNsUlW2KjghR8` |
| `WEBHOOK_URL` | `https://hybridcoffee-za9sy.ondigitalocean.app` |
| `DEEPSEEK_API_KEY` | `sk-698124ba5ed24bcea3c8d298b73f2f52` |
| `GOOGLE_GEMINI_API_KEY` | `AIzaSyC2xuhoigUFCPp9g_MkhTrFbOKDlTWK6Ks` |
| `AI_MODEL` | `auto` |
| `MONGODB_URI` | `mongodb+srv://ChoengRayu:C9r6nhxOVLCUkkGd@cluster0.2ott03t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0` |
| `WEBHOOK_SECRET` | `mathbot_webhook_secret_2025_production` |
| `SECRET_KEY` | `mathbot_secret_key_2025_production_secure` |
| `ALLOWED_HOSTS` | `*` |

### Step 3: Deploy

1. Go to your DigitalOcean App Platform dashboard
2. Update your app with the new environment variables
3. Redeploy the application
4. Wait for deployment to complete

### Step 4: Set Webhook

After deployment, set the webhook:

```bash
curl -X GET "https://hybridcoffee-za9sy.ondigitalocean.app/set_webhook"
```

### Step 5: Test

1. **Health Check**: https://hybridcoffee-za9sy.ondigitalocean.app/health
2. **Bot Test**: https://t.me/rayumathbot
3. **Send**: `/start`
4. **Try**: `⚙️ Settings` to test AI model selection

## Features Available After Deployment

✅ **Dual AI Support**: Gemini + DeepSeek
✅ **User AI Model Selection**: Via Settings menu
✅ **Math Solving**: All mathematical capabilities
✅ **Alarm System**: Time-based reminders
✅ **OCR Support**: Image math extraction (if enabled)
✅ **PDF Generation**: Solution reports
✅ **Statistics**: User progress tracking

## Monitoring

- **App Dashboard**: DigitalOcean App Platform
- **Logs**: Real-time in DigitalOcean dashboard
- **Health**: https://hybridcoffee-za9sy.ondigitalocean.app/health
- **Stats**: https://hybridcoffee-za9sy.ondigitalocean.app/stats
