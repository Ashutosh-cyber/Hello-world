# Complete Setup Instructions

This guide will walk you through setting up each component of the WhatsApp AI Bot.

## 🔧 Step-by-Step Setup

### 1. Twilio WhatsApp Setup

#### Free Tier (Sandbox)
1. Sign up at [Twilio](https://www.twilio.com)
2. Go to Twilio Console > Develop > Messaging > Try it out > Send a WhatsApp message
3. Follow the instructions to join the sandbox
4. Note your sandbox number: `whatsapp:+14155238886`
5. Set webhook URL: `https://your-domain.com/webhook`

#### Production (WhatsApp Business API)
1. Apply for WhatsApp Business API access
2. Complete business verification
3. Get approved phone number
4. Set up webhook URL

**Required Environment Variables:**
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
```

### 2. OpenAI API Setup

#### Free Tier
1. Sign up at [OpenAI](https://platform.openai.com)
2. Go to API Keys section
3. Create new API key
4. Note: Free tier includes $5 credit

#### Alternative: GPT4Free (Completely Free)
If you want to avoid OpenAI costs, you can use GPT4Free:

```python
# Install: pip install g4f
import g4f

def generate_ai_response_free(self, user_message, context=""):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{context}\n{user_message}"}],
        )
        return response
    except:
        return "Thank you for your message. Our team will get back to you soon!"
```

**Required Environment Variables:**
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Google Services Setup

#### Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "WhatsApp Bot"
3. Enable APIs:
   - Google Sheets API
   - Google Drive API
   - Google Forms API (optional)

#### Service Account Creation
1. Go to IAM & Admin > Service Accounts
2. Create service account: "whatsapp-bot-service"
3. Download JSON key file
4. Rename to `google_credentials.json`
5. Place in project root

#### Google Sheets Setup
1. Create two Google Sheets:
   - "Customer Onboarding Data"
   - "Confirmed Leads"
2. Share sheets with service account email
3. Grant "Editor" permissions

#### Google Forms Setup
1. Create new Google Form
2. Use questions from `google_form_handler.py`
3. Copy form URL
4. Set up response destination (optional)

**Form Questions Template:**
```
1. What is your full name? (Short answer, Required)
2. What is your WhatsApp phone number? (Short answer, Required)
3. What is your age? (Short answer, Required)
4. What is your annual income range? (Multiple choice, Required)
   - Under $25,000
   - $25,000 - $50,000
   - $50,000 - $75,000
   - $75,000 - $100,000
   - $100,000 - $150,000
   - Over $150,000
5. What is your investment experience? (Multiple choice, Required)
   - Beginner - No prior experience
   - Some experience - Basic knowledge
   - Experienced - Good understanding
   - Expert - Extensive experience
6. What is your investment timeline? (Multiple choice, Required)
   - Less than 1 year
   - 1-3 years
   - 3-5 years
   - 5-10 years
   - More than 10 years
7. How would you describe your risk tolerance? (Multiple choice, Required)
   - Conservative - Prefer stable, low-risk investments
   - Moderate - Balanced approach with some risk
   - Aggressive - Comfortable with high-risk, high-reward investments
8. What are your specific investment goals? (Paragraph, Optional)
9. What is your email address? (Short answer, Optional)
```

**Required Environment Variables:**
```env
GOOGLE_FORM_URL=https://forms.gle/your_form_id_here
```

### 4. Google Apps Script Setup

#### Create Apps Script Project
1. Go to [Google Apps Script](https://script.google.com)
2. Create new project: "WhatsApp Bot Form Handler"
3. Paste code from `google_apps_script.js`
4. Update configuration variables:
   ```javascript
   const WEBHOOK_URL = 'https://your-domain.com/form-webhook';
   // Replace YOUR_FORM_ID_HERE with actual form ID
   ```

#### Set Up Form Trigger
1. Run `setupFormTrigger()` function once
2. Authorize permissions when prompted
3. Test with `testWebhook()` function

#### Alternative: Manual Webhook Setup
If Apps Script doesn't work, use Zapier:
1. Create Zapier account
2. New Zap: Google Forms → Webhooks
3. Connect your form
4. Set webhook URL: `https://your-domain.com/form-webhook`
5. Map form fields to JSON payload

### 5. Calendly Setup

