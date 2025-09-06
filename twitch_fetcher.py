import streamlink

def get_twitch_stream_url(channel_name):
    try:
        streams = streamlink.streams(f"https://www.twitch.tv/{channel_name}")
        if streams:
            # Try to get the 'best' quality stream, or a specific quality if available
            if 'best' in streams:
                return streams['best'].url
            elif 'source' in streams:
                return streams['source'].url
            else:
                # Return the URL of the first available stream if 'best' or 'source' are not found
                return list(streams.values())[0].url
        else:
            return None
    except streamlink.exceptions.NoPluginError:
        print(f"No streamlink plugin found for Twitch.tv.")
        return None
    except streamlink.exceptions.StreamlinkException as e:
        print(f"Streamlink error: {e}")
        return None

if __name__ == "__main__":
    channel = "randomtodaytv"
    stream_url = get_twitch_stream_url(channel)
    if stream_url:
        print(f"Found stream URL for {channel}: {stream_url}")
    else:
        print(f"No live stream found for {channel}.")


