/**
 * Google Apps Script for Google Forms webhook integration
 * This script automatically sends form responses to your WhatsApp bot
 */

// Configuration - Replace with your actual webhook URL
const WEBHOOK_URL = 'https://your-app-domain.com/form-webhook';

/**
 * Function to handle form submissions
 * This function will be triggered when a form is submitted
 */
function onFormSubmit(e) {
  try {
    // Get form response
    const formResponse = e.response;
    const itemResponses = formResponse.getItemResponses();
    
    // Extract form data
    const formData = {};
    
    // Map form responses to our data structure
    itemResponses.forEach(function(itemResponse) {
      const question = itemResponse.getItem().getTitle();
      const answer = itemResponse.getResponse();
      
      // Map questions to field names
      if (question.toLowerCase().includes('name')) {
        formData.name = answer;
      } else if (question.toLowerCase().includes('phone') || question.toLowerCase().includes('whatsapp')) {
        formData.phone = answer;
      } else if (question.toLowerCase().includes('age')) {
        formData.age = answer;
      } else if (question.toLowerCase().includes('income')) {
        formData.income = answer;
      } else if (question.toLowerCase().includes('experience')) {
        formData.experience = answer;
      } else if (question.toLowerCase().includes('timeline')) {
        formData.timeline = answer;
      } else if (question.toLowerCase().includes('risk') || question.toLowerCase().includes('tolerance')) {
        formData.risk_tolerance = answer;
      } else if (question.toLowerCase().includes('goals') || question.toLowerCase().includes('preferences')) {
        formData.preferences = answer;
      } else if (question.toLowerCase().includes('email')) {
        formData.email = answer;
      }
    });
    
    // Add timestamp
    formData.timestamp = new Date().toISOString();
    formData.form_id = formResponse.getId();
    
    // Send data to webhook
    const payload = {
      'method': 'POST',
      'headers': {
        'Content-Type': 'application/json',
      },
      'payload': JSON.stringify(formData)
    };
    
    const response = UrlFetchApp.fetch(WEBHOOK_URL, payload);
    
    if (response.getResponseCode() === 200) {
      console.log('Form data sent successfully to webhook');
    } else {
      console.error('Error sending data to webhook:', response.getResponseCode());
    }
    
  } catch (error) {
    console.error('Error in onFormSubmit:', error);
    
    // Optional: Send error notification
    sendErrorNotification(error.toString());
  }
}

/**
 * Function to set up the form trigger
 * Run this once to set up automatic form submission handling
 */
function setupFormTrigger() {
  try {
    // Get the form - replace with your form ID
    const form = FormApp.openById('YOUR_FORM_ID_HERE');
    
    // Delete existing triggers
    const triggers = ScriptApp.getProjectTriggers();
    triggers.forEach(function(trigger) {
      if (trigger.getHandlerFunction() === 'onFormSubmit') {
        ScriptApp.deleteTrigger(trigger);
      }
    });
    
    // Create new trigger
    ScriptApp.newTrigger('onFormSubmit')
      .timeBased()
      .onFormSubmit()
      .create();
    
    console.log('Form trigger set up successfully');
    
  } catch (error) {
    console.error('Error setting up form trigger:', error);
  }
}

/**
 * Function to test the webhook connection
 */
function testWebhook() {
  const testData = {
    name: 'Test User',
    phone: '+1234567890',
    age: '30',
    income: '$50,000 - $75,000',
    experience: 'Some experience - Basic knowledge',
    timeline: '3-5 years',
    risk_tolerance: 'Moderate - Balanced approach with some risk',
    preferences: 'Looking for balanced growth with moderate risk',
    email: 'test@example.com',
    timestamp: new Date().toISOString(),
    form_id: 'test_submission'
  };
  
  const payload = {
    'method': 'POST',
    'headers': {
      'Content-Type': 'application/json',
    },
    'payload': JSON.stringify(testData)
  };
  
  try {
    const response = UrlFetchApp.fetch(WEBHOOK_URL, payload);
    console.log('Test webhook response:', response.getResponseCode());
    console.log('Response body:', response.getContentText());
  } catch (error) {
    console.error('Test webhook error:', error);
  }
}

/**
 * Function to send error notifications
 */
