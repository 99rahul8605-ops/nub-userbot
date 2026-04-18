import uvloop
from pyrogram.enums import MessageEntityType
import json
import logging
from pyrogram import Client
from convopyro import Conversation
import requests
import time
from pyrogram import enums
import shutil
import datetime
from config import *
import asyncio
from pyrogram import Client
import pymongo
import datetime
from pyrogram import enums
from pyrogram.errors import FloodWait
import asyncio
import random
import re
from pyrogram import Client, filters
from pyrogram.types import Message
import datetime
from pytz import timezone
import yt_dlp
from pyrogram.types import Chat
import asyncio
import time
import sys
import re
import pyrogram
from pyrogram import filters,enums
import os
from pyrogram import Client
from pyrogram.errors.exceptions import AuthKeyDuplicated, MessageIdInvalid
from pyrogram.errors.exceptions import AuthKeyUnregistered
from pyrogram.errors.exceptions import SessionRevoked,ChatForwardsRestricted
from pyrogram.errors.exceptions import PeerFlood,UserRestricted,FileReferenceExpired
from pyrogram.errors.exceptions import UserDeactivatedBan
from pyrogram.errors.exceptions import PeerIdInvalid
from pyrogram.errors.exceptions import UserDeactivated
from pyrogram.enums import ChatType, UserStatus
from pyrogram import __version__ as versipyro
import imageio
import imageio_ffmpeg as ffmpeg
from PIL import Image

# Telethon imports removed - using Pyrogram only
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
)

logger = logging.getLogger("userbot")

ggg = os.getcwd()
StartTime = time.time()

print("Starting Userbot...")

async def main():
    # Get session string from environment or user input
    session_string = SESSION_STR if SESSION_STR else input("Enter your Pyrogram session string: ")

    # Initialize bot client with bot-specific plugins only
    app = Client(
        "main_bot", 
        api_id=API_ID, 
        api_hash=API_HASH, 
        bot_token=BOT_TOKEN, 
        in_memory=True,
        sleep_threshold=30,
        plugins=dict(
            root="plugins",
            include=["inline", "sg"]  # Bot-specific plugins for inline queries and special group features
        )
    )
    apps["app"] = app
    
    # Initialize conversation for the bot
    Conversation(app)

    # Initialize userbot client with userbot-specific plugins
    userbot = Client(
        "userbot_session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
        plugins=dict(
            root="plugins",
            include=[
                "account",      # Profile management, clone/revert
                "afk",          # AFK system with mentions
                "ai",           # AI chat and commands
                "antyspam",     # Spam control and protection
                "clone",        # Profile cloning functionality
                "eval",         # Code evaluation
                "font",         # Text formatting styles
                "forward",      # Message forwarding automation
                "gcast",        # Global broadcast messaging
                "game_solver",  # Game solving functionality
                "group_tools",  # Group management tools
                "info",         # User and chat information
                "music",        # Music related commands
                "ocr",          # Optical character recognition
                "purge",        # Message deletion and purging
                "react",        # Reaction handling
                "schedule",     # Scheduled message sending
                "spam",         # Spam commands
                "status",       # Status and alive commands
                "stickers",     # Sticker management and creation
                "sudo",         # Sudo commands
                "userbot",      # Core userbot functionality
                "vctools",      # Voice chat tools
                "welcome",      # Welcome messages
                "wordchain",    # Word chain game
                "wordgrider",   # Word grider game
                "wordseek_auto" # Word seek automation
            ]
        )
    )
    
    # Initialize conversation for userbot
    Conversation(userbot)

    try:
        # Start bot client if token is provided
        if BOT_TOKEN:
            await app.start()
            bot_me = await app.get_me()
            print(f"Bot started successfully!")
            print(f"Bot logged in as: {bot_me.first_name} (@{bot_me.username})")
        
        # Start userbot client
        await userbot.start()
        me = await userbot.get_me()
        print(f"Userbot started successfully!")
        print(f"Userbot logged in as: {me.first_name} (@{me.username})")

        # Add to clients dict for compatibility
        clients[me.id] = userbot

        # Keep both clients running
        await userbot.idle()

    except Exception as e:
        print(f"Error starting clients: {e}")
    finally:
        if BOT_TOKEN:
            await app.stop()
        await userbot.stop()

if __name__ == "__main__":
    asyncio.run(main())