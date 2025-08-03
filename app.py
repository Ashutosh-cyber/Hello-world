from flask import Flask, request, jsonify
import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import re
from datetime import datetime, timedelta
import requests
from urllib.parse import urlencode

app = Flask(__name__)

# Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_FORM_URL = os.getenv('GOOGLE_FORM_URL')
CALENDLY_LINK = os.getenv('CALENDLY_LINK')

# Initialize clients
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai.api_key = OPENAI_API_KEY

# Google Sheets setup
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'google_credentials.json'

class WhatsAppBot:
    def __init__(self):
        self.user_sessions = {}
        self.setup_google_sheets()
    
    def setup_google_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
            self.gc = gspread.authorize(creds)
            
            # Open spreadsheets
            self.user_data_sheet = self.gc.open("Customer Onboarding Data").sheet1
            self.leads_sheet = self.gc.open("Confirmed Leads").sheet1
            
            # Initialize headers if needed
            self.initialize_sheets()
        except Exception as e:
            print(f"Google Sheets setup error: {e}")
            self.gc = None
    
    def initialize_sheets(self):
        """Set up sheet headers if they don't exist"""
        try:
            # User data sheet headers
            user_headers = ['Timestamp', 'Phone', 'Name', 'Age', 'Income', 'Preferences', 
                          'Risk_Appetite', 'Recommended_Product', 'Status']
            if not self.user_data_sheet.row_values(1):
                self.user_data_sheet.insert_row(user_headers, 1)
            
            # Leads sheet headers
            leads_headers = ['Timestamp', 'Phone', 'Name', 'Product_Interest', 'Meeting_Scheduled', 
                           'Chat_History', 'Status']
            if not self.leads_sheet.row_values(1):
                self.leads_sheet.insert_row(leads_headers, 1)
        except Exception as e:
            print(f"Sheet initialization error: {e}")
    
    def get_user_session(self, phone_number):
        """Get or create user session"""
        if phone_number not in self.user_sessions:
            self.user_sessions[phone_number] = {
                'stage': 'initial',
                'data': {},
                'chat_history': [],
                'last_interaction': datetime.now()
            }
        return self.user_sessions[phone_number]
    
    def update_user_status(self, phone_number, status):
        """Update user status in Google Sheets"""
        if not self.gc:
            return
        
        try:
            # Find user row
            phone_col = self.user_data_sheet.col_values(2)  # Phone column
            if phone_number in phone_col:
                row_index = phone_col.index(phone_number) + 1
                self.user_data_sheet.update_cell(row_index, 9, status)  # Status column
        except Exception as e:
            print(f"Status update error: {e}")
    
    def analyze_risk_profile(self, user_data):
        """Analyze user data to determine risk appetite"""
        try:
            age = int(user_data.get('age', 30))
            income = float(user_data.get('income', 50000))
            preferences = user_data.get('preferences', '').lower()
            
            # Rule-based risk assessment
            risk_score = 0
            
            # Age factor (younger = higher risk tolerance)
            if age < 30:
                risk_score += 3
            elif age < 45:
                risk_score += 2
            else:
                risk_score += 1
            
            # Income factor
            if income > 100000:
                risk_score += 3
            elif income > 50000:
                risk_score += 2
            else:
                risk_score += 1
            
            # Preference keywords
            high_risk_keywords = ['aggressive', 'high return', 'growth', 'stocks', 'crypto']
            low_risk_keywords = ['safe', 'conservative', 'stable', 'bonds', 'savings']
            
            for keyword in high_risk_keywords:
                if keyword in preferences:
                    risk_score += 2
                    break
            
            for keyword in low_risk_keywords:
                if keyword in preferences:
                    risk_score -= 1
                    break
            
            # Determine risk category
            if risk_score >= 7:
                return 'high'
            elif risk_score >= 4:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            print(f"Risk analysis error: {e}")
            return 'medium'  # Default to medium risk
    
    def get_product_recommendation(self, risk_appetite):
        """Get product recommendation based on risk appetite"""
        recommendations = {
            'low': {
                'product': 'Conservative Investment Portfolio',
                'description': 'A balanced mix of bonds and stable dividend stocks with 6-8% expected returns',
                'features': ['Low volatility', 'Steady income', 'Capital preservation']
            },
            'medium': {
                'product': 'Balanced Growth Portfolio',
                'description': 'Diversified portfolio with 60% stocks and 40% bonds, targeting 8-12% returns',
                'features': ['Moderate growth', 'Diversified risk', 'Regular rebalancing']
            },
            'high': {
                'product': 'Aggressive Growth Portfolio',
                'description': 'High-growth stocks and emerging markets with 12-18% potential returns',
                'features': ['High growth potential', 'Active management', 'Higher volatility']
            }
        }
        return recommendations.get(risk_appetite, recommendations['medium'])
    
    def generate_ai_response(self, user_message, context=""):
        """Generate AI response using OpenAI"""
        try:
            prompt = f"""
            You are a helpful financial advisor assistant for a WhatsApp bot. 
            Context: {context}
            User message: {user_message}
            
            Provide a brief, friendly response (max 160 characters) that guides the user through the onboarding process.
            Be professional but conversational.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI response error: {e}")
            return "Thank you for your message. Our team will get back to you soon!"

bot = WhatsAppBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '').replace('whatsapp:', '')
    
    # Get user session
    session = bot.get_user_session(from_number)
    session['chat_history'].append(f"User: {incoming_msg}")
    session['last_interaction'] = datetime.now()
    
    # Create response
    resp = MessagingResponse()
    msg = resp.message()
    
    # Handle different conversation stages
    if session['stage'] == 'initial':
        response_text = handle_initial_contact(from_number, incoming_msg, session)
    elif session['stage'] == 'form_sent':
        response_text = handle_form_followup(from_number, incoming_msg, session)
    elif session['stage'] == 'recommendation_sent':
        response_text = handle_recommendation_response(from_number, incoming_msg, session)
    else:
        response_text = bot.generate_ai_response(incoming_msg, f"Stage: {session['stage']}")
    
    msg.body(response_text)
    session['chat_history'].append(f"Bot: {response_text}")
    
    return str(resp)

def handle_initial_contact(phone_number, message, session):
    """Handle initial user contact"""
    bot.update_user_status(phone_number, "Form Sent")
    session['stage'] = 'form_sent'
    
    return f"""👋 Welcome! I'm here to help you find the perfect investment solution.

