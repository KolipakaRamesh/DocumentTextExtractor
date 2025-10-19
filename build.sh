#!/bin/bash
set -e

# Create a directory for Tesseract
mkdir -p tesseract

# Download and extract Tesseract
curl -L "https://github.com/bweigel/aws-lambda-tesseract-layer/releases/download/v4.1.1-amazon-linux-2/tesseract-v4.1.1-amazon-linux-2.zip" -o "/tmp/tesseract.zip"
unzip "/tmp/tesseract.zip" -d "tesseract"