function sendErrorNotification(errorMessage) {
  try {
    // You can implement email notifications or other error handling here
    const emailBody = `
      WhatsApp Bot Form Integration Error
      
      Time: ${new Date().toISOString()}
      Error: ${errorMessage}
      
      Please check the Google Apps Script logs for more details.
    `;
    
    // Uncomment and configure if you want email notifications
    // GmailApp.sendEmail('your-email@gmail.com', 'WhatsApp Bot Error', emailBody);
    
    console.error('Error notification:', errorMessage);
  } catch (error) {
    console.error('Error sending notification:', error);
  }
}

/**
 * Function to get form entry IDs for debugging
 * This helps you map form questions to the correct field names
 */
function getFormStructure() {
  try {
    // Replace with your form ID
    const form = FormApp.openById('YOUR_FORM_ID_HERE');
    const items = form.getItems();
    
    console.log('Form Structure:');
    items.forEach(function(item, index) {
      console.log(`Question ${index + 1}: ${item.getTitle()}`);
      console.log(`Type: ${item.getType()}`);
      console.log(`ID: ${item.getId()}`);
      console.log('---');
    });
    
  } catch (error) {
    console.error('Error getting form structure:', error);
  }
}

/**
 * Function to create a sample form (for testing)
 */
function createSampleForm() {
  try {
    const form = FormApp.create('Investment Profile Assessment - WhatsApp Bot');
    
    form.setDescription('Help us understand your investment goals and preferences');
    
    // Add form questions
    form.addTextItem()
      .setTitle('What is your full name?')
      .setRequired(true);
    
    form.addTextItem()
      .setTitle('What is your WhatsApp phone number? (with country code, e.g., +1234567890)')
      .setRequired(true);
    
    form.addTextItem()
      .setTitle('What is your age?')
      .setRequired(true);
    
    form.addMultipleChoiceItem()
      .setTitle('What is your annual income range?')
      .setChoiceValues([
        'Under $25,000',
        '$25,000 - $50,000',
        '$50,000 - $75,000', 
        '$75,000 - $100,000',
        '$100,000 - $150,000',
        'Over $150,000'
      ])
      .setRequired(true);
    
    form.addMultipleChoiceItem()
      .setTitle('What is your investment experience?')
      .setChoiceValues([
        'Beginner - No prior experience',
        'Some experience - Basic knowledge',
        'Experienced - Good understanding',
        'Expert - Extensive experience'
      ])
      .setRequired(true);
    
    form.addMultipleChoiceItem()
      .setTitle('What is your investment timeline?')
      .setChoiceValues([
        'Less than 1 year',
        '1-3 years',
        '3-5 years',
        '5-10 years', 
        'More than 10 years'
      ])
      .setRequired(true);
    
    form.addMultipleChoiceItem()
      .setTitle('How would you describe your risk tolerance?')
      .setChoiceValues([
        'Conservative - Prefer stable, low-risk investments',
        'Moderate - Balanced approach with some risk',
        'Aggressive - Comfortable with high-risk, high-reward investments'
      ])
      .setRequired(true);
    
    form.addParagraphTextItem()
      .setTitle('What are your specific investment goals and preferences? (e.g., retirement, buying a house, wealth building)')
      .setRequired(false);
    
    form.addTextItem()
      .setTitle('What is your email address?')
      .setRequired(false);
    
    const formUrl = form.getPublishedUrl();
    console.log('Sample form created successfully!');
    console.log('Form URL:', formUrl);
    console.log('Form ID:', form.getId());
    
    return form;
    
  } catch (error) {
    console.error('Error creating sample form:', error);
  }
}

/**
 * Setup instructions for the Google Apps Script
 */
function showSetupInstructions() {
  const instructions = `
  GOOGLE APPS SCRIPT SETUP INSTRUCTIONS:
  
  1. Create a new Google Form or use existing one
  2. Open Google Apps Script (script.google.com)
  3. Create a new project and paste this code
  4. Update the WEBHOOK_URL constant with your app's URL
  5. Update YOUR_FORM_ID_HERE with your actual form ID
  6. Run setupFormTrigger() function once
  7. Test with testWebhook() function
  
  To get your form ID:
  - Open your Google Form
  - Look at the URL: https://docs.google.com/forms/d/FORM_ID_HERE/edit
  - Copy the FORM_ID_HERE part
  
  To deploy as web app (alternative to webhooks):
  1. Click Deploy > New Deployment
  2. Choose "Web app" as type
  3. Set execute as "Me" and access to "Anyone"
  4. Copy the web app URL for use in your bot
  `;
  
  console.log(instructions);
}

// Run setup instructions when script is opened
showSetupInstructions();