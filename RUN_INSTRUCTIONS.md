# 🚀 How to Run the WhatsApp AI Bot

## ✅ Setup Complete!

Your WhatsApp AI Bot is ready to run! Here are your options:

## 🎮 Option 1: Demo Mode (No Credentials Needed)

**Perfect for testing the bot logic without any external services**

```bash
# Activate virtual environment
source whatsapp_bot_env/bin/activate

# Run demo version
python demo_app.py
```

**Access Points:**
- 🏠 **Home**: http://localhost:5000
- 🧪 **Interactive Demo**: http://localhost:5000/demo
- 📊 **Health Check**: http://localhost:5000/health

**Demo Features:**
- ✅ Full conversation flow simulation
- ✅ AI risk assessment logic
- ✅ Product recommendations
- ✅ Meeting scheduling simulation
- ✅ Interactive web interface
- ❌ No real WhatsApp integration
- ❌ No Google Sheets storage
- ❌ No real AI (uses mock responses)

## 🔧 Option 2: Production Mode (With Real Credentials)

**For actual WhatsApp integration with real services**

### Step 1: Configure Credentials

Edit `.env` file:
```bash
nano .env
```

Add your real credentials:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_FORM_URL=https://forms.gle/your_actual_form_id
CALENDLY_LINK=https://calendly.com/yourusername/consultation
```

### Step 2: Add Google Credentials (Optional)

Place your `google_credentials.json` file in the project root.

### Step 3: Run Production Bot

```bash
# Option A: Use startup script
./start.sh

# Option B: Manual start
source whatsapp_bot_env/bin/activate
python app.py
```

## 🌐 Option 3: Easy Startup Script

```bash
# Make executable (first time only)
chmod +x start.sh

# Run the bot
./start.sh
```

This script will:
- ✅ Activate virtual environment
- ✅ Check Redis is running
- ✅ Start the Flask application
- ✅ Show helpful information

## 🧪 Testing Your Bot

### 1. **Local Testing (Demo Mode)**

Visit http://localhost:5000/demo and try:
- Type "Hi" → Bot welcomes you
- Type "done" → Bot provides recommendation  
- Type "yes" → Bot schedules meeting

### 2. **WhatsApp Testing (Production Mode)**

For real WhatsApp testing:

1. **Install ngrok** (expose localhost to internet):
   ```bash
   # Download from https://ngrok.com/download
   # Then run:
   ngrok http 5000
   ```

2. **Configure Twilio Webhook**:
   - Copy ngrok URL (e.g., `https://abc123.ngrok.io`)
   - Go to [Twilio Console](https://console.twilio.com)
   - Set webhook: `https://abc123.ngrok.io/webhook`

3. **Test via WhatsApp**:
   - Send message to +1 415 523 8886 with your sandbox code
   - Bot should respond with welcome message

## 🔄 Background Tasks (Optional)

For automated follow-ups and analytics:

### Terminal 2 - Celery Worker:
```bash
source whatsapp_bot_env/bin/activate
celery -A automation_scripts worker --loglevel=info
```

### Terminal 3 - Celery Beat (Scheduler):
```bash
source whatsapp_bot_env/bin/activate
celery -A automation_scripts beat --loglevel=info
```

## 📊 Monitoring

- **Bot Status**: http://localhost:5000/health
- **Redis Status**: `redis-cli ping`
- **Logs**: Check terminal output
- **Demo Interface**: http://localhost:5000/demo

## 🚨 Troubleshooting

### Issue: "Virtual environment not found"
```bash
python3 -m venv whatsapp_bot_env
source whatsapp_bot_env/bin/activate
pip install -r requirements.txt
```

### Issue: "Redis connection failed"
```bash
redis-server --daemonize yes
redis-cli ping  # Should return PONG
```

### Issue: "Credentials required"
- Use `demo_app.py` for testing without credentials
- Or configure real credentials in `.env` file

### Issue: "Google Sheets error"
- This is normal without `google_credentials.json`
- Bot works without Google integration

## 🎯 Recommended Development Flow

1. **Start with Demo Mode** → Test bot logic
2. **Get Twilio Credentials** → Test WhatsApp integration  
3. **Add OpenAI Key** → Enable AI responses
4. **Set up Google Services** → Enable data storage
5. **Deploy to Cloud** → Go live!

## 📁 File Overview

- `demo_app.py` → Demo version (no credentials needed)
- `app.py` → Production version (requires credentials)
- `start.sh` → Easy startup script
- `test_setup.py` → Verify installation
- `.env` → Configuration file
- `requirements.txt` → Python dependencies

## 🎉 Quick Commands

```bash
# Test installation
python test_setup.py

# Run demo (no setup needed)
python demo_app.py

# Run production (needs credentials)
./start.sh

# Check health
curl http://localhost:5000/health
```

---

**🎊 Congratulations! Your WhatsApp AI Bot is ready to automate customer onboarding!**

Choose your preferred option above and start testing. The demo mode is perfect for understanding the bot's behavior before connecting real services.