#!/bin/bash

# Twitch to RTMP Forwarder - Run Script
# This script starts the Streamlit application

echo "Starting Twitch to RTMP Forwarder..."

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: FFmpeg is not installed. Please install FFmpeg first."
    echo "Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "macOS: brew install ffmpeg"
    exit 1
fi

# Check if Python dependencies are installed
if ! python3 -c "import streamlit, streamlink" &> /dev/null; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Start Streamlit app
echo "Starting Streamlit app on http://localhost:8501"
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

