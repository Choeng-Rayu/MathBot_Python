import re
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db_manager
from math_solver import math_solver
from function_analyzer import function_analyzer
from pdf_generator import pdf_generator
from alarm_manager import alarm_manager
from ai_assistant import ai_assistant
from config import Config
import os

class BotHandlers:
    def __init__(self):
        # Define custom keyboard
        self.main_keyboard = [
            ['🧮 Solve Math', '📈 Solve Function'],
            ['⏰ Set Alarm', '📊 My Stats'],
            ['📋 List Alarms', '🤖 AI Chat']
        ]
        self.reply_markup = ReplyKeyboardMarkup(
            self.main_keyboard, 
            resize_keyboard=True, 
            one_time_keyboard=False
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        
        # Check if user exists, if not create them
        existing_user = db_manager.get_user(user_id)
        if not existing_user:
            success = db_manager.create_user(
                user_id=user_id,
                username=user.username,
                first_name=user.first_name
            )
            if success:
                welcome_message = (
                    f"🎉 Welcome to MathBot, {user.first_name}!\n\n"
                    "I can help you with:\n"
                    "🧮 **Solve Math Expressions** - Calculate complex mathematical expressions\n"
                    "📈 **Analyze Functions** - Get detailed function analysis with graphs\n"
                    "⏰ **Set Custom Alarms** - Create reminders with streak tracking\n"
                    "🤖 **AI Chat** - Natural conversation with intelligent assistance\n\n"
                    "Choose an option from the menu below to get started!"
                )
            else:
                welcome_message = "❌ Error creating your profile. Please try again."
        else:
            welcome_message = (
                f"👋 Welcome back, {user.first_name}!\n\n"
                "What would you like to do today?"
            )
        
        # Update last activity
        db_manager.update_last_activity(user_id)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=self.reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = update.effective_user.id
        text = update.message.text
        
        # Update last activity
        db_manager.update_last_activity(user_id)
        
        if text == '🧮 Solve Math':
            await self.prompt_math_expression(update, context)
        elif text == '📈 Solve Function':
            await self.prompt_function_analysis(update, context)
        elif text == '⏰ Set Alarm':
            await self.prompt_set_alarm(update, context)
        elif text == '📊 My Stats':
            await self.show_user_stats(update, context)
        elif text == '📋 List Alarms':
            await self.list_user_alarms(update, context)
        elif text == '🤖 AI Chat':
            await self.prompt_ai_chat(update, context)
        else:
            # Check if it's a function first (higher priority than math expressions)
            if self.is_function_expression(text):
                await self.analyze_function(update, context, text)
            elif self.is_alarm_time(text):
                await self.add_alarm(update, context, text)
            elif self.is_math_expression(text):
                await self.solve_math_expression(update, context, text)
            else:
                # Handle with AI assistant for natural conversation
                await self.handle_ai_conversation(update, context, text)

    async def handle_ai_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Handle conversation with AI assistant"""
        user_id = update.effective_user.id

        try:
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

            # Get conversation history
            conversation_history = await ai_assistant.get_conversation_history(user_id)

            # Get AI response
            ai_response = await ai_assistant.get_ai_response(text, user_id, conversation_history)

            # Send response
            await update.message.reply_text(
                ai_response,
                parse_mode='Markdown',
                reply_markup=self.reply_markup
            )

        except Exception as e:
            print(f"Error in AI conversation: {e}")
            # Fallback response
            fallback_response = ai_assistant.get_fallback_response(text)
            await update.message.reply_text(
                fallback_response,
                parse_mode='Markdown',
                reply_markup=self.reply_markup
            )

    async def prompt_ai_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Prompt user to start AI conversation"""
        user = update.effective_user

        welcome_message = (
            f"🤖 **AI Chat Mode Activated!**\n\n"
            f"Hello {user.first_name}! I'm your intelligent assistant created by Choeng Rayu.\n\n"
            "💬 **You can now chat with me naturally!** Ask me anything:\n\n"
            "• ❓ General questions and conversations\n"
            "• 🧮 Math help and explanations\n"
            "• 📚 Learning assistance\n"
            "• 💡 Problem-solving guidance\n"
            "• 🎯 Productivity tips\n"
            "• 🔧 Bot feature explanations\n\n"
            "Just type your message and I'll respond! I remember our conversation context.\n\n"
            "**Example questions:**\n"
            "• \"How do derivatives work?\"\n"
            "• \"What's the best way to study math?\"\n"
            "• \"Tell me about your creator\"\n"
            "• \"Help me understand functions\""
        )

        await update.message.reply_text(
            welcome_message,
            parse_mode='Markdown',
            reply_markup=self.reply_markup
        )

    def is_math_expression(self, text: str) -> bool:
        """Check if text looks like a math expression"""
        math_patterns = [
            r'[\+\-\*/\^]',  # Basic operators
            r'(sin|cos|tan|log|ln|sqrt|exp|abs)',  # Functions
            r'\d+\.\d+',  # Decimals
            r'\(\d+\)',  # Numbers in parentheses
        ]
        return any(re.search(pattern, text.lower()) for pattern in math_patterns)
    
    def is_function_expression(self, text: str) -> bool:
        """Check if text looks like a function definition"""
        # Strong function indicators (explicit function notation)
        strong_function_patterns = [
            r'f\(x\)\s*=',  # f(x) = ...
            r'y\s*=',       # y = ...
            r'g\(x\)\s*=',  # g(x) = ...
            r'h\(x\)\s*=',  # h(x) = ...
        ]

        # Check for explicit function notation first
        if any(re.search(pattern, text.lower()) for pattern in strong_function_patterns):
            return True

        # Check for polynomial-like expressions with x
        # These are likely functions if they contain x with powers or operations
        if 'x' in text.lower():
            polynomial_patterns = [
                r'x\^?\d+',     # x^2, x2, x^3, etc.
                r'x\s*[\+\-]',  # x + ..., x - ...
                r'[\+\-]\s*x',  # ... + x, ... - x
                r'\d+\s*\*?\s*x',  # 2x, 2*x, etc.
                r'x\s*\*\s*x',  # x*x
            ]

            # Check for trigonometric functions with x
            trig_with_x_patterns = [
                r'sin\s*\(\s*x',    # sin(x)
                r'cos\s*\(\s*x',    # cos(x)
                r'tan\s*\(\s*x',    # tan(x)
                r'log\s*\(\s*x',    # log(x)
                r'ln\s*\(\s*x',     # ln(x)
                r'sqrt\s*\(\s*x',   # sqrt(x)
                r'exp\s*\(\s*x',    # exp(x)
            ]

            # If it contains x and polynomial patterns, it's likely a function
            if any(re.search(pattern, text.lower()) for pattern in polynomial_patterns):
                # Additional check: if it's just a number, it's not a function
                if not re.match(r'^\s*\d+\.?\d*\s*$', text):
                    return True

            # If it contains trigonometric functions with x, it's a function
            if any(re.search(pattern, text.lower()) for pattern in trig_with_x_patterns):
                return True

        return False
    
    def is_alarm_time(self, text: str) -> bool:
        """Check if text looks like a time format"""
        time_pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
        return bool(re.match(time_pattern, text.strip()))
    
    async def prompt_math_expression(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Prompt user to enter a math expression"""
        await update.message.reply_text(
            "🧮 **Math Expression Solver**\n\n"
            "Send me a mathematical expression to solve!\n\n"
            "**Examples:**\n"
            "• `2^3 + log(100) + sin(pi/2)`\n"
            "• `sqrt(16) * cos(0) + 5!`\n"
            "• `exp(2) - ln(10) + abs(-5)`\n\n"
            "I support:\n"
            "✅ Basic operations (+, -, *, /, ^)\n"
            "✅ Trigonometric functions (sin, cos, tan)\n"
            "✅ Logarithms (log, ln, log10)\n"
            "✅ Exponentials and roots (exp, sqrt)\n"
            "✅ Constants (pi, e)\n"
            "✅ Factorials (!)",
            parse_mode='Markdown'
        )
    
    async def solve_math_expression(self, update: Update, context: ContextTypes.DEFAULT_TYPE, expression: str):
        """Solve a mathematical expression"""
        user_id = update.effective_user.id
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Solve the expression
        success, result, steps = math_solver.solve_expression(expression)
        
        if success:
            # Generate PDF
            pdf_filename = pdf_generator.generate_math_pdf(
                expression=expression,
                result=result,
                steps=steps,
                user_id=user_id
            )
            
            if pdf_filename and os.path.exists(pdf_filename):
                # Send PDF
                with open(pdf_filename, 'rb') as pdf_file:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=pdf_file,
                        filename=f"math_solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        caption=f"📊 **Solution for:** `{expression}`\n**Result:** `{result}`",
                        parse_mode='Markdown'
                    )
                
                # Clean up PDF file
                pdf_generator.cleanup_file(pdf_filename)
            else:
                # Fallback to text message
                await update.message.reply_text(
                    f"🧮 **Math Solution**\n\n"
                    f"**Expression:** `{expression}`\n"
                    f"**Result:** `{result}`\n\n"
                    f"**Steps:**\n```\n{steps or 'Direct calculation'}\n```",
                    parse_mode='Markdown'
                )
        else:
            await update.message.reply_text(
                f"❌ **Error solving expression:**\n`{expression}`\n\n"
                f"**Error:** {result}\n\n"
                "Please check your expression and try again.",
                parse_mode='Markdown'
            )
    
    async def prompt_function_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Prompt user to enter a function for analysis"""
        await update.message.reply_text(
            "📈 **Function Analyzer**\n\n"
            "Send me a function to analyze!\n\n"
            "**Examples:**\n"
            "• `f(x) = x^2 + 2x + 1`\n"
            "• `y = sin(x) + cos(x)`\n"
            "• `f(x) = ln(x) + x^3`\n"
            "• `y = 1/x + x^2`\n\n"
            "I'll provide:\n"
            "✅ Domain and range analysis\n"
            "✅ First and second derivatives\n"
            "✅ Critical points and extrema\n"
            "✅ Limits at infinity\n"
            "✅ Sign and variation tables\n"
            "✅ Function graph\n"
            "✅ Intercepts and asymptotes",
            parse_mode='Markdown'
        )
    
    async def analyze_function(self, update: Update, context: ContextTypes.DEFAULT_TYPE, function_str: str):
        """Analyze a mathematical function"""
        user_id = update.effective_user.id
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Analyze the function
            analysis = function_analyzer.analyze_function(function_str)
            
            if 'error' in analysis:
                await update.message.reply_text(
                    f"❌ **Error analyzing function:**\n`{function_str}`\n\n"
                    f"**Error:** {analysis['error']}\n\n"
                    "Please check your function syntax and try again.",
                    parse_mode='Markdown'
                )
                return
            
            # Generate graph
            graph_base64 = function_analyzer.plot_function(function_str)
            
            # Generate PDF
            pdf_filename = pdf_generator.generate_function_pdf(
                analysis=analysis,
                graph_base64=graph_base64,
                user_id=user_id
            )
            
            if pdf_filename and os.path.exists(pdf_filename):
                # Send PDF
                with open(pdf_filename, 'rb') as pdf_file:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=pdf_file,
                        filename=f"function_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        caption=f"📈 **Complete analysis for:** `{function_str}`",
                        parse_mode='Markdown'
                    )
                
                # Clean up PDF file
                pdf_generator.cleanup_file(pdf_filename)
            else:
                # Fallback to text message
                summary = (
                    f"📈 **Function Analysis**\n\n"
                    f"**Function:** `{analysis.get('function', function_str)}`\n"
                    f"**Domain:** {analysis.get('domain', 'N/A')}\n"
                    f"**Derivative:** {analysis.get('derivative', 'N/A')}\n\n"
                    "PDF generation failed, but analysis completed successfully."
                )
                await update.message.reply_text(summary, parse_mode='Markdown')
                
        except Exception as e:
            await update.message.reply_text(
                f"❌ **Unexpected error:**\n{str(e)}\n\n"
                "Please try again or contact support.",
                parse_mode='Markdown'
            )
    
    async def prompt_set_alarm(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Prompt user to set an alarm"""
        user_id = update.effective_user.id
        user_alarms = db_manager.get_user_alarms(user_id)
        
        if len(user_alarms) >= Config.MAX_ALARMS_PER_USER:
            await update.message.reply_text(
                f"⚠️ **Alarm Limit Reached**\n\n"
                f"You already have {len(user_alarms)} alarms (maximum: {Config.MAX_ALARMS_PER_USER}).\n"
                "Please remove some alarms before adding new ones.",
                parse_mode='Markdown'
            )
            return
        
        await update.message.reply_text(
            "⏰ **Set New Alarm**\n\n"
            "Send me the time for your alarm in HH:MM format.\n\n"
            "**Examples:**\n"
            "• `08:30` (8:30 AM)\n"
            "• `14:15` (2:15 PM)\n"
            "• `22:00` (10:00 PM)\n\n"
            f"**Timezone:** {Config.TIMEZONE}\n"
            f"**Current alarms:** {len(user_alarms)}/{Config.MAX_ALARMS_PER_USER}",
            parse_mode='Markdown'
        )


    async def add_alarm(self, update: Update, context: ContextTypes.DEFAULT_TYPE, alarm_time: str):
        """Add a new alarm"""
        user_id = update.effective_user.id

        # Validate time format
        if not self.is_alarm_time(alarm_time):
            await update.message.reply_text(
                "❌ **Invalid time format!**\n\n"
                "Please use HH:MM format (e.g., 08:30, 14:15)",
                parse_mode='Markdown'
            )
            return

        # Add alarm to database
        success = db_manager.add_alarm(user_id, alarm_time)

        if success:
            # Schedule the alarm
            if alarm_manager:
                alarm_manager.schedule_alarm(user_id, alarm_time)

            await update.message.reply_text(
                f"✅ **Alarm Set Successfully!**\n\n"
                f"⏰ **Time:** {alarm_time}\n"
                f"🌍 **Timezone:** {Config.TIMEZONE}\n\n"
                "I'll send you a notification at this time every day with streak tracking!",
                parse_mode='Markdown',
                reply_markup=self.reply_markup
            )
        else:
            user_alarms = db_manager.get_user_alarms(user_id)
            if len(user_alarms) >= Config.MAX_ALARMS_PER_USER:
                message = f"❌ **Cannot add alarm!**\n\nYou've reached the maximum limit of {Config.MAX_ALARMS_PER_USER} alarms."
            else:
                # Check if alarm already exists
                existing_times = [alarm['time'] for alarm in user_alarms]
                if alarm_time in existing_times:
                    message = f"❌ **Alarm already exists!**\n\nYou already have an alarm set for {alarm_time}."
                else:
                    message = "❌ **Error adding alarm!**\n\nPlease try again."

            await update.message.reply_text(message, parse_mode='Markdown')

    async def list_user_alarms(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all user alarms with delete buttons"""
        user_id = update.effective_user.id
        user_alarms = db_manager.get_user_alarms(user_id)

        if not user_alarms:
            await update.message.reply_text(
                "📋 **Your Alarms**\n\n"
                "You don't have any alarms set yet.\n"
                "Use '⏰ Set Alarm' to create your first alarm!",
                parse_mode='Markdown',
                reply_markup=self.reply_markup
            )
            return

        # Create inline keyboard for alarm deletion
        keyboard = []
        alarm_list = "📋 **Your Alarms**\n\n"

        for i, alarm in enumerate(user_alarms):
            alarm_time = alarm['time']
            created_date = alarm.get('created_at', 'Unknown')
            if hasattr(created_date, 'strftime'):
                created_str = created_date.strftime('%Y-%m-%d')
            else:
                created_str = 'Unknown'

            alarm_list += f"⏰ **{alarm_time}** (created: {created_str})\n"

            # Add delete button
            keyboard.append([
                InlineKeyboardButton(
                    f"🗑️ Delete {alarm_time}",
                    callback_data=f"delete_alarm_{i}"
                )
            ])

        alarm_list += f"\n**Total:** {len(user_alarms)}/{Config.MAX_ALARMS_PER_USER} alarms"

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            alarm_list,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    async def show_user_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user statistics"""
        user_id = update.effective_user.id
        user = db_manager.get_user(user_id)

        if not user:
            await update.message.reply_text(
                "❌ **Error loading your stats.**\n"
                "Please try the /start command first.",
                parse_mode='Markdown'
            )
            return

        user_alarms = user.get('alarms', [])
        streak = user.get('streak', 0)
        last_activity = user.get('last_activity')
        created_at = user.get('created_at')

        # Format dates
        if hasattr(last_activity, 'strftime'):
            last_activity_str = last_activity.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_activity_str = 'Unknown'

        if hasattr(created_at, 'strftime'):
            member_since = created_at.strftime('%Y-%m-%d')
        else:
            member_since = 'Unknown'

        # Create streak emoji
        if streak == 0:
            streak_emoji = "💤"
        elif streak < 7:
            streak_emoji = "🔥"
        elif streak < 30:
            streak_emoji = "🚀"
        else:
            streak_emoji = "👑"

        stats_message = (
            f"📊 **Your Statistics**\n\n"
            f"👤 **User:** {user.get('first_name', 'Unknown')}\n"
            f"📅 **Member since:** {member_since}\n"
            f"⏰ **Active alarms:** {len(user_alarms)}/{Config.MAX_ALARMS_PER_USER}\n"
            f"🔥 **Current streak:** {streak} {streak_emoji}\n"
            f"🕐 **Last activity:** {last_activity_str}\n\n"
        )

        # Add motivational message based on streak
        if streak == 0:
            stats_message += "💪 **Ready to start your streak? Set an alarm and begin your journey!**"
        elif streak == 1:
            stats_message += "🌟 **Great start! Keep it up tomorrow!**"
        elif streak < 7:
            stats_message += f"🔥 **{streak} days strong! You're building a great habit!**"
        elif streak < 30:
            stats_message += f"🚀 **{streak} days! You're on fire! Keep pushing!**"
        else:
            stats_message += f"👑 **{streak} days! You're a champion! Absolutely incredible!**"

        await update.message.reply_text(
            stats_message,
            parse_mode='Markdown',
            reply_markup=self.reply_markup
        )

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()

        callback_data = query.data

        if callback_data.startswith('delete_alarm_'):
            await self.handle_delete_alarm(update, context, callback_data)
        elif callback_data.startswith('alarm_done_') or callback_data.startswith('alarm_skip_'):
            await self.handle_alarm_response(update, context, callback_data)

    async def handle_delete_alarm(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
        """Handle alarm deletion"""
        user_id = update.effective_user.id

        try:
            alarm_index = int(callback_data.split('_')[-1])
            user_alarms = db_manager.get_user_alarms(user_id)

            if 0 <= alarm_index < len(user_alarms):
                alarm_time = user_alarms[alarm_index]['time']

                # Remove from database
                success = db_manager.remove_alarm(user_id, alarm_index)

                if success:
                    # Remove from scheduler
                    if alarm_manager:
                        alarm_manager.remove_scheduled_alarm(user_id, alarm_time)

                    await update.callback_query.edit_message_text(
                        f"✅ **Alarm Deleted**\n\n"
                        f"Alarm for {alarm_time} has been removed successfully.",
                        parse_mode='Markdown'
                    )
                else:
                    await update.callback_query.edit_message_text(
                        "❌ **Error deleting alarm.**\n"
                        "Please try again.",
                        parse_mode='Markdown'
                    )
            else:
                await update.callback_query.edit_message_text(
                    "❌ **Invalid alarm selection.**",
                    parse_mode='Markdown'
                )

        except Exception as e:
            await update.callback_query.edit_message_text(
                f"❌ **Error:** {str(e)}",
                parse_mode='Markdown'
            )

    async def handle_alarm_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
        """Handle alarm notification response"""
        if alarm_manager:
            response = await alarm_manager.handle_alarm_response(
                callback_data,
                update.callback_query.message.message_id
            )

            await update.callback_query.edit_message_text(
                response,
                parse_mode='Markdown'
            )
        else:
            await update.callback_query.edit_message_text(
                "❌ Alarm system not available.",
                parse_mode='Markdown'
            )

# Global bot handlers instance
bot_handlers = BotHandlers()
