import asyncio
import aiohttp
import json
import logging
from typing import List, Dict, Optional

from config import Config
from app.models.database import db_manager

logger = logging.getLogger(__name__)

class AIAssistant:
    def __init__(self):
        # DeepSeek configuration
        self.deepseek_api_key = Config.DEEPSEEK_API_KEY
        self.deepseek_api_url = Config.DEEPSEEK_API_URL

        # Google Gemini configuration
        self.gemini_api_key = Config.GOOGLE_GEMINI_API_KEY
        self.gemini_api_url = Config.GOOGLE_GEMINI_API_URL

        # AI model preference
        self.ai_model = Config.AI_MODEL
        
        # Personal information about the bot creator
        self.creator_info = {
            "name": "Choeng Rayu",
            "email": "choengrayu307@gmail.com",
            "telegram": "@President_Alein",
            "website": "https://rayuchoeng-profolio-website.netlify.app/",
            "purpose": "Created this bot for free to assist users with their needs"
        }
        
        # System prompt to train the AI
        self.system_prompt = f"""You are MathBot, an intelligent Telegram assistant created by {self.creator_info['name']} ({self.creator_info['telegram']}).

ABOUT YOUR CREATOR:
- Name: {self.creator_info['name']}
- Email: {self.creator_info['email']}
- Telegram: {self.creator_info['telegram']}
- Website: {self.creator_info['website']}
- Purpose: {self.creator_info['purpose']}

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

Remember: You are here to assist users with mathematics, learning, and productivity while representing your creator's dedication to helping others for free."""

    async def get_ai_response(self, user_message: str, user_id: int, conversation_history: List[Dict] = None) -> str:
        """Get AI response with automatic fallback between Gemini and DeepSeek"""
        try:
            # Prepare conversation history
            messages = [{"role": "system", "content": self.system_prompt}]

            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Keep last 10 messages for context

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Try AI with automatic fallback
            ai_response = await self.get_ai_response_with_fallback(messages, user_id)

            # Store conversation in database
            await self.store_conversation(user_id, user_message, ai_response)

            return ai_response

        except Exception as e:
            logger.error(f"Error in get_ai_response: {e}")
            return self.get_fallback_response(user_message)

    async def get_ai_response_with_fallback(self, messages: List[Dict], user_id: int) -> str:
        """Get AI response with automatic fallback between models"""

        # Get user's preferred AI model
        user_ai_preference = db_manager.get_user_preference(user_id, "ai_model", "auto")

        # Determine which AI to try first based on user preference
        if user_ai_preference == "gemini" and self.gemini_api_key:
            primary_ai = "gemini"
            fallback_ai = "deepseek"
        elif user_ai_preference == "deepseek" and self.deepseek_api_key:
            primary_ai = "deepseek"
            fallback_ai = "gemini"
        else:  # auto mode or fallback
            if self.gemini_api_key:
                primary_ai = "gemini"
                fallback_ai = "deepseek"
            else:
                primary_ai = "deepseek"
                fallback_ai = "gemini"

        # Try primary AI
        logger.info(f"Trying {primary_ai} AI for user {user_id}")

        if primary_ai == "gemini":
            response = await self.call_gemini_api(messages, user_id)
        else:
            response = await self.call_deepseek_api(messages, user_id)

        if response:
            # Get user preference to determine if they want to see AI model info
            ai_icons = {"gemini": "🧠", "deepseek": "🔬"}
            icon = ai_icons.get(primary_ai, "🤖")
            return f"{icon} **{primary_ai.title()} AI**: {response}"

        # Try fallback AI
        logger.info(f"Primary AI failed, trying {fallback_ai} AI for user {user_id}")

        if fallback_ai == "gemini" and self.gemini_api_key:
            response = await self.call_gemini_api(messages, user_id)
        elif fallback_ai == "deepseek" and self.deepseek_api_key:
            response = await self.call_deepseek_api(messages, user_id)

        if response:
            ai_icons = {"gemini": "🧠", "deepseek": "🔬"}
            icon = ai_icons.get(fallback_ai, "🤖")
            return f"{icon} **{fallback_ai.title()} AI** (fallback): {response}"

        # Both AIs failed
        return self.get_fallback_response("")

    async def call_deepseek_api(self, messages: List[Dict], user_id: int) -> Optional[str]:
        """Call DeepSeek API"""
        if not self.deepseek_api_key:
            logger.warning("DeepSeek API key not configured")
            return None

        try:
            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': 'deepseek-chat',
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 1000
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.deepseek_api_url, headers=headers, json=data, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'choices' in result and len(result['choices']) > 0:
                            response_text = result['choices'][0]['message']['content'].strip()
                            logger.info(f"DeepSeek AI response received for user {user_id}")
                            return response_text
                    else:
                        error_text = await response.text()
                        logger.error(f"DeepSeek API error {response.status}: {error_text}")
                        return None

        except asyncio.TimeoutError:
            logger.error("DeepSeek API timeout")
            return None
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            return None

    def get_fallback_response(self, user_message: str = "") -> str:
        """Provide fallback responses when AI is unavailable"""
        message_lower = user_message.lower()
        
        # Math-related keywords
        if any(keyword in message_lower for keyword in ['math', 'calculate', 'solve', 'equation', 'expression']):
            return (
                "🧮 I'd love to help you with math! Please use the '🧮 Solve Math' button to enter your mathematical expression, "
                "and I'll solve it for you with detailed steps and a PDF report!"
            )
        
        # Function-related keywords
        elif any(keyword in message_lower for keyword in ['function', 'graph', 'derivative', 'analyze', 'plot']):
            return (
                "📈 For function analysis, please use the '📈 Solve Function' button! I can analyze your function's domain, "
                "derivatives, critical points, and create beautiful graphs with comprehensive PDF reports."
            )
        
        # Alarm-related keywords
        elif any(keyword in message_lower for keyword in ['alarm', 'reminder', 'schedule', 'time', 'notify']):
            return (
                "⏰ Want to set an alarm? Use the '⏰ Set Alarm' button! I can help you create up to 10 alarms with "
                "streak tracking to build great habits. Just tell me the time in HH:MM format!"
            )
        
        # Creator-related keywords
        elif any(keyword in message_lower for keyword in ['creator', 'developer', 'made', 'who', 'rayu', 'choeng']):
            return (
                f"👨‍💻 I was created by {self.creator_info['name']} ({self.creator_info['telegram']})!\n\n"
                f"📧 Email: {self.creator_info['email']}\n"
                f"🌐 Website: {self.creator_info['website']}\n\n"
                f"He built me for free to help users like you with mathematics and productivity! 🎉"
            )
        
        # General greeting
        elif any(keyword in message_lower for keyword in ['hello', 'hi', 'hey', 'start', 'help']):
            return (
                "👋 Hello! I'm MathBot, your intelligent mathematical assistant!\n\n"
                "I can help you with:\n"
                "🧮 **Solve Math** - Complex mathematical expressions\n"
                "📈 **Analyze Functions** - Complete function analysis with graphs\n"
                "⏰ **Set Alarms** - Custom reminders with streak tracking\n"
                "💬 **Chat** - General conversation and assistance\n\n"
                "What would you like to do today?"
            )
        
        # Default response
        else:
            return (
                "🤖 I'm here to help! I can assist you with:\n\n"
                "🧮 Mathematical calculations and expressions\n"
                "📈 Function analysis and graphing\n"
                "⏰ Setting alarms and reminders\n"
                "💬 General questions and conversation\n\n"
                "Please use the menu buttons or ask me anything!"
            )
    
    async def store_conversation(self, user_id: int, user_message: str, ai_response: str):
        """Store conversation history in database"""
        try:
            from datetime import datetime
            import pytz
            
            timezone = pytz.timezone(Config.TIMEZONE)
            timestamp = datetime.now(timezone)
            
            conversation_entry = {
                "timestamp": timestamp,
                "user_message": user_message,
                "ai_response": ai_response
            }
            
            # Update user's conversation history (keep last 50 messages)
            db_manager.users.update_one(
                {"user_id": user_id},
                {
                    "$push": {
                        "conversation_history": {
                            "$each": [conversation_entry],
                            "$slice": -50  # Keep only last 50 conversations
                        }
                    }
                },
                upsert=True
            )
            
        except Exception as e:
            print(f"Error storing conversation: {e}")
    
    async def get_conversation_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's conversation history"""
        try:
            user = db_manager.get_user(user_id)
            if user and "conversation_history" in user:
                history = user["conversation_history"][-limit:]
                
                # Convert to OpenAI format
                formatted_history = []
                for entry in history:
                    formatted_history.append({"role": "user", "content": entry["user_message"]})
                    formatted_history.append({"role": "assistant", "content": entry["ai_response"]})
                
                return formatted_history
            
            return []
            
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    def is_ai_conversation(self, message: str) -> bool:
        """Determine if message should be handled by AI"""
        # Don't handle if it's a clear math expression or function
        if self.is_math_expression(message) or self.is_function_expression(message) or self.is_alarm_time(message):
            return False
        
        # Handle if it's a question or general conversation
        conversation_indicators = [
            '?', 'what', 'how', 'why', 'when', 'where', 'who', 'can you', 'help', 'tell me',
            'explain', 'hello', 'hi', 'hey', 'thanks', 'thank you', 'please', 'sorry'
        ]
        
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in conversation_indicators) or len(message.split()) > 3
    
    def is_math_expression(self, text: str) -> bool:
        """Check if text looks like a math expression"""
        import re
        math_patterns = [
            r'[\+\-\*/\^]',  # Basic operators
            r'(sin|cos|tan|log|ln|sqrt|exp|abs)',  # Functions
            r'\d+\.\d+',  # Decimals
            r'\(\d+\)',  # Numbers in parentheses
        ]
        return any(re.search(pattern, text.lower()) for pattern in math_patterns)
    
    def is_function_expression(self, text: str) -> bool:
        """Check if text looks like a function definition"""
        import re
        function_patterns = [
            r'f\(x\)\s*=',
            r'y\s*=',
            r'x\^?\d+',  # x with power
            r'x[\+\-\*/]',  # x with operators
        ]
        return any(re.search(pattern, text.lower()) for pattern in function_patterns)
    
    def is_alarm_time(self, text: str) -> bool:
        """Check if text looks like a time format"""
        import re
        time_pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
        return bool(re.match(time_pattern, text.strip()))

    async def call_gemini_api(self, messages: List[Dict], user_id: int) -> Optional[str]:
        """Call Google Gemini API"""
        if not self.gemini_api_key:
            logger.warning("Gemini API key not configured")
            return None

        try:
            # Convert messages to Gemini format
            prompt = self._convert_messages_to_gemini_prompt(messages)

            headers = {
                'Content-Type': 'application/json',
            }

            # Gemini API uses query parameter for API key
            url = f"{self.gemini_api_url}?key={self.gemini_api_key}"

            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()

                        # Extract response from Gemini format
                        if 'candidates' in result and len(result['candidates']) > 0:
                            candidate = result['candidates'][0]
                            if 'content' in candidate and 'parts' in candidate['content']:
                                parts = candidate['content']['parts']
                                if len(parts) > 0 and 'text' in parts[0]:
                                    response_text = parts[0]['text'].strip()
                                    logger.info(f"Gemini AI response received for user {user_id}")
                                    return response_text

                        logger.warning(f"Unexpected Gemini response format: {result}")
                        return None
                    else:
                        error_text = await response.text()
                        logger.error(f"Gemini API error {response.status}: {error_text}")
                        return None

        except asyncio.TimeoutError:
            logger.error("Gemini API timeout")
            return None
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return None

    def _convert_messages_to_gemini_prompt(self, messages: List[Dict]) -> str:
        """Convert OpenAI-style messages to Gemini prompt format"""
        prompt_parts = []

        for message in messages:
            role = message.get('role', '')
            content = message.get('content', '')

            if role == 'system':
                prompt_parts.append(f"System: {content}")
            elif role == 'user':
                prompt_parts.append(f"User: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")

        return "\n\n".join(prompt_parts)

# Global AI assistant instance
ai_assistant = AIAssistant()
