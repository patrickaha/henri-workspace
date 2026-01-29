#!/bin/bash
# Peter Tweets - Quick Launch Script

set -e

echo "🚀 Peter Tweets - Parallel Agent Launcher"
echo "========================================"

# Check if in correct directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: Run this from ~/clawd/peter-tweets/"
    exit 1
fi

# Check for Twitter API key
if [ -z "$TWITTER_BEARER_TOKEN" ]; then
    if [ -f "$HOME/clawd/.env" ]; then
        source "$HOME/clawd/.env"
    fi
    
    if [ -z "$TWITTER_BEARER_TOKEN" ]; then
        echo "❌ Missing TWITTER_BEARER_TOKEN"
        echo "Add to ~/clawd/.env:"
        echo "TWITTER_BEARER_TOKEN=your-key-here"
        exit 1
    fi
fi

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install if needed
if ! command -v peter-tweets &> /dev/null; then
    echo "📦 Installing peter-tweets..."
    pip install -e . > /dev/null 2>&1
fi

# Run health check
echo ""
echo "🏥 Running health check..."
peter-tweets health

# Show options
echo ""
echo "🎯 What would you like to do?"
echo ""
echo "1) Start parallel monitoring (5 agents)"
echo "2) Check latest tweets"
echo "3) Get today's wisdom"
echo "4) Search tweet history"
echo "5) Run orchestration demo"
echo "6) Run full test suite"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo "Starting parallel agents..."
        peter-tweets monitor --agents 5
        ;;
    2)
        peter-tweets latest --limit 10
        ;;
    3)
        peter-tweets wisdom --period today
        ;;
    4)
        read -p "Search query: " query
        peter-tweets search "$query"
        ;;
    5)
        peter-tweets orchestrate
        ;;
    6)
        peter-tweets test --full
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac