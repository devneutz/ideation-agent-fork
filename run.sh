#!/bin/bash

# Ideation Agent Launcher Script

echo "Starting Ideation Agent..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
python3 -c "import anthropic" 2>/dev/null || python3 -c "import openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

# Run the agent
python3 ideation_agent.py

echo ""
echo "Session ended. Goodbye!"
