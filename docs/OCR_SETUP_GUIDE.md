# 📷 OCR Setup Guide - Google Cloud Vision API

This guide will help you set up Google Cloud Vision API to enable text extraction from photos in your Telegram bot.

## 🎯 What This Enables

Once configured, your bot will be able to:
- ✅ Extract text from photos containing math calculations
- ✅ Automatically solve math expressions found in images
- ✅ Analyze functions written in photos
- ✅ Process handwritten or printed mathematical content

## 💰 Cost Information

- **Free Tier**: 1,000 text detection requests per month
- **Additional Credits**: $300 free credits for new Google Cloud users
- **Cost After Free Tier**: ~$1.50 per 1,000 requests

## 🚀 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Sign in with your Google account
3. Click the project selector (top left) → "New Project"
4. Name your project (e.g., "MathBot-OCR")
5. Click "Create"

### Step 2: Enable Billing

1. In Google Cloud Console, go to "Billing"
2. Link a credit card (required for free tier)
3. **Note**: No charges unless you exceed free limits

### Step 3: Enable Cloud Vision API

1. Go to "APIs & Services" → "Enabled APIs & Services"
2. Click "+ ENABLE APIS AND SERVICES"
3. Search for "Cloud Vision API"
4. Click "ENABLE"

### Step 4: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" → "Service Account"
3. Name it (e.g., "mathbot-vision-access")
4. Click "CREATE AND CONTINUE"
5. For role, select "Cloud Vision API User"
6. Click "CONTINUE" → "DONE"

### Step 5: Download Credentials

1. On the Credentials page, find your service account
2. Click the three dots → "Manage keys"
3. Click "ADD KEY" → "Create new key"
4. Choose "JSON" → "CREATE"
5. Save the downloaded file as `google_vision_key.json`

### Step 6: Configure Your Bot

#### For Local Development:

1. Place `google_vision_key.json` in your project root
2. Update your `.env` file:
```
GOOGLE_CLOUD_CREDENTIALS_PATH=google_vision_key.json
```

#### For Render.com Deployment:

1. Copy the entire content of `google_vision_key.json`
2. In Render.com dashboard, go to your service
3. Go to "Environment" tab
4. Add environment variable:
   - **Key**: `GOOGLE_CLOUD_CREDENTIALS_JSON`
   - **Value**: Paste the entire JSON content

5. Update your production `.env` or Render environment:
```
GOOGLE_CLOUD_CREDENTIALS_PATH=/tmp/google_credentials.json
```

6. Add this code to your `main.py` startup (for Render.com):
```python
# Add this to setup_telegram_bot function
import json
import tempfile

# Setup Google Cloud credentials for Render.com
if os.getenv('GOOGLE_CLOUD_CREDENTIALS_JSON'):
    credentials_json = os.getenv('GOOGLE_CLOUD_CREDENTIALS_JSON')
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(credentials_json)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
```

## 🧪 Testing the Setup

1. Install the required package:
```bash
pip install google-cloud-vision
```

2. Test with this simple script:
```python
from ocr_service import ocr_service

# Check if OCR is enabled
if ocr_service.is_enabled:
    print("✅ OCR service is ready!")
else:
    print("❌ OCR service not configured")
```

3. Send a photo with math content to your bot
4. The bot should extract and process the text automatically

## 📱 How It Works

1. **User sends photo** → Bot receives image
2. **OCR Processing** → Google Vision API extracts text
3. **Math Detection** → Bot checks if text contains math
4. **Auto-Processing** → Bot automatically solves math expressions
5. **Results** → User gets solved math with PDF report

## 🔧 Troubleshooting

### "OCR service is not available"
- Check that `GOOGLE_CLOUD_CREDENTIALS_PATH` is set correctly
- Verify the JSON file exists and is valid
- Ensure Google Cloud Vision API is enabled

### "Unauthorized" errors
- Verify your service account has "Cloud Vision API User" role
- Check that billing is enabled on your Google Cloud project
- Ensure the JSON credentials file is not corrupted

### Poor text recognition
- Use clear, well-lit photos
- Ensure text is large and readable
- Avoid blurry or tilted images
- Try different angles or lighting

## 💡 Tips for Best Results

- **Good Lighting**: Natural light works best
- **Clear Text**: Printed text works better than handwritten
- **Proper Angle**: Take photos straight-on, not at an angle
- **High Resolution**: Use good quality camera settings
- **Contrast**: Dark text on light background works best

## 🔒 Security Notes

- Keep your `google_vision_key.json` file secure
- Never commit credentials to version control
- Use environment variables for production
- Regularly rotate service account keys

## 📊 Usage Monitoring

Monitor your usage in Google Cloud Console:
1. Go to "APIs & Services" → "Quotas"
2. Search for "Vision API"
3. Check your current usage against limits

---

**Need Help?** If you encounter issues, check the Google Cloud Vision API documentation or contact support.
