# 🚀 Render.com Deployment Guide with OCR

This guide shows how to securely deploy your MathBot with OCR functionality to Render.com.

## 🔒 Security First

✅ **Credentials are NOT in the repository** (as they should be)
✅ **Environment variables are used** for sensitive data
✅ **GitHub security protection** prevented credential exposure

## 📋 Prerequisites

1. ✅ Render.com account
2. ✅ GitHub repository (this one)
3. ✅ Google Cloud Vision API credentials (you have these)

## 🚀 Deployment Steps

### Step 1: Create New Web Service

1. Go to [Render.com Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository: `Choeng-Rayu/MathBot_Python`
4. Configure the service:
   - **Name**: `mathbot-python` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`

### Step 2: Set Environment Variables

In the Render.com dashboard, go to your service → "Environment" tab and add these variables:

#### Required Variables:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
MONGODB_URI=your_mongodb_connection_string_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
PORT=8000
WEBHOOK_URL=https://your-service-name.onrender.com
```

#### For OCR Functionality:
```
GOOGLE_CLOUD_CREDENTIALS_JSON=your_google_cloud_credentials_json_here
```

**Important**:
1. Replace all placeholder values with your actual credentials
2. For `GOOGLE_CLOUD_CREDENTIALS_JSON`, copy the entire JSON content from your local `google_vision_key.json` file as one line
3. The JSON should start with `{"type":"service_account"...` and be all on one line
4. Contact the bot administrator for the actual credential values if needed

### Step 3: Update Webhook URL

After deployment, update the `WEBHOOK_URL` environment variable with your actual Render URL:
```
WEBHOOK_URL=https://your-actual-service-name.onrender.com
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete
3. Check logs for successful startup

## ✅ Expected Deployment Logs

You should see:
```
✅ Google Cloud Vision OCR enabled
✅ Webhook set successfully to: https://your-service.onrender.com/webhook
✅ Telegram bot initialized successfully
🚀 Bot is now running and ready to receive messages!
```

## 🧪 Testing

1. Send a message to @rayumathbot
2. Send a photo with math content
3. Verify OCR functionality works

## 🔧 Troubleshooting

### OCR Not Working
- Check `GOOGLE_CLOUD_CREDENTIALS_JSON` is set correctly
- Verify the JSON is valid (no line breaks in the middle)
- Check Google Cloud Vision API is enabled

### Bot Not Responding
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check `WEBHOOK_URL` matches your Render service URL
- Look at deployment logs for errors

### Database Issues
- Verify `MONGODB_URI` is correct
- Check MongoDB Atlas network access settings

## 🔒 Security Best Practices

✅ **Never commit credentials** to git
✅ **Use environment variables** for all secrets
✅ **Rotate credentials** periodically
✅ **Monitor usage** in Google Cloud Console

## 💰 Cost Monitoring

- **Render.com**: Free tier available
- **Google Cloud Vision**: 1,000 free requests/month
- **MongoDB Atlas**: Free tier available

---

**Need Help?** Check the logs in Render.com dashboard or refer to the troubleshooting guides.
