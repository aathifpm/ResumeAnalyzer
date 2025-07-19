#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install wheel setuptools
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

echo "Build completed successfully!" 