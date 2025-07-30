#!/usr/bin/env python3
"""
Test script to verify both Gemini and DeepSeek AI models work correctly
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.services.ai_assistant import ai_assistant

async def test_ai_models():
    """Test both AI models"""
    print("🤖 Testing AI Models")
    print("=" * 50)
    
    # Test message
    test_message = "Hello! Can you help me solve 2 + 2 * 3?"
    user_id = 12345
    
    print(f"📝 Test Message: {test_message}")
    print(f"👤 User ID: {user_id}")
    
    try:
        # Test the AI response
        print("\n🔄 Getting AI response...")
        response = await ai_assistant.get_ai_response(test_message, user_id)
        
        print(f"\n✅ AI Response:")
        print(f"📤 {response}")
        
        # Test individual APIs
        print("\n" + "=" * 50)
        print("🧪 Testing Individual APIs")
        print("=" * 50)
        
        # Prepare messages for direct API calls
        messages = [
            {"role": "system", "content": "You are a helpful math assistant."},
            {"role": "user", "content": test_message}
        ]
        
        # Test Gemini API
        if ai_assistant.gemini_api_key:
            print("\n🔍 Testing Gemini API...")
            gemini_response = await ai_assistant.call_gemini_api(messages, user_id)
            if gemini_response:
                print(f"✅ Gemini Response: {gemini_response[:100]}...")
            else:
                print("❌ Gemini API failed")
        else:
            print("⚠️ Gemini API key not configured")
        
        # Test DeepSeek API
        if ai_assistant.deepseek_api_key:
            print("\n🔍 Testing DeepSeek API...")
            deepseek_response = await ai_assistant.call_deepseek_api(messages, user_id)
            if deepseek_response:
                print(f"✅ DeepSeek Response: {deepseek_response[:100]}...")
            else:
                print("❌ DeepSeek API failed")
        else:
            print("⚠️ DeepSeek API key not configured")
        
        print("\n🎉 AI Model testing completed!")
        
    except Exception as e:
        print(f"❌ Error testing AI models: {e}")

async def main():
    """Main test function"""
    print("🧪 MathBot AI Models Test")
    print("=" * 50)
    
    # Check configuration
    print("🔍 Checking AI Configuration...")
    print(f"   AI Model: {ai_assistant.ai_model}")
    print(f"   Gemini API: {'✅ Available' if ai_assistant.gemini_api_key else '❌ Not configured'}")
    print(f"   DeepSeek API: {'✅ Available' if ai_assistant.deepseek_api_key else '❌ Not configured'}")
    
    if not ai_assistant.gemini_api_key and not ai_assistant.deepseek_api_key:
        print("❌ No AI APIs configured! Please check your .env file.")
        return
    
    await test_ai_models()

if __name__ == "__main__":
    asyncio.run(main())
