#!/usr/bin/env python3
"""
Test script to verify WhatsApp bot setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        from twilio.rest import Client
        print("✅ Twilio imported successfully")
    except ImportError as e:
        print(f"❌ Twilio import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import gspread
        print("✅ GSpread imported successfully")
    except ImportError as e:
        print(f"❌ GSpread import failed: {e}")
        return False
    
    try:
        import redis
        print("✅ Redis imported successfully")
    except ImportError as e:
        print(f"❌ Redis import failed: {e}")
        return False
    
    try:
        from celery import Celery
        print("✅ Celery imported successfully")
    except ImportError as e:
        print(f"❌ Celery import failed: {e}")
        return False
    
    return True

def test_redis_connection():
    """Test Redis connection"""
    print("\n🔍 Testing Redis connection...")
    
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        response = r.ping()
        if response:
            print("✅ Redis connection successful")
            return True
        else:
            print("❌ Redis connection failed")
            return False
    except Exception as e:
        print(f"❌ Redis connection error: {e}")
        return False

def test_environment_variables():
    """Test if environment variables are set"""
    print("\n🔍 Testing environment variables...")
    
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 
        'TWILIO_PHONE_NUMBER',
        'OPENAI_API_KEY',
        'GOOGLE_FORM_URL',
        'CALENDLY_LINK'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            # Mask sensitive values
            value = os.getenv(var)
            if 'key' in var.lower() or 'token' in var.lower() or 'sid' in var.lower():
                masked_value = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please update your .env file with the required credentials")
        return False
    
    return True

def test_flask_app():
    """Test if Flask app can be imported"""
    print("\n🔍 Testing Flask app...")
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 WhatsApp AI Bot Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_redis_connection,
        test_environment_variables,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your WhatsApp bot setup is ready!")
        print("\n📝 Next steps:")
        print("1. Update your .env file with actual credentials")
        print("2. Set up Google credentials (google_credentials.json)")
        print("3. Create your Google Form")
        print("4. Run the bot with: python app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()