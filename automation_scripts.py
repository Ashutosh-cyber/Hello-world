from celery import Celery
from datetime import datetime, timedelta
import os
from twilio.rest import Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

# Initialize Celery
app = Celery('whatsapp_bot')
app.config_from_object('celeryconfig')

# Initialize Twilio
twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

class AutomationManager:
    def __init__(self):
        self.setup_google_sheets()
    
    def setup_google_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('google_credentials.json', scope)
            self.gc = gspread.authorize(creds)
            self.user_data_sheet = self.gc.open("Customer Onboarding Data").sheet1
            self.leads_sheet = self.gc.open("Confirmed Leads").sheet1
        except Exception as e:
            print(f"Google Sheets setup error: {e}")
            self.gc = None

automation_manager = AutomationManager()

@app.task
def send_followup_message(phone_number, message_type, user_name=""):
    """Send automated follow-up messages"""
    try:
        messages = {
            'form_reminder': f"""👋 Hi {user_name}! 

Just a friendly reminder to complete your investment profile form. It only takes 2 minutes and helps us recommend the perfect investment solution for you.

Form link: {os.getenv('GOOGLE_FORM_URL')}

Need help? Just reply to this message! 😊""",
            
            'recommendation_followup': f"""Hi {user_name}! 

I sent you a personalized investment recommendation earlier. Have you had a chance to review it?

If you're interested in learning more, just reply 'YES' and I'll help you schedule a free consultation with our advisor.

Any questions? I'm here to help! 💼""",
            
            'meeting_reminder': f"""Hi {user_name}! 

This is a reminder about your upcoming investment consultation. 

If you haven't scheduled yet, please use this link:
{os.getenv('CALENDLY_LINK')}

Looking forward to helping you achieve your financial goals! 📈""",
            
            'abandoned_cart': f"""Hi {user_name}! 

I noticed you started the investment profile process but didn't complete it. No worries! 

Your personalized recommendations are just one form away. Complete it here:
{os.getenv('GOOGLE_FORM_URL')}

Questions? Just reply to this message! 🚀"""
        }
        
        message_body = messages.get(message_type, "Thank you for your interest! Our team will be in touch soon.")
        
        # Send WhatsApp message
        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=f'whatsapp:{phone_number}'
        )
        
        print(f"Follow-up message sent to {phone_number}: {message.sid}")
        return message.sid
        
    except Exception as e:
        print(f"Error sending follow-up message: {e}")
        return None

@app.task
def check_form_dropoffs():
    """Check for users who received form link but didn't complete it"""
    if not automation_manager.gc:
        return
    
    try:
        # Get all records from user data sheet
        records = automation_manager.user_data_sheet.get_all_records()
        current_time = datetime.now()
        
        for record in records:
            if record['Status'] == 'Form Sent':
                # Check if form was sent more than 24 hours ago
                timestamp = datetime.strptime(record['Timestamp'], '%Y-%m-%d %H:%M:%S')
                time_diff = current_time - timestamp
                
                if time_diff > timedelta(hours=24) and time_diff < timedelta(hours=25):
                    # Send first reminder after 24 hours
                    send_followup_message.delay(
                        record['Phone'], 
                        'form_reminder',
                        record.get('Name', '')
                    )
                elif time_diff > timedelta(hours=72) and time_diff < timedelta(hours=73):
                    # Send second reminder after 72 hours
                    send_followup_message.delay(
                        record['Phone'], 
                        'abandoned_cart',
                        record.get('Name', '')
                    )
                    
    except Exception as e:
        print(f"Error checking form dropoffs: {e}")

@app.task
def check_recommendation_followups():
    """Check for users who received recommendations but didn't respond"""
    if not automation_manager.gc:
        return
    
    try:
        records = automation_manager.user_data_sheet.get_all_records()
        current_time = datetime.now()
        
        for record in records:
            if record['Status'] == 'Recommended':
                timestamp = datetime.strptime(record['Timestamp'], '%Y-%m-%d %H:%M:%S')
                time_diff = current_time - timestamp
                
                if time_diff > timedelta(hours=48) and time_diff < timedelta(hours=49):
                    # Send follow-up after 48 hours
                    send_followup_message.delay(
                        record['Phone'],
                        'recommendation_followup', 
                        record.get('Name', '')
                    )
                    
    except Exception as e:
        print(f"Error checking recommendation follow-ups: {e}")

@app.task
def update_user_status(phone_number, new_status):
    """Update user status in Google Sheets"""
    if not automation_manager.gc:
        return
    
    try:
        # Find user row
        phone_col = automation_manager.user_data_sheet.col_values(2)  # Phone column
        if phone_number in phone_col:
            row_index = phone_col.index(phone_number) + 1
            automation_manager.user_data_sheet.update_cell(row_index, 9, new_status)  # Status column
            print(f"Updated status for {phone_number} to {new_status}")
    except Exception as e:
        print(f"Status update error: {e}")

