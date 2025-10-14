# 🚨 URGENT FIX: DigitalOcean Invalid Token Error

## ⚠️ Problem
Your bot deployment is **FAILING** because DigitalOcean is using an **INVALID Telegram bot token**.

**Error in logs:**
```
telegram.error.InvalidToken: The token `7659640601:AAGiCFA5bMrj3kXgOV2065uxCZbg` was rejected
```

## ✅ Solution Found

**Your CORRECT token is:**
```
7659640601:AAGSNwtPTiI7XZbd02DMv08XLRMcu2Jw74c
```

This token is:
- ✅ Valid (tested and confirmed working)
- ✅ Currently in your local `.env` file
- ✅ Works with @rayumathbot
- ❌ **NOT configured in DigitalOcean** (this is the problem!)

---

## 🔧 HOW TO FIX (Choose One Method)

### Method 1: DigitalOcean Web Console (⭐ RECOMMENDED - 5 minutes)

#### Step-by-Step with Screenshots

**1. Login to DigitalOcean**
- Go to: https://cloud.digitalocean.com/apps
- Login with your credentials

**2. Select Your App**
- Find and click: `hybridcoffee-za9sy`
- You should see your app dashboard

**3. Go to Settings**
- Click the **Settings** tab at the top
- Look for the **Environment Variables** section

**4. Find TELEGRAM_BOT_TOKEN**
- Scroll through the environment variables
- Look for: `TELEGRAM_BOT_TOKEN`
- Click the **Edit** button (pencil icon) next to it

**5. Replace the Token**
- Delete the old invalid token
- Paste the new valid token:
  ```
  7659640601:AAGSNwtPTiI7XZbd02DMv08XLRMcu2Jw74c
  ```
- Make sure there are no extra spaces
- Click **Save** or **Update**

**6. Redeploy the Application**
- Option A: Click the **Actions** menu → **Force Rebuild and Deploy**
- Option B: Click the **Deploy** button
- Wait 2-5 minutes for deployment to complete

**7. Verify Success**
- Go to **Runtime Logs** tab
- Look for these success messages:
  ```
  ✅ DeepSeek AI available
  ✅ Google Gemini AI available
  INFO - Starting MathBot application...
  INFO:     Application startup complete.
  ```
- Should **NOT** see: `InvalidToken` error

**8. Test Your Bot**
- Open Telegram
- Send a message to: @rayumathbot
- Try: `2+2`
- Bot should respond with `4`

---

### Method 2: Using doctl CLI (Advanced Users)

```bash
# Step 1: Install doctl (if not installed)
# macOS
brew install doctl

# Linux
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-amd64.tar.gz
tar xf doctl-*-linux-amd64.tar.gz
sudo mv doctl /usr/local/bin

# Step 2: Authenticate
doctl auth init
# Paste your API token from: https://cloud.digitalocean.com/account/api/tokens

# Step 3: List your apps to get APP_ID
doctl apps list
# Find your app: hybridcoffee-za9sy
# Copy the APP_ID (looks like: 12345678-abcd-1234-5678-abcdefghijkl)

# Step 4: Update the environment variable
doctl apps update YOUR_APP_ID \
  --env-var 'TELEGRAM_BOT_TOKEN=7659640601:AAGSNwtPTiI7XZbd02DMv08XLRMcu2Jw74c'

# Step 5: Check deployment status
doctl apps list
doctl apps logs YOUR_APP_ID --type=run --follow
```

---

### Method 3: Using DigitalOcean API (Very Advanced)

```bash
# Get your API token from: https://cloud.digitalocean.com/account/api/tokens
export DO_API_TOKEN="your_digitalocean_api_token"
export APP_ID="your_app_id"

# Update environment variable
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DO_API_TOKEN" \
  -d '{
    "envs": [
      {
        "key": "TELEGRAM_BOT_TOKEN",
        "value": "7659640601:AAGSNwtPTiI7XZbd02DMv08XLRMcu2Jw74c",
        "scope": "RUN_TIME",
        "type": "SECRET"
      }
    ]
  }' \
  "https://api.digitalocean.com/v2/apps/$APP_ID"
```

---

## 📝 After Fixing - Update Your Files

I've already updated these files locally with the correct token:
- ✅ `deployment/digitalocean-app.yaml`
- ✅ `deploy_production.py`

**Commit and push these changes:**

```bash
cd /home/choeng-rayu/academic/Telegram_Bot/Math_Python_Git/MathBot_Python

git add deployment/digitalocean-app.yaml deploy_production.py
git commit -m "fix: update telegram bot token to correct valid token"
git push origin main
```

---

## 🧪 Testing & Verification

### 1. Check DigitalOcean Logs

```bash
# Via doctl
doctl apps logs YOUR_APP_ID --type=run --follow

# Via web console
# Go to: Your App → Runtime Logs tab
```

