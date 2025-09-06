import subprocess
import time
import os
from twitch_fetcher import get_twitch_stream_url

class RTMPForwarder:
    def __init__(self, twitch_channel, rtmp_destinations, sample_video_path="./sample.mp4"):
        self.twitch_channel = twitch_channel
        self.rtmp_destinations = rtmp_destinations
        self.sample_video_path = sample_video_path
        self.ffmpeg_process = None
        self.current_input_url = None

    def start_forwarding(self):
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            print("FFmpeg process is already running.")
            return

        twitch_stream_url = get_twitch_stream_url(self.twitch_channel)

        if twitch_stream_url:
            self.current_input_url = twitch_stream_url
            print(f"Twitch stream is LIVE. Using: {self.current_input_url}")
        else:
            self.current_input_url = self.sample_video_path
            print(f"Twitch stream is OFFLINE. Using sample video: {self.current_input_url}")

        command = [
            'ffmpeg',
            '-re', # Read input at native frame rate (important for looping video)
            '-i', self.current_input_url, # Input from Twitch or sample video
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'flv'
        ]

        for dest in self.rtmp_destinations:
            command.extend(['-f', 'flv', dest])

        print(f"Starting FFmpeg with command: {' '.join(command)}")
        try:
            # Use preexec_fn to detach the child process from the parent
            # This is a common way to daemonize processes in Python
            # Also redirect stdout/stderr to /dev/null to prevent blocking
            self.ffmpeg_process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
            print(f"FFmpeg process started with PID: {self.ffmpeg_process.pid}")
        except FileNotFoundError:
            print("FFmpeg not found. Please ensure it is installed and in your PATH.")
        except Exception as e:
            print(f"Error starting FFmpeg process: {e}")

    def stop_forwarding(self):
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            print(f"Stopping FFmpeg process with PID: {self.ffmpeg_process.pid}")
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait(timeout=5) # Give it some time to terminate
            if self.ffmpeg_process.poll() is None:
                print("FFmpeg process did not terminate gracefully, killing it.")
                self.ffmpeg_process.kill()
            self.ffmpeg_process = None
            print("FFmpeg process stopped.")
        else:
            print("FFmpeg process is not running.")

    def is_running(self):
        return self.ffmpeg_process is not None and self.ffmpeg_process.poll() is None

if __name__ == "__main__":
    # Example Usage:
    channel = "randomtodaytv"
    destinations = [
        "rtmp://a.rtmp.youtube.com/live2/YOUR_YOUTUBE_STREAM_KEY",
        "rtmp://live.twitch.tv/app/YOUR_TWITCH_STREAM_KEY"
    ]

    forwarder = RTMPForwarder(channel, destinations)

    # Start forwarding
    forwarder.start_forwarding()

    # Keep the script running for a while to observe (in a real app, this would be managed by Streamlit)
    try:
        while True:
            time.sleep(60) # Keep running and check status periodically
            if not forwarder.is_running():
                print("FFmpeg process died. Attempting to restart...")
                forwarder.start_forwarding()
    except KeyboardInterrupt:
        print("Stopping forwarder...")
        forwarder.stop_forwarding()