@app.task
def generate_daily_report():
    """Generate daily analytics report"""
    if not automation_manager.gc:
        return
    
    try:
        records = automation_manager.user_data_sheet.get_all_records()
        leads_records = automation_manager.leads_sheet.get_all_records()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Count statistics
        stats = {
            'total_contacts': len(records),
            'forms_sent': len([r for r in records if r['Status'] == 'Form Sent']),
            'forms_completed': len([r for r in records if r['Status'] in ['Recommended', 'Meeting Scheduled']]),
            'recommendations_sent': len([r for r in records if r['Status'] == 'Recommended']),
            'meetings_scheduled': len([r for r in records if r['Status'] == 'Meeting Scheduled']),
            'confirmed_leads': len(leads_records)
        }
        
        # Calculate conversion rates
        if stats['total_contacts'] > 0:
            form_completion_rate = (stats['forms_completed'] / stats['forms_sent']) * 100 if stats['forms_sent'] > 0 else 0
            meeting_conversion_rate = (stats['meetings_scheduled'] / stats['recommendations_sent']) * 100 if stats['recommendations_sent'] > 0 else 0
        
        report = f"""
📊 Daily WhatsApp Bot Report - {today}

📈 Key Metrics:
• Total Contacts: {stats['total_contacts']}
• Forms Sent: {stats['forms_sent']}
• Forms Completed: {stats['forms_completed']}
• Recommendations Sent: {stats['recommendations_sent']}
• Meetings Scheduled: {stats['meetings_scheduled']}
• Confirmed Leads: {stats['confirmed_leads']}

📊 Conversion Rates:
• Form Completion: {form_completion_rate:.1f}%
• Meeting Conversion: {meeting_conversion_rate:.1f}%

Status Breakdown:
"""
        
        # Add status breakdown
        status_counts = {}
        for record in records:
            status = record['Status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            report += f"• {status}: {count}\n"
        
        print(report)
        
        # Optionally send report via email or save to file
        with open(f'reports/daily_report_{today}.txt', 'w') as f:
            f.write(report)
            
        return stats
        
    except Exception as e:
        print(f"Error generating daily report: {e}")
        return None

@app.task
def cleanup_old_sessions():
    """Clean up old user sessions (runs daily)"""
    try:
        # This would clean up old session data from memory/database
        # For now, just log the cleanup
        current_time = datetime.now()
        print(f"Session cleanup completed at {current_time}")
        
        # In a production system, you might:
        # - Remove sessions older than 7 days
        # - Archive old conversation data
        # - Clean up temporary files
        
    except Exception as e:
        print(f"Session cleanup error: {e}")

@app.task
def send_bulk_promotional_message(phone_numbers, message_template, user_data=None):
    """Send bulk promotional messages (use carefully to avoid spam)"""
    try:
        sent_count = 0
        failed_count = 0
        
        for phone_number in phone_numbers:
            try:
                # Personalize message if user data provided
                if user_data and phone_number in user_data:
                    user_info = user_data[phone_number]
                    message = message_template.format(**user_info)
                else:
                    message = message_template
                
                # Send message with delay to avoid rate limiting
                twilio_client.messages.create(
                    body=message,
                    from_=TWILIO_PHONE_NUMBER,
                    to=f'whatsapp:{phone_number}'
                )
                
                sent_count += 1
                
                # Add delay between messages to respect rate limits
                import time
                time.sleep(2)  # 2 second delay between messages
                
            except Exception as e:
                print(f"Failed to send message to {phone_number}: {e}")
                failed_count += 1
        
        return {
            'sent': sent_count,
            'failed': failed_count,
            'total': len(phone_numbers)
        }
        
    except Exception as e:
        print(f"Bulk message error: {e}")
        return None

# Periodic task scheduling
from celery.schedules import crontab

app.conf.beat_schedule = {
    'check-form-dropoffs': {
        'task': 'automation_scripts.check_form_dropoffs',
        'schedule': crontab(minute=0),  # Every hour
    },
    'check-recommendation-followups': {
        'task': 'automation_scripts.check_recommendation_followups', 
        'schedule': crontab(minute=30),  # Every hour at 30 minutes
    },
    'generate-daily-report': {
        'task': 'automation_scripts.generate_daily_report',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    'cleanup-old-sessions': {
        'task': 'automation_scripts.cleanup_old_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}

app.conf.timezone = 'UTC'

if __name__ == '__main__':
    # Test functions
    print("Testing automation functions...")
    
    # Test follow-up message
    test_phone = "+1234567890"  # Replace with test number
    send_followup_message.delay(test_phone, 'form_reminder', 'Test User')
    
    print("Automation scripts initialized successfully!")