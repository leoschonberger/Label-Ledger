#!/bin/bash

# Exit on any error
set -e

echo "Starting installation process..."

# Install CUPS
echo "Installing CUPS..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y cups
elif command -v brew &> /dev/null; then
    brew install cups
else
    echo "Error: Could not determine package manager (apt-get or brew)"
    exit 1
fi

# Get the desktop path
DESKTOP_PATH="$HOME/Desktop"

# Find the zip file on desktop
ZIP_FILE=$(find "$DESKTOP_PATH" -maxdepth 1 -name "*.zip" | head -n 1)

if [ -z "$ZIP_FILE" ]; then
    echo "Error: No zip file found on desktop"
    exit 1
fi

echo "Found zip file: $ZIP_FILE"

# Create a temporary directory for extraction
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Unzip the file
echo "Unzipping file..."
unzip "$ZIP_FILE" -d "$TEMP_DIR"

# Find the tar archive
TAR_FILE=$(find "$TEMP_DIR" -name "*.tar.gz" | head -n 1)

if [ -z "$TAR_FILE" ]; then
    echo "Error: No tar.gz file found in extracted contents"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "Found tar archive: $TAR_FILE"

# Extract the tar archive
echo "Extracting tar archive..."
tar zxf "$TAR_FILE" -C "$TEMP_DIR"

# Find and run the install script
INSTALL_SCRIPT=$(find "$TEMP_DIR" -name "install" -type f | head -n 1)

if [ -z "$INSTALL_SCRIPT" ]; then
    echo "Error: No install script found in extracted contents"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "Found install script: $INSTALL_SCRIPT"
echo "Running install script with sudo..."
sudo "$INSTALL_SCRIPT"

# Cleanup
echo "Cleaning up temporary files..."
rm -rf "$TEMP_DIR"

echo "Installation completed successfully!"
