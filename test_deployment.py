#!/usr/bin/env python3
"""
Quick test script to verify all components work before deployment
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test environment variables"""
    print("🔍 Testing Environment Variables...")
    
    required_vars = [
        "TELEGRAM_BOT_TOKEN",
        "MONGODB_URI", 
        "DEEPSEEK_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All required environment variables found")
        return True

def test_imports():
    """Test all required imports"""
    print("\n🔍 Testing Imports...")
    
    try:
        from config import Config
        print("✅ Config import successful")
        
        from app.core.app import create_app
        print("✅ App import successful")
        
        from app.handlers.bot_handlers import bot_handlers
        print("✅ Bot handlers import successful")
        
        from app.services.math_solver import math_solver
        print("✅ Math solver import successful")
        
        from app.models.database import db_manager
        print("✅ Database import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration validation"""
    print("\n🔍 Testing Configuration...")
    
    try:
        from config import Config
        Config.validate()
        print("✅ Configuration validation successful")
        print(f"   Environment: {Config.ENVIRONMENT}")
        print(f"   Port: {Config.PORT}")
        print(f"   Host: {Config.HOST}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n🔍 Testing Database Connection...")
    
    try:
        from app.models.database import db_manager
        # Try to ping the database
        db_manager.client.admin.command('ping')
        print("✅ Database connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   This might be normal for local development if using MongoDB Atlas")
        return False

def main():
    """Run all tests"""
    print("🧪 MathBot Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment),
        ("Python Imports", test_imports),
        ("Configuration", test_config),
        ("Database Connection", test_database)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Tests Passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 All tests passed! Ready for deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
