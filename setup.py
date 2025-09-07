#!/usr/bin/env python3
"""
Setup script for MathBot
"""

import os
import sys
import subprocess

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("📝 Creating .env file from template...")
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created")
            print("⚠️  Please edit .env file with your actual credentials")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file already exists")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['temp', 'logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory already exists: {directory}")

def run_tests():
    """Run basic tests"""
    print("🧪 Running basic tests...")
    try:
        subprocess.check_call([sys.executable, "test_math.py"])
        print("✅ Tests completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 MathBot Setup")
    print("=" * 30)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Run tests
    print("\n🧪 Running tests to verify installation...")
    if run_tests():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your credentials")
        print("2. Run: python run.py")
        print("3. Set webhook: visit https://your-domain.com/set_webhook")
    else:
        print("\n⚠️  Setup completed with test failures")
        print("Please check the error messages above")

if __name__ == "__main__":
    main()
