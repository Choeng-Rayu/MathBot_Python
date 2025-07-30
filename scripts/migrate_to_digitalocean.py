#!/usr/bin/env python3
"""
Migration script to help transition from Render.com to DigitalOcean
"""

import os
import sys
import shutil
import subprocess

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {description}")
    print(f"{'='*60}")

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def main():
    """Main migration function"""
    print("🚀 MathBot Migration to DigitalOcean")
    print("This script helps you migrate from Render.com to DigitalOcean")
    
    # Step 1: Check current directory
    print_step(1, "Checking project structure")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "Dockerfile",
        "app/core/app.py",
        "config/config.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not check_file_exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure you've run the migration script correctly.")
        return False
    
    print("✅ All required files found!")
    
    # Step 2: Check environment variables
    print_step(2, "Checking environment configuration")
    
    env_file = ".env"
    if check_file_exists(env_file):
        print("✅ .env file found")
        
        # Read and check environment variables
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        required_vars = [
            "TELEGRAM_BOT_TOKEN",
            "MONGODB_URI", 
            "DEEPSEEK_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in env_content:
                missing_vars.append(var)
        
        if missing_vars:
            print("⚠️ Missing environment variables:")
            for var in missing_vars:
                print(f"   - {var}")
        else:
            print("✅ All required environment variables found")
            
        # Check for Render-specific variables
        render_vars = ["RENDER_", "onrender.com"]
        render_found = []
        for var in render_vars:
            if var in env_content:
                render_found.append(var)
        
        if render_found:
            print("⚠️ Found Render-specific configurations:")
            for var in render_found:
                print(f"   - {var}")
            print("   Please update these for DigitalOcean deployment")
    else:
        print("❌ .env file not found")
        print("   Please create a .env file with your configuration")
    
    # Step 3: Check Git status
    print_step(3, "Checking Git repository")
    
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            
            # Check for uncommitted changes
            if "nothing to commit" in result.stdout:
                print("✅ No uncommitted changes")
            else:
                print("⚠️ You have uncommitted changes")
                print("   Consider committing them before deployment")
        else:
            print("❌ Not a git repository")
            print("   Initialize git with: git init")
    except FileNotFoundError:
        print("❌ Git not found")
        print("   Please install Git")
    
    # Step 4: Deployment checklist
    print_step(4, "Deployment Checklist")
    
    checklist = [
        "✅ Project structure refactored",
        "✅ Dockerfile created",
        "✅ DigitalOcean App spec created",
        "✅ GitHub Actions workflow added",
        "⚠️ Update GitHub repository URL in deployment files",
        "⚠️ Set environment variables in DigitalOcean",
        "⚠️ Update WEBHOOK_URL after deployment",
        "⚠️ Test the deployment"
    ]
    
    for item in checklist:
        print(f"   {item}")
    
    # Step 5: Next steps
    print_step(5, "Next Steps")
    
    next_steps = [
        "1. Update GitHub repository URL in deployment/digitalocean-app.yaml",
        "2. Push code to GitHub: git add . && git commit -m 'Migrate to DigitalOcean' && git push",
        "3. Create DigitalOcean App and connect GitHub repository",
        "4. Set environment variables in DigitalOcean dashboard",
        "5. Deploy the application",
        "6. Update WEBHOOK_URL environment variable with your app URL",
        "7. Set webhook: curl https://your-app-url/set_webhook",
        "8. Test the bot functionality"
    ]
    
    for step in next_steps:
        print(f"   {step}")
    
    print(f"\n{'='*60}")
    print("📚 For detailed instructions, see: docs/DIGITALOCEAN_DEPLOYMENT.md")
    print("🆘 Need help? Contact: choengrayu307@gmail.com")
    print(f"{'='*60}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
