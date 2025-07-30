#!/usr/bin/env python3
"""
Test script to verify AI model selection functionality
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.models.database import db_manager
from app.services.ai_assistant import ai_assistant

async def test_ai_model_selection():
    """Test AI model selection functionality"""
    print("🤖 Testing AI Model Selection")
    print("=" * 50)
    
    test_user_id = 12345
    test_message = "What is 2 + 2 * 3?"
    
    # Test different AI model preferences
    ai_models = ["auto", "gemini", "deepseek"]
    
    for ai_model in ai_models:
        print(f"\n🔧 Testing AI Model: {ai_model}")
        print("-" * 30)
        
        # Update user preference
        success = db_manager.update_user_preference(test_user_id, "ai_model", ai_model)
        if success:
            print(f"✅ User preference updated to: {ai_model}")
        else:
            print(f"❌ Failed to update user preference to: {ai_model}")
            continue
        
        # Get AI response
        try:
            response = await ai_assistant.get_ai_response(test_message, test_user_id)
            print(f"📤 Response: {response[:100]}...")
            
            # Check which AI model was used
            if "Gemini AI" in response:
                print("🧠 Used: Google Gemini")
            elif "Deepseek AI" in response:
                print("🔬 Used: DeepSeek AI")
            else:
                print("🤖 Used: Unknown/Fallback")
                
        except Exception as e:
            print(f"❌ Error getting AI response: {e}")
    
    # Test user preferences retrieval
    print(f"\n📊 Final User Preferences:")
    preferences = db_manager.get_user_preferences(test_user_id)
    print(f"   AI Model: {preferences.get('ai_model', 'not set')}")
    print(f"   Language: {preferences.get('language', 'not set')}")
    print(f"   Notifications: {preferences.get('notifications', 'not set')}")

def test_database_preferences():
    """Test database preference functions"""
    print("\n🗄️ Testing Database Preferences")
    print("=" * 50)
    
    test_user_id = 54321
    
    # Test creating user with preferences
    print("👤 Creating test user...")
    success = db_manager.create_user(test_user_id, "testuser", "Test User")
    if success:
        print("✅ User created successfully")
    else:
        print("⚠️ User already exists or creation failed")
    
    # Test getting default preferences
    print("\n📋 Getting default preferences...")
    preferences = db_manager.get_user_preferences(test_user_id)
    print(f"   Default AI Model: {preferences.get('ai_model')}")
    print(f"   Default Language: {preferences.get('language')}")
    print(f"   Default Notifications: {preferences.get('notifications')}")
    
    # Test updating individual preferences
    print("\n🔧 Testing preference updates...")
    test_updates = [
        ("ai_model", "gemini"),
        ("language", "es"),
        ("notifications", False)
    ]
    
    for key, value in test_updates:
        success = db_manager.update_user_preference(test_user_id, key, value)
        if success:
            print(f"✅ Updated {key} to {value}")
        else:
            print(f"❌ Failed to update {key}")
    
    # Verify updates
    print("\n✅ Verifying updates...")
    updated_preferences = db_manager.get_user_preferences(test_user_id)
    for key, expected_value in test_updates:
        actual_value = updated_preferences.get(key)
        if actual_value == expected_value:
            print(f"✅ {key}: {actual_value} (correct)")
        else:
            print(f"❌ {key}: {actual_value} (expected {expected_value})")

async def main():
    """Main test function"""
    print("🧪 MathBot AI Model Selection Test")
    print("=" * 50)
    
    # Test database preferences
    test_database_preferences()
    
    # Test AI model selection
    await test_ai_model_selection()
    
    print("\n🎉 AI Model Selection Testing Complete!")
    print("\n📱 To test in Telegram:")
    print("   1. Go to https://t.me/rayumathbot")
    print("   2. Send /start")
    print("   3. Tap '⚙️ Settings'")
    print("   4. Select different AI models")
    print("   5. Test with '🤖 AI Chat' or math problems")

if __name__ == "__main__":
    asyncio.run(main())