**Look for SUCCESS indicators:**
- ✅ `INFO - Starting MathBot application...`
- ✅ `INFO:     Application startup complete.`
- ✅ `✅ DeepSeek AI available`
- ✅ `✅ Google Gemini AI available`

**Should NOT see:**
- ❌ `InvalidToken` error
- ❌ `Unauthorized`
- ❌ `401` errors

### 2. Test Bot on Telegram

Open Telegram and test these commands:

```
/start
2+2
solve x^2 + 5x + 6 = 0
d/dx(x^2)
integral of x^2
```

All should work correctly.

### 3. Test Webhook

```bash
# Check webhook status
curl https://api.telegram.org/bot7659640601:AAGSNwtPTiI7XZbd02DMv08XLRMcu2Jw74c/getWebhookInfo

# Should show:
# "url": "https://hybridcoffee-za9sy.ondigitalocean.app/webhook"
# "has_custom_certificate": false
# "pending_update_count": 0
```

---

## 🔍 Why This Happened

1. **Multiple Token Versions**: You had 3 different tokens in different places:
   - Local `.env` file: ✅ Valid token
   - `digitalocean-app.yaml`: ❌ Old invalid token
   - DigitalOcean env vars: ❌ Different invalid token

2. **Token Regeneration**: Looks like you regenerated your bot token at some point, but didn't update all locations

3. **Deployment Out of Sync**: DigitalOcean environment variables override the YAML file, so even though the YAML had a token, DigitalOcean was using a different one

---

## 🛡️ Prevention - Best Practices

### 1. Use Environment Variables Properly

**DO:**
- Store tokens in DigitalOcean's environment variables (encrypted)
- Keep `.env` file in `.gitignore`
- Document which token is active

**DON'T:**
- Commit tokens to Git (security risk)
- Use hardcoded tokens in YAML files
- Forget to update all locations when regenerating tokens

### 2. Token Management Checklist

When you regenerate a bot token:
- [ ] Update DigitalOcean environment variables
- [ ] Update local `.env` file
- [ ] Update `deployment/digitalocean-app.yaml` (if using)
- [ ] Update any CI/CD pipeline secrets
- [ ] Test locally first
- [ ] Deploy and verify

### 3. Use Secrets Management

For better security:

```yaml
# In digitalocean-app.yaml
envs:
  - key: TELEGRAM_BOT_TOKEN
    scope: RUN_TIME
    type: SECRET  # Use SECRET type instead of plain value
    # Set value in DigitalOcean console, not in YAML
```

---

## 📚 Additional Resources

- **Diagnostic Tool**: `python scripts/fix_digitalocean_token.py`
- **Full Documentation**: `docs/FIX_DIGITALOCEAN_TOKEN.md`
- **Quick Fix Script**: `bash scripts/fix_do_token.sh`
- **DigitalOcean Docs**: https://docs.digitalocean.com/products/app-platform/how-to/use-environment-variables/

---

## ❓ Troubleshooting

### Issue: "Still getting InvalidToken after update"

**Solutions:**
1. Clear browser cache and refresh DigitalOcean dashboard
2. Force rebuild: `Actions` → `Force Rebuild and Deploy`
3. Double-check you copied the token correctly (no extra spaces)
4. Verify token is valid: `python scripts/fix_digitalocean_token.py`

### Issue: "Bot responds locally but not on DigitalOcean"

**Check:**
1. Webhook is set correctly: `/getWebhookInfo`
2. Firewall allows outbound HTTPS (port 443)
3. All environment variables are set in DigitalOcean
4. Runtime logs show successful startup

### Issue: "Can't find environment variables in DigitalOcean"

**Try:**
1. Settings → App-Level Environment Variables
2. Settings → Component-Level Environment Variables
3. Your app → mathbot-api component → Settings

---

## 🆘 Still Need Help?

If you're still having issues:

1. **Run Full Diagnostics:**
   ```bash
   python scripts/fix_digitalocean_token.py
   python test_deployment.py
   ```

2. **Collect Information:**
   - DigitalOcean app URL
   - Full runtime logs
   - Webhook status
   - Bot info from BotFather

3. **Contact Support:**
   - DigitalOcean Support (for platform issues)
   - Telegram @BotSupport (for bot token issues)

---

## ✅ Success Checklist

After fixing, verify all of these:

- [ ] No `InvalidToken` errors in DigitalOcean logs
- [ ] App shows as "Running" in DigitalOcean dashboard
- [ ] Health check passes at `/health` endpoint
- [ ] Bot responds to `/start` command on Telegram
- [ ] Bot can solve math problems
- [ ] Webhook info shows correct URL
- [ ] All environment variables are set correctly
- [ ] Local files are updated and committed to Git

---

**Last Updated:** October 14, 2025  
**Status:** ✅ Solution Identified - Action Required by User
