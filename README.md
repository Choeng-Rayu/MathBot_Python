# 🤖 MathBot - Advanced Mathematical Assistant

A powerful Telegram bot that solves mathematical problems, generates graphs, creates PDFs, and manages alarms with AI assistance. Now optimized for DigitalOcean App Platform deployment with improved architecture.

## ✨ Features

### 🧮 Mathematical Capabilities
- **Basic Arithmetic**: Addition, subtraction, multiplication, division
- **Advanced Math**: Trigonometry, logarithms, exponentials
- **Algebra**: Equation solving, simplification
- **Calculus**: Derivatives, integrals, limits
- **Statistics**: Mean, median, mode, standard deviation

### 📊 Visualization
- **Graph Generation**: 2D function plotting with matplotlib
- **PDF Reports**: Comprehensive solution reports with graphs
- **Step-by-step Solutions**: Detailed mathematical explanations

### 🤖 AI Integration
- **DeepSeek AI**: Advanced problem-solving assistance
- **Natural Language**: Understands math problems in plain English
- **Context Awareness**: Remembers conversation history

### ⏰ Alarm System
- **Smart Alarms**: Set time-based reminders
- **Timezone Support**: Automatic timezone handling
- **Interactive Responses**: Snooze, dismiss, or respond to alarms

### 📸 OCR Support
- **Image Recognition**: Extract math from photos using Google Cloud Vision
- **Handwriting Support**: Recognizes handwritten equations
- **Automatic Solving**: Solves extracted mathematical expressions

### 📈 Analytics
- **User Statistics**: Track solving history and streaks
- **Performance Metrics**: Monitor bot usage and efficiency
- **Progress Tracking**: Personal mathematical journey

## 🏗️ Project Structure

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

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Telegram Bot Token
- MongoDB Atlas account
- DeepSeek API key
- DigitalOcean account (for production)

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/MathBot_Python.git
cd MathBot_Python
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment Setup:**
Create a `.env` file in the root directory:

```env
# Development Configuration
ENVIRONMENT=development
TELEGRAM_BOT_TOKEN=your_bot_token_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DEEPSEEK_API_KEY=your_deepseek_api_key_here
PORT=8000
LOG_LEVEL=INFO

# Optional: For OCR functionality
GOOGLE_CLOUD_CREDENTIALS_JSON=your_google_cloud_credentials_json_here
```

4. **Create Telegram Bot:**
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Copy the bot token to your `.env` file

5. **Setup MongoDB:**
   - Create a MongoDB Atlas cluster
   - Get the connection string
   - Add it to your `.env` file

6. **Run the bot:**
```bash
python main.py
```

## 🚀 Production Deployment

### DigitalOcean App Platform (Recommended)

For detailed deployment instructions, see [DigitalOcean Deployment Guide](docs/DIGITALOCEAN_DEPLOYMENT.md).

**Quick Steps:**
1. Push code to GitHub
2. Create DigitalOcean App
3. Connect GitHub repository
4. Set environment variables
5. Deploy and set webhook

### Docker Deployment

```bash
# Build the image
docker build -t mathbot .

# Run the container
docker run -d \
  --name mathbot \
  -p 8000:8000 \
  --env-file .env \
  mathbot
```

## 🧪 Testing

Run tests to ensure everything works:

```bash
# Run all tests
python -m pytest tests/ -v

# Test specific components
python tests/test_math.py
python tests/test_ai.py
```

## 📚 Documentation

- [DigitalOcean Deployment Guide](docs/DIGITALOCEAN_DEPLOYMENT.md)
- [OCR Setup Guide](docs/OCR_SETUP_GUIDE.md)
- [Enhanced Alarm Flow](docs/ENHANCED_ALARM_FLOW.md)
- [File Cleanup Summary](docs/FILE_CLEANUP_SUMMARY.md)

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Your Telegram bot token |
| `MONGODB_URI` | Yes | MongoDB connection string |
| `DEEPSEEK_API_KEY` | Yes | DeepSeek AI API key |
| `WEBHOOK_URL` | Production | Your app's webhook URL |
| `WEBHOOK_SECRET` | Recommended | Webhook security token |
| `GOOGLE_CLOUD_CREDENTIALS_JSON` | Optional | For OCR functionality |
| `ENVIRONMENT` | No | `development` or `production` |
| `LOG_LEVEL` | No | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Creator

**Choeng Rayu**
- 📧 Email: choengrayu307@gmail.com
- 📱 Telegram: @President_Alein
- 🌐 Website: https://rayuchoeng-profolio-website.netlify.app/

## 🆘 Support

If you encounter any issues:

1. Check the [troubleshooting guide](docs/DIGITALOCEAN_DEPLOYMENT.md#troubleshooting)
2. Review the logs in your deployment platform
3. Open an issue on GitHub
4. Contact the creator via Telegram

---

**Made with ❤️ for the mathematical community**
