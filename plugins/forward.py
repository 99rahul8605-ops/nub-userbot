
import uvloop
from pyrogram.enums import MessageEntityType
import json
import uvloop
from convopyro import Conversation
from convopyro import listen_message
import logging
from config import *
from tools import *
from pyrogram import Client

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
)

# Create a logger object
logger = logging.getLogger("userbot")
import requests
import time
import pytesseract
from moviepy.editor import VideoFileClip, AudioFileClip
from io import BytesIO
from PIL import Image

from pyrogram import enums
import shutil
import datetime
from pyrogram.raw.types import DataJSON
import asyncio
from pyrogram import Client
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.types import InputPeerChannel
from pyrogram.raw.functions.phone import GetCallConfig, JoinGroupCall
from pyrogram.raw.types import InputGroupCall
import pymongo
from pytgcalls.types import ChatUpdate
import certifi
import datetime
from pyrogram import enums
from pyrogram.errors import FloodWait
import asyncio
import random
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.types import MessageEntityTextUrl, MessageEntityMentionName
import datetime
from pytz import timezone
import yt_dlp
from pyrogram.types import Chat
import asyncio
import textwrap
import time
import math
import shlex
from typing import Tuple
from typing import Any, Dict
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from pymediainfo import MediaInfo
from pyrogram.handlers import MessageHandler
import queue
import subprocess
import certifi
import random
from random import randint
import asyncio
import time
import sys
import re
import pyrogram
from pyrogram import filters,enums
import os
import pymongo
from pyrogram import Client
from pyrogram.errors.exceptions.unauthorized_401 import SessionPasswordNeeded
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.errors.exceptions.bad_request_400 import PasswordHashInvalid
from pyrogram.errors.exceptions.bad_request_400 import PhoneCodeInvalid
from pyrogram.errors.exceptions import AuthKeyDuplicated, MessageIdInvalid
from pyrogram.errors.exceptions import AuthKeyUnregistered, PremiumAccountRequired
from pyrogram.errors.exceptions import SessionRevoked,ChatForwardsRestricted
from pyrogram.errors.exceptions import PeerFlood,UserRestricted,FileReferenceExpired
from pyrogram.errors.exceptions import UserDeactivatedBan
from pyrogram.errors.exceptions import PeerIdInvalid
from pyrogram.errors.exceptions import UserDeactivated

import imageio
import imageio_ffmpeg as ffmpeg
from PIL import Image

ggg=os.getcwd()
current_dir = f"{ggg}"

