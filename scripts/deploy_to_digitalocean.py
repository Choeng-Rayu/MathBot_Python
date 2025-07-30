#!/usr/bin/env python3
"""
Deployment script for DigitalOcean with automatic webhook setup
"""

import os
import sys
import subprocess
import time
import requests

def run_command(command, description):
    """Run a shell command and return the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True, result.stdout
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False, str(e)

def check_app_health(app_url, max_retries=10, delay=30):
    """Check if the app is healthy"""
    health_url = f"{app_url}/health"
    
    for attempt in range(max_retries):
        try:
            print(f"🔍 Checking app health (attempt {attempt + 1}/{max_retries})...")
            response = requests.get(health_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print("✅ App is healthy and running!")
                    return True
                else:
                    print(f"⚠️ App responded but status is: {data.get('status', 'unknown')}")
            else:
                print(f"⚠️ App responded with status code: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Health check failed: {e}")
        
        if attempt < max_retries - 1:
            print(f"⏳ Waiting {delay} seconds before next attempt...")
            time.sleep(delay)
    
    return False

def set_webhook(app_url):
    """Set the webhook for the Telegram bot"""
    webhook_url = f"{app_url}/set_webhook"
    
    try:
        print(f"🔗 Setting webhook...")
        response = requests.get(webhook_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook set successfully: {data.get('message', 'Success')}")
            return True
        else:
            print(f"❌ Failed to set webhook: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error setting webhook: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 DigitalOcean Deployment Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Step 1: Check git status
    print("\n📋 Step 1: Checking Git Repository")
    success, output = run_command("git status --porcelain", "Checking for uncommitted changes")
    
    if output.strip():
        print("⚠️ You have uncommitted changes:")
        print(output)
        
        commit = input("\n❓ Do you want to commit these changes? (y/n): ").lower().strip()
        if commit == 'y':
            commit_msg = input("📝 Enter commit message: ").strip()
            if not commit_msg:
                commit_msg = "Deploy to DigitalOcean with fixes"
            
            run_command("git add .", "Adding files to git")
            run_command(f'git commit -m "{commit_msg}"', "Committing changes")
        else:
            print("⚠️ Proceeding with uncommitted changes...")
    
    # Step 2: Push to GitHub
    print("\n📋 Step 2: Pushing to GitHub")
    success, output = run_command("git push origin main", "Pushing to GitHub")
    
    if not success:
        print("❌ Failed to push to GitHub. Please check your git configuration.")
        sys.exit(1)
    
    # Step 3: Wait for user to deploy on DigitalOcean
    print("\n📋 Step 3: DigitalOcean Deployment")
    print("🔗 Please complete these steps in DigitalOcean:")
    print("   1. Go to https://cloud.digitalocean.com/apps")
    print("   2. Create a new app or redeploy existing app")
    print("   3. Connect your GitHub repository")
    print("   4. Wait for deployment to complete")
    
    app_url = input("\n🌐 Enter your DigitalOcean app URL (e.g., https://mathbot-xxxxx.ondigitalocean.app): ").strip()
    
    if not app_url:
        print("❌ App URL is required")
        sys.exit(1)
    
    if not app_url.startswith("http"):
        app_url = f"https://{app_url}"
    
    # Step 4: Check app health
    print(f"\n📋 Step 4: Checking App Health")
    if not check_app_health(app_url):
        print("❌ App health check failed. Please check the deployment logs in DigitalOcean.")
        sys.exit(1)
    
    # Step 5: Set webhook
    print(f"\n📋 Step 5: Setting Webhook")
    if set_webhook(app_url):
        print("✅ Webhook configured successfully!")
    else:
        print("⚠️ Webhook setup failed. You can try manually:")
        print(f"   curl -X GET '{app_url}/set_webhook'")
    
    # Step 6: Final verification
    print(f"\n📋 Step 6: Final Verification")
    print("🧪 Test your bot:")
    print("   1. Go to https://t.me/rayumathbot")
    print("   2. Send /start command")
    print("   3. Try solving a math problem: 2 + 2 * 3")
    
    print(f"\n🎉 Deployment Complete!")
    print(f"📱 Bot URL: https://t.me/rayumathbot")
    print(f"🌐 App URL: {app_url}")
    print(f"📊 Health Check: {app_url}/health")
    print(f"📈 Stats: {app_url}/stats")

if __name__ == "__main__":
    main()