#### Free Account
1. Sign up at [Calendly](https://calendly.com)
2. Create event type: "Investment Consultation"
3. Set duration: 30 minutes
4. Add questions (optional):
   - Phone number
   - Investment interest
   - Preferred contact method
5. Copy scheduling link

#### Alternative: Google Calendar
Use Google Calendar API for direct scheduling:

```python
# Add to requirements.txt: google-calendar-api==2.0.0
from googleapiclient.discovery import build

def create_calendar_event(user_data, time_slot):
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': f'Investment Consultation - {user_data["name"]}',
        'start': {'dateTime': time_slot},
        'end': {'dateTime': time_slot + timedelta(minutes=30)},
        'attendees': [{'email': user_data.get('email', '')}]
    }
    service.events().insert(calendarId='primary', body=event).execute()
```

**Required Environment Variables:**
```env
CALENDLY_LINK=https://calendly.com/your_username/consultation
```

### 6. Redis Setup

#### Local Development
```bash
# macOS with Homebrew
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server

# Windows (use WSL or Docker)
docker run -d -p 6379:6379 redis:alpine
```

#### Production Options
1. **Heroku Redis** (Free tier available)
2. **Redis Cloud** (Free tier: 30MB)
3. **AWS ElastiCache** (Free tier eligible)
4. **DigitalOcean Managed Redis**

**Required Environment Variables:**
```env
REDIS_URL=redis://localhost:6379/0
```

### 7. Deployment Options

#### Option 1: Heroku (Recommended for beginners)

```bash
# Install Heroku CLI
# Create app
heroku create your-whatsapp-bot

# Add Redis addon
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set TWILIO_PHONE_NUMBER=whatsapp:+14155238886
heroku config:set OPENAI_API_KEY=your_openai_key
heroku config:set GOOGLE_FORM_URL=your_form_url
heroku config:set CALENDLY_LINK=your_calendly_link

# Deploy
git add .
git commit -m "Initial deployment"
git push heroku main

# Scale dynos
heroku ps:scale web=1 worker=1 beat=1
```

#### Option 2: Railway

1. Connect GitHub repo to Railway
2. Add Redis database
3. Set environment variables
4. Deploy automatically

#### Option 3: DigitalOcean App Platform

1. Create new app from GitHub
2. Add Redis database component
3. Configure environment variables
4. Deploy

#### Option 4: Self-hosted (VPS)

```bash
# Ubuntu server setup
sudo apt update
sudo apt install python3 python3-pip redis-server nginx

# Install dependencies
pip3 install -r requirements.txt

# Set up systemd services
sudo nano /etc/systemd/system/whatsapp-bot.service
sudo nano /etc/systemd/system/whatsapp-bot-worker.service
sudo nano /etc/systemd/system/whatsapp-bot-beat.service

# Start services
sudo systemctl enable whatsapp-bot whatsapp-bot-worker whatsapp-bot-beat
sudo systemctl start whatsapp-bot whatsapp-bot-worker whatsapp-bot-beat

# Configure Nginx reverse proxy
sudo nano /etc/nginx/sites-available/whatsapp-bot
sudo ln -s /etc/nginx/sites-available/whatsapp-bot /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 🧪 Testing Your Setup

### 1. Test Individual Components

#### Test Google Sheets Connection
```python
python -c "from google_form_handler import GoogleFormHandler; h = GoogleFormHandler(); print('Google Sheets connected successfully' if h.gc else 'Connection failed')"
```

#### Test Twilio Connection
```python
python -c "from twilio.rest import Client; import os; client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN')); print('Twilio connected successfully')"
```

#### Test OpenAI Connection
```python
python -c "import openai; import os; openai.api_key = os.getenv('OPENAI_API_KEY'); print(openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'test'}]))"
```

#### Test Redis Connection
```python
python -c "import redis; import os; r = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0')); r.ping(); print('Redis connected successfully')"
```

### 2. Test Full Workflow

1. Send message to WhatsApp bot
2. Verify form link is received
3. Fill out form
4. Check if recommendation is sent
5. Test meeting scheduling
6. Verify data in Google Sheets

### 3. Test Automation

```python
# Test follow-up automation
python -c "from automation_scripts import send_followup_message; send_followup_message.delay('+1234567890', 'form_reminder', 'Test User')"

# Test daily report
python -c "from automation_scripts import generate_daily_report; generate_daily_report.delay()"
```

## 🔍 Monitoring & Maintenance

### Health Checks
- Bot health: `GET /health`
- Celery monitoring: Use Flower
- Google Sheets API quota
- Twilio message logs

### Logs to Monitor
- Flask application logs
- Celery worker logs
- Celery beat logs
- Google Apps Script execution logs
- Twilio webhook logs

### Regular Maintenance
- Monitor API quotas and usage
- Update dependencies monthly
- Backup Google Sheets data
- Review and optimize message templates
- Analyze conversion rates and optimize

## 🚨 Troubleshooting Common Issues

### Issue: Google Sheets Permission Denied
**Solution:**
1. Check service account email in `google_credentials.json`
2. Ensure sheets are shared with service account
3. Verify API is enabled in Google Cloud Console

### Issue: Twilio Webhook Not Receiving Messages
**Solution:**
1. Verify webhook URL is publicly accessible
2. Check Twilio console for webhook errors
3. Ensure webhook endpoint returns 200 status
4. Use ngrok for local testing: `ngrok http 5000`

### Issue: Celery Tasks Not Running
**Solution:**
1. Ensure Redis is running: `redis-cli ping`
2. Check Celery worker logs
3. Verify task routing configuration
4. Restart Celery workers

### Issue: Form Webhook Not Triggering
**Solution:**
1. Check Google Apps Script execution logs
2. Verify trigger is set up correctly
3. Test webhook manually with `testWebhook()`
4. Ensure webhook URL is correct

### Issue: AI Responses Not Working
**Solution:**
1. Check OpenAI API key and quota
2. Verify API key permissions
3. Monitor rate limits
4. Consider using GPT4Free as fallback

## 💰 Cost Optimization

### Free Tier Limits
- **Twilio**: $15 credit (sandbox unlimited)
- **OpenAI**: $5 credit (~750k tokens)
- **Google APIs**: 100 requests/100 seconds
- **Calendly**: 1 event type, unlimited bookings
- **Heroku**: 550-1000 dyno hours/month

### Cost-Saving Tips
1. Use GPT4Free instead of OpenAI
2. Implement message caching
3. Optimize API calls
4. Use Twilio sandbox for testing
5. Monitor usage regularly

### Scaling Costs
- **100 users/month**: ~$10-20
- **1000 users/month**: ~$50-100
- **10k users/month**: ~$300-500

This covers hardware, API calls, and basic hosting. Actual costs may vary based on usage patterns.

---

**🎉 Congratulations! Your WhatsApp AI Bot is now ready to automate customer onboarding and generate leads!**