# Get the current date and time
current_time = datetime.datetime.now()
print(f"Current Date and Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

from functools import wraps

def retry(max_retries=3, initial_delay=5, backoff=2, exceptions=(FloodWait, OSError)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    wait = e.value if isinstance(e, FloodWait) else delay
                    print(f"Retry {retries}/{max_retries} for {func.__name__} after {wait}s")
                    await asyncio.sleep(wait)
                    delay *= backoff
                except Exception as e:
                    print(f"Unexpected error in {func.__name__}: {str(e)}")
                    raise
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def generate_thumbnail(video_path, thumb_path):
    reader = imageio.get_reader(video_path)
    frame = reader.get_data(0)
    image = Image.fromarray(frame)
    image.thumbnail((320, 320))
    image.save(thumb_path, format="JPEG")

import cv2

def with_opencv(filename):
    video = cv2.VideoCapture(filename)

    # Get frames per second (fps)
    fps = video.get(cv2.CAP_PROP_FPS)

    # Get total number of frames
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    # Calculate duration in seconds
    duration = frame_count / fps if fps else 0

    video.release()  # Release the video capture object
    print(int(duration))
    return int(duration)

class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

def get_file_name_from_url(url):
        response = requests.head(url, allow_redirects=True)

        # Check if the response has a Content-Disposition header
        if 'Content-Disposition' in response.headers:
            content_disposition = response.headers['Content-Disposition']
            # Extract the filename from the header
            filename = content_disposition.split('filename=')[-1].strip('"')
            return filename
        else:
            # If no Content-Disposition header, fallback to the last part of the URL
            return url.split('/')[-1]

# Example usage
async def big_file(msg,sender,zip_filename):
                import requests
                edit=0
                url = "https://api.gofile.io/getServer"

# Send an HTTP GET request and get the JSON response
                response = requests.get(url)
                data = response.json()

# Extract the server from the JSON response
                server = data["data"]["server"]
                if not server:
        # Handle the scenario where the server variable is not available
        # Move the zip file to a specific directory based on an environmental value
                 #
                   return await bot.edit_message(msg,"No storage available in gofile.io please try again later:")

    # Your existing code...


# Print the server
                file_size = os.path.getsize(zip_filename)
                print(server)


                await bot.edit_message(msg,'File size is greater than 2GB\nUploading file to gofile.io server...')

                transfer_url =f"https://{server}.gofile.io/uploadFile"
                try:
                 command=["curl","-F", f"file=@{zip_filename}", transfer_url]
                 start_time=time.time()
                 print(command)
                 output= subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True, bufsize=1,   universal_newlines=True, )
                 for line in output.stdout:
                        type_of = "Uploading\nProgress:"
                        line = line.strip()
                        if line:
                            output_text = line
                            print(line)

                            if edit % 5 == 0:
                                parts = line.split()

                                if len(parts) > 10:
                                     print(parts[1])
                                     total_size = parts[1]
                                     total =re.sub("[^0-9]", "", total_size)
                                     current_size = parts[5]
                                     current=re.sub("[^0-9]", "",current_size)

                                # Check if the parts contain valid numerical values
                                     if total.isdigit() and current.isdigit():
                                            total = int(total)
                                            current = int(current)

                                            if current != 0 and total != 0:
                                                progress_percent = current * 100 / total
                                                progress_message = f"Downloading {zip_filename}: {progress_percent:.2f}%\n\n"

                                                elapsed_time = time.time() - start_time
                                                speed = current / (elapsed_time*10)
                                                progress_message += f"Speed: {speed:.2f} MB/s\n"

                                                time_left = (total - current) / (speed*10)
                                                progress_message += f"Time left: {time_left:.2f} seconds"
                                                progress_message += f"Size: {current / (1):.2f} MB / {total / (1):.2f} MB"

                                                progress_bar_length = int(progress_percent / 5)
                                                progress_bar_text = "█" * progress_bar_length + "░" * (20 - progress_bar_length)
                                                progress_message += f"\n[{progress_bar_text}]"

                                                message_text = f"{progress_message}"

                                                try:
                                                    if random.choices([True, False], weights=[1, 99])[0]:
                                                        await bot.edit_message(msg,message_text, parse_mode='html')
                                                except Exception as e:
                                                        print(e)


                        edit+=1
                 text=line
                 start_index = text.find("https://gofile.io")
                 end_index = text.find('"', start_index)

# Extract the link
                 link = text[start_index:end_index]
                            #sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)

#print(sanitized_link)
                 try:
                                await bot.send_message(sender,f"Not able to upload files more than 500MB here\n So I provided this download link:", buttons=Button.url("Download File",link))
                 except Exception as e:
                                print(f"Error sending link: {link}, Error: {e}")
    # Clean up the user directory
                except subprocess.CalledProcessError as e:
                    print(e)
    # Clean up the user directory

# Pyrogram client setup
create_channel_filter = filters.create(
    lambda _, client, message: (
        message.chat
        and message.chat.id in getuser_data(client.me.id).get("channel", [])
    )
)

def getuser_data(user_id):
    # Simulated user data, replace with actual database call
    user_data = user_sessions.find_one({"user_id": user_id})
    if not user_data:
        gg=my_dict = {
    "name": "John",
    "age": 30,
    "city": "New York"
}
        return gg
    return user_data

@Client.on_message(create_channel_filter)
@retry()
async def forward_message_handler(client, message):
        sender = client.me.id

        session_name = f'user_{sender}'
        user_dir = f"{ggg}/{session_name}"
        os.makedirs(user_dir, exist_ok=True)
        channel_name = message.chat.title
        channel_username = f"@{message.chat.username}" if message.chat.username else ""
        if message.chat.username:
                            message_link = f"https://t.me/{message.chat.username}/{message.id}"
        else:
                          message_id_str = str(message.chat.id).replace('-100', '')
                          message_link = f"https://t.me/c/{message_id_str}/{message.id}"
        channel_details = f"<b>{channel_name}</b> {channel_username} <a href='{message_link}'>Link to message</a>"
        try:
           mess=await message.copy(app.me.username)
           await app.send_message(chat_id=sender,text=channel_details,reply_to_message_id=mess.id)
        except (ChatForwardsRestricted, FileReferenceExpired):
           if message.media:
                        timer = Timer()
                        async def progress_bar(current, total,start_time=time.time()):
                         if timer.can_send() and total != 0:  # Add a check to ensure total is not zero
                           progress_percent = current * 100 / total
                           filename=message.media.name
                           progress_message = f"{type_of} {filename}: {progress_percent:.2f}%\n"

            # Calculate progress bar length
                           progress_bar_length = 20
                           num_ticks = int(progress_percent / (100 / progress_bar_length))
                           progress_bar_text = '█' * num_ticks + '░' * (progress_bar_length - num_ticks)


          # Calculate speed in MB/s
                           elapsed_time = time.time() - start_time
                           speed = current / (elapsed_time * 1024 * 1024)
                           progress_message += f"Speed: {speed:.2f} MB/s\n"

              # C alculate estimated time left to complete
                           time_left = (total - current) / (speed * 1024 * 1024) if speed != 0 else 0  # C>
                           progress_message += f"Time left: {time_left:.2f} seconds\n"
          # Display current size and total size
                           progress_message += f"Size: {current / (1024 * 1024):.2f} MB / {total / (1024 * 1024):.2f} MB"

          # Combine progress bar and message
                           progress_message += f"\n[{progress_bar_text}]"
             # Create a message with HTML formatting for better appearance
                           message_text = f"{progress_message}"
                           try:
                              if random.choices([True, False], weights=[1, 99])[0]:
                                await bot.edit_message(msg,message_text)
                           except Exception as e:
                              print(e)
                        msg = await bot.send_message(sender, "Downloading media/document......")
                        type_of="Downloading"
                        file_path=await message.download(f"{user_dir}/" ,progress=progress_bar)
                        file_extension = file_path.split('.')[-1]
                        type_of= "Uploading"
                        channel_name = message.chat.title
                        channel_username = f"@{message.chat.username}" if message.chat.username else ""
                        if message.chat.username:
                            message_link = f"https://t.me/{message.chat.username}/{message.id}"
                        else:
                          message_id_str = str(message.chat.id).replace('-100', '')
                          message_link = f"https://t.me/c/{message_id_str}/{message.id}"
                        channel_details = f"<b>{channel_name}</b> {channel_username} <a href='{message_link}'>Link to message</a>"

                        caption = f"<br><br>{message.text if message.caption is None else message.caption}\n\n{channel_details}"

                        if os.path.getsize(file_path) <= 2100000000:
                          if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                            await app.send_photo(chat_id=sender, photo=file_path, caption=caption,progress=progress_bar)
                          elif file_extension in ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a']:
                            await app.send_audio(chat_id=sender, audio=file_path, caption=caption ,progress=progress_bar)
                          elif file_extension in ['mp4', 'mov', 'avi', 'mkv', 'webm', 'wmv']:
                            thumb_path = f"{file_path}_thumb.jpg"
                            generate_thumbnail(file_path, thumb_path)
                            duration=with_opencv(file_path)
                            await app.send_video(chat_id=sender, video=file_path, caption=caption ,progress=progress_bar,duration=duration,thumb=thumb_path)
                            os.remove(thumb_path)
                          else:
                            await app.send_document( sender, file_path, caption=caption ,progress=progress_bar)
                        else:
                         await big_file(msg,sender,file_path)
                        await msg.delete()
                        os.remove(file_path)
           else:
                 await bot.send_message(sender,message.text)
