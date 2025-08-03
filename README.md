# WhatsApp AI Customer Onboarding Bot

An intelligent WhatsApp bot that automates customer onboarding and provides personalized investment recommendations using free/low-cost tools.

## 🚀 Features

- **WhatsApp Integration**: Automated conversations via Twilio
- **Google Forms**: Seamless data collection
- **AI Risk Assessment**: Smart risk profiling and product recommendations
- **Google Sheets**: Automatic data storage and lead tracking
- **Meeting Scheduling**: Calendly integration for consultations
- **Follow-up Automation**: Smart reminders and abandoned cart recovery
- **Status Tracking**: Complete customer journey monitoring
- **Analytics**: Daily reports and conversion tracking

## 🛠 Tech Stack

- **Backend**: Python Flask
- **Messaging**: Twilio WhatsApp API
- **AI**: OpenAI GPT-3.5-turbo
- **Data Storage**: Google Sheets
- **Forms**: Google Forms
- **Scheduling**: Calendly
- **Background Tasks**: Celery + Redis
- **Automation**: Google Apps Script

## 📋 Prerequisites

Before setting up the bot, you'll need:

1. **Twilio Account** (Free tier available)
2. **OpenAI API Key** (Free tier available)
3. **Google Account** (For Forms, Sheets, Apps Script)
4. **Calendly Account** (Free tier available)
5. **Redis** (For background tasks)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd whatsapp-ai-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Update the `.env` file with your actual credentials:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Google Services
GOOGLE_FORM_URL=https://forms.gle/your_form_id
CALENDLY_LINK=https://calendly.com/your_username/consultation

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Redis (for Celery background tasks)
REDIS_URL=redis://localhost:6379/0
```

### 4. Set up Google Services

#### Google Sheets API:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API
4. Create service account credentials
5. Download the JSON key file as `google_credentials.json`
6. Place it in the project root directory

#### Google Forms:
1. Create a new Google Form using the template in `google_form_handler.py`
2. Copy the form URL and add it to your `.env` file
3. Set up Google Apps Script webhook (see instructions below)

### 5. Set up Google Apps Script

1. Go to [Google Apps Script](https://script.google.com)
2. Create a new project
3. Paste the code from `google_apps_script.js`
4. Update the `WEBHOOK_URL` and `YOUR_FORM_ID_HERE` variables
5. Run `setupFormTrigger()` function once
6. Test with `testWebhook()` function

### 6. Set up Twilio WhatsApp

1. Sign up for [Twilio](https://www.twilio.com)
2. Get your Account SID and Auth Token
3. For testing, use Twilio Sandbox for WhatsApp
4. Set webhook URL: `https://your-domain.com/webhook`

### 7. Start Redis Server

```bash
# On macOS with Homebrew
brew services start redis

# On Ubuntu/Debian
sudo systemctl start redis-server

# Using Docker
docker run -d -p 6379:6379 redis:alpine
```

## 🚀 Running the Application

### 1. Start the Flask App

```bash
python app.py
```

The app will run on `http://localhost:5000`

### 2. Start Celery Worker (for background tasks)

In a new terminal:

```bash
celery -A automation_scripts worker --loglevel=info
```

### 3. Start Celery Beat (for scheduled tasks)

In another terminal:

```bash
celery -A automation_scripts beat --loglevel=info
```

## 📱 Usage Flow

1. **User Contact**: User sends message to WhatsApp business number
2. **Form Link**: Bot responds with Google Form link
3. **Form Submission**: User fills out investment profile form
4. **AI Analysis**: Bot analyzes responses and determines risk profile
5. **Recommendations**: Bot sends personalized product recommendations
6. **Meeting Scheduling**: User can schedule consultation via Calendly
7. **Follow-ups**: Automated reminders for incomplete actions

## 🎯 Bot Conversation Flow

```
User: Hi
Bot: 👋 Welcome! I'm here to help you find the perfect investment solution.

To get started, please fill out this quick form (takes 2 minutes):
[Google Form Link]

Once completed, I'll analyze your profile and recommend the best products for you! 📊

User: Done
Bot: ✅ Thank you! Based on your profile, here's my recommendation:

🎯 **Balanced Growth Portfolio**

Diversified portfolio with 60% stocks and 40% bonds, targeting 8-12% returns

Key Features:
• Moderate growth
• Diversified risk  
• Regular rebalancing

Interested in learning more? Reply 'YES' to schedule a free consultation call! 📞

User: Yes
Bot: 🎉 Great! Let's schedule your consultation.

Please book a convenient time here:
[Calendly Link]

Our advisor will call you to discuss your Balanced Growth Portfolio in detail.

Looking forward to helping you achieve your financial goals! 💼
```

