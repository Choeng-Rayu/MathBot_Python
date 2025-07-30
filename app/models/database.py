import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import pytz

from config import Config

class DatabaseManager:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.users = self.db[Config.USERS_COLLECTION]
        self.timezone = pytz.timezone(Config.TIMEZONE)
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        try:
            self.users.create_index("user_id", unique=True)
        except Exception as e:
            print(f"Index creation warning: {e}")
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data from database"""
        return self.users.find_one({"user_id": user_id})
    
    def create_user(self, user_id: int, username: str = None, first_name: str = None) -> bool:
        """Create a new user in the database"""
        try:
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "alarms": [],
                "streak": 0,
                "last_activity": datetime.now(self.timezone),
                "created_at": datetime.now(self.timezone)
            }
            self.users.insert_one(user_data)
            return True
        except DuplicateKeyError:
            return False
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def update_last_activity(self, user_id: int):
        """Update user's last activity timestamp"""
        self.users.update_one(
            {"user_id": user_id},
            {"$set": {"last_activity": datetime.now(self.timezone)}}
        )
    
    def add_alarm(self, user_id: int, alarm_time: str, alarm_name: str = None) -> bool:
        """Add an alarm for a user"""
        user = self.get_user(user_id)
        if not user:
            return False

        # Check if user already has maximum alarms
        if len(user.get("alarms", [])) >= Config.MAX_ALARMS_PER_USER:
            return False

        # Check if alarm time already exists
        existing_alarms = [alarm["time"] for alarm in user.get("alarms", [])]
        if alarm_time in existing_alarms:
            return False

        # Add the alarm
        alarm_data = {
            "time": alarm_time,
            "name": alarm_name or f"Alarm {alarm_time}",
            "created_at": datetime.now(self.timezone)
        }

        self.users.update_one(
            {"user_id": user_id},
            {"$push": {"alarms": alarm_data}}
        )
        return True
    
    def remove_alarm(self, user_id: int, alarm_index: int) -> bool:
        """Remove an alarm by index"""
        user = self.get_user(user_id)
        if not user or not user.get("alarms"):
            return False
        
        alarms = user["alarms"]
        if alarm_index < 0 or alarm_index >= len(alarms):
            return False
        
        # Remove the alarm at the specified index
        alarms.pop(alarm_index)
        
        self.users.update_one(
            {"user_id": user_id},
            {"$set": {"alarms": alarms}}
        )
        return True
    
    def get_user_alarms(self, user_id: int) -> List[Dict]:
        """Get all alarms for a user"""
        user = self.get_user(user_id)
        return user.get("alarms", []) if user else []
    
    def update_streak(self, user_id: int, increment: bool = True):
        """Update user's streak (increment or reset)"""
        if increment:
            self.users.update_one(
                {"user_id": user_id},
                {"$inc": {"streak": 1}}
            )
        else:
            self.users.update_one(
                {"user_id": user_id},
                {"$set": {"streak": 0}}
            )
    
    def get_all_users_with_alarms(self) -> List[Dict]:
        """Get all users who have alarms set"""
        return list(self.users.find({"alarms": {"$ne": []}}))
    
    def close(self):
        """Close database connection"""
        self.client.close()

# Global database instance
db_manager = DatabaseManager()
