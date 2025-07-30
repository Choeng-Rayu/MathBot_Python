const fetch = require('node-fetch');
const Config = require('./config').Config;
const dbManager = require('./database').db_manager;

class AIAssistant {
    constructor() {
        this.apiKey = Config.DEEPSEEK_API_KEY;
        this.apiUrl = Config.DEEPSEEK_API_URL;

        this.creatorInfo = {
            name: "Choeng Rayu",
            email: "choengrayu307@gmail.com",
            telegram: "@President_Alein",
            website: "https://rayuchoeng-profolio-website.netlify.app/",
            purpose: "Created this bot for free to assist users with their needs"
        };

        this.systemPrompt = `You are MathBot, an intelligent Telegram assistant created by ${this.creatorInfo.name} (${this.creatorInfo.telegram}).

ABOUT YOUR CREATOR:
- Name: ${this.creatorInfo.name}
- Email: ${this.creatorInfo.email}
- Telegram: ${this.creatorInfo.telegram}
- Website: ${this.creatorInfo.website}
- Purpose: ${this.creatorInfo.purpose}

YOUR CAPABILITIES:
1. 🧮 Mathematical Expression Solving - You can solve complex mathematical expressions including:
   - Basic arithmetic operations
   - Trigonometric functions (sin, cos, tan)
   - Logarithmic and exponential functions
   - Mathematical constants (pi, e)
   - Generate step-by-step solutions with PDF reports

2. 📈 Function Analysis - You can analyze mathematical functions including:
   - Domain and range analysis
   - First and second derivatives
   - Critical points and extrema
   - Limits at infinity
   - Sign and variation tables
   - Function graphs with detailed analysis
   - Professional PDF reports with embedded graphs

3. ⏰ Alarm System - You can help users set custom alarms with:
   - Up to 10 alarms per user
   - Streak tracking for habit building
   - Motivational messages
   - Timezone support (Asia/Phnom_Penh)

4. 💬 General Conversation - You can have natural conversations and help with various topics.

PERSONALITY:
- Be friendly, helpful, and encouraging
- Use emojis to make conversations more engaging
- Be patient and explain things clearly
- Show enthusiasm for mathematics and learning
- Be proud of your creator's work and mention them when appropriate
- Always try to help users achieve their goals

IMPORTANT GUIDELINES:
- When users ask about math expressions, guide them to use the 🧮 Solve Math feature
- When users ask about function analysis, guide them to use the 📈 Solve Function feature
- When users want to set reminders or alarms, guide them to use the ⏰ Set Alarm feature
- Always be respectful and professional
- If you don't know something, admit it and suggest alternatives
- Encourage users to explore all the bot's features

Remember: You are here to assist users with mathematics, learning, and productivity while representing your creator's dedication to helping others for free.`;
    }

    async getAIResponse(userMessage, userId, conversationHistory = []) {
        try {
            let messages = [{ role: "system", content: this.systemPrompt }];
            if (conversationHistory && conversationHistory.length > 0) {
                messages = messages.concat(conversationHistory.slice(-10));
            }
            messages.push({ role: "user", content: userMessage });

            const payload = {
                model: "deepseek-chat",
                messages: messages,
                max_tokens: 1000,
                temperature: 0.7,
                stream: false
            };

            const headers = {
                "Authorization": `Bearer ${this.apiKey}`,
                "Content-Type": "application/json"
            };

            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(payload),
                timeout: 30000
            });

