# MathBot Deployment Guide

This guide will help you deploy your AI-powered MathBot to production.

## 🚀 Quick Deployment Checklist

- [ ] Telegram Bot Token obtained
- [ ] DeepSeek AI API Key configured
- [ ] MongoDB Atlas cluster created
- [ ] Environment variables configured
- [ ] Webhook URL set up
- [ ] Dependencies installed
- [ ] Tests passed

## 📋 Prerequisites

### 1. Telegram Bot Setup
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot: `/newbot`
3. Choose a name and username for your bot
4. Copy the bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. DeepSeek AI API Key
- Your API key: `sk-698124ba5ed24bcea3c8d298b73f2f52`
- Already configured in your `.env` file

### 3. MongoDB Atlas
- Your connection string is already configured
- Database: `telegram_math_bot`
- Collection: `users`

## 🔧 Local Development Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Your `.env` file is already configured with:
```env
TELEGRAM_BOT_TOKEN=7645640741:AAEQzRGjycPrhJCU52qNY8WA74BW2y5Hocw
WEBHOOK_URL=https://alarmbot-d1r4.onrender.com
DEEPSEEK_API_KEY=sk-698124ba5ed24bcea3c8d298b73f2f52
MONGODB_URI=mongodb+srv://ChoengRayu:C9r6nhxOVLCUkkGd@cluster0.2ott03t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
PORT=8000
```

### 3. Run Tests
```bash
# Test mathematical components
python test_math.py

# Test AI functionality
python test_ai.py
```

### 4. Start Local Development
```bash
python run.py
```

## 🌐 Production Deployment

### Option 1: Render (Recommended)

1. **Connect Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `mathbot-telegram`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

3. **Environment Variables**
   Add these in Render dashboard:
   ```
   TELEGRAM_BOT_TOKEN=7645640741:AAEQzRGjycPrhJCU52qNY8WA74BW2y5Hocw
   WEBHOOK_URL=https://your-render-app.onrender.com
   DEEPSEEK_API_KEY=sk-698124ba5ed24bcea3c8d298b73f2f52
   MONGODB_URI=mongodb+srv://ChoengRayu:C9r6nhxOVLCUkkGd@cluster0.2ott03t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
   PORT=8000
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your app URL: `https://your-app-name.onrender.com`

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI
   npm install -g heroku
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-mathbot-app
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=7645640741:AAEQzRGjycPrhJCU52qNY8WA74BW2y5Hocw
   heroku config:set WEBHOOK_URL=https://your-mathbot-app.herokuapp.com
   heroku config:set DEEPSEEK_API_KEY=sk-698124ba5ed24bcea3c8d298b73f2f52
   heroku config:set MONGODB_URI="mongodb+srv://ChoengRayu:C9r6nhxOVLCUkkGd@cluster0.2ott03t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy MathBot with AI"
   git push heroku main
   ```

## 🔗 Post-Deployment Setup

### 1. Set Webhook
After deployment, visit your webhook setup endpoint:
```
https://your-app-url.com/set_webhook
```

### 2. Verify Deployment
Check these endpoints:
- Health check: `https://your-app-url.com/health`
- Bot stats: `https://your-app-url.com/stats`
- Webhook info: `https://your-app-url.com/webhook_info`

### 3. Test Your Bot
1. Find your bot on Telegram: `@your_bot_username`
2. Send `/start` to initialize
3. Test all features:
   - 🧮 Math solving
   - 📈 Function analysis
   - ⏰ Alarm setting
   - 🤖 AI conversation

## 🔍 Monitoring & Troubleshooting

### Health Checks
```bash
# Check if bot is running
curl https://your-app-url.com/health

# Check webhook status
curl https://your-app-url.com/webhook_info

# Check bot statistics
curl https://your-app-url.com/stats
```

### Common Issues

1. **Webhook Not Set**
   - Visit: `https://your-app-url.com/set_webhook`
   - Check response for success

2. **AI Not Responding**
   - Verify DeepSeek API key is correct
   - Check API quota and limits
   - Review logs for API errors

3. **Database Connection Issues**
   - Verify MongoDB URI is correct
   - Check MongoDB Atlas network access
   - Ensure database user has proper permissions

4. **Math/Function Errors**
   - Check if all Python packages are installed
   - Verify matplotlib can generate graphs
   - Test PDF generation locally

### Logs
```bash
# Heroku logs
heroku logs --tail

# Render logs
# Available in Render dashboard
```

## 🔒 Security Considerations

1. **Environment Variables**
   - Never commit `.env` file to repository
   - Use platform-specific environment variable settings
   - Rotate API keys periodically

2. **MongoDB Security**
   - Use strong passwords
   - Enable IP whitelisting
   - Regular backups

3. **Bot Security**
   - Monitor bot usage
   - Implement rate limiting if needed
   - Regular security updates

## 📊 Performance Optimization

1. **Database Indexing**
   - User ID index (already implemented)
   - Consider additional indexes for heavy queries

2. **AI Response Caching**
   - Consider caching common responses
   - Implement conversation context limits

3. **PDF Generation**
   - Clean up temporary files (already implemented)
   - Consider using cloud storage for large files

## 🎯 Your Bot Information

**Creator**: Choeng Rayu (@President_Alein)
**Email**: choengrayu307@gmail.com
**Website**: https://rayuchoeng-profolio-website.netlify.app/
**Purpose**: Free mathematical assistance for users

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review application logs
3. Test individual components with test scripts
4. Contact the development team

## 🎉 Congratulations!

Your AI-powered MathBot is now ready to help users with:
- ✅ Mathematical expression solving
- ✅ Function analysis with graphs
- ✅ Custom alarms with streak tracking
- ✅ Intelligent AI conversations
- ✅ Professional PDF reports

Users can now interact naturally with your bot and get personalized assistance!
