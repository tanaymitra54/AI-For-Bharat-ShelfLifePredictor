#!/bin/bash
# setup_env.sh - Setup .env file with API keys

cd AI-For-Bharat-ShelfLifePredictor/config

# Copy .env.example to .env
cp .env.example .env

echo "========================================"
echo "Configuration Setup"
echo "========================================"
echo ""
echo "Please enter your API keys:"
echo ""

# Prompt for ElevenLabs API key
read -p "ElevenLabs API Key (or press Enter to skip): " ELEVENLABS_KEY

# Prompt for OpenRouter API key
read -p "OpenRouter API Key (or press Enter to skip): " OPENROUTER_KEY

# Update .env file
if [ -n "$ELEVENLABS_KEY" ]; then
    sed -i "s/your_elevenlabs_api_key/$ELEVENLABS_KEY/" .env
fi

if [ -n "$OPENROUTER_KEY" ]; then
    sed -i "s/your_openrouter_api_key/$OPENROUTER_KEY/" .env
fi

echo ""
echo "✓ .env file configured successfully"
echo ""
echo "API Keys configured:"
if [ -n "$ELEVENLABS_KEY" ]; then
    echo "  ✓ ElevenLabs: ${ELEVENLABS_KEY:0:20}..."
else
    echo "  ✗ ElevenLabs: Not configured (optional)"
fi
if [ -n "$OPENROUTER_KEY" ]; then
    echo "  ✓ OpenRouter: ${OPENROUTER_KEY:0:20}..."
else
    echo "  ✗ OpenRouter: Not configured (optional)"
fi
echo ""
echo "Note: Core prediction features work without API keys."
echo "      API keys are only needed for voice and chat features."
echo ""
