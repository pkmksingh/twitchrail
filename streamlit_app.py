import streamlit as st
import subprocess
import os
import signal
import time
from rtmp_forwarder import RTMPForwarder
from twitch_fetcher import get_twitch_stream_url

# Initialize session state
if 'forwarder' not in st.session_state:
    st.session_state.forwarder = None
if 'background_process' not in st.session_state:
    st.session_state.background_process = None
if 'rtmp_destinations' not in st.session_state:
    st.session_state.rtmp_destinations = []

st.title("Twitch to RTMP Forwarder")
st.markdown("This app fetches a Twitch stream and forwards it to multiple RTMP destinations.")

# Configuration Section
st.header("Configuration")

# Twitch Channel Input
twitch_channel = st.text_input("Twitch Channel Name", value="randomtodaytv", help="Enter the Twitch channel name (without 'https://www.twitch.tv/')")

# RTMP Destinations
st.subheader("RTMP Destinations")
st.markdown("Add your RTMP destinations below. Each destination should be a complete RTMP URL with stream key.")

# Add new RTMP destination
new_destination = st.text_input("Add RTMP Destination", placeholder="rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY")
if st.button("Add Destination"):
    if new_destination and new_destination not in st.session_state.rtmp_destinations:
        st.session_state.rtmp_destinations.append(new_destination)
        st.success(f"Added destination: {new_destination}")
    elif new_destination in st.session_state.rtmp_destinations:
        st.warning("This destination is already in the list.")
    else:
        st.error("Please enter a valid RTMP destination.")

# Display current destinations
if st.session_state.rtmp_destinations:
    st.subheader("Current RTMP Destinations")
    for i, dest in enumerate(st.session_state.rtmp_destinations):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(dest)
        with col2:
            if st.button(f"Remove", key=f"remove_{i}"):
                st.session_state.rtmp_destinations.pop(i)
                st.rerun()

# Status Section
st.header("Status")

# Check Twitch stream status
if st.button("Check Twitch Stream Status"):
    with st.spinner("Checking Twitch stream..."):
        stream_url = get_twitch_stream_url(twitch_channel)
        if stream_url:
            st.success(f"✅ Twitch stream for '{twitch_channel}' is LIVE!")
        else:
            st.warning(f"⚠️ Twitch stream for '{twitch_channel}' is OFFLINE. Will use sample video.")

# Control Section
st.header("Stream Control")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Start Streaming", type="primary"):
        if not st.session_state.rtmp_destinations:
            st.error("Please add at least one RTMP destination before starting.")
        else:
            # Start the background process
            destinations_str = ",".join(st.session_state.rtmp_destinations)
            cmd = [
                "nohup", "python3", "background_forwarder.py", 
                twitch_channel, destinations_str, "./sample.mp4"
            ]
            
            try:
                # Start the background process
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
                st.session_state.background_process = process.pid
                st.success(f"✅ Background streaming started! PID: {process.pid}")
                st.info("The stream will continue running even if you close this app.")
            except Exception as e:
                st.error(f"Failed to start background streaming: {e}")

with col2:
    if st.button("Stop Streaming", type="secondary"):
        if st.session_state.background_process:
            try:
                # Kill the background process
                os.killpg(st.session_state.background_process, signal.SIGTERM)
                st.session_state.background_process = None
                st.success("✅ Background streaming stopped!")
            except Exception as e:
                st.error(f"Failed to stop background streaming: {e}")
        else:
            st.warning("No background streaming process found.")

with col3:
    if st.button("Check Status"):
        if st.session_state.background_process:
            try:
                # Check if the process is still running
                os.kill(st.session_state.background_process, 0)
                st.success(f"✅ Background streaming is running (PID: {st.session_state.background_process})")
            except OSError:
                st.warning("⚠️ Background streaming process is not running.")
                st.session_state.background_process = None
        else:
            st.info("No background streaming process.")

# Information Section
st.header("Information")
st.markdown("""
### How it works:
1. **Configure**: Enter your Twitch channel name and add RTMP destinations
2. **Start**: Click "Start Streaming" to begin forwarding
3. **Background**: The stream runs in the background even if you close this app
4. **Fallback**: When the Twitch stream is offline, a sample video is streamed instead

### Features:
- ✅ Real-time Twitch stream forwarding
- ✅ Multiple RTMP destinations support
- ✅ Background streaming (persistent)
- ✅ Automatic fallback to sample video when Twitch is offline
- ✅ Stream continues even when app is closed

### Notes:
- Make sure your RTMP destinations are valid and include the correct stream keys
- The background process will automatically restart if it crashes
- To completely stop all streaming, use the "Stop Streaming" button
""")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Powered by FFmpeg and Streamlink")

