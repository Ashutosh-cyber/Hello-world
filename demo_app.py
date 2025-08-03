from flask import Flask, request, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)

# Demo mode - works without real credentials
DEMO_MODE = True

class DemoWhatsAppBot:
    def __init__(self):
        self.user_sessions = {}
    
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
    
    def analyze_risk_profile(self, user_data):
        """Demo risk analysis"""
        age = int(user_data.get('age', 30))
        if age < 30:
            return 'high'
        elif age < 50:
            return 'medium'
        else:
            return 'low'
    
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

bot = DemoWhatsAppBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages (demo mode)"""
    if request.is_json:
        data = request.json
        incoming_msg = data.get('Body', '').strip().lower()
        from_number = data.get('From', 'demo_user')
    else:
        incoming_msg = request.values.get('Body', '').strip().lower()
        from_number = request.values.get('From', 'demo_user')
    
    # Get user session
    session = bot.get_user_session(from_number)
    session['chat_history'].append(f"User: {incoming_msg}")
    session['last_interaction'] = datetime.now()
    
    # Handle different conversation stages
    if session['stage'] == 'initial':
        response_text = handle_initial_contact(from_number, incoming_msg, session)
    elif session['stage'] == 'form_sent':
        response_text = handle_form_followup(from_number, incoming_msg, session)
    elif session['stage'] == 'recommendation_sent':
        response_text = handle_recommendation_response(from_number, incoming_msg, session)
    else:
        response_text = "Thank you for your message. Our team will get back to you soon!"
    
    session['chat_history'].append(f"Bot: {response_text}")
    
    # Return response in both formats for compatibility
    if DEMO_MODE:
        return jsonify({
            'response': response_text,
            'session': session,
            'status': 'success'
        })
    else:
        # Twilio TwiML format
        from twilio.twiml.messaging_response import MessagingResponse
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(response_text)
        return str(resp)

def handle_initial_contact(phone_number, message, session):
    """Handle initial user contact"""
    session['stage'] = 'form_sent'
    
    return f"""👋 Welcome! I'm here to help you find the perfect investment solution.

To get started, please fill out this quick form (takes 2 minutes):
https://forms.gle/demo_form_link

Once completed, I'll analyze your profile and recommend the best products for you! 📊

[DEMO MODE: Type 'done' to simulate form completion]"""

def handle_form_followup(phone_number, message, session):
    """Handle messages after form is sent"""
    if any(word in message for word in ['completed', 'done', 'filled', 'submitted']):
        return process_form_completion(phone_number, session)
    elif any(word in message for word in ['help', 'problem', 'issue']):
        return "Having trouble with the form? Please try this link again: https://forms.gle/demo_form_link"
    else:
        return "Please complete the form first, then let me know when you're done! 😊"

def handle_recommendation_response(phone_number, message, session):
    """Handle user response to recommendations"""
    if any(word in message for word in ['interested', 'yes', 'call', 'meeting', 'schedule']):
        return schedule_meeting(phone_number, session)
    elif any(word in message for word in ['no', 'not interested', 'maybe later']):
        return "No problem! Feel free to reach out anytime if you change your mind. Have a great day! 👍"
    else:
        return "Would you like to schedule a call to discuss this recommendation? Just reply 'yes' or 'schedule meeting'."

def process_form_completion(phone_number, session):
    """Process form completion and generate recommendations"""
    # Demo user data
    demo_data = {
        'name': 'Demo User',
        'age': '35',
        'income': '75000',
        'preferences': 'balanced growth with some risk'
    }
    
    # Analyze risk profile
    risk_appetite = bot.analyze_risk_profile(demo_data)
    recommendation = bot.get_product_recommendation(risk_appetite)
    
    # Update session
    session['stage'] = 'recommendation_sent'
    session['data'] = demo_data
    session['risk_appetite'] = risk_appetite
    session['recommendation'] = recommendation
    
    return f"""✅ Thank you! Based on your profile, here's my recommendation:

