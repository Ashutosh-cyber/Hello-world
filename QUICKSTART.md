# 🚀 Quick Start Guide

Get your WhatsApp AI Bot running in minutes!

## ✅ Prerequisites Installed

- ✅ Python 3.13.3
- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ Redis server installed and running

## 🔧 Quick Setup (5 minutes)

### 1. **Configure Environment Variables**

Edit the `.env` file with your actual credentials:

```bash
nano .env
```

**Required credentials:**

```env
# Get from https://console.twilio.com
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_auth_token

# For testing, use Twilio Sandbox
TWILIO_PHONE_NUMBER=whatsapp:+14155238886

# Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Create your Google Form and paste URL here
GOOGLE_FORM_URL=https://forms.gle/your_actual_form_id

# Create your Calendly link
CALENDLY_LINK=https://calendly.com/yourusername/consultation
```

### 2. **Get Google Credentials (Optional for testing)**

For full functionality, you need Google Sheets access:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API and Google Drive API
4. Create a service account
5. Download the JSON key as `google_credentials.json`
6. Place it in the project root

**For now, you can skip this and test without Google Sheets.**

### 3. **Create Your Google Form (Optional)**

1. Go to [Google Forms](https://forms.google.com)
2. Create a new form titled "Investment Profile Assessment"
3. Add these questions:
   - Name (Short answer, Required)
   - WhatsApp phone number (Short answer, Required)  
   - Age (Short answer, Required)
   - Annual income range (Multiple choice, Required)
   - Investment experience (Multiple choice, Required)
   - Risk tolerance (Multiple choice, Required)
4. Copy the form URL and update your `.env` file

## 🏃‍♂️ Run the Bot

### Option 1: Use the Startup Script (Recommended)

```bash
./start.sh
```

### Option 2: Manual Start

```bash
# Activate virtual environment
source whatsapp_bot_env/bin/activate

# Start the bot
python app.py
```

The bot will start at: **http://localhost:5000**

## 🧪 Test Your Setup

### 1. **Health Check**

Visit: http://localhost:5000/health

You should see:
```json
{"status": "healthy", "timestamp": "2024-01-15T10:30:00"}
```

### 2. **Test WhatsApp Integration**

For local testing, you need to expose your localhost to the internet:

```bash
# Install ngrok (if not installed)
# Download from https://ngrok.com/download

# Expose your local server
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and:

1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to Messaging > Try it out > Send a WhatsApp message
3. Set webhook URL to: `https://abc123.ngrok.io/webhook`
4. Join the sandbox by sending the code to +1 415 523 8886
5. Send a test message to the bot

### 3. **Expected Bot Behavior**

```
You: Hi
Bot: 👋 Welcome! I'm here to help you find the perfect investment solution.

To get started, please fill out this quick form (takes 2 minutes):
[Google Form Link]

Once completed, I'll analyze your profile and recommend the best products for you! 📊
```

## 🔧 Background Tasks (Optional)

For automated follow-ups and analytics, start Celery workers:

### Terminal 2:
```bash
source whatsapp_bot_env/bin/activate
celery -A automation_scripts worker --loglevel=info
```

### Terminal 3:
```bash
source whatsapp_bot_env/bin/activate  
celery -A automation_scripts beat --loglevel=info
```

## 📊 Monitor Your Bot

- **Health**: http://localhost:5000/health
- **Logs**: Check terminal output
- **Redis**: `redis-cli monitor`
- **Data**: Check Google Sheets (if configured)

## 🚨 Common Issues & Solutions

### Issue: "Google Sheets setup error"
**Solution**: This is normal if you haven't set up Google credentials yet. The bot will work without it for testing.

### Issue: "Redis connection failed"
**Solution**: 
```bash
redis-server --daemonize yes
redis-cli ping  # Should return PONG
```

### Issue: "Twilio webhook not working"
**Solution**: 
- Make sure ngrok is running
- Use the HTTPS ngrok URL in Twilio webhook settings
- Check ngrok logs for incoming requests

### Issue: "OpenAI API error"
**Solution**: 
- Verify your API key is correct
- Check your OpenAI account has credits
- The bot will work with fallback responses if OpenAI fails

## 🎯 Next Steps

1. **Get Real Credentials**: Replace placeholder values in `.env`
2. **Set up Google Integration**: Add `google_credentials.json`
3. **Create Your Form**: Build your actual Google Form
4. **Deploy**: Use Heroku, Railway, or other cloud platform
5. **Go Live**: Apply for WhatsApp Business API

## 💡 Testing Tips

- Use Twilio Sandbox for free testing
- Test with your own phone number first
- Monitor logs for debugging
- Use ngrok for local webhook testing
- Start simple and add features gradually

## 📚 Full Documentation

- **Complete Setup**: See `setup_instructions.md`
- **API Documentation**: See `README.md`
- **Deployment**: See deployment section in `README.md`

---

**🎉 Your WhatsApp AI Bot is ready to automate customer onboarding!**

Need help? Check the troubleshooting section in `README.md` or review the setup logs.