import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleFormHandler:
    def __init__(self):
        self.setup_sheets()
        self.webhook_url = os.getenv('WEBHOOK_URL', 'http://localhost:5000/form-webhook')
    
    def setup_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('google_credentials.json', scope)
            self.gc = gspread.authorize(creds)
            
            # Create or open spreadsheets
            self.create_spreadsheets()
        except Exception as e:
            print(f"Google Sheets setup error: {e}")
            self.gc = None
    
    def create_spreadsheets(self):
        """Create required spreadsheets if they don't exist"""
        try:
            # Try to open existing sheets, create if they don't exist
            try:
                self.user_data_sheet = self.gc.open("Customer Onboarding Data").sheet1
            except gspread.SpreadsheetNotFound:
                spreadsheet = self.gc.create("Customer Onboarding Data")
                self.user_data_sheet = spreadsheet.sheet1
                # Set up headers
                headers = ['Timestamp', 'Phone', 'Name', 'Age', 'Income', 'Preferences', 
                          'Risk_Appetite', 'Recommended_Product', 'Status']
                self.user_data_sheet.insert_row(headers, 1)
                
                # Share with your email (replace with your email)
                spreadsheet.share('your-email@gmail.com', perm_type='user', role='writer')
            
            try:
                self.leads_sheet = self.gc.open("Confirmed Leads").sheet1
            except gspread.SpreadsheetNotFound:
                spreadsheet = self.gc.create("Confirmed Leads")
                self.leads_sheet = spreadsheet.sheet1
                # Set up headers
                headers = ['Timestamp', 'Phone', 'Name', 'Product_Interest', 'Meeting_Scheduled', 
                          'Chat_History', 'Status']
                self.leads_sheet.insert_row(headers, 1)
                
                # Share with your email
                spreadsheet.share('your-email@gmail.com', perm_type='user', role='writer')
                
        except Exception as e:
            print(f"Spreadsheet creation error: {e}")
    
    def process_form_response(self, form_data):
        """Process Google Form response and extract relevant data"""
        # Map form fields to our data structure
        # Adjust these mappings based on your actual form questions
        processed_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'name': form_data.get('entry.123456789', ''),  # Replace with actual entry ID
            'phone': form_data.get('entry.987654321', ''),  # Replace with actual entry ID
            'age': form_data.get('entry.111111111', ''),    # Replace with actual entry ID
            'income': form_data.get('entry.222222222', ''), # Replace with actual entry ID
            'preferences': form_data.get('entry.333333333', ''), # Replace with actual entry ID
            'email': form_data.get('entry.444444444', ''),  # Replace with actual entry ID
        }
        
        return processed_data
    
    def save_form_data(self, processed_data):
        """Save processed form data to Google Sheets"""
        if not self.gc:
            return False
        
        try:
            row_data = [
                processed_data['timestamp'],
                processed_data['phone'],
                processed_data['name'],
                processed_data['age'],
                processed_data['income'],
                processed_data['preferences'],
                '',  # Risk appetite (to be calculated)
                '',  # Recommended product (to be calculated)
                'Form Submitted'
            ]
            
            self.user_data_sheet.append_row(row_data)
            return True
        except Exception as e:
            print(f"Save form data error: {e}")
            return False
    
    def get_form_entry_ids(self, form_url):
        """
        Helper function to get entry IDs from Google Form
        You'll need to inspect your form's HTML source to get these IDs
        """
        instructions = """
        To get the entry IDs for your Google Form:
        
        1. Open your Google Form
        2. Click "Send" and copy the link
        3. Open the link in a new tab
        4. Right-click and "View Page Source"
        5. Search for "entry." in the source code
        6. Copy the entry IDs (like entry.123456789) for each field
        7. Update the process_form_response method with these IDs
        
        Example mapping:
        - Name field: entry.123456789
        - Phone field: entry.987654321
        - Age field: entry.111111111
        - Income field: entry.222222222
        - Preferences field: entry.333333333
        """
        
        print(instructions)
        return instructions

def create_google_form_template():
    """
    Template for creating a Google Form with the required fields
    """
    form_questions = {
        "form_title": "Investment Profile Assessment",
        "form_description": "Help us understand your investment goals and preferences",
        "questions": [
            {
                "type": "short_answer",
                "question": "What is your full name?",
                "required": True
            },
            {
                "type": "short_answer", 
                "question": "What is your WhatsApp phone number? (with country code, e.g., +1234567890)",
                "required": True
            },
            {
                "type": "short_answer",
                "question": "What is your age?",
                "required": True
            },
            {
                "type": "multiple_choice",
                "question": "What is your annual income range?",
                "options": [
                    "Under $25,000",
                    "$25,000 - $50,000", 
                    "$50,000 - $75,000",
                    "$75,000 - $100,000",
                    "$100,000 - $150,000",
                    "Over $150,000"
                ],
                "required": True
            },
            {
                "type": "multiple_choice",
                "question": "What is your investment experience?",
                "options": [
                    "Beginner - No prior experience",
                    "Some experience - Basic knowledge",
                    "Experienced - Good understanding",
                    "Expert - Extensive experience"
                ],
                "required": True
            },
            {
                "type": "multiple_choice",
                "question": "What is your investment timeline?",
                "options": [
                    "Less than 1 year",
                    "1-3 years",
                    "3-5 years", 
                    "5-10 years",
                    "More than 10 years"
                ],
                "required": True
            },
            {
                "type": "multiple_choice",
                "question": "How would you describe your risk tolerance?",
                "options": [
                    "Conservative - Prefer stable, low-risk investments",
                    "Moderate - Balanced approach with some risk",
                    "Aggressive - Comfortable with high-risk, high-reward investments"
                ],
                "required": True
            },
            {
                "type": "paragraph",
                "question": "What are your specific investment goals and preferences? (e.g., retirement, buying a house, wealth building)",
                "required": False
            },
            {
                "type": "short_answer",
                "question": "What is your email address?",
                "required": False
            }
        ]
    }
    
    return form_questions

# Example usage and setup instructions
if __name__ == "__main__":
    handler = GoogleFormHandler()
    
    # Print form template
    template = create_google_form_template()
    print("=== GOOGLE FORM SETUP INSTRUCTIONS ===")
    print("\n1. Create a new Google Form at https://forms.google.com")
    print(f"\n2. Set the title: {template['form_title']}")
    print(f"\n3. Set the description: {template['form_description']}")
    print("\n4. Add the following questions:")
    
    for i, q in enumerate(template['questions'], 1):
        print(f"\n   Question {i}: {q['question']}")
        print(f"   Type: {q['type']}")
        print(f"   Required: {q['required']}")
        if 'options' in q:
            print(f"   Options: {', '.join(q['options'])}")
    
    print("\n5. After creating the form:")
    print("   - Click 'Send' and copy the form URL")
    print("   - Add the URL to your .env file as GOOGLE_FORM_URL")
    print("   - Set up form response notifications or use Google Apps Script for webhooks")
    
    print("\n6. To get entry IDs:")
    handler.get_form_entry_ids("")