## 🔄 Automation Features

### Follow-up Messages
- **24 hours**: Form reminder if not completed
- **48 hours**: Recommendation follow-up if no response
- **72 hours**: Abandoned cart recovery message

### Status Tracking
- `Form Sent`: Initial contact made
- `Form Submitted`: User completed form
- `Recommended`: AI recommendation sent
- `Meeting Scheduled`: User booked consultation
- `Not Interested`: User declined offer

### Daily Reports
Automated daily analytics including:
- Total contacts
- Form completion rates
- Meeting conversion rates
- Status breakdown

## 🎨 Customization

### Risk Assessment Logic

The bot uses rule-based risk assessment in `app.py`. You can customize the logic by modifying the `analyze_risk_profile()` method:

```python
def analyze_risk_profile(self, user_data):
    # Your custom risk assessment logic here
    age = int(user_data.get('age', 30))
    income = float(user_data.get('income', 50000))
    # ... add your logic
```

### Product Recommendations

Customize product recommendations in the `get_product_recommendation()` method:

```python
recommendations = {
    'low': {
        'product': 'Your Conservative Product',
        'description': 'Your product description',
        'features': ['Feature 1', 'Feature 2']
    },
    # ... add your products
}
```

### Message Templates

Customize bot messages in `automation_scripts.py`:

```python
messages = {
    'form_reminder': f"""Your custom reminder message""",
    'recommendation_followup': f"""Your custom follow-up""",
    # ... customize all messages
}
```

## 📊 Analytics & Monitoring

### Google Sheets Structure

**Customer Onboarding Data Sheet:**
- Timestamp, Phone, Name, Age, Income, Preferences, Risk_Appetite, Recommended_Product, Status

**Confirmed Leads Sheet:**
- Timestamp, Phone, Name, Product_Interest, Meeting_Scheduled, Chat_History, Status

### Health Check Endpoint

Monitor bot health: `GET /health`

### Daily Reports

Automated reports saved to `reports/` directory with:
- Key metrics
- Conversion rates
- Status breakdown

## 🔒 Security & Privacy

- All credentials stored in environment variables
- Google Sheets access via service account
- No sensitive data stored in code
- WhatsApp messages encrypted by Twilio
- Form data validated and sanitized

## 🚀 Deployment

### Heroku Deployment

1. Create Heroku app:
```bash
heroku create your-app-name
```

2. Add Redis addon:
```bash
heroku addons:create heroku-redis:hobby-dev
```

3. Set environment variables:
```bash
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
# ... set all variables
```

4. Deploy:
```bash
git push heroku main
```

5. Scale workers:
```bash
heroku ps:scale web=1 worker=1 beat=1
```

### Alternative Deployments

- **Railway**: Simple deployment with built-in Redis
- **DigitalOcean App Platform**: Easy container deployment  
- **AWS EC2**: Full control with custom setup
- **Google Cloud Run**: Serverless container deployment

## 🛠 Troubleshooting

### Common Issues

1. **Google Sheets Permission Error**
   - Ensure service account has access to sheets
   - Check `google_credentials.json` file

2. **Twilio Webhook Not Working**
   - Verify webhook URL is publicly accessible
   - Check Twilio console for error logs

3. **Celery Tasks Not Running**
   - Ensure Redis is running
   - Check Celery worker logs

4. **Form Webhook Not Triggering**
   - Verify Google Apps Script trigger is set up
   - Check Apps Script execution logs

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Scaling Considerations

For high-volume usage:

1. **Database**: Replace Google Sheets with PostgreSQL/MongoDB
2. **Message Queue**: Use RabbitMQ or AWS SQS instead of Redis
3. **Caching**: Add Redis caching for user sessions
4. **Load Balancing**: Use multiple app instances
5. **Monitoring**: Add APM tools like New Relic or DataDog

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the troubleshooting section
2. Review Google Sheets/Forms setup
3. Verify all environment variables
4. Check Twilio webhook configuration

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Voice message handling
- [ ] Image/document processing
- [ ] CRM integration (HubSpot, Salesforce)
- [ ] Advanced AI models (GPT-4, local LLMs)
- [ ] A/B testing for messages
- [ ] Advanced analytics dashboard
- [ ] WhatsApp Business API (for production)

---

**Built with ❤️ using free/low-cost tools for maximum accessibility**
