import asyncio
import os
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream.input_file import InputAudioStream
import yt_dlp

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
GROUP_CHAT = -1002763557170
YOUTUBE_URL = "https://www.youtube.com/watch?v=741La0kqlVw"
AUDIO_FILE = "audio.mp3"

app = Client("userbot", api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(app)

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': AUDIO_FILE,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def main():
    print("Starting bot...")
    download_audio(YOUTUBE_URL)

    await app.start()
    await pytgcalls.start()

    await pytgcalls.join_group_call(
        GROUP_CHAT,
        InputStream(
            InputAudioStream(AUDIO_FILE)
        ),
        stream_type='local_stream'
    )

    print("✅ Streaming started in the voice chat!")
    await asyncio.get_event_loop().create_future()

asyncio.run(main())