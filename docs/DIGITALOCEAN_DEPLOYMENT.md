# 🚀 DigitalOcean Deployment Guide

This guide shows how to deploy your MathBot to DigitalOcean App Platform with GitHub integration and webhook support.

## 🏗️ Project Structure

The project has been refactored with a standard structure for better maintainability:

```
MathBot_Python/
├── app/
│   ├── core/           # Core application logic
│   ├── handlers/       # Telegram bot handlers
│   ├── services/       # Business logic services
│   └── models/         # Data models and database
├── config/             # Configuration files
├── docs/               # Documentation
├── scripts/            # Utility scripts
├── tests/              # Test files
├── deployment/         # Deployment configurations
├── .github/workflows/  # GitHub Actions
├── Dockerfile          # Docker configuration
├── main.py             # Application entry point
└── requirements.txt    # Python dependencies
```

## 📋 Prerequisites

1. ✅ DigitalOcean account
2. ✅ GitHub repository
3. ✅ Telegram Bot Token
4. ✅ MongoDB Atlas database
5. ✅ DeepSeek API key
6. ✅ Google Cloud Vision API credentials (optional, for OCR)

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. **Push the refactored code to GitHub:**
   ```bash
   git add .
   git commit -m "Refactor for DigitalOcean deployment"
   git push origin main
   ```

### Step 2: Create DigitalOcean App

1. **Go to DigitalOcean Dashboard:**
   - Visit [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
   - Click "Create App"

2. **Connect GitHub Repository:**
   - Choose "GitHub" as source
   - Select your repository: `YOUR_USERNAME/MathBot_Python`
   - Choose branch: `main`
   - Enable "Autodeploy" for automatic deployments

3. **Configure App Settings:**
   - **App Name**: `mathbot-telegram`
   - **Region**: Choose closest to your users
   - **Plan**: Basic ($5/month recommended)

### Step 3: Environment Variables

Set these environment variables in DigitalOcean App Platform:

#### Required Variables:
```env
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
WEBHOOK_URL=https://mathbot-telegram-xxxxx.ondigitalocean.app
WEBHOOK_SECRET=your_webhook_secret_here

# Database
MONGODB_URI=your_mongodb_connection_string_here

# AI Service
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=*
```

#### Optional (for OCR functionality):
```env
GOOGLE_CLOUD_CREDENTIALS_JSON=your_google_cloud_credentials_json_here
```

### Step 4: Deploy

1. **Review and Deploy:**
   - Review your configuration
   - Click "Create Resources"
   - Wait for deployment to complete (5-10 minutes)

2. **Get Your App URL:**
   - Note your app URL: `https://mathbot-telegram-xxxxx.ondigitalocean.app`
   - Update the `WEBHOOK_URL` environment variable with this URL

### Step 5: Set Webhook

After deployment, set the webhook:

1. **Automatic (via endpoint):**
   ```bash
   curl -X GET "https://your-app-url.ondigitalocean.app/set_webhook"
   ```

2. **Manual (using script):**
   ```bash
   python scripts/set_webhook.py set
   ```

## ✅ Verification

### Health Check
```bash
curl https://your-app-url.ondigitalocean.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "telegram_bot": "running",
  "alarm_scheduler": "running",
  "scheduled_jobs": 0,
  "environment": "production"
}
```

### Webhook Info
```bash
curl https://your-app-url.ondigitalocean.app/webhook_info
```

### Bot Statistics
```bash
curl https://your-app-url.ondigitalocean.app/stats
```

## 🔧 GitHub Actions (Automated Deployment)

The project includes GitHub Actions for automated testing and deployment:

1. **Set GitHub Secrets:**
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add: `DIGITALOCEAN_ACCESS_TOKEN`

2. **Automatic Deployment:**
   - Push to `main` branch triggers deployment
   - Tests run before deployment
   - Webhook is automatically set after deployment

## 🧪 Testing

1. **Send a message to your bot on Telegram**
2. **Test math solving:**
   ```
   /start
   🧮 Solve Math
   2 + 2 * 3
   ```

3. **Test OCR (if enabled):**
   - Send a photo with math content
   - Bot should extract and solve the math

4. **Test alarms:**
   ```
   ⏰ Set Alarm
   08:30
   ```

## 🔧 Troubleshooting

### Bot Not Responding
- Check environment variables are set correctly
- Verify `WEBHOOK_URL` matches your app URL
- Check app logs in DigitalOcean dashboard

### Database Connection Issues
- Verify `MONGODB_URI` is correct
- Check MongoDB Atlas network access settings
- Ensure database user has proper permissions

### OCR Not Working
- Verify `GOOGLE_CLOUD_CREDENTIALS_JSON` is set
- Check Google Cloud Vision API is enabled
- Ensure JSON credentials are valid

### Webhook Issues
- Check webhook info endpoint: `/webhook_info`
- Verify `WEBHOOK_SECRET` is set
- Try setting webhook manually: `/set_webhook`

## 📊 Monitoring

### App Metrics
- Monitor in DigitalOcean dashboard
- Check CPU, memory, and request metrics
- Set up alerts for downtime

### Logs
- View real-time logs in DigitalOcean dashboard
- Use log level `INFO` for production
- Set to `DEBUG` for troubleshooting

### Health Checks
- DigitalOcean automatically monitors `/health` endpoint
- App restarts automatically if health check fails

## 💰 Cost Optimization

### Basic Plan ($5/month)
- 512 MB RAM
- 1 vCPU
- Suitable for small to medium usage

### Scaling
- Monitor resource usage
- Upgrade plan if needed
- Consider horizontal scaling for high traffic

## 🔒 Security Best Practices

1. **Environment Variables:**
   - Never commit secrets to git
   - Use DigitalOcean's encrypted environment variables
   - Rotate credentials regularly

2. **Webhook Security:**
   - Always set `WEBHOOK_SECRET`
   - Use HTTPS only
   - Validate webhook signatures

3. **Database Security:**
   - Use MongoDB Atlas with authentication
   - Restrict network access
   - Regular backups

## 🔄 Updates and Maintenance

### Automatic Updates
- Push to `main` branch triggers deployment
- GitHub Actions handles testing and deployment
- Zero-downtime deployments

### Manual Updates
- Use DigitalOcean dashboard
- Deploy specific commits
- Rollback if needed

### Monitoring
- Set up alerts for errors
- Monitor bot usage statistics
- Regular health checks

---

**Need Help?** Check the troubleshooting section or contact support through the DigitalOcean dashboard.