To get started, please fill out this quick form (takes 2 minutes):
{GOOGLE_FORM_URL}

Once completed, I'll analyze your profile and recommend the best products for you! 📊"""

def handle_form_followup(phone_number, message, session):
    """Handle messages after form is sent"""
    if any(word in message for word in ['completed', 'done', 'filled', 'submitted']):
        return process_form_completion(phone_number, session)
    elif any(word in message for word in ['help', 'problem', 'issue']):
        return "Having trouble with the form? Please try this link again: " + GOOGLE_FORM_URL
    else:
        return "Please complete the form first, then let me know when you're done! 😊"

def handle_recommendation_response(phone_number, message, session):
    """Handle user response to recommendations"""
    if any(word in message for word in ['interested', 'yes', 'call', 'meeting', 'schedule']):
        return schedule_meeting(phone_number, session)
    elif any(word in message for word in ['no', 'not interested', 'maybe later']):
        bot.update_user_status(phone_number, "Not Interested")
        return "No problem! Feel free to reach out anytime if you change your mind. Have a great day! 👍"
    else:
        return "Would you like to schedule a call to discuss this recommendation? Just reply 'yes' or 'schedule meeting'."

def process_form_completion(phone_number, session):
    """Process form completion and generate recommendations"""
    # In a real implementation, you'd fetch data from Google Sheets
    # For now, we'll simulate the process
    
    # Mock user data (in production, fetch from Google Sheets)
    mock_data = {
        'name': 'John Doe',
        'age': '35',
        'income': '75000',
        'preferences': 'balanced growth with some risk'
    }
    
    # Analyze risk profile
    risk_appetite = bot.analyze_risk_profile(mock_data)
    recommendation = bot.get_product_recommendation(risk_appetite)
    
    # Update session
    session['stage'] = 'recommendation_sent'
    session['data'] = mock_data
    session['risk_appetite'] = risk_appetite
    session['recommendation'] = recommendation
    
    # Update status
    bot.update_user_status(phone_number, "Recommended")
    
    # Save recommendation to sheets
    save_user_data(phone_number, mock_data, risk_appetite, recommendation['product'])
    
    return f"""✅ Thank you! Based on your profile, here's my recommendation:

🎯 **{recommendation['product']}**

{recommendation['description']}

Key Features:
{chr(10).join(['• ' + feature for feature in recommendation['features']])}

Interested in learning more? Reply 'YES' to schedule a free consultation call! 📞"""