            if (response.status === 200) {
                const result = await response.json();
                const aiResponse = result.choices[0].message.content;
                await this.storeConversation(userId, userMessage, aiResponse);
                return aiResponse;
            } else {
                const errorText = await response.text();
                console.error(`DeepSeek API error ${response.status}: ${errorText}`);
                return this.getFallbackResponse(userMessage);
            }
        } catch (e) {
            if (e.type === 'request-timeout') {
                console.error("DeepSeek API timeout");
                return "⏰ Sorry, I'm taking a bit longer to respond. Please try again!";
            }
            console.error(`Error calling DeepSeek API: ${e}`);
            return this.getFallbackResponse(userMessage);
        }
    }

    getFallbackResponse(userMessage) {
        const messageLower = userMessage.toLowerCase();

        if (['math', 'calculate', 'solve', 'equation', 'expression'].some(k => messageLower.includes(k))) {
            return "🧮 I'd love to help you with math! Please use the '🧮 Solve Math' button to enter your mathematical expression, and I'll solve it for you with detailed steps and a PDF report!";
        } else if (['function', 'graph', 'derivative', 'analyze', 'plot'].some(k => messageLower.includes(k))) {
            return "📈 For function analysis, please use the '📈 Solve Function' button! I can analyze your function's domain, derivatives, critical points, and create beautiful graphs with comprehensive PDF reports.";
        } else if (['alarm', 'reminder', 'schedule', 'time', 'notify'].some(k => messageLower.includes(k))) {
            return "⏰ Want to set an alarm? Use the '⏰ Set Alarm' button! I can help you create up to 10 alarms with streak tracking to build great habits. Just tell me the time in HH:MM format!";
        } else if (['creator', 'developer', 'made', 'who', 'rayu', 'choeng'].some(k => messageLower.includes(k))) {
            return `👨‍💻 I was created by ${this.creatorInfo.name} (${this.creatorInfo.telegram})!\n\n📧 Email: ${this.creatorInfo.email}\n🌐 Website: ${this.creatorInfo.website}\n\nHe built me for free to help users like you with mathematics and productivity! 🎉`;
        } else if (['hello', 'hi', 'hey', 'start', 'help'].some(k => messageLower.includes(k))) {
            return "👋 Hello! I'm MathBot, your intelligent mathematical assistant!\n\nI can help you with:\n🧮 **Solve Math** - Complex mathematical expressions\n📈 **Analyze Functions** - Complete function analysis with graphs\n⏰ **Set Alarms** - Custom reminders with streak tracking\n💬 **Chat** - General conversation and assistance\n\nWhat would you like to do today?";
        } else {
            return "🤖 I'm here to help! I can assist you with:\n\n🧮 Mathematical calculations and expressions\n📈 Function analysis and graphing\n⏰ Setting alarms and reminders\n💬 General questions and conversation\n\nPlease use the menu buttons or ask me anything!";
        }
    }

    async storeConversation(userId, userMessage, aiResponse) {
        try {
            const timestamp = new Date().toISOString();
            const conversationEntry = {
                timestamp: timestamp,
                user_message: userMessage,
                ai_response: aiResponse
            };
            // Update user's conversation history (keep last 50 messages)
            await dbManager.users.updateOne(
                { user_id: userId },
                {
                    $push: {
                        conversation_history: {
                            $each: [conversationEntry],
                            $slice: -50
                        }
                    }
                },
                { upsert: true }
            );
        } catch (e) {
            console.error(`Error storing conversation: ${e}`);
        }
    }

    async getConversationHistory(userId, limit = 10) {
        try {
            const user = await dbManager.get_user(userId);
            if (user && user.conversation_history) {
                const history = user.conversation_history.slice(-limit);
                const formattedHistory = [];
                for (const entry of history) {
                    formattedHistory.push({ role: "user", content: entry.user_message });
                    formattedHistory.push({ role: "assistant", content: entry.ai_response });
                }
                return formattedHistory;
            }
            return [];
        } catch (e) {
            console.error(`Error getting conversation history: ${e}`);
            return [];
        }
    }

    isAIConversation(message) {
        if (this.isMathExpression(message) || this.isFunctionExpression(message) || this.isAlarmTime(message)) {
            return false;
        }
        const conversationIndicators = [
            '?', 'what', 'how', 'why', 'when', 'where', 'who', 'can you', 'help', 'tell me',
            'explain', 'hello', 'hi', 'hey', 'thanks', 'thank you', 'please', 'sorry'
        ];
        const messageLower = message.toLowerCase();
        return conversationIndicators.some(ind => messageLower.includes(ind)) || message.split(/\s+/).length > 3;
    }

    isMathExpression(text) {
        const mathPatterns = [
            /[\+\-\*\/\^]/, // Basic operators
            /(sin|cos|tan|log|ln|sqrt|exp|abs)/i, // Functions
            /\d+\.\d+/, // Decimals
            /\(\d+\)/ // Numbers in parentheses
        ];
        return mathPatterns.some(pattern => pattern.test(text));
    }

    isFunctionExpression(text) {
        const functionPatterns = [
            /f\(x\)\s*=/i,
            /y\s*=/i,
            /x\^?\d+/i, // x with power
            /x[\+\-\*\/]/i // x with operators
        ];
        return functionPatterns.some(pattern => pattern.test(text));
    }

    isAlarmTime(text) {
        const timePattern = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
        return timePattern.test(text.trim());
    }
}

// Global AI assistant instance
const aiAssistant = new AIAssistant();
module.exports = { aiAssistant, AIAssistant };