🎯 **{recommendation['product']}**

{recommendation['description']}

Key Features:
{chr(10).join(['• ' + feature for feature in recommendation['features']])}

Interested in learning more? Reply 'YES' to schedule a free consultation call! 📞"""

def schedule_meeting(phone_number, session):
    """Handle meeting scheduling"""
    return f"""🎉 Great! Let's schedule your consultation.

Please book a convenient time here:
https://calendly.com/demo/consultation

Our advisor will call you to discuss your {session.get('recommendation', {}).get('product', 'investment options')} in detail.

Looking forward to helping you achieve your financial goals! 💼"""

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'mode': 'demo' if DEMO_MODE else 'production',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def home():
    """Home page with demo instructions"""
    return f"""
    <h1>🤖 WhatsApp AI Bot - Demo Mode</h1>
    
    <h2>📱 Test the Bot</h2>
    <p>Send a POST request to <code>/webhook</code> with this JSON:</p>
    <pre>
{{
    "Body": "Hi",
    "From": "+1234567890"
}}
    </pre>
    
    <h2>🔗 Endpoints</h2>
    <ul>
        <li><a href="/health">Health Check</a></li>
        <li><a href="/demo">Interactive Demo</a></li>
    </ul>
    
    <h2>💡 Demo Flow</h2>
    <ol>
        <li>Send "Hi" → Bot responds with form link</li>
        <li>Send "done" → Bot provides recommendation</li>
        <li>Send "yes" → Bot provides meeting link</li>
    </ol>
    
    <p><strong>Status:</strong> Running in {'Demo' if DEMO_MODE else 'Production'} mode</p>
    """

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    """Interactive demo page"""
    if request.method == 'POST':
        message = request.form.get('message', '')
        phone = request.form.get('phone', '+1234567890')
        
        # Simulate webhook call
        response = webhook_internal(message, phone)
        
        return f"""
        <h2>Bot Response:</h2>
        <div style="background:#f0f0f0; padding:10px; border-radius:5px;">
            {response.replace(chr(10), '<br>')}
        </div>
        <br>
        <a href="/demo">← Back to Demo</a>
        """
    
    return """
    <h1>🤖 Interactive WhatsApp Bot Demo</h1>
    
    <form method="POST">
        <label>Your Phone Number:</label><br>
        <input type="text" name="phone" value="+1234567890" style="width:200px; margin:5px;"><br><br>
        
        <label>Your Message:</label><br>
        <input type="text" name="message" placeholder="Type your message..." style="width:300px; margin:5px;"><br><br>
        
        <button type="submit" style="padding:10px 20px; background:#25D366; color:white; border:none; border-radius:5px;">
            Send Message
        </button>
    </form>
    
    <h3>💡 Try these messages:</h3>
    <ul>
        <li><strong>"Hi"</strong> - Start conversation</li>
        <li><strong>"done"</strong> - Simulate form completion</li>
        <li><strong>"yes"</strong> - Show interest in recommendation</li>
        <li><strong>"no"</strong> - Decline recommendation</li>
    </ul>
    """

def webhook_internal(message, phone):
    """Internal webhook function for demo"""
    session = bot.get_user_session(phone)
    session['chat_history'].append(f"User: {message}")
    
    if session['stage'] == 'initial':
        response = handle_initial_contact(phone, message, session)
    elif session['stage'] == 'form_sent':
        response = handle_form_followup(phone, message, session)
    elif session['stage'] == 'recommendation_sent':
        response = handle_recommendation_response(phone, message, session)
    else:
        response = "Thank you for your message!"
    
    session['chat_history'].append(f"Bot: {response}")
    return response

if __name__ == '__main__':
    print("🚀 Starting WhatsApp AI Bot in Demo Mode...")
    print("📱 Bot available at: http://localhost:5000")
    print("🧪 Interactive demo: http://localhost:5000/demo")
    print("📊 Health check: http://localhost:5000/health")
    print("\n💡 This demo works without any external credentials!")
    print("🛑 Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)