def schedule_meeting(phone_number, session):
    """Handle meeting scheduling"""
    bot.update_user_status(phone_number, "Meeting Scheduled")
    
    # Save to leads sheet
    save_confirmed_lead(phone_number, session)
    
    return f"""🎉 Great! Let's schedule your consultation.

Please book a convenient time here:
{CALENDLY_LINK}

Our advisor will call you to discuss your {session.get('recommendation', {}).get('product', 'investment options')} in detail.

Looking forward to helping you achieve your financial goals! 💼"""

def save_user_data(phone_number, user_data, risk_appetite, recommended_product):
    """Save user data to Google Sheets"""
    if not bot.gc:
        return
    
    try:
        row_data = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            phone_number,
            user_data.get('name', ''),
            user_data.get('age', ''),
            user_data.get('income', ''),
            user_data.get('preferences', ''),
            risk_appetite,
            recommended_product,
            'Recommended'
        ]
        bot.user_data_sheet.append_row(row_data)
    except Exception as e:
        print(f"Save user data error: {e}")

def save_confirmed_lead(phone_number, session):
    """Save confirmed lead to leads sheet"""
    if not bot.gc:
        return
    
    try:
        chat_history = '\n'.join(session['chat_history'])
        row_data = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            phone_number,
            session['data'].get('name', ''),
            session.get('recommendation', {}).get('product', ''),
            'Pending',
            chat_history,
            'Meeting Scheduled'
        ]
        bot.leads_sheet.append_row(row_data)
    except Exception as e:
        print(f"Save lead error: {e}")

@app.route('/form-webhook', methods=['POST'])
def form_webhook():
    """Handle Google Form submissions via webhook"""
    try:
        data = request.json
        phone_number = data.get('phone_number')
        
        if phone_number:
            session = bot.get_user_session(phone_number)
            session['data'] = data
            
            # Send thank you message
            message_body = "✅ Thank you for completing the form! I'm analyzing your responses and will send recommendations shortly..."
            
            twilio_client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=f'whatsapp:{phone_number}'
            )
            
            # Process and send recommendations
            risk_appetite = bot.analyze_risk_profile(data)
            recommendation = bot.get_product_recommendation(risk_appetite)
            
            recommendation_msg = f"""🎯 Based on your profile, I recommend:

**{recommendation['product']}**
{recommendation['description']}

Interested? Reply 'YES' for a free consultation! 📞"""
            
            twilio_client.messages.create(
                body=recommendation_msg,
                from_=TWILIO_PHONE_NUMBER,
                to=f'whatsapp:{phone_number}'
            )
            
            session['stage'] = 'recommendation_sent'
            bot.update_user_status(phone_number, "Recommended")
        
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Form webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)