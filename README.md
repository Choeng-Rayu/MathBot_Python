# MathBot - Telegram Mathematical Assistant

A comprehensive Telegram bot that provides mathematical expression solving, function analysis, and custom alarm functionality with streak tracking.

## Features

### 🧮 Mathematical Expression Solver
- Evaluates complex mathematical expressions
- Supports trigonometric functions (sin, cos, tan)
- Logarithmic and exponential functions (log, ln, exp)
- Mathematical constants (pi, e)
- Generates professional PDF reports with step-by-step solutions

### 📈 Function Analyzer
- Complete mathematical function analysis
- Domain and range determination
- First and second derivatives
- Critical points and extrema
- Limits at infinity
- Sign and variation tables
- Function graphs with matplotlib
- Intercepts and asymptotes analysis
- Professional PDF reports with embedded graphs

### ⏰ Custom Alarm System
- Set up to 10 alarms per user
- Timezone support (Asia/Phnom_Penh)
- Streak tracking for habit building
- Motivational messages
- Inline keyboard responses
- Automatic streak reset on timeout

### 🤖 AI Assistant Integration
- Natural conversation with DeepSeek AI
- Contextual responses with conversation memory
- Personalized assistance from Choeng Rayu's AI
- Intelligent help with math concepts and learning
- Fallback responses when AI is unavailable
- Seamless integration with bot features

## Installation

### Prerequisites
- Python 3.8+
- MongoDB Atlas account
- Telegram Bot Token

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd MathBot_Python
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration:**
```bash
cp .env.example .env
```

Edit `.env` file with your credentials:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-domain.com
DEEPSEEK_API_KEY=your_deepseek_api_key_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
PORT=8000
```

4. **Create Telegram Bot:**
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Copy the bot token to your `.env` file

5. **Setup MongoDB:**
   - Create a MongoDB Atlas cluster
   - Get the connection string
   - Add it to your `.env` file

## Deployment

### Local Development
```bash
python main.py
```

### Production Deployment (Render/Heroku)

1. **Deploy to Render:**
   - Connect your GitHub repository
   - Set environment variables
   - Deploy the service

2. **Set Webhook:**
   After deployment, visit:
   ```
   https://your-domain.com/set_webhook
   ```

## Usage

### Bot Commands

- `/start` - Initialize the bot and show main menu
- Send math expressions directly (e.g., `2^3 + log(100)`)
- Send function definitions (e.g., `f(x) = x^2 + 2x + 1`)
- Send alarm times (e.g., `08:30`)

### Menu Options

- **🧮 Solve Math** - Enter mathematical expressions
- **📈 Solve Function** - Analyze mathematical functions
- **⏰ Set Alarm** - Create custom alarms
- **📊 My Stats** - View your statistics and streak
- **📋 List Alarms** - Manage your alarms
- **🤖 AI Chat** - Natural conversation with intelligent AI assistant

### Mathematical Expression Examples

```
2^3 + log(100) + sin(pi/2)
sqrt(16) * cos(0) + 5!
exp(2) - ln(10) + abs(-5)
tan(pi/4) + log10(1000)
```

### Function Analysis Examples

```
f(x) = x^2 + 2x + 1
y = sin(x) + cos(x)
f(x) = ln(x) + x^3
y = 1/x + x^2
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /webhook` - Telegram webhook endpoint
- `GET /set_webhook` - Set webhook URL
- `GET /webhook_info` - Get webhook information
- `GET /stats` - Bot usage statistics

## Project Structure

```
MathBot_Python/
├── main.py                 # FastAPI application and webhook
├── bot_handlers.py         # Telegram bot command handlers
├── math_solver.py          # Mathematical expression evaluation
├── function_analyzer.py    # Function analysis and graphing
├── alarm_manager.py        # Alarm scheduling and management
├── database.py             # MongoDB operations
├── pdf_generator.py        # PDF creation with graphs
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Technical Details

### Architecture
- **FastAPI** - Web framework for webhook handling
- **python-telegram-bot** - Telegram Bot API wrapper
- **MongoDB** - User data and alarm storage
- **APScheduler** - Alarm scheduling
- **SymPy** - Mathematical computation
- **Matplotlib** - Graph generation
- **ReportLab** - PDF generation

### Database Schema
```javascript
{
  "user_id": 123456789,
  "username": "user123",
  "first_name": "John",
  "alarms": [
    {
      "time": "08:30",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "streak": 5,
  "last_activity": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Features Implementation

#### Math Solver
- Uses SymPy for symbolic mathematics
- Supports complex expressions with multiple functions
- Generates step-by-step solutions
- Error handling for invalid expressions

#### Function Analyzer
- Complete calculus analysis
- Matplotlib integration for graphs
- Professional mathematical notation
- Comprehensive PDF reports

#### Alarm System
- Cron-based scheduling with APScheduler
- Timezone-aware notifications
- Streak tracking with motivational messages
- Timeout handling for missed responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions:
- Create an issue on GitHub
- Contact the development team

## Changelog

### Version 1.0.0
- Initial release
- Math expression solver
- Function analyzer with graphs
- Alarm system with streak tracking
- PDF report generation
- Webhook-based architecture
