#!/bin/bash

# Ideation Agent Setup Script

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           IDEATION AGENT - SETUP                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    exit 1
fi
echo "✓ Python 3 is installed"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt -q
echo "✓ Dependencies installed"

# Check for .env file
echo ""
if [ -f ".env" ]; then
    echo "✓ .env file already exists"

    # Check if API key is configured
    if grep -q "MY_API_KEY=sk-ant-" .env; then
        echo "✓ API key appears to be configured"
    else
        echo "⚠  API key may not be configured in .env"
        echo "  Please edit .env and add your Anthropic API key"
    fi
else
    echo "⚠  .env file not found"
    read -p "Would you like to create it now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo "✓ Created .env from .env.example"
        echo ""
        echo "Please edit .env and add your API key:"
        echo "  MY_API_KEY=sk-ant-api03-your-actual-key-here"
    fi
fi

# Create output directory
mkdir -p ideation_outputs
echo "✓ Output directory ready"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           SETUP COMPLETE                                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "To run the agent:"
echo "  ./run.sh"
echo ""
echo "Or:"
echo "  python3 ideation_agent.py"
echo ""
