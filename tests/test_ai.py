#!/usr/bin/env python3
"""
Test script for AI assistant functionality
"""

import asyncio
import os
from ai_assistant import ai_assistant
from config import Config

async def test_ai_responses():
    """Test AI assistant responses"""
    print("🤖 Testing AI Assistant...")
    print("-" * 40)
    
    # Check if API key is configured
    if not Config.DEEPSEEK_API_KEY:
        print("❌ DEEPSEEK_API_KEY not configured")
        print("Please set your DeepSeek API key in the .env file")
        return
    
    print(f"✅ API Key configured: {Config.DEEPSEEK_API_KEY[:10]}...")
    
    test_messages = [
        "Hello! Who are you?",
        "Tell me about your creator",
        "How do derivatives work?",
        "What can you help me with?",
        "Can you solve 2+2?",
        "What's the best way to study mathematics?",
        "Help me understand functions",
        "Invalid math expression test"
    ]
    
    user_id = 12345  # Test user ID
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Testing message: '{message}'")
        print("-" * 30)
        
        try:
            # Test AI response
            response = await ai_assistant.get_ai_response(message, user_id)
            print(f"✅ AI Response: {response[:100]}...")
            
            # Test fallback response
            fallback = ai_assistant.get_fallback_response(message)
            print(f"🔄 Fallback: {fallback[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)

def test_message_classification():
    """Test message classification"""
    print("🔍 Testing Message Classification...")
    print("-" * 40)
    
    test_cases = [
        ("2+2*3", "math"),
        ("f(x) = x^2", "function"),
        ("08:30", "alarm"),
        ("Hello, how are you?", "conversation"),
        ("What is a derivative?", "conversation"),
        ("sin(pi/2) + cos(0)", "math"),
        ("y = 3x + 1", "function"),
        ("14:45", "alarm"),
    ]
    
    for message, expected_type in test_cases:
        print(f"\nMessage: '{message}'")
        
        is_math = ai_assistant.is_math_expression(message)
        is_function = ai_assistant.is_function_expression(message)
        is_alarm = ai_assistant.is_alarm_time(message)
        is_conversation = ai_assistant.is_ai_conversation(message)
        
        detected_type = "unknown"
        if is_math:
            detected_type = "math"
        elif is_function:
            detected_type = "function"
        elif is_alarm:
            detected_type = "alarm"
        elif is_conversation:
            detected_type = "conversation"
        
        status = "✅" if detected_type == expected_type else "❌"
        print(f"{status} Expected: {expected_type}, Detected: {detected_type}")
    
    print("\n" + "=" * 50)

def test_creator_info():
    """Test creator information"""
    print("👨‍💻 Testing Creator Information...")
    print("-" * 40)
    
    creator_info = ai_assistant.creator_info
    
    print(f"Name: {creator_info['name']}")
    print(f"Email: {creator_info['email']}")
    print(f"Telegram: {creator_info['telegram']}")
    print(f"Website: {creator_info['website']}")
    print(f"Purpose: {creator_info['purpose']}")
    
    # Test system prompt
    print(f"\nSystem prompt length: {len(ai_assistant.system_prompt)} characters")
    print("✅ Creator information properly configured")
    
    print("\n" + "=" * 50)

async def test_conversation_history():
    """Test conversation history functionality"""
    print("💬 Testing Conversation History...")
    print("-" * 40)
    
    user_id = 12345
    
    try:
        # Test storing conversation
        await ai_assistant.store_conversation(
            user_id, 
            "Hello!", 
            "Hi there! How can I help you today?"
        )
        print("✅ Conversation stored successfully")
        
        # Test retrieving conversation history
        history = await ai_assistant.get_conversation_history(user_id, limit=5)
        print(f"✅ Retrieved {len(history)} conversation entries")
        
        for entry in history:
            print(f"  - {entry['role']}: {entry['content'][:50]}...")
            
    except Exception as e:
        print(f"❌ Error testing conversation history: {e}")
    
    print("\n" + "=" * 50)

def test_environment():
    """Test environment configuration"""
    print("🔧 Testing Environment Configuration...")
    print("-" * 40)
    
    try:
        Config.validate()
        print("✅ All required environment variables are set")
        
        print(f"✅ Telegram Bot Token: {Config.TELEGRAM_BOT_TOKEN[:10]}...")
        print(f"✅ Webhook URL: {Config.WEBHOOK_URL}")
        print(f"✅ DeepSeek API Key: {Config.DEEPSEEK_API_KEY[:10]}...")
        print(f"✅ MongoDB URI: {Config.MONGODB_URI[:20]}...")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    
    print("\n" + "=" * 50)

async def main():
    """Run all AI tests"""
    print("🧪 AI Assistant Test Suite")
    print("=" * 50)
    
    # Test environment first
    test_environment()
    
    # Test creator info
    test_creator_info()
    
    # Test message classification
    test_message_classification()
    
    # Test conversation history
    await test_conversation_history()
    
    # Test AI responses (requires API key)
    if Config.DEEPSEEK_API_KEY:
        await test_ai_responses()
    else:
        print("⚠️  Skipping AI response tests - API key not configured")
    
    print("🎉 AI test suite completed!")
    print("Check the output above for any errors.")

if __name__ == "__main__":
    asyncio.run(main())
