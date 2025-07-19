#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify apt sources.list to use archive.debian.org for stretch
echo "Using apt-get to install system dependencies..."
apt-get update -y
apt-get install -y build-essential python3-dev

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install wheel setuptools
pip install -r requirements.txt

echo "Build completed successfully!" 