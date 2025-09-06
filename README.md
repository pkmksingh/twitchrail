# Twitch to RTMP Forwarder

A Streamlit application that fetches Twitch streams in real-time and forwards them to multiple custom RTMP destinations. The application keeps streams running in the background even when the Twitch feed is offline or the app is closed.

## Features

- ✅ Real-time Twitch stream forwarding
- ✅ Multiple RTMP destinations support
- ✅ Background streaming (persistent)
- ✅ Automatic fallback to sample video when Twitch is offline
- ✅ Stream continues even when app is closed
- ✅ Web-based configuration interface

## Requirements

- Python 3.7+
- FFmpeg
- Streamlit
- Streamlink

## Installation

1. Clone or download this project
2. Install Python dependencies:
   ```bash
   pip install streamlit streamlink
   ```
3. Install FFmpeg:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Configure your settings:
   - Enter the Twitch channel name (default: randomtodaytv)
   - Add your RTMP destinations (e.g., YouTube, Twitch, Facebook Live, etc.)

4. Click "Start Streaming" to begin forwarding

5. The stream will run in the background even if you close the browser or app

## Configuration

### Twitch Channel
Enter the channel name without the full URL. For example, for `https://www.twitch.tv/randomtodaytv`, just enter `randomtodaytv`.

### RTMP Destinations
Add complete RTMP URLs with stream keys. Examples:
- YouTube: `rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY`
- Twitch: `rtmp://live.twitch.tv/app/YOUR_STREAM_KEY`
- Facebook: `rtmp://live-api-s.facebook.com:80/rtmp/YOUR_STREAM_KEY`

## How It Works

1. **Stream Detection**: The app uses Streamlink to detect if the Twitch channel is live
2. **Live Forwarding**: When live, it forwards the stream to all configured RTMP destinations
3. **Offline Fallback**: When offline, it streams a sample video to keep destinations active
4. **Background Process**: Uses nohup and process groups to run independently
5. **Auto-Restart**: Automatically restarts if the FFmpeg process crashes

## Files

- `streamlit_app.py` - Main Streamlit web interface
- `twitch_fetcher.py` - Twitch stream detection using Streamlink
- `rtmp_forwarder.py` - RTMP forwarding logic using FFmpeg
- `background_forwarder.py` - Background process manager
- `sample.mp4` - Sample video for offline fallback
- `README.md` - This documentation

## Troubleshooting

### Stream Not Starting
- Check that FFmpeg is installed and in your PATH
- Verify your RTMP destinations are correct
- Ensure you have proper stream keys

### Background Process Not Running
- Check if the process is running: `ps aux | grep background_forwarder`
- Check system logs for errors
- Restart the application

### Stream Quality Issues
- The app uses FFmpeg's ultrafast preset for low latency
- Modify the FFmpeg parameters in `rtmp_forwarder.py` for different quality settings

## Advanced Usage

### Running Without Streamlit
You can run the background forwarder directly:
```bash
python3 background_forwarder.py randomtodaytv "rtmp://dest1,rtmp://dest2" ./sample.mp4
```

### Custom Sample Video
Replace `sample.mp4` with your own video file for offline streaming.

### Multiple Instances
You can run multiple instances for different Twitch channels by using different working directories.

## Security Notes

- Keep your RTMP stream keys private
- Don't share screenshots or logs that contain stream keys
- Consider using environment variables for sensitive configuration

## License

This project is provided as-is for educational and personal use.

