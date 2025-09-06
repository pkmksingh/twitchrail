import subprocess
import sys
import os
import time
from rtmp_forwarder import RTMPForwarder
from twitch_fetcher import get_twitch_stream_url

# This script is meant to be run as a detached process.
# It will continuously try to forward the stream.

def run_forwarder_in_background(twitch_channel, rtmp_destinations, sample_video_path):
    forwarder = RTMPForwarder(twitch_channel, rtmp_destinations, sample_video_path)
    while True:
        if not forwarder.is_running():
            print("FFmpeg process is not running or has stopped. Attempting to restart...")
            forwarder.start_forwarding()
        time.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    # This part will be called when the script is run directly
    # It expects arguments for twitch_channel and rtmp_destinations
    # For testing, you can hardcode them or pass them via command line
    
    # Example usage if run directly for testing:
    # python3 background_forwarder.py randomtodaytv "rtmp://a.rtmp.youtube.com/live2/YOUR_YOUTUBE_STREAM_KEY,rtmp://live.twitch.tv/app/YOUR_TWITCH_STREAM_KEY"

    if len(sys.argv) < 3:
        print("Usage: python3 background_forwarder.py <twitch_channel> <rtmp_destinations_comma_separated> [sample_video_path]")
        sys.exit(1)

    twitch_channel = sys.argv[1]
    rtmp_destinations = sys.argv[2].split(",")
    sample_video_path = sys.argv[3] if len(sys.argv) > 3 else "./sample.mp4"

    print(f"Starting background forwarder for Twitch channel: {twitch_channel}")
    print(f"RTMP Destinations: {rtmp_destinations}")
    print(f"Sample Video Path: {sample_video_path}")

    run_forwarder_in_background(twitch_channel, rtmp_destinations, sample_video_path)


