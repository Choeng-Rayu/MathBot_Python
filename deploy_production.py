#!/usr/bin/env python3
"""
Production deployment script for DigitalOcean
"""

import os
import sys
import subprocess
import time
import requests

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n📋 Step {step}: {description}")
    print("-" * 40)

def run_command(command, description):
    """Run a shell command"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True, result.stdout
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, str(e)

def check_health(url, max_retries=10, delay=30):
    """Check if the app is healthy"""
    health_url = f"{url}/health"
    
    for attempt in range(max_retries):
        try:
            print(f"🔍 Health check attempt {attempt + 1}/{max_retries}...")
            response = requests.get(health_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print("✅ App is healthy and running!")
                    return True
                else:
                    print(f"⚠️ App status: {data.get('status', 'unknown')}")
            else:
                print(f"⚠️ HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Health check failed: {e}")
        
        if attempt < max_retries - 1:
            print(f"⏳ Waiting {delay} seconds...")
            time.sleep(delay)
    
    return False

def set_webhook(url):
    """Set the webhook"""
    webhook_url = f"{url}/set_webhook"
    
    try:
        print(f"🔗 Setting webhook...")
        response = requests.get(webhook_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook set: {data.get('message', 'Success')}")
            return True
        else:
            print(f"❌ Webhook failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Webhook error: {e}")
        return False

def main():
    """Main deployment function"""
    print_header("MathBot Production Deployment")
    
    app_url = "https://hybridcoffee-za9sy.ondigitalocean.app"
    
    print(f"🌐 App URL: {app_url}")
    print(f"🤖 Bot URL: https://t.me/rayumathbot")
    
    # Step 1: Check git status
    print_step(1, "Preparing Git Repository")
    
    if not os.path.exists(".git"):
        print("❌ Not a git repository. Please run 'git init' first.")
        return False
    
    # Check for uncommitted changes
    success, output = run_command("git status --porcelain", "Checking git status")
    if output.strip():
        print("📝 Uncommitted changes found:")
        print(output)
        
        commit = input("\n❓ Commit changes? (y/n): ").lower().strip()
        if commit == 'y':
            run_command("git add .", "Adding files")
            run_command('git commit -m "Deploy to production with AI model selection"', "Committing")
    
    # Step 2: Push to GitHub
    print_step(2, "Pushing to GitHub")
    success, _ = run_command("git push origin main", "Pushing to GitHub")
    if not success:
        print("❌ Failed to push to GitHub")
        return False
    
    # Step 3: Environment Variables
    print_step(3, "Environment Variables")
    print("📋 Copy these environment variables to DigitalOcean:")
    print("\n" + "="*50)
    
    env_vars = [
        ("ENVIRONMENT", "production"),
        ("HOST", "0.0.0.0"),
        ("PORT", "8000"),
        ("LOG_LEVEL", "INFO"),
        ("TELEGRAM_BOT_TOKEN", "7659640601:AAHvuGO4r1esUjG3HYqkdcKNsUlW2KjghR8"),
        ("WEBHOOK_URL", app_url),
        ("DEEPSEEK_API_KEY", "sk-698124ba5ed24bcea3c8d298b73f2f52"),
        ("GOOGLE_GEMINI_API_KEY", "AIzaSyC2xuhoigUFCPp9g_MkhTrFbOKDlTWK6Ks"),
        ("AI_MODEL", "auto"),
        ("MONGODB_URI", "mongodb+srv://ChoengRayu:C9r6nhxOVLCUkkGd@cluster0.2ott03t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"),
        ("WEBHOOK_SECRET", "mathbot_webhook_secret_2025_production"),
        ("SECRET_KEY", "mathbot_secret_key_2025_production_secure"),
        ("ALLOWED_HOSTS", "*")
    ]
    
    for key, value in env_vars:
        print(f"{key}={value}")
    
    print("="*50)
    
    # Step 4: Wait for deployment
    print_step(4, "Waiting for Deployment")
    input("⏳ Press Enter after you've updated the environment variables and redeployed in DigitalOcean...")
    
    # Step 5: Health check
    print_step(5, "Health Check")
    if not check_health(app_url):
        print("❌ Health check failed")
        return False
    
    # Step 6: Set webhook
    print_step(6, "Setting Webhook")
    if not set_webhook(app_url):
        print("⚠️ Webhook setup failed, but you can set it manually")
    
    # Step 7: Final verification
    print_step(7, "Final Verification")
    
    print("🧪 Test your bot:")
    print(f"   1. Health: {app_url}/health")
    print(f"   2. Stats: {app_url}/stats")
    print("   3. Bot: https://t.me/rayumathbot")
    print("   4. Send /start")
    print("   5. Try ⚙️ Settings to test AI model selection")
    
    print_header("Deployment Complete! 🎉")
    print(f"🌐 App: {app_url}")
    print(f"🤖 Bot: https://t.me/rayumathbot")
    print("📱 Features: Dual AI, Model Selection, Math Solving, Alarms")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
