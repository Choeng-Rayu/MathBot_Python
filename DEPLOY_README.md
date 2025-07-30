# 🚀 Quick Deployment Guide

## Your App Details
- **App URL**: https://hybridcoffee-za9sy.ondigitalocean.app
- **Bot URL**: https://t.me/rayumathbot
- **GitHub**: Push to main branch for auto-deploy

## 📋 Environment Variables for DigitalOcean

Copy and paste these **EXACT** values into DigitalOcean App Platform Environment Variables:

```
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
TELEGRAM_BOT_TOKEN=7659640601:AAHvuGO4r1esUjG3HYqkdcKNsUlW2KjghR8
WEBHOOK_URL=https://hybridcoffee-za9sy.ondigitalocean.app
DEEPSEEK_API_KEY=sk-698124ba5ed24bcea3c8d298b73f2f52
GOOGLE_GEMINI_API_KEY=AIzaSyC2xuhoigUFCPp9g_MkhTrFbOKDlTWK6Ks
AI_MODEL=auto
MONGODB_URI=mongodb+srv://ChoengRayu:C9r6nhxOVLCUkkGd@cluster0.2ott03t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
WEBHOOK_SECRET=mathbot_webhook_secret_2025_production
SECRET_KEY=mathbot_secret_key_2025_production_secure
ALLOWED_HOSTS=*
```

## 🚀 Quick Deploy

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to production"
   git push origin main
   ```

2. **Update DigitalOcean**:
   - Add environment variables above
   - Redeploy app

3. **Set Webhook**:
   ```bash
   curl https://hybridcoffee-za9sy.ondigitalocean.app/set_webhook
   ```

4. **Test**:
   - Health: https://hybridcoffee-za9sy.ondigitalocean.app/health
   - Bot: https://t.me/rayumathbot

## ✅ Features Ready

- 🤖 **Dual AI**: Gemini + DeepSeek
- ⚙️ **AI Selection**: User can choose AI model
- 🧮 **Math Solving**: All mathematical capabilities
- ⏰ **Alarms**: Time-based reminders
- 📊 **Statistics**: User progress tracking
