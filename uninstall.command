#!/bin/bash

cd "$(dirname "$0")"

echo "========================================"
echo "   MESSENGER WRAPPER UNINSTALLER"
echo "========================================"

APP_PATH="./dist/Messenger Wrapper.app"
DATA_DIR="$HOME/Documents/MessengerWrapperData"

if [ -d "$APP_PATH" ]; then
    echo "Removing application..."
    rm -rf "$APP_PATH"
else
    echo "Application not found in current directory."
fi

if [ -d "$DATA_DIR" ]; then
    echo "Removing user data and credentials..."
    rm -rf "$DATA_DIR"
else
    echo "User data directory not found."
fi

echo "Cleaning temporary files..."
rm -rf build dist venv *.spec

echo "========================================"
echo "Uninstallation complete."
echo "========================================"