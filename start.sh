#!/bin/bash

# WhatsApp AI Bot Startup Script
echo "🚀 Starting WhatsApp AI Bot..."

# Activate virtual environment
source whatsapp_bot_env/bin/activate

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "⚠️  Redis not running. Starting Redis..."
    redis-server --daemonize yes
    sleep 2
fi

# Check environment variables
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Start the Flask app
echo "🌐 Starting Flask application..."
echo "📱 Bot will be available at: http://localhost:5000"
echo "📊 Health check: http://localhost:5000/health"
echo ""
echo "💡 To test locally, use ngrok to expose your localhost:"
echo "   ngrok http 5000"
echo ""
echo "🛑 Press Ctrl+C to stop the bot"
echo ""

python app.py