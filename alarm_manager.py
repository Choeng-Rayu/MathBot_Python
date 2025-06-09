import asyncio
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from typing import Dict, List
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from database import db_manager
from config import Config

class AlarmManager:
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone(Config.TIMEZONE))
        self.timezone = pytz.timezone(Config.TIMEZONE)
        self.pending_alarms = {}  # Track alarms waiting for response
        
    def start_scheduler(self):
        """Start the alarm scheduler"""
        self.scheduler.start()
        print("Alarm scheduler started")
    
    def stop_scheduler(self):
        """Stop the alarm scheduler"""
        self.scheduler.shutdown()
        print("Alarm scheduler stopped")
    
    def schedule_user_alarms(self, user_id: int):
        """Schedule all alarms for a specific user"""
        user_alarms = db_manager.get_user_alarms(user_id)
        
        for alarm in user_alarms:
            self.schedule_alarm(user_id, alarm['time'])
    
    def schedule_alarm(self, user_id: int, alarm_time: str):
        """Schedule a single alarm"""
        try:
            # Parse time (format: HH:MM)
            hour, minute = map(int, alarm_time.split(':'))
            
            # Create job ID
            job_id = f"alarm_{user_id}_{alarm_time.replace(':', '')}"
            
            # Remove existing job if it exists
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
            
            # Schedule the alarm
            self.scheduler.add_job(
                self.send_alarm_notification,
                CronTrigger(hour=hour, minute=minute, timezone=self.timezone),
                args=[user_id, alarm_time],
                id=job_id,
                replace_existing=True
            )
            
            print(f"Scheduled alarm for user {user_id} at {alarm_time}")
            return True
            
        except Exception as e:
            print(f"Error scheduling alarm: {e}")
            return False
    
    def remove_scheduled_alarm(self, user_id: int, alarm_time: str):
        """Remove a scheduled alarm"""
        try:
            job_id = f"alarm_{user_id}_{alarm_time.replace(':', '')}"
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                print(f"Removed scheduled alarm for user {user_id} at {alarm_time}")
                return True
            return False
        except Exception as e:
            print(f"Error removing scheduled alarm: {e}")
            return False
    
    async def send_alarm_notification(self, user_id: int, alarm_time: str):
        """Send alarm notification to user"""
        try:
            # Get user and find the alarm name
            user = db_manager.get_user(user_id)
            current_streak = user.get('streak', 0) if user else 0

            # Find the alarm name
            alarm_name = f"Alarm {alarm_time}"  # Default name
            if user and user.get('alarms'):
                for alarm in user['alarms']:
                    if alarm['time'] == alarm_time:
                        alarm_name = alarm.get('name', f"Alarm {alarm_time}")
                        break

            # Create inline keyboard for response
            keyboard = [
                [
                    InlineKeyboardButton("✅ I did it!", callback_data=f"alarm_done_{user_id}_{alarm_time}"),
                    InlineKeyboardButton("❌ Skip", callback_data=f"alarm_skip_{user_id}_{alarm_time}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            message = (
                f"⏰ **Alarm Notification!**\n\n"
                f"📝 **{alarm_name}**\n"
                f"⏰ Time: {alarm_time}\n"
                f"🔥 Current streak: {current_streak}\n\n"
                f"Did you complete your task?"
            )
            
            # Send notification
            sent_message = await self.bot.send_message(
                chat_id=user_id,
                text=message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            # Track this alarm for timeout handling
            alarm_key = f"{user_id}_{alarm_time}_{sent_message.message_id}"
            self.pending_alarms[alarm_key] = {
                'user_id': user_id,
                'alarm_time': alarm_time,
                'message_id': sent_message.message_id,
                'timestamp': datetime.now(self.timezone)
            }
            
            # Schedule timeout check (1 hour from now)
            from datetime import timedelta
            timeout_time = datetime.now(self.timezone) + timedelta(seconds=Config.ALARM_RESPONSE_TIMEOUT)

            self.scheduler.add_job(
                self.handle_alarm_timeout,
                'date',
                run_date=timeout_time,
                args=[alarm_key],
                id=f"timeout_{alarm_key}"
            )
            
        except Exception as e:
            print(f"Error sending alarm notification: {e}")
    
    async def handle_alarm_response(self, callback_data: str, message_id: int) -> str:
        """Handle user response to alarm"""
        try:
            parts = callback_data.split('_')
            action = parts[1]  # 'done' or 'skip'
            user_id = int(parts[2])
            alarm_time = parts[3]
            
            # Find and remove pending alarm
            alarm_key = None
            for key, alarm_info in self.pending_alarms.items():
                if (alarm_info['user_id'] == user_id and 
                    alarm_info['alarm_time'] == alarm_time and 
                    alarm_info['message_id'] == message_id):
                    alarm_key = key
                    break
            
            if alarm_key:
                del self.pending_alarms[alarm_key]
                # Remove timeout job
                timeout_job_id = f"timeout_{alarm_key}"
                if self.scheduler.get_job(timeout_job_id):
                    self.scheduler.remove_job(timeout_job_id)
            
            # Update user streak based on response
            if action == 'done':
                db_manager.update_streak(user_id, increment=True)
                user = db_manager.get_user(user_id)
                new_streak = user.get('streak', 0) if user else 0
                
                response = f"🎉 Great job! Your streak is now {new_streak} 🔥"
                
                # Add motivational messages based on streak
                if new_streak == 1:
                    response += "\n🌟 You're starting strong!"
                elif new_streak == 7:
                    response += "\n🏆 One week streak! Amazing!"
                elif new_streak == 30:
                    response += "\n🎊 30 days! You're unstoppable!"
                elif new_streak % 10 == 0:
                    response += f"\n🚀 {new_streak} days! Keep it up!"
                    
            else:  # skip
                response = "⏭️ Alarm skipped. No worries, try again next time!"
            
            # Update last activity
            db_manager.update_last_activity(user_id)
            
            return response
            
        except Exception as e:
            print(f"Error handling alarm response: {e}")
            return "❌ Error processing your response."
    
    async def handle_alarm_timeout(self, alarm_key: str):
        """Handle alarm timeout (no response within time limit)"""
        try:
            if alarm_key in self.pending_alarms:
                alarm_info = self.pending_alarms[alarm_key]
                user_id = alarm_info['user_id']
                
                # Reset streak to 0
                db_manager.update_streak(user_id, increment=False)
                
                # Send timeout message
                await self.bot.send_message(
                    chat_id=user_id,
                    text="⏰ Alarm timeout! Your streak has been reset to 0. Don't give up! 💪",
                    parse_mode='Markdown'
                )
                
                # Remove from pending alarms
                del self.pending_alarms[alarm_key]
                
        except Exception as e:
            print(f"Error handling alarm timeout: {e}")
    
    def schedule_all_user_alarms(self):
        """Schedule alarms for all users with alarms"""
        try:
            users_with_alarms = db_manager.get_all_users_with_alarms()
            
            for user in users_with_alarms:
                user_id = user['user_id']
                for alarm in user.get('alarms', []):
                    self.schedule_alarm(user_id, alarm['time'])
                    
            print(f"Scheduled alarms for {len(users_with_alarms)} users")
            
        except Exception as e:
            print(f"Error scheduling all user alarms: {e}")
    
    def get_scheduled_jobs(self) -> List[Dict]:
        """Get list of all scheduled alarm jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            if job.id.startswith('alarm_'):
                jobs.append({
                    'id': job.id,
                    'next_run': job.next_run_time,
                    'trigger': str(job.trigger)
                })
        return jobs

# Global alarm manager instance (will be initialized in main.py)
alarm_manager = None
