#!/usr/bin/env python3
"""
Installation script for OCR functionality
Installs Google Cloud Vision API dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔧 Installing OCR Dependencies for MathBot")
    print("=" * 50)
    
    # List of packages to install
    packages = [
        "google-cloud-vision==3.4.5"
    ]
    
    success_count = 0
    
    for package in packages:
        print(f"📦 Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
            success_count += 1
        else:
            print(f"❌ Failed to install {package}")
    
    print("\n" + "=" * 50)
    
    if success_count == len(packages):
        print("🎉 All OCR dependencies installed successfully!")
        print("\n📋 Next Steps:")
        print("1. Follow the OCR_SETUP_GUIDE.md to configure Google Cloud Vision API")
        print("2. Set up your Google Cloud credentials")
        print("3. Update your .env file with GOOGLE_CLOUD_CREDENTIALS_PATH")
        print("4. Restart your bot to enable OCR functionality")
        
        # Test the installation
        print("\n🧪 Testing installation...")
        try:
            from google.cloud import vision
            print("✅ Google Cloud Vision library imported successfully")
        except ImportError as e:
            print(f"❌ Import test failed: {e}")
            
    else:
        print(f"⚠️ {len(packages) - success_count} packages failed to install")
        print("Please check your internet connection and try again")
    
    print("\n💡 For detailed setup instructions, see OCR_SETUP_GUIDE.md")

if __name__ == "__main__":
    main()
