#!/bin/bash

cd "$(dirname "$0")"

echo "========================================"
echo "   MESSENGER WRAPPER BUILDER"
echo "========================================"

DATA_DIR="$HOME/Documents/MessengerWrapperData"
ENV_FILE="$DATA_DIR/.env"

mkdir -p "$DATA_DIR"

if [ ! -f "$ENV_FILE" ]; then
    echo "No saved login data found."
    echo "Please enter your Facebook credentials."
    echo "----------------------------------------"
    
    read -p "Enter Email: " FB_EMAIL
    read -s -p "Enter Password: " FB_PASSWORD
    echo ""
    
    echo "FB_EMAIL=$FB_EMAIL" > "$ENV_FILE"
    echo "FB_PASSWORD=$FB_PASSWORD" >> "$ENV_FILE"
    
    echo "Credentials saved."
    echo "----------------------------------------"
else
    echo "Found existing credentials."
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Checking dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    pip install pyinstaller -q
else
    echo "ERROR: requirements.txt not found!"
    exit 1
fi

if [ ! -f "messenger_wrapper.py" ]; then
    echo "ERROR: messenger_wrapper.py not found!"
    exit 1
fi

echo "Cleaning up old build files..."
rm -rf build dist *.spec

echo "Starting application build..."

if [ -f "app_icon.icns" ]; then
    echo "Building with custom icon..."
    pyinstaller --noconsole --name "Messenger Wrapper" --icon="app_icon.icns" messenger_wrapper.py
else
    echo "Building with default icon..."
    pyinstaller --noconsole --name "Messenger Wrapper" messenger_wrapper.py
fi

if [ -d "dist/Messenger Wrapper.app" ]; then
    echo "========================================"
    echo "SUCCESS! Application ready."
    echo "Opening application folder..."
    echo "========================================"
    open dist
else
    echo "ERROR: Application build failed."
fi