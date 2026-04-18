# Standard library imports
import asyncio
import ast
import base64
import certifi
import contextlib
import cv2
import datetime
import html
import imageio
import imageio_ffmpeg as ffmpeg
import inspect
import json
import logging
import magic
import math
import os
import pymongo
import pytesseract
import queue
import random
import re
import requests
import shlex
import shutil
import speedtest
import subprocess
import sys
import textwrap
import time
import traceback
import uvloop
import yt_dlp
from functools import wraps
from io import BytesIO, StringIO
from platform import python_version
from random import choice, randint
from typing import Any, Dict, List, Optional, Tuple, Union

# Third-party imports
import aiohttp
from google import genai
import pytz
from bson.objectid import ObjectId
from moviepy.editor import VideoFileClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
from pymediainfo import MediaInfo
from pymongo import MongoClient
from pytz import timezone

# Pyrogram imports
import pyrogram
from pyrogram import Client, filters, enums, idle, __version__ as versipyro
from pyrogram.enums import ChatAction as CA, ChatMembersFilter, ChatMemberStatus, ChatType, MessageEntityType, MessageEntityType as MET, ParseMode, UserStatus
from pyrogram.errors import (
    ChatAdminRequired, FloodWait, RPCError, StickersetInvalid, UserAdminInvalid, 
    UserNotParticipant, UserRestricted, YouBlockedUser
)
from pyrogram.errors.exceptions import (
    AuthKeyDuplicated, AuthKeyUnregistered, ChatForwardsRestricted, FileReferenceExpired,
    MessageIdInvalid, PeerFlood, PeerIdInvalid, PremiumAccountRequired, SessionRevoked,
    UserDeactivated, UserDeactivatedBan
)
from pyrogram.errors.exceptions.bad_request_400 import PasswordHashInvalid, PhoneCodeInvalid
from pyrogram.errors.exceptions.unauthorized_401 import SessionPasswordNeeded
from pyrogram.handlers import DisconnectHandler, MessageHandler
from pyrogram.raw import functions
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.contacts import GetBlocked
from pyrogram.raw.functions.messages import GetFullChat, GetStickerSet
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall, GetCallConfig, JoinGroupCall, InviteToGroupCall
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.raw.types import (
    DataJSON, InputGroupCall, InputPeerChannel, InputPeerChat, MessageEntityMentionName,
    MessageEntityTextUrl, InputStickerSetShortName
)
from pyrogram.types import (
    CallbackQuery, Chat, ChatPermissions, InlineKeyboardButton,
    InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Message
)

# Compatibility: ChatPrivileges not available in Pyrogram 2.2.13
try:
    from pyrogram.types import ChatPrivileges
except ImportError:
    ChatPrivileges = ChatPermissions

# Telethon removed - using Pyrogram only

# PyTgCalls imports
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import ChatUpdate, Device, ExternalMedia

# Local imports
from convopyro import Conversation, listen_message
from parser import mention_html, mention_markdown
from tools import *
from utils.message import Msg
from youtube import handle_youtube, get_video_details, extract_video_id, format_number, format_duration, time_to_seconds
# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
)

# Create a logger object
logger = logging.getLogger("userbot")
current_dir = f"{ggg}"

# Get the current date and time
current_time = datetime.datetime.now()
logger.info(f"[USERBOT] Plugin loaded at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Iterate over all sub-directories







# Stubs: premium/payment checks removed - all users allowed
def premium_only():
    def decorator(func):
        from functools import wraps
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def paid_only():
    def decorator(func):
        from functools import wraps
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def paid_not_private():
    def decorator(func):
        from functools import wraps
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator



# Paid-only decorator





# Store user's phone number
# Define client outside of any function scope

response_lock = asyncio.Lock()
IGNORE_DURATION = 5
# Define the /play command handler

# Run the bot


async def get_youtube_duration(youtube_link):
    ydl_opts = {
        'quiet': True, 
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_link, download=False)
            duration = info.get('duration')  # Get duration in seconds 
            return duration
        except Exception as e:
            logger.error(f"[USERBOT] YouTube duration error: {e}")
            return None  # Or handle the error appropriately

# Helper function to split users into chunks


# Invite users to voice chat directly with the command handler

# Pyrogram client setup
create_channel_filter = filters.create(
    lambda _, client, message: (
        message.chat
        and message.chat.id in getuser_data(client.me.id).get("channel", [])
    )
)


create_raid_filter = filters.create(
    lambda _, client, message: (
        message.from_user
        and message.from_user.id in getuser_data(client.me.id).get('raid_users', [])))

      
create_custom_filter = filters.create(lambda _, __, message: re.match(getuser_data(message.from_user.id).get("save_com", "^(Wow|wow)$"), message.text) if message.from_user else False)


@Client.on_message(filters.me & filters.text & create_custom_filter)
@paid_not_private()
async def handle_message(client, message):
    sender = message.from_user.id
    session_name = f'user_{sender}'
    user_dir = f"{ggg}/{session_name}"
    os.makedirs(user_dir, exist_ok=True)
    
    if message.reply_to_message:
        # Get the replied-to message
        try:
            message = message.reply_to_message
            if str(message.chat.type).endswith("PRIVATE"):
                chat_details = f"<b>{message.from_user.first_name} {message.from_user.last_name or ''}</b> @{message.chat.username or ''}"
            else:
                chat_title = message.chat.title
                chat_username = f"@{message.chat.username}" if message.chat.username else ""
                if message.chat.username:
                    message_link = f"https://t.me/{message.chat.username}/{message.id}"
                else:
                    message_id_str = str(message.chat.id).replace('-100', '')
                    message_link = f"https://t.me/c/{message_id_str}/{message.id}"
                chat_details = f"<b>{chat_title}</b> {chat_username} <a href='{message_link}'>Link to message</a>"
            
            try:
                message = await message.copy(app.me.username)
                await asyncio.sleep(2)
                
                # Build detailed info about saved message
                from_user = message.from_user
                chat = message.chat
                
                details = f"📥 **Media Saved**\n\n"
                details += f"👤 **From:** {from_user.first_name}"
                if from_user.last_name:
                    details += f" {from_user.last_name}"
                if from_user.username:
                    details += f" (@{from_user.username})"
                details += f"\n🆔 **User ID:** `{from_user.id}`\n"
                
                if str(chat.type).endswith("PRIVATE"):
                    details += f"💬 **Chat:** Private Chat\n"
                else:
                    details += f"💬 **Chat:** {chat.title or 'Unknown'}\n"
                    if chat.username:
                        details += f"🔗 **Username:** @{chat.username}\n"
                
                details += f"🆔 **Chat ID:** `{chat.id}`\n"
                details += f"#️⃣ **Message ID:** `{message.id}`\n"
                
                if message.date:
                    details += f"📅 **Date:** {message.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                if not str(chat.type).endswith("PRIVATE") and chat.username:
                    message_link = f"https://t.me/{chat.username}/{message.id}"
                    details += f"🔗 **Link:** {message_link}\n"
                
                await app.send_message(
                    chat_id=sender,
                    text=details,
                    reply_to_message_id=message.id
                )
            except (ChatForwardsRestricted, FileReferenceExpired):
                if message.media:
                    timer = Timer()
                    async def progress_bar(current, total, start_time=time.time()):
                        if timer.can_send() and total != 0:
                            progress_percent = current * 100 / total
                            filename = getattr(message.media, 'name', 'media')
                            progress_bar_length = 20
                            num_ticks = int(progress_percent / (100 / progress_bar_length))
                            progress_bar_text = '█' * num_ticks + '░' * (progress_bar_length - num_ticks)
                            elapsed_time = time.time() - start_time
                            speed = current / (elapsed_time * 1024 * 1024)
                            time_left = (total - current) / (speed * 1024 * 1024) if speed != 0 else 0
                            progress_message = (
                                f"{type_of} {filename}: {progress_percent:.2f}%\n"
                                f"Speed: {speed:.2f} MB/s\n"
                                f"Time left: {time_left:.2f} seconds\n"
                                f"Size: {current / (1024 * 1024):.2f} MB / {total / (1024 * 1024):.2f} MB\n"
                                f"[{progress_bar_text}]"
                            )
                            try:
                                if random.choices([True, False], weights=[1, 99])[0]:
                                    await bot.edit_message(msg, progress_message)
                            except Exception as e:
                                logger.exception(f"Progress bar update error: {e}")
                    
                    msg = await bot.send_message(sender, f"╭── 📥 DOWNLOADING ──╮\n┃ ⏳ Please wait...\n╰━━━━━━━━━━━━━━━━━━━━╯")
                    type_of = "Downloading"
                    file_path = await message.download(f"{user_dir}/", progress=progress_bar)
                    file_extension = file_path.split('.')[-1]
                    type_of = "Uploading"
                    
                    # Build detailed caption with message info
                    from_user = message.from_user
                    chat = message.chat
                    
                    caption = f"📥 **Media Saved**\n\n"
                    caption += f"👤 **From:** {from_user.first_name}"
                    if from_user.last_name:
                        caption += f" {from_user.last_name}"
                    if from_user.username:
                        caption += f" (@{from_user.username})"
                    caption += f"\n🆔 **User ID:** `{from_user.id}`\n"
                    
                    if str(chat.type).endswith("PRIVATE"):
                        caption += f"💬 **Chat:** Private Chat\n"
                    else:
                        caption += f"💬 **Chat:** {chat.title or 'Unknown'}\n"
                        if chat.username:
                            caption += f"🔗 **Username:** @{chat.username}\n"
                    
                    caption += f"🆔 **Chat ID:** `{chat.id}`\n"
                    caption += f"#️⃣ **Message ID:** `{message.id}`\n"
                    
                    if message.date:
                        caption += f"📅 **Date:** {message.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    
                    if not str(chat.type).endswith("PRIVATE") and chat.username:
                        message_link = f"https://t.me/{chat.username}/{message.id}"
                        caption += f"🔗 **Link:** {message_link}\n"
                    
                    # Add original caption/text if exists
                    original_text = message.text if message.caption is None else message.caption
                    if original_text:
                        caption += f"\n📝 **Caption:** {original_text}\n"
                    
                    if os.path.getsize(file_path) <= 2000000000:
                        if file_extension.lower() in ['jpg', 'jpeg', 'png', 'gif']:
                            await app.send_photo(chat_id=sender, photo=file_path, caption=caption, progress=progress_bar)
                        elif file_extension.lower() in ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a']:
                            await app.send_audio(chat_id=sender, audio=file_path, caption=caption, progress=progress_bar)
                        elif file_extension.lower() in ['mp4', 'mov', 'avi', 'mkv', 'webm', 'wmv']:
                            thumb_path = f"{file_path}_thumb.jpg"
                            generate_thumbnail(file_path, thumb_path)
                            duration = with_opencv(file_path)
                            await app.send_video(chat_id=sender, video=file_path, caption=caption, progress=progress_bar, duration=duration, thumb=thumb_path)
                            os.remove(thumb_path)
                        else:
                            await app.send_document(sender, file_path, caption=caption, progress=progress_bar)
                    else:
                        await bot.edit_message(msg, Msg.ERR_FILE_TOO_LARGE)
                    await msg.delete()
                    os.remove(file_path)
                else:
                    # Text message - send with details
                    from_user = message.from_user
                    chat = message.chat
                    
                    details = f"📥 **Message Saved**\n\n"
                    details += f"👤 **From:** {from_user.first_name}"
                    if from_user.last_name:
                        details += f" {from_user.last_name}"
                    if from_user.username:
                        details += f" (@{from_user.username})"
                    details += f"\n🆔 **User ID:** `{from_user.id}`\n"
                    
                    if str(chat.type).endswith("PRIVATE"):
                        details += f"💬 **Chat:** Private Chat\n"
                    else:
                        details += f"💬 **Chat:** {chat.title or 'Unknown'}\n"
                        if chat.username:
                            details += f"🔗 **Username:** @{chat.username}\n"
                    
                    details += f"🆔 **Chat ID:** `{chat.id}`\n"
                    details += f"#️⃣ **Message ID:** `{message.id}`\n"
                    
                    if message.date:
                        details += f"📅 **Date:** {message.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    
                    if not str(chat.type).endswith("PRIVATE") and chat.username:
                        message_link = f"https://t.me/{chat.username}/{message.id}"
                        details += f"🔗 **Link:** {message_link}\n"
                    
                    details += f"\n📝 **Text:**\n{message.text}"
                    
                    await bot.send_message(sender, details)
        except Exception as e:
            await bot.send_message(sender, styled_error(f"Error: {e}"))

PASS=False








# Define a filter to handle outgoing messages containing the command "^info"
info_filter = filters.outgoing & filters.command("info", prefixes=HARDCODED_PREFIXES)




me_filter = (filters.me | sudoers_filter()) & filters.command("qt", prefixes=HARDCODED_PREFIXES)
@Client.on_message(me_filter)
@premium_only()
async def duck_command_handler(client, message):
    """Enhanced quote command handler with better error handling and features"""
    USERBOT = await edit_or_reply(message, f"╭── 📝 QUOTE ──╮\n┃ ⏳ Generating quote...\n╰━━━━━━━━━━━━━━━━━━━━╯")

    # Check if the message is a reply
    if not message.reply_to_message:
        await USERBOT.edit_text(Msg.ERR_REPLY_TO_QUOTE)
        await asyncio.sleep(3)
        await USERBOT.delete()
        return

    try:
        sender = message.from_user.id
        replied_message = message.reply_to_message
        user = replied_message.from_user

        # Admin check
        if is_admin_user(user.id):
            return await USERBOT.edit_text(
                "You are fucking requesting me to create fake quote of my lord and my creator.\nSo I won't...**Fuck off!!**"
            )

        # Setup directories
        session_name = f'user_{sender}'
        user_dir = f"{ggg}/{session_name}"
        os.makedirs(user_dir, exist_ok=True)

        # Parse command text and check for flags
        HARDCODED_PREFIXES = ["!", "_", "?", "^", "."]
        escaped_prefixes = '|'.join(re.escape(p) for p in HARDCODED_PREFIXES)
        cmd_match = re.search(rf"^({escaped_prefixes})\w+", message.text or "")
        words_to_remove = []
        if cmd_match:
            words_to_remove.append(cmd_match.group(0))

        include_reply = False
        force_custom = False

        raw_text = message.text or ""

        # Check for -r flag (include reply)
        if "-r" in raw_text:
            include_reply = True
            words_to_remove.append("-r")

        # Check for -f flag (force custom text)
        if "-f" in raw_text:
            force_custom = True
            words_to_remove.append("-f")

        # Extract command specific entities if needed
        command_text, custom_entities = update_message_and_entities(
            text=raw_text,
            entities=message.entities or [],
            words_to_remove=words_to_remove
        )

        # Determine quote text based on flags and available text
        if force_custom and command_text:
            # Use custom text when -f flag is present and text is provided
            quote_text = command_text
        else:
            # Default: always use original message content (when no -f flag or no custom text)
            quote_text = await get_message_content(replied_message)

        # If no text content but message has media, use a placeholder
        if not quote_text and await has_media(replied_message):
            quote_text = " "  # Use space as placeholder for media-only messages

        if not quote_text:
            await USERBOT.edit_text(Msg.ERR_NO_TEXT_TO_QUOTE)
            await asyncio.sleep(3)
            await USERBOT.delete()
            return

        # Step 1: Collect all information first
        
        # Collect user information
        user_info = await build_user_info(client, user)
        
        # Collect entities
        entities = []
        if force_custom and command_text:
            entities = await convert_entities(custom_entities)
        else:
            source_entities = replied_message.entities or replied_message.caption_entities
            if source_entities:
                quote_text, processed_entities = update_message_and_entities(
                    text=quote_text,
                    entities=source_entities
                )
                entities = await convert_entities(processed_entities)
        
        # Collect media information (only if not using custom text with -f flag)
        media_info = None
        if not (force_custom and command_text):
            media_info = await get_media_info(client, replied_message)
        
        # Collect reply information (only if -r flag is present and reply exists)
        reply_info = None
        if include_reply and replied_message.reply_to_message:
            reply_info = await build_reply_info(client, replied_message.reply_to_message)
        
        # Step 2: Validate all collected information
        if not user_info or "id" not in user_info:
            await USERBOT.edit_text(Msg.ERR_GET_USER_INFO_FAILED)
            await asyncio.sleep(3)
            await USERBOT.delete()
            return
        
        # Step 3: Build the complete payload after all information is collected
        
        # Create the main message object
        message_obj = {
            "from": user_info,
            "text": quote_text[:4096],  # Limit text length as per API docs
            "entities": entities,
            "avatar": True
        }
        
        # Add media if available
        if media_info:
            message_obj["media"] = media_info
        
        # Add reply if available
        if reply_info:
            message_obj["replyMessage"] = reply_info
        
        # Create the final payload
        quote_payload = {
            "type": "quote",
            "format": "webp",
            "backgroundColor": "#1b1429",
            "width": 512,
            "height": 768,
            "scale": 2,
            "emojiBrand": "apple",
            "botToken": BOT_TOKEN,  # Required for custom_emoji resolution via Telegram API
            "messages": [message_obj]
        }
        
        

        quote_path = await generate_quote(client, quote_payload, user_dir)

        if not quote_path:
            await USERBOT.edit_text(Msg.ERR_GENERATE_QUOTE_FAILED)
            await asyncio.sleep(3)
            await USERBOT.delete()
            return

    except Exception as e:
        error_msg = f"Quote generation preparation error: {str(e)}"
        logger.error(error_msg)
        try:
            await bot.send_message(client.me.id, f"ERROR in quote handler: {error_msg}")
            await USERBOT.edit_text(Msg.ERR_QUOTE_FAILED)
            await asyncio.sleep(3)
            await USERBOT.delete()
        except:
            pass  # If even error handling fails, just continue
        return

    max_retries = 2
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Send the sticker
            await client.send_sticker(
                chat_id=app.me.id,
                sticker=quote_path
            )
            await client.send_sticker(
                chat_id=message.chat.id,
                sticker=quote_path,
                reply_to_message_id=replied_message.id
            )
            await USERBOT.delete()
            return  # Success, exit the retry loop

        except PeerIdInvalid as e:
            retry_count += 1
            error_msg = f"PEER_ID_INVALID error (attempt {retry_count}/{max_retries}): {str(e)}"
            logger.warning(error_msg)
            
            if retry_count < max_retries:
                # Wait before retrying (exponential backoff)
                wait_time = 2 ** retry_count
                await USERBOT.edit_text(f"⚠️ Warning\n╰▸ Retrying... ({retry_count}/{max_retries})")
                await asyncio.sleep(wait_time)
            else:
                # Max retries reached
                try:
                    await bot.send_message(client.me.id, f"ERROR in quote handler after {max_retries} retries: {error_msg}")
                    await USERBOT.edit_text(Msg.ERR_QUOTE_RETRIES_FAILED)
                    await asyncio.sleep(3)
                    await USERBOT.delete()
                except:
                    pass
                return

        except Exception as e:
            error_msg = f"Quote send error: {str(e)}"
            logger.error(error_msg)
            try:
                await bot.send_message(client.me.id, f"ERROR in quote handler: {error_msg}")
                await USERBOT.edit_text(Msg.ERR_QUOTE_FAILED)
                await asyncio.sleep(3)
                await USERBOT.delete()
            except:
                pass  # If even error handling fails, just continue
            return  # Exit on non-PEER_ID_INVALID errors


async def build_user_info(client, user) -> Optional[Dict[str, Any]]:
    """Build user information according to API spec with comprehensive error handling"""
    try:
        if not user:
            logger.debug("No user object provided")
            return None
            
        user_info = {
            "id": user.id
        }
        
        # Handle name - use name field or first_name/last_name
        try:
            if user.first_name and user.last_name:
                user_info["first_name"] = user.first_name
                user_info["last_name"] = user.last_name
            elif user.first_name:
                user_info["first_name"] = user.first_name
            elif user.username:
                user_info["username"] = user.username
                user_info["name"] = f"@{user.username}"
            else:
                user_info["name"] = "Unknown User"
        except Exception as e:
            logger.warning(f"Error processing username info: {e}")
            user_info["name"] = "Unknown User"
        
        # Handle profile photo
        try:
            if hasattr(user, 'photo') and user.photo:
                if hasattr(user.photo, 'big_file_id') and user.photo.big_file_id:
                    user_info["photo"] = {"big_file_id": user.photo.big_file_id}
                elif hasattr(user.photo, 'small_file_id') and user.photo.small_file_id:
                    user_info["photo"] = {"big_file_id": user.photo.small_file_id}
        except Exception as e:
            logger.warning(f"Error getting user photo: {e}")
        
        # Handle emoji status
        try:
            if hasattr(user, 'emoji_status') and user.emoji_status:
                if hasattr(user.emoji_status, 'custom_emoji_id') and user.emoji_status.custom_emoji_id:
                    user_info["emoji_status"] = str(user.emoji_status.custom_emoji_id)
        except Exception as e:
            logger.warning(f"Error getting emoji status: {e}")
        
        return user_info
        
    except Exception as e:
        logger.error(f"Critical error in build_user_info: {e}")
        return None



def upload_file_data_binary_to_bashupload(file_path, file_name=None):
    """
    Uploads a file to bashupload.com using the --data-binary method and returns the download URL.

    Args:
        file_path (str): The path to the file to upload.
        file_name (str, optional): The desired name for the file on bashupload.com. 
                                   If None, the original file name will be used.

    Returns:
        str: The download URL of the uploaded file, or None if the upload fails.
    """
    if not os.path.exists(file_path):
        return None

    if file_name is None:
        file_name = os.path.basename(file_path)

    url = f'https://bashupload.com/{file_name}'
    
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(url, data=f)
        
        if response.status_code == 200:
            match = re.search(r'wget (https://bashupload.com/[^\s]+)', response.text)
            if match:
                return match.group(1)
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred during bashupload: {e}")
        return None


async def get_media_info(client, message) -> Optional[Dict[str, Any]]:
    logger.debug(f"[DEBUG] get_media_info called with message: {message}")
    """Extract media information for quote-api according to API spec with validation"""
    
    # Initial validation
    if not message:
        logger.debug("[DEBUG] No message provided")
        return None
        
    if not hasattr(message, 'media'):
        logger.debug("[DEBUG] Message has no media attribute")
        return None
    
    logger.debug(f"[DEBUG] Message has media attribute: {message.media}")

    # Get media type from message.media.value
    media_type = message.media.value if hasattr(message.media, 'value') else None
    logger.debug(f"[DEBUG] Raw media_type: {media_type}")

    if not media_type:
        logger.debug("[DEBUG] No media_type found")
        return None

    # Convert media type to attribute name (remove "MessageMediaType." prefix if present)
    if media_type.startswith('MessageMediaType.'):
        media_attr = media_type.replace('MessageMediaType.', '').lower()
        logger.debug(f"[DEBUG] Converted media_attr from MessageMediaType: {media_attr}")
    else:
        media_attr = media_type.lower()
        logger.debug(f"[DEBUG] Converted media_attr (no prefix): {media_attr}")

    # Get the media object using getattr
    media_obj = getattr(message, media_attr, None)
    logger.debug(f"[DEBUG] Media object retrieved: {media_obj}")

    if not media_obj:
        logger.debug(f"[DEBUG] No media object found for type: {media_attr}")
        return None

    # Get thumbnail file_id using the simplified approach
    logger.debug(f"[DEBUG] Attempting to get thumbnail from media_attr: {media_attr}")
    try:
        media_attribute = getattr(message, media_attr)
        logger.debug(f"[DEBUG] Media attribute object: {media_attribute}")
        
        thumbs = getattr(media_attribute, 'thumbs', None)
        logger.debug(f"[DEBUG] Thumbs attribute: {thumbs}")
        
        if thumbs and len(thumbs) > 0:
            thumbnail_file_id = thumbs[0].file_id
            logger.debug(f"[DEBUG] Thumbnail file_id found: {thumbnail_file_id}")
        else:
            logger.debug(f"[DEBUG] No thumbs found or thumbs is empty")
            return None
            
    except (AttributeError, IndexError, TypeError) as e:
        logger.debug(f"[DEBUG] Exception getting thumbnail for media type {media_attr}: {e}")
        return None

    # Download the thumbnail
    temp_file_path = None
    try:
        logger.debug(f"[DEBUG] Starting thumbnail download process")
        
        # Create user-specific directory
        session_name = f'user_{client.me.id}'
        user_dir = f"{ggg}/{session_name}"
        logger.debug(f"[DEBUG] User directory: {user_dir}")
        
        os.makedirs(user_dir, exist_ok=True)
        logger.debug(f"[DEBUG] User directory created/verified")

        # Create temporary file in user directory
        logger.debug(f"[DEBUG] Downloading media with file_id: {thumbnail_file_id}")
        temp_file_path = await client.download_media(message=thumbnail_file_id, file_name=f"{user_dir}/")
        logger.debug(f"[DEBUG] Media downloaded to: {temp_file_path}")

        # Upload to bashupload
        logger.debug(f"[DEBUG] Uploading file to bashupload: {temp_file_path}")
        upload_url = upload_file_to_bashupload(temp_file_path)
        logger.debug(f"[DEBUG] Upload result: {upload_url}")

        if upload_url:
            logger.debug(f"[DEBUG] Media thumbnail uploaded successfully: {upload_url}")
            return {"url": upload_url}
        else:
            logger.debug("[DEBUG] Failed to upload thumbnail to bashupload")
            return None

    except Exception as e:
        logger.debug(f"[DEBUG] Exception during download/upload process: {e}")
        return None
        
    finally:
        # Clean up temporary file
        logger.debug(f"[DEBUG] Cleanup phase - temp_file_path: {temp_file_path}")
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.debug(f"[DEBUG] Temporary file deleted successfully: {temp_file_path}")
            except OSError as e:
                logger.debug(f"[DEBUG] Error deleting temporary file: {e}")
        else:
            logger.debug(f"[DEBUG] No temporary file to delete or file doesn't exist")

    logger.debug("[DEBUG] Function completed, returning None")
    return None


async def has_media(message):
    """Check if message contains any media content"""
    return any([
        message.sticker,
        message.photo,
        message.video,
        message.audio,
        message.voice,
        message.document,
        message.animation,
        message.video_note
    ])


async def get_message_content(message):
    """Extract content from any message type according to quote-api standards"""
    # For text messages, return the text directly
    if message.text:
        return message.text

    # For media with captions, return the caption
    if message.caption:
        return message.caption

    # For stickers, return empty string so the sticker media gets processed
    if message.sticker:
        return ""

    # For other media types without captions, return empty string
    # The media will be handled by the media processing function
    if any([message.photo, message.video, message.audio, message.voice,
            message.document, message.animation, message.video_note]):
        return ""

    # For contact messages, return contact info
    if message.contact:
        return f"{message.contact.first_name} {message.contact.last_name or ''}".strip()

    # For location messages, return coordinates or venue info
    if message.location:
        return f"📍 Location"

    if message.venue:
        return message.venue.title

    # For polls, return the question
    if message.poll:
        return message.poll.question

    # For dice/darts, return the emoji
    if message.dice:
        return message.dice.emoji

    # For games, return the title
    if message.game:
        return message.game.title

    # For service messages or unknown types, return empty string
    return ""


async def build_reply_info(client, reply_message) -> Optional[Dict[str, Any]]:
    """Build reply message information according to API spec with validation"""
    try:
        if not reply_message:
            logger.debug("No reply message provided")
            return None
            
        if not hasattr(reply_message, 'from_user') or not reply_message.from_user:
            logger.debug("Reply message has no from_user")
            return None

        reply_user = reply_message.from_user
        
        # Get reply text content
        reply_text = ""
        try:
            reply_text = reply_message.text or reply_message.caption or "Media"
        except Exception as e:
            logger.warning(f"Error getting reply text: {e}")
            reply_text = "Media"

        # Get reply entities
        reply_entities = []
        try:
            if hasattr(reply_message, 'entities') and reply_message.entities:
                reply_entities = await convert_entities(reply_message.entities)
        except Exception as e:
            logger.warning(f"Error getting reply entities: {e}")

        # Build reply user info
        reply_user_info = await build_user_info(client, reply_user)
        if not reply_user_info:
            logger.warning("Failed to build reply user info")
            return None

        reply_info = {
            "name": reply_user_info.get("name") or reply_user_info.get("first_name", "Unknown"),
            "text": reply_text[:100],  # Limit reply text length
            "entities": reply_entities,
            "chatId": getattr(reply_message.chat, 'id', 0),
            "from": reply_user_info
        }

        logger.debug(f"Reply info collected: {reply_info}")
        return reply_info

    except Exception as e:
        logger.error(f"Error building reply info: {e}")
        return None


async def convert_entities(entities) -> List[Dict[str, Any]]:
    """Convert Pyrogram entities to quote API format"""
    converted = []

    # Mapping of Pyrogram entity types to quote API types
    entity_type_mapping = {
        # Legacy mappings
        'MessageEntityBold': 'bold',
        'MessageEntityItalic': 'italic',
        'MessageEntityCode': 'code',
        'MessageEntityPre': 'pre',
        'MessageEntityTextUrl': 'text_link',
        'MessageEntityUrl': 'url',
        'MessageEntityMention': 'mention',
        'MessageEntityHashtag': 'hashtag',
        'MessageEntityBotCommand': 'bot_command',
        'MessageEntityStrike': 'strikethrough',
        'MessageEntityUnderline': 'underline',
        'MessageEntityCustomEmoji': 'custom_emoji',
        'MessageEntitySpoiler': 'spoiler',
        'MessageEntityCashtag': 'cashtag',
        'MessageEntityPhone': 'phone_number',
        'MessageEntityEmail': 'email',
        
        # Pyrogram v2 Enums
        'BOLD': 'bold',
        'ITALIC': 'italic',
        'CODE': 'code',
        'PRE': 'pre',
        'TEXT_LINK': 'text_link',
        'URL': 'url',
        'MENTION': 'mention',
        'HASHTAG': 'hashtag',
        'BOT_COMMAND': 'bot_command',
        'STRIKETHROUGH': 'strikethrough',
        'UNDERLINE': 'underline',
        'CUSTOM_EMOJI': 'custom_emoji',
        'SPOILER': 'spoiler',
        'CASHTAG': 'cashtag',
        'PHONE_NUMBER': 'phone_number',
        'EMAIL': 'email',
        'BLOCKQUOTE': 'blockquote',
        'TEXT_MENTION': 'text_mention'
    }

    try:
        for entity in entities:
            # Get entity type name — use enum's .name attr (e.g. CUSTOM_EMOJI) like main.py
            entity_type_name = ""
            if hasattr(entity, 'type'):
                if hasattr(entity.type, 'name'):
                    entity_type_name = entity.type.name
                elif hasattr(entity.type, '__name__'):
                    entity_type_name = entity.type.__name__
                else:
                    entity_type_name = str(entity.type).split('.')[-1].replace('>', '')

            # Map to quote API type
            api_type = entity_type_mapping.get(entity_type_name, 'text')

            entity_dict = {
                "type": api_type,
                "offset": entity.offset,
                "length": entity.length
            }

            # Add additional fields based on entity type
            if hasattr(entity, 'url') and entity.url:
                entity_dict["url"] = entity.url
            if hasattr(entity, 'custom_emoji_id') and entity.custom_emoji_id:
                entity_dict["custom_emoji_id"] = str(entity.custom_emoji_id)  # API requires string
            if hasattr(entity, 'language') and entity.language:
                entity_dict["language"] = entity.language

            converted.append(entity_dict)

    except Exception as e:
        logger.error(f"Error converting entities: {e}")

    return converted


async def generate_quote(client, payload: Dict[str, Any], user_dir: str) -> Optional[str]:
    """Generate quote using the API with proper error handling and fallback"""
    
    # List of endpoints to try in order
    endpoints = [
        'https://bot.lyo.su/quote/generate',
        'https://quote.nubcoder.com/generate',
        'http://quote-api:3000/generate',
        'http://127.0.0.1:3000/generate'
    ]
    
    for i, endpoint in enumerate(endpoints, 1):
        try:
            logger.debug(f"Attempting quote generation with endpoint {i}: {endpoint}")
            response = requests.post(endpoint, json=payload).json()
            buffer = base64.b64decode(response['result']['image'].encode('utf-8'))
            quote_path = f'{user_dir}/Quotly.webp'
            open(quote_path, 'wb').write(buffer)
            logger.info(f"Quote generated successfully using endpoint {i}")
            return quote_path
        except Exception as e:
            logger.warning(f"Quote generation error with endpoint {i} ({endpoint}): {e}")
            if i == len(endpoints):
                logger.error("All endpoints failed")
                return None
            else:
                logger.debug("Trying next endpoint...")
                continue
    
    return None


class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False









def get_args_from_caret(message):
    """Extract arguments from prefixed commands (supports all HARDCODED_PREFIXES)"""
    if not message.text:
        return []
    
    # Check if message starts with any hardcoded prefix
    first_char = message.text[0]
    if first_char not in HARDCODED_PREFIXES:
        return []
    
    # Remove the prefix and split into command and args
    text = message.text[1:]  # Remove prefix
    parts = text.split()
    
    if len(parts) <= 1:
        return []
    
    return parts[1:]  # Return everything after the command

def get_command_from_caret(message):
    """Extract command name from prefixed commands and log it (supports all HARDCODED_PREFIXES).
    Returns empty string when message has no recognized prefix.
    """
    if not message.text:
        return ""
    
    # Check if message starts with any hardcoded prefix
    first_char = message.text[0]
    if first_char not in HARDCODED_PREFIXES:
        return ""

    text = message.text[1:]  # Remove prefix
    parts = text.split()

    if not parts:
        return ""

    command = parts[0]

    # Lightweight logging for debugging
    try:
        # Logger preferred (shows up in Docker logs)
        logger.info(f"[command] prefix='{first_char}' command='{command}' text='{message.text[:120]}'")
    except Exception:
        pass
    # Also print once for local visibility
    # Optional debug output (already logged above); retained behind logger only
    try:
        logger.debug(f"[get_command_from_caret] text='{message.text}' -> command='{command}'")
    except Exception:
        pass

    return command  # Return the command name

















# ═══════════════════════════════════════
#  .help <command> — Styled Help Handler
# ═══════════════════════════════════════

def _parse_help_entry(raw_text):
    """Parse a raw help entry into structured fields."""
    desc = usage = example = note = warning = flags = ""
    lines = raw_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        ll = line.lower()
        if ll.startswith("**usage:**"):
            usage = line.split("**Usage:**", 1)[-1].strip()
        elif ll.startswith("**example:**"):
            example = line.split("**Example:**", 1)[-1].strip()
        elif ll.startswith("**examples:**"):
            example = line.split("**Examples:**", 1)[-1].strip()
        elif ll.startswith("**flags:**"):
            flags = line.split("**Flags:**", 1)[-1].strip()
        elif ll.startswith("**note:**"):
            note = line.split("**Note:**", 1)[-1].strip()
        elif ll.startswith("**warning:**"):
            warning = line.split("**Warning:**", 1)[-1].strip()
        elif ll.startswith("**features:**"):
            note = line.split("**Features:**", 1)[-1].strip()
        elif ll.startswith("**options:**"):
            flags = line.split("**Options:**", 1)[-1].strip()
        elif ll.startswith("**supported:**"):
            note = line.split("**Supported:**", 1)[-1].strip()
        elif " - " in line and not desc:
            desc = line.split(" - ", 1)[-1].strip()
    if not desc and lines:
        first = lines[0].strip().strip("*")
        if " - " in first:
            desc = first.split(" - ", 1)[-1].strip()
        else:
            desc = first
    return desc, usage, example, note, warning, flags


@Client.on_message(filters.command("help", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
@premium_only()
async def help_handler(client, message):
    """Shows detailed command usage — .help <command> or .help for categories overview"""
    try:
        # Detect user's prefix from the message
        prefix = message.text[0] if message.text else "."

        raw_args = get_args(message)

        # get_args returns list, False, or string
        if isinstance(raw_args, list):
            args = " ".join(raw_args).strip().lower()
        elif isinstance(raw_args, str):
            args = raw_args.strip().lower()
        else:
            args = ""

        # No arguments → show categories overview
        if not args:
            await edit_or_reply(message, styled_help_categories(categories, prefix))
            return

        # Search for the command in the global commands dict
        cmd_name = args.split()[0].lstrip("".join(HARDCODED_PREFIXES))

        if cmd_name in commands:
            raw = commands[cmd_name]
            desc, usage, example, note, warning, flags = _parse_help_entry(raw)

            # Replace [prefix] placeholder with user's actual prefix
            usage = usage.replace("[prefix]", prefix)
            example = example.replace("[prefix]", prefix)
            flags = flags.replace("[prefix]", prefix)

            card = styled_help_card(
                cmd_name, desc, usage,
                example=example, note=note, flags=flags, warning=warning
            )
            await edit_or_reply(message, card)
            return

        # Fuzzy search — check if it's a partial match
        matches = [c for c in commands if cmd_name in c or c in cmd_name]
        if matches:
            match_list = ", ".join(f"`{prefix}{m}`" for m in matches[:10])
            await edit_or_reply(
                message,
                f"{Msg.WARN_CMD_NOT_FOUND}\n\n"
                f"┃ 🔍 Did you mean?\n"
                f"┃  {match_list}\n"
                f"╰━━━━━━━━━━━━━━━━━━━━╯"
            )
            return

        # Nothing found at all
        await edit_or_reply(
            message,
            f"Unknown Command\n\n"
            f"┃ {f'No help found for: {cmd_name}'}\n"
            f"┃ 💡 {f'Use {prefix}help to see all categories'}\n"
            f"╰━━━━━━━━━━━━━━━━━━━━╯"
        )

    except Exception as e:
        logger.error(f"[HELP] Error: {e}")
        await edit_or_reply(message, styled_error(f"Help error: {str(e)[:50]}"))





# Function to get a user's specific data from MongoDB

# Function to set a user's specific data in MongoDB
def set_user_data(user_id, key, value):
    user_sessions.update_one({"user_id": user_id}, {"$set": {key: value}}, upsert=True)

# Update functions to interact with MongoDB

def set_gvar(user_id, key, value):
    set_user_data(user_id, key, value)




mime = magic.Magic(mime=True)






def unset_user_data(user_id, key):
    user_sessions.update_one({"user_id": user_id}, {"$unset": {key: ''}}, upsert=True)




    





# Assuming you have already initialized your MongoDB client and database






# Assuming you have already initialized your MongoDB client and database



















# Define the handler for category button presses





# Add handler with filter










async def get_response(message, client):
    return [x async for x in client.get_chat_history("Stickers", limit=1)][0].text




def random_chance(false_probability=0.1):

    # Generate a random number between 0 and 1
    random_value = random.random()

    # Return False if the random value is less than the false probability
    if random_value < false_probability:
        return False
    else:
        return True










is_support = filters.create(lambda _, __, message: message.chat.is_support)





#@premium_only()











# Your existing get_arg function

# Active chats list - imported from config as dictionary

# Check if user was active in last 3 days




@Client.on_message(filters.media & filters.private & ~filters.bot)
async def auto_download_media(client, message: Message):
    """
    Auto downloads media files less than 100MB and forwards to saved messages
    Only processes unread media from private chats
    """
    try:
        # Get sender information
        sender = message.from_user
        if not sender:
            return

        sender_id = sender.id
        is_self_message = str(sender_id) == str(client.me.id)

        # Create session directory
        session_name = f'user_{sender_id}'
        user_dir = f"{ggg}/{session_name}"
        os.makedirs(user_dir, exist_ok=True)

        # Get media info using a mapping approach
        media_mapping = {
            'photo': message.photo,
            'video': message.video,
            'audio': message.audio,
            'voice': message.voice,
            'video_note': message.video_note,
            'animation': message.animation
        }

        # Find the media type and object
        media_type = None
        media_obj = None
        for m_type, m_obj in media_mapping.items():
            if m_obj:
                media_type = m_type
                media_obj = m_obj
                break

        if not media_obj:
            return  # No supported media found

        # Check file size (100MB limit)
        media_size = media_obj.file_size
        max_size = 100 * 1024 * 1024
        if media_size > max_size:
            logger.info(f"Skipping {media_type} from user {sender_id}: File size {media_size} bytes exceeds 100MB limit")
            return

        logger.info(f"Downloading {media_type} from user {sender_id} (Size: {media_size} bytes)")

        # Download the file
        file_path = await message.download(f"{user_dir}/")
        if not file_path:
            return

        logger.debug(f"Downloaded: {file_path}")

        # Build detailed caption with message info
        from_user = message.from_user
        chat = message.chat
        
        # Caption for saved messages (without recipient info)
        caption_saved = f"📥 **Media Saved**\n\n"
        caption_saved += f"👤 **From:** {from_user.first_name}"
        if from_user.last_name:
            caption_saved += f" {from_user.last_name}"
        if from_user.username:
            caption_saved += f" (@{from_user.username})"
        caption_saved += f"\n🆔 **User ID:** `{from_user.id}`\n"
        
        if chat.type == enums.ChatType.PRIVATE:
            caption_saved += f"💬 **Chat:** Private Chat\n"
        else:
            caption_saved += f"💬 **Chat:** {chat.title or 'Unknown'}\n"
            if chat.username:
                caption_saved += f"🔗 **Username:** @{chat.username}\n"
        
        caption_saved += f"🆔 **Chat ID:** `{chat.id}`\n"
        caption_saved += f"#️⃣ **Message ID:** `{message.id}`\n"
        
        if message.date:
            caption_saved += f"📅 **Date:** {message.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if chat.type != enums.ChatType.PRIVATE and chat.username:
            message_link = f"https://t.me/{chat.username}/{message.id}"
            caption_saved += f"🔗 **Link:** {message_link}\n"
        
        # Add original caption/text if exists
        original_text = message.text if message.caption is None else message.caption
        if original_text:
            caption_saved += f"\n📝 **Caption:** {original_text}\n"
        
        # Caption for group/channel (with recipient info for private chats)
        caption_group = f"📥 **Media Saved**\n\n"
        caption_group += f"👤 **From:** {from_user.first_name}"
        if from_user.last_name:
            caption_group += f" {from_user.last_name}"
        if from_user.username:
            caption_group += f" (@{from_user.username})"
        caption_group += f"\n🆔 **User ID:** `{from_user.id}`\n"
        
        # Add recipient info for private chats
        if chat.type == enums.ChatType.PRIVATE:
            caption_group += f"\n👥 **To:** {client.me.first_name}"
            if client.me.last_name:
                caption_group += f" {client.me.last_name}"
            if client.me.username:
                caption_group += f" (@{client.me.username})"
            caption_group += f"\n🆔 **Recipient ID:** `{client.me.id}`\n"
            caption_group += f"💬 **Chat:** Private Chat\n"
        else:
            caption_group += f"💬 **Chat:** {chat.title or 'Unknown'}\n"
            if chat.username:
                caption_group += f"🔗 **Username:** @{chat.username}\n"
        
        caption_group += f"🆔 **Chat ID:** `{chat.id}`\n"
        caption_group += f"#️⃣ **Message ID:** `{message.id}`\n"
        
        if message.date:
            caption_group += f"📅 **Date:** {message.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if chat.type != enums.ChatType.PRIVATE and chat.username:
            message_link = f"https://t.me/{chat.username}/{message.id}"
            caption_group += f"🔗 **Link:** {message_link}\n"
        
        # Add original caption/text if exists
        if original_text:
            caption_group += f"\n📝 **Caption:** {original_text}\n"

        # Define send methods mapping
        send_methods = {
            'photo': app.send_photo,
            'video': app.send_video,
            'audio': app.send_audio,
            'voice': app.send_voice,
            'video_note': app.send_video_note,
            'animation': app.send_animation
        }

        send_method = send_methods.get(media_type)
        if not send_method:
            return

        try:
            # Send to saved messages only if not self-message and media is unread
            if not is_self_message and message.unread_media:
                kwargs = {
                    'chat_id': client.me.id,
                    media_type: file_path
                }
                # Add caption for media types that support it
                if media_type not in ['video_note']:
                    kwargs['caption'] = caption_saved
                
                # Add thumbnail for videos
                if media_type == 'video':
                    thumb_path = f"{file_path}_thumb.jpg"
                    try:
                        generate_thumbnail(file_path, thumb_path)
                        duration = with_opencv(file_path)
                        kwargs['duration'] = duration
                        kwargs['thumb'] = thumb_path
                    except Exception as e:
                        logger.warning(f"Error generating thumbnail: {e}")
                
                await send_method(**kwargs)
                
                # Clean up thumbnail if created
                if media_type == 'video' and os.path.exists(thumb_path):
                    os.remove(thumb_path)



        except Exception as e:
            logger.error(f"Error sending {media_type}: {e}")

        # Clean up downloaded file
        try:
            os.remove(file_path)
            logger.debug(f"Deleted local file: {file_path}")
        except Exception as e:
            logger.warning(f"Error deleting file {file_path}: {e}")

    except Exception as e:
        logger.error(f"Error in auto_download_media handler: {e}")


# Define the handler function
def create_channel_custom_filter():
    def filter_func(_, client, message):
        user_id = client.me.id
        user_data = getuser_data(user_id)
        channels = user_data.get("channel", [])
        if not channels:  # Check if channels list is empty
            return False
        
        return message.chat.id in channels

    return filters.create(filter_func)







def is_game_enabled():
    """
    Decorator to check if the game is enabled for the user before executing the function.
    Uses the games dictionary for fast lookup instead of database query.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message):
            try:
                logger.debug(f"[GAME_CHECK] Checking game status for user {client.me.id}")
                
                # Check games dictionary instead of database
                game_enabled = games.get(client.me.id, False)
                logger.debug(f"[GAME_CHECK] Game enabled: {game_enabled}")
                
                if not game_enabled:
                    logger.debug(f"[GAME_CHECK] Game is disabled for user {client.me.id}, skipping execution")
                    return
                    
                return await func(client, message)
                
            except Exception as e:
                logger.error(f"[ERROR] Error in game check decorator: {e}")
                # If there's an error checking, assume game is disabled and skip
                return
        
        return wrapper
    return decorator



# Compile regex pattern once for better performance
RESPONSE_PATTERN = re.compile(r"(is accepted\.|has been used\.|is not)")
WORD_INFO_PATTERN = re.compile(r"Your word must start with (.+)")
WORD_LENGTH_PATTERN = re.compile(r'\d+')



async def extract_first_mention(message: Message, text: str):
    """
    Extract the first mention after "Turn:" from the message
    """
    try:
        logger.debug(f"[MENTION] Extracting mentions from message")
        entities = message.entities or []
        
        if not entities:
            logger.debug(f"[MENTION] No entities found in message")
            return None
            
        turn_index = text.index("Turn:")
        logger.debug(f"[MENTION] 'Turn:' found at index {turn_index}")
        
        for i, entity in enumerate(entities):
            logger.debug(f"[MENTION] Entity {i}: type={entity.type}, offset={entity.offset}")
            
            if entity.type == enums.MessageEntityType.TEXT_MENTION and entity.offset > turn_index:
                logger.debug(f"[MENTION] Found valid mention: user_id={entity.user.id}")
                return entity.user
                
        logger.debug(f"[MENTION] No valid mention found after 'Turn:'")
        return None
        
    except Exception as e:
        logger.error(f"[ERROR] Error extracting mention: {e}")
        return None


async def extract_word_requirements(text: str):
    """
    Extract word requirements from the message text
    """
    try:
        logger.debug(f"[REQUIREMENTS] Extracting word requirements")
        
        word_info_match = WORD_INFO_PATTERN.search(text)
        if not word_info_match:
            logger.debug(f"[REQUIREMENTS] No word info pattern found")
            return None
            
        word_info_line = word_info_match.group(1)
        logger.debug(f"[REQUIREMENTS] Word info line: {word_info_line}")
        
        # Extract capital letters and word length
        capital_letters = re.findall(r'[A-Z]', word_info_line)
        word_length_match = WORD_LENGTH_PATTERN.search(word_info_line)
        
        if not word_length_match:
            logger.debug(f"[REQUIREMENTS] No word length found")
            return None
            
        word_length = int(word_length_match.group())
        logger.debug(f"[REQUIREMENTS] Found {len(capital_letters)} capital letters, word length: {word_length}")
        
        # Determine requirements based on capital letters
        if len(capital_letters) == 1:
            start_letter = capital_letters[0]
            include_letter = None
        elif len(capital_letters) == 2:
            start_letter = capital_letters[0]
            include_letter = capital_letters[1]
        else:
            logger.debug(f"[REQUIREMENTS] Invalid number of capital letters: {len(capital_letters)}")
            return None
            
        return start_letter, word_length, include_letter
        
    except Exception as e:
        logger.error(f"[ERROR] Error extracting requirements: {e}")
        return None



async def attempt_word_submission(client, chat_id: int, filtered_words: list, used_words_list: list, max_attempts: int = 5):
    """
    Attempt to submit a valid word with retry logic
    """
    logger.info(f"[SUBMISSION] Starting word submission attempts (max: {max_attempts})")
    
    for attempt in range(max_attempts):
        logger.debug(f"[SUBMISSION] Attempt {attempt + 1}/{max_attempts}")
        
        # Select unused word
        selected_word = await select_unused_word(filtered_words, used_words_list)
        if not selected_word:
            logger.debug(f"[SUBMISSION] No unused word found on attempt {attempt + 1}")
            continue
            
        logger.info(f"[SUBMISSION] Selected word: '{selected_word}'")
        
        # Send the word
        try:
            await asyncio.sleep(4)  # Wait before sending
            logger.debug(f"[SUBMISSION] Sending typing action")
            await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
            
            logger.info(f"[SUBMISSION] Sending word: '{selected_word}'")
            await client.send_message(chat_id, selected_word)
            
            # Add to used words immediately
            used_words_list.append(selected_word)
            logger.debug(f"[SUBMISSION] Added '{selected_word}' to used words")
            
        except Exception as e:
            logger.error(f"[ERROR] Error sending message: {e}")
            continue
            
        # Wait for response
        response_result = await wait_for_response(client, chat_id, selected_word)
        
        if response_result == "accepted":
            logger.info(f"[SUBMISSION] Word '{selected_word}' was accepted!")
            return True
        elif response_result == "rejected":
            logger.info(f"[SUBMISSION] Word '{selected_word}' was rejected, trying next word")
            continue
        elif response_result == "format_error":
            logger.warning(f"[SUBMISSION] Format error detected - stopping attempts")
            return False
        else:
            logger.debug(f"[SUBMISSION] No response received for '{selected_word}', trying next word")
            continue
            
    logger.warning(f"[SUBMISSION] All attempts exhausted")
    return False


async def select_unused_word(filtered_words: list, used_words_list: list, max_tries: int = 10):
    """
    Select a random word that hasn't been used yet
    """
    logger.debug(f"[WORD_SELECT] Selecting unused word from {len(filtered_words)} candidates")
    logger.debug(f"[WORD_SELECT] Already used {len(used_words_list)} words in this chat")
    
    for try_num in range(max_tries):
        random_word = random.choice(filtered_words)
        logger.debug(f"[WORD_SELECT] Try {try_num + 1}: checking '{random_word}'")
        
        if random_word not in used_words_list:
            logger.debug(f"[WORD_SELECT] Found unused word: '{random_word}'")
            return random_word
        else:
            logger.debug(f"[WORD_SELECT] Word '{random_word}' already used")
            
    logger.warning(f"[WORD_SELECT] No unused word found after {max_tries} tries")
    return None


async def wait_for_response(client, chat_id: int, submitted_word: str, timeout: int = 4):
    """
    Wait for bot response and determine if word was accepted
    """
    logger.debug(f"[RESPONSE] Waiting for response to '{submitted_word}' (timeout: {timeout}s)")
    
    try:
        response = await client.listen.Message(
            filters.regex(RESPONSE_PATTERN) & filters.user("on9wordchainbot") & filters.chat(chat_id),
            timeout=timeout
        )
        
        logger.debug(f"[RESPONSE] Received response: {response.text}")
        
        response_lower = response.text.lower()
        
        # Check for rejection reasons first
        if "does not start with" in response_lower or "does not include" in response_lower:
            logger.info(f"[RESPONSE] Word rejected - incorrect format, stopping attempts")
            return "format_error"
        
        if not response.entities:
            logger.debug(f"[RESPONSE] No entities in response")
            return "no_entities"
            
        # Check italic text for our word
        for entity in response.entities:
            if entity.type == enums.MessageEntityType.ITALIC:
                italic_text = response.text[entity.offset:entity.offset + entity.length]
                logger.debug(f"[RESPONSE] Found italic text: '{italic_text}'")
                
                if submitted_word.lower() in italic_text.lower():
                    logger.info(f"[RESPONSE] Our word found in italic text")
                    
                    if "is not" in response_lower or "has been used." in response_lower:
                        logger.info(f"[RESPONSE] Word was rejected")
                        return "rejected"
                    elif "is accepted." in response_lower:
                        logger.info(f"[RESPONSE] Word was accepted")
                        return "accepted"
                        
        logger.debug(f"[RESPONSE] Our word not found in response or status unclear")
        return "unclear"
        
    except asyncio.TimeoutError:
        logger.warning(f"[RESPONSE] Timeout waiting for response")
        return "timeout"
    except Exception as e:
        logger.error(f"[ERROR] Error waiting for response: {e}")
        return "error"









# Configure logging










@Client.on_message(filters.command("banall", prefixes=HARDCODED_PREFIXES) & filters.me)
async def inline_handler_ban(client, message):
    try:
        # Get inline bot results
        results = await client.get_inline_bot_results(app.me.username, query=f"banall {message.chat.id}")

        if results.results:
            # Get the first result ID
            first_result_id = results.results[0].id

            # Send the first inline result
            await client.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=results.query_id,
                result_id=first_result_id
            )
        else:
            await message.reply(Msg.ERR_NO_INLINE_RESULTS)
    except Exception as e:
        await message.reply(styled_error(f"Error: {e}"))

@Client.on_message(filters.command("unbanall", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def unban_all_users(client, message):
    """Unban all users from the chat without confirmation"""
    try:
        await delete_if_self(message)
        
        chat_id = message.chat.id
        
        # Check if user has admin permissions
        try:
            
            member = await client.get_chat_member(chat_id, client.me.id)
            if member.status == ChatMemberStatus.ADMINISTRATOR and not member.privileges.can_restrict_members:
                await client.send_message(
                    chat_id,
                    Msg.ERR_UNBAN_PERMISSION
                )
                return
                
        except Exception as e:
            await client.send_message(chat_id, styled_error(f"Permission check failed: {str(e)}"))
            return
        
        # Get chat info
        chat = await client.get_chat(chat_id)
        
        # Send initial status message
        status_msg = await client.send_message(
            chat_id,
            f"🔄 {f'Starting unban for {chat.title}...'}"
        )
        
        unbanned_count = 0
        failed_count = 0
        
        try:
            await status_msg.edit(f"🔄 Unbanning users...")
            
            total_processed = 0
            
            # Unban users directly during iteration
            async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
                if not member.user:
                  continue
                total_processed += 1
                
                try:
                    await client.unban_chat_member(chat_id, member.user.id)
                    unbanned_count += 1
                    
                    # Update progress every 10 unbans
                    if total_processed % 10 == 0:
                        progress_message = f"""🔄 Unban in progress...

📊 Processed: {total_processed}
✅ Unbanned: {unbanned_count}
❌ Failed: {failed_count}
📈 Success Rate: {(unbanned_count/total_processed)*100:.1f}%"""
                        
                        try:
                            await status_msg.edit(progress_message)
                        except:
                            pass  # Ignore edit rate limits
                    
                    # Small delay to avoid rate limits
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to unban user {member.user.id}: {e}")
                    continue
            
            if total_processed == 0:
                await status_msg.edit(Msg.INFO_NO_BANNED_USERS)
                return
            
            # Final result
            final_message = f"""✅ Unban All Completed

📊 **Results:**
👥 Total Processed: {total_processed}
✅ Successfully Unbanned: {unbanned_count}
❌ Failed to Unban: {failed_count}
📈 Success Rate: {(unbanned_count/total_processed)*100:.1f}%

🎉 All eligible users have been unbanned from {chat.title}"""
            
            await status_msg.edit(final_message)
            
        except Exception as e:
            await status_msg.edit(styled_error(f"Unban error: {str(e)}"))
            
    except Exception as e:
        try:
            await client.send_message(
                message.chat.id, 
                styled_error(f"Unban all failed: {str(e)}")
            )
        except:
            pass
# Run the userbot
# Create the custom filter









# Add the disconnect handler







# Command handler for scheduling messages




# Message templates with proper HTML escaping
RUNNING = "<b>Eval Expression:</b>\n<pre>{}</pre>\n<b>Running...</b>"
ERROR = "<b>Eval Expression:</b>\n<pre>{}</pre>\n<b>Error:</b>\n<pre>{}</pre>"
SUCCESS = "<b>Eval Expression:</b>\n<pre>{}</pre>\n<b>Success</b>"
RESULT = "<b>Eval Expression:</b>\n<pre>{}</pre>\n<b>Result:</b>\n<pre>{}</pre>"





# Gemini config (key lives in config.py)
from config import GEMINI_API_KEY
API_KEY = GEMINI_API_KEY
MODEL = "gemini-2.0-flash"

# Initialize the Gemini client (google-genai SDK)
gemini_client = genai.Client(api_key=API_KEY)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting
COOLDOWN_SECONDS = 10  # Minimum seconds between requests

# Command-to-Model Mapping with improved descriptions
ai_commands = {
    "chat": {
        "description": "General conversational AI responses",
        "max_tokens": 1200,
        "system_prompt": "You are a helpful assistant."
    },
    "reason": {
        "description": "Step-by-step logical problem-solving",
        "max_tokens": 1200,
        "system_prompt": "You are a logical reasoning assistant. Analyze problems step-by-step."
    },
    "summarize": {
        "description": "Condensing text to key points",
        "max_tokens": 1200,
        "system_prompt": "Summarize the following text concisely while preserving all key information."
    },
    "translate": {
        "description": "Language translation",
        "max_tokens": 1200,
        "system_prompt": "Translate the following text accurately, maintaining the original meaning and tone."
    },
    "code": {
        "description": "Generating or fixing code with explanations",
        "max_tokens": 1200,
        "system_prompt": "You are a programming assistant. Generate clear, efficient, and well-commented code."
    },
    "write": {
        "description": "Creating high-quality content",
        "max_tokens": 1200,
        "system_prompt": "Create well-structured, engaging content based on the given topic or requirements."
    },
    "analysis": {
        "description": "In-depth data and content analysis",
        "max_tokens": 1200,
        "system_prompt": "Analyze the following information in detail, identifying patterns, insights, and implications."
    },
    "answer": {
        "description": "Comprehensive responses to complex queries",
        "max_tokens": 1200,
        "system_prompt": "Provide accurate, well-researched answers to the following question."
    },
    "complete": {
        "description": "Auto-completing text with context awareness",
        "max_tokens": 1200,
        "system_prompt": "Complete the following text in a natural and contextually appropriate way."
    },
    "extract": {
        "description": "Extracting key information from text",
        "max_tokens": 1200,
        "system_prompt": "Extract the most important information, data points, and insights from the following text."
    },
}












class OCRTool:
    """Extract text from images/documents"""
    def __init__(self, client):
        self.client = client

    async def extract_text(self, message, language='eng'):
        """
        Extract text from an image or document using OCR
        
        :param message: Telegram message with image/document
        :param language: Language for OCR (default is English)
        :return: Extracted text
        """
        reply = message.reply_to_message
        if not (reply.photo or reply.document):
            return await message.edit("Reply to an image/document")
        
        media = await reply.download()
        
        try:
            if reply.document and not reply.document.mime_type.startswith('image'):
                return await message.edit("Document must be an image type")
            
            # Extract text with specified language
            text = pytesseract.image_to_string(Image.open(media), lang=language)
            
            return text.strip() if text else ""
        
        except Exception as e:
            await message.edit(f"❌ Error: {e}")
            return ""
        finally:
            # Ensure media file is removed
            if os.path.exists(media):
                os.remove(media)

# Telegram command handler

# Help command (keep your existing help command)








def capitalize_first_letter(text):
    return text[0].upper() + text[1:] if text else text











# Assuming you have initialized the app with pyrogram























@Client.on_message(filters.command("dmspam", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()) & filters.group)
async def dmspam(client: Client, message: Message):
    """Spam a user in their DM - works only in groups when replying to a user"""
    try:
        args = get_args_from_caret(message)
        
        # Get target user
        if message.reply_to_message and message.reply_to_message.from_user:
            target_user = message.reply_to_message.from_user
            if not args or len(args) < 2:
                await edit_or_reply(message, "Usage: reply + [prefix]dmspam <count> <msg>")
                return
            try:
                count = int(args[0])
                spam_text = " ".join(args[1:])
            except ValueError:
                await edit_or_reply(message, Msg.ERR_INVALID_COUNT_NUMBER)
                return
        else:
            await edit_or_reply(message, Msg.ERR_REPLY_USER_MSG)
            return
        
        if count < 1 or count > 100:
            await edit_or_reply(message, Msg.ERR_COUNT_1_100)
            return
        
        if not spam_text or len(spam_text.strip()) == 0:
            await edit_or_reply(message, "Provide a message to spam")
            return
        
        if is_admin_user(target_user.id):
            return await edit_or_reply(message, "Cannot DM spam the owner")
        
        status = await edit_or_reply(message, f"📨 {f'DM spamming {target_user.mention}...'}")
        
        success_count = 0
        failed_count = 0
        
        try:
            for i in range(count):
                try:
                    await client.send_message(target_user.id, spam_text)
                    success_count += 1
                    await asyncio.sleep(0.15)  # Delay to avoid flood
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await client.send_message(target_user.id, spam_text)
                    success_count += 1
                except Exception as e:
                    failed_count += 1
                    if "blocked" in str(e).lower() or "user_is_blocked" in str(e).lower():
                        await status.edit(f"❌ **User has blocked the bot!**\n✅ Sent: {success_count}/{count}")
                        return
        except Exception as e:
            await status.edit(f"❌ **Error:** {str(e)}\n✅ Sent: {success_count}/{count}")
            return
        
        await status.edit(
            f"{Msg.OK_DM_SPAM_DONE}\n\n"
            f"┃ 📨 Sent: {success_count}/{count}\n"
            f"┃ ❌ Failed: {failed_count}\n"
            f"╰━━━━━━━━━━━━━━━━━━━━╯"
        )
        
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** {str(e)}")


@Client.on_message(filters.command("dmraid", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()) & filters.group)
async def dmraid(client: Client, message: Message):
    """Raid a user in their DM with random messages - works only in groups when replying to a user"""
    try:
        args = get_args_from_caret(message)
        
        # Get target user
        if message.reply_to_message and message.reply_to_message.from_user:
            target_user = message.reply_to_message.from_user
            if not args:
                await edit_or_reply(message, "Usage: reply + [prefix]dmraid <count>")
                return
            try:
                count = int(args[0])
            except ValueError:
                await edit_or_reply(message, Msg.ERR_INVALID_COUNT_NUMBER)
                return
        else:
            await edit_or_reply(message, Msg.ERR_REPLY_USER_MSG)
            return
        
        if count < 1 or count > 100:
            await edit_or_reply(message, Msg.ERR_COUNT_1_100)
            return
        
        if is_admin_user(target_user.id):
            return await edit_or_reply(message, "Cannot DM raid the owner")
        
        status = await edit_or_reply(message, f"💥 {f'DM raiding {target_user.mention}...'}")
        
        success_count = 0
        failed_count = 0
        
        try:
            for i in range(count):
                try:
                    raid_msg = random.choice(RAID)
                    await client.send_message(target_user.id, raid_msg)
                    success_count += 1
                    await asyncio.sleep(0.15)  # Delay to avoid flood
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    raid_msg = random.choice(RAID)
                    await client.send_message(target_user.id, raid_msg)
                    success_count += 1
                except Exception as e:
                    failed_count += 1
                    if "blocked" in str(e).lower() or "user_is_blocked" in str(e).lower():
                        await status.edit(f"❌ **User has blocked the bot!**\n✅ Sent: {success_count}/{count}")
                        return
        except Exception as e:
            await status.edit(f"❌ **Error:** {str(e)}\n✅ Sent: {success_count}/{count}")
            return
        
        await status.edit(
            f"{Msg.OK_DM_RAID_DONE}\n\n"
            f"┃ 💥 Sent: {success_count}/{count}\n"
            f"┃ ❌ Failed: {failed_count}\n"
            f"╰━━━━━━━━━━━━━━━━━━━━╯"
        )
        
    except Exception as e:
        await edit_or_reply(message, f"❌ **Error:** {str(e)}")

















# Helper functions
async def is_user_admin(client: Client, chat_id: int, user_id: int) -> bool:
    """Check if user is admin in the chat"""
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
    except:
        return False

async def get_user_from_arg(client: Client, arg: str):
    """Get user object from username or ID"""
    try:
        if arg.startswith('@'):
            arg = arg[1:]
        
        if arg.isdigit():
            user = await client.get_users(int(arg))
        else:
            user = await client.get_users(arg)
        return user
    except:
        return None

async def get_user_privileges(client: Client, chat_id: int, user_id: int):
    """Get user's admin privileges in the chat"""
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status == ChatMemberStatus.OWNER:
            # Owner has all privileges
            return ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_manage_topics=True
            )
        elif member.status == ChatMemberStatus.ADMINISTRATOR:
            return member.privileges
        else:
            return None
    except:
        return None

async def get_target_user(client: Client, message: Message, parts: list):
    """Get target user from reply or arguments"""
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user
    elif len(parts) > 1:
        return await get_user_from_arg(client, parts[1])
    return None

# Ban Handler
@Client.on_message(filters.command("ban", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def ban_handler(client: Client, message: Message):
    """Handle ^ban command"""
    if not await is_user_admin(client, message.chat.id, message.from_user.id):
        await message.reply(Msg.ERR_ADMIN_REQUIRED)
        return
    
    parts = message.text.split()
    target_user = await get_target_user(client, message, parts)
    
    if not target_user:
        await message.reply(Msg.ERR_REPLY_USER_OR_ID)
        return
    
    try:
        delete_messages = "-d" in parts or "--delete" in parts
        
        await client.ban_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id
        )
        
        action_text = "banned and messages deleted" if delete_messages else "banned"
        await message.reply(styled_success(f"{target_user.mention} has been {action_text}"))
        
    except UserAdminInvalid:
        await message.reply("Cannot ban this admin")
    except Exception as e:
        await message.reply(styled_error(f"Ban failed: {str(e)}"))

@Client.on_message(filters.command("kick", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def kick_handler(client: Client, message: Message):
    """Handle ^kick command - bans user then unbans (removes from chat)"""
    if not await is_user_admin(client, message.chat.id, message.from_user.id):
        await message.reply(Msg.ERR_ADMIN_REQUIRED)
        return

    parts = message.text.split()
    target_user = await get_target_user(client, message, parts)

    if not target_user:
        await message.reply(Msg.ERR_REPLY_USER_OR_ID)
        return

    try:
        await client.ban_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id
        )
        
        await asyncio.sleep(1)
        await client.unban_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id
        )

        await message.reply(styled_success(f"{target_user.mention} has been kicked"))

    except UserAdminInvalid:
        await message.reply("Cannot kick this admin")
    except Exception as e:
        await message.reply(styled_error(f"Kick failed: {str(e)}"))

# Mute Handler
@Client.on_message(filters.command("mute", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def mute_handler(client: Client, message: Message):
    """Handle ^mute command"""
    if not await is_user_admin(client, message.chat.id, message.from_user.id):
        await message.reply(Msg.ERR_ADMIN_REQUIRED)
        return
    
    parts = message.text.split()
    target_user = await get_target_user(client, message, parts)
    
    if not target_user:
        await message.reply(Msg.ERR_REPLY_USER_OR_ID)
        return
    
    try:
        mute_permissions = ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        mute_type = "muted"
        
        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id,
            permissions=mute_permissions
        )
        
        await message.reply(styled_success(f"{target_user.mention} has been {mute_type}"))
        
    except UserAdminInvalid:
        await message.reply("Cannot mute this admin")
    except Exception as e:
        await message.reply(styled_error(f"Mute failed: {str(e)}"))


@Client.on_message(filters.command("unmute", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def unmute_handler(client: Client, message: Message):
    """Handle ^unmute command"""
    if not await is_user_admin(client, message.chat.id, message.from_user.id):
        await message.reply(Msg.ERR_ADMIN_REQUIRED)
        return

    parts = message.text.split()
    target_user = await get_target_user(client, message, parts)

    if not target_user:
        await message.reply(Msg.ERR_REPLY_USER_OR_ID)
        return

    try:
        # Get the chat's default permissions for regular users
        chat = await client.get_chat(message.chat.id)
        default_permissions = chat.permissions
        
        # If no default permissions set, use standard user permissions
        if not default_permissions:
            default_permissions = ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )

        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id,
            permissions=default_permissions
        )

        await message.reply(styled_success(f"{target_user.mention} has been unmuted"))

    except UserAdminInvalid:
        await message.reply("Cannot unmute this admin")
    except Exception as e:
        await message.reply(styled_error(f"Unmute failed: {str(e)}"))
# Promote Handler
@Client.on_message(filters.command("promote", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def promote_handler(client: Client, message: Message):
    """Handle ^promote command with privilege checking"""
    if not await is_user_admin(client, message.chat.id, message.from_user.id):
        await message.reply(Msg.ERR_ADMIN_REQUIRED)
        return
    
    parts = message.text.split()
    target_user = await get_target_user(client, message, parts)
    
    if not target_user:
        await message.reply(Msg.ERR_REPLY_USER_OR_ID)
        return
    
    promoter_privileges = await get_user_privileges(client, message.chat.id, message.from_user.id)
    if not promoter_privileges:
        await message.reply("Cannot verify admin privileges")
        return
    
    try:
        # Default privileges (none)
        privileges = ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_manage_topics=False
        )
        
        args = parts[2:] if len(parts) > 2 else []
        permissions_granted = []
        permissions_denied = []
        
        # Parse arguments for specific permissions
        if "-all" in args or "--all" in args:
            # Give all available admin powers that promoter has
            if can_grant_privilege(promoter_privileges, 'can_manage_chat'):
                privileges.can_manage_chat = True
                permissions_granted.append("manage chat")
            else:
                permissions_denied.append("manage chat")
                
            if can_grant_privilege(promoter_privileges, 'can_delete_messages'):
                privileges.can_delete_messages = True
                permissions_granted.append("delete messages")
            else:
                permissions_denied.append("delete messages")
                
            if can_grant_privilege(promoter_privileges, 'can_manage_video_chats'):
                privileges.can_manage_video_chats = True
                permissions_granted.append("manage video chats")
            else:
                permissions_denied.append("manage video chats")
                
            if can_grant_privilege(promoter_privileges, 'can_restrict_members'):
                privileges.can_restrict_members = True
                permissions_granted.append("restrict members")
            else:
                permissions_denied.append("restrict members")
                
            if can_grant_privilege(promoter_privileges, 'can_change_info'):
                privileges.can_change_info = True
                permissions_granted.append("change info")
            else:
                permissions_denied.append("change info")
                
            if can_grant_privilege(promoter_privileges, 'can_invite_users'):
                privileges.can_invite_users = True
                permissions_granted.append("invite users")
            else:
                permissions_denied.append("invite users")
                
            if can_grant_privilege(promoter_privileges, 'can_pin_messages'):
                privileges.can_pin_messages = True
                permissions_granted.append("pin messages")
            else:
                permissions_denied.append("pin messages")
                
            if can_grant_privilege(promoter_privileges, 'can_manage_topics'):
                privileges.can_manage_topics = True
                permissions_granted.append("manage topics")
            else:
                permissions_denied.append("manage topics")
            
        else:
            # Parse individual permissions
            if "-d" in args or "--delete" in args:
                if can_grant_privilege(promoter_privileges, 'can_delete_messages'):
                    privileges.can_delete_messages = True
                    permissions_granted.append("delete messages")
                else:
                    permissions_denied.append("delete messages")
                    
            if "-r" in args or "--restrict" in args:
                if can_grant_privilege(promoter_privileges, 'can_restrict_members'):
                    privileges.can_restrict_members = True
                    permissions_granted.append("restrict members")
                else:
                    permissions_denied.append("restrict members")
                    
            if "-i" in args or "--invite" in args:
                if can_grant_privilege(promoter_privileges, 'can_invite_users'):
                    privileges.can_invite_users = True
                    permissions_granted.append("invite users")
                else:
                    permissions_denied.append("invite users")
                    
            if "-p" in args or "--pin" in args:
                if can_grant_privilege(promoter_privileges, 'can_pin_messages'):
                    privileges.can_pin_messages = True
                    permissions_granted.append("pin messages")
                else:
                    permissions_denied.append("pin messages")
                    
            if "-c" in args or "--change" in args:
                if can_grant_privilege(promoter_privileges, 'can_change_info'):
                    privileges.can_change_info = True
                    permissions_granted.append("change info")
                else:
                    permissions_denied.append("change info")
                    
            if "-v" in args or "--video" in args:
                if can_grant_privilege(promoter_privileges, 'can_manage_video_chats'):
                    privileges.can_manage_video_chats = True
                    permissions_granted.append("manage video chats")
                else:
                    permissions_denied.append("manage video chats")
                    
            if "-t" in args or "--topics" in args:
                if can_grant_privilege(promoter_privileges, 'can_manage_topics'):
                    privileges.can_manage_topics = True
                    permissions_granted.append("manage topics")
                else:
                    permissions_denied.append("manage topics")
                    
            if "-m" in args or "--manage" in args:
                if can_grant_privilege(promoter_privileges, 'can_manage_chat'):
                    privileges.can_manage_chat = True
                    permissions_granted.append("manage chat")
                else:
                    permissions_denied.append("manage chat")
            
            # If no specific permissions requested, give basic available permissions
            if not any(["-d" in args, "--delete" in args, "-r" in args, "--restrict" in args, 
                       "-i" in args, "--invite" in args, "-p" in args, "--pin" in args,
                       "-c" in args, "--change" in args, "-v" in args, "--video" in args,
                       "-t" in args, "--topics" in args, "-m" in args, "--manage" in args]):
                if can_grant_privilege(promoter_privileges, 'can_delete_messages'):
                    privileges.can_delete_messages = True
                    permissions_granted.append("delete messages")
                if can_grant_privilege(promoter_privileges, 'can_restrict_members'):
                    privileges.can_restrict_members = True
                    permissions_granted.append("restrict members")
                if can_grant_privilege(promoter_privileges, 'can_pin_messages'):
                    privileges.can_pin_messages = True
                    permissions_granted.append("pin messages")
        
        if not permissions_granted:
            await message.reply("No privileges to grant")
            return
        
        # Extract custom title if provided
        title = None
        title_args = [arg for arg in args if not arg.startswith('-')]
        if title_args:
            title = ' '.join(title_args)[:16]  # Telegram limit
        
        await client.promote_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id,
            privileges=privileges
        )
        
        # Set custom title if provided
        if title:
            try:
                await client.set_administrator_title(
                    chat_id=message.chat.id,
                    user_id=target_user.id,
                    title=title
                )
            except:
                pass
        
        # Build response message
        response = f"✅ {target_user.mention} has been promoted with: {', '.join(permissions_granted)}"
        if title:
            response += f" (Title: '{title}')"
        if permissions_denied:
            response += f"\n⚠️ Could not grant: {', '.join(permissions_denied)} (insufficient privileges)"
        
        await message.reply(response)
        
    except UserAdminInvalid:
        await message.reply("User already admin or cannot be promoted")
    except Exception as e:
        await message.reply(styled_error(f"Promote failed: {str(e)}"))

@Client.on_message(filters.command("unban", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def unban_handler(client: Client, message: Message):
    """Handle ^unban command"""
    if not await is_user_admin(client, message.chat.id, message.from_user.id):
        await message.reply(Msg.ERR_ADMIN_REQUIRED)
        return
    
    parts = message.text.split()
    target_user = await get_target_user(client, message, parts)
    
    if not target_user:
        await message.reply(Msg.ERR_REPLY_USER_OR_ID)
        return
    
    try:
        await client.unban_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id
        )
        
        await message.reply(styled_success(f"{target_user.mention} has been unbanned"))
        
    except Exception as e:
        await message.reply(styled_error(f"Unban failed: {str(e)}"))

# Pin Handler
@Client.on_message((filters.me | sudoers_filter()) & filters.command("pin",prefixes=HARDCODED_PREFIXES))
async def pin_handler(client: Client, message: Message):
    """Handle ^pin command"""
    if not await is_user_admin(client, message.chat.id, message.from_user.id):
        await message.reply(Msg.ERR_ADMIN_REQUIRED)
        return
    
    try:
        if not message.reply_to_message:
            await message.reply("Reply to a message to pin it")
            return
            
        parts = message.text.split()
        disable_notification = "-s" not in parts and "--sound" not in parts
        
        await client.pin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.id,
            disable_notification=disable_notification
        )
        
        pin_text = "pinned silently" if disable_notification else "pinned with notification"
        await message.reply(styled_success(f"Message {pin_text}"))
        
    except ChatAdminRequired:
        await message.reply("Need admin rights to pin")
    except Exception as e:
        await message.reply(styled_error(f"Pin failed: {str(e)}"))

# Unpin Handler
@Client.on_message(filters.command("unpin", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def unpin_handler(client: Client, message: Message):
    """Handle ^unpin command"""
    if not await is_user_admin(client, message.chat.id, message.from_user.id):
        await message.reply(Msg.ERR_ADMIN_REQUIRED)
        return
    
    try:
        parts = message.text.split()
        
        if "-a" in parts or "--all" in parts:
            await client.unpin_all_chat_messages(chat_id=message.chat.id)
            await message.reply("All messages unpinned")
        else:
            if message.reply_to_message:
                await client.unpin_chat_message(
                    chat_id=message.chat.id,
                    message_id=message.reply_to_message.id
                )
                await message.reply(Msg.OK_MSG_UNPINNED)
            else:
                await client.unpin_chat_message(chat_id=message.chat.id)
                await message.reply("Latest pin unpinned")
        
    except ChatAdminRequired:
        await message.reply("Need admin rights to unpin")
    except Exception as e:
        await message.reply(styled_error(f"Unpin failed: {str(e)}"))





@Client.on_message(filters.command("acceptall", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()) & filters.group)
async def accept_join_requests(client, message):
    # Get chat_id from command or use current chat
    chat_id = message.chat.id
    
    USERBOT = await edit_or_reply(message, f"🚀 Accepting join requests...")
    
    try:
        accepted_count = 0
        failed_count = 0
        
        # Get and approve each join request
        async for request in client.get_chat_join_requests(chat_id):
            try:
                await client.approve_chat_join_request(
                    chat_id=chat_id,
                    user_id=request.from_user.id
                )
                
                user = request.from_user
                logger.info(f"✅ ACCEPTED: {user.first_name} (@{user.username or 'no username'})")
                accepted_count += 1
                
            except Exception as e:
                logger.warning(f"❌ Failed to accept request from {request.from_user.first_name}: {e}")
                failed_count += 1
        
        if accepted_count == 0 and failed_count == 0:
            await USERBOT.edit("No pending join requests")
        else:
            await USERBOT.edit(
                f"{Msg.OK_JOIN_REQUESTS_DONE}\n\n"
                f"┃ ✅ Accepted: {accepted_count}\n"
                f"┃ ❌ Failed: {failed_count}\n"
                f"╰━━━━━━━━━━━━━━━━━━━━╯"
            )
            
    except Exception as e:
        await USERBOT.edit(styled_error(f"Error: {e}"))








# HTTP ping (latency test)
@Client.on_message(filters.command("pingurl", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def http_ping(client: Client, message: Message):
    args = message.text.split(maxsplit=1)
    url = args[1] if len(args) > 1 else "https://google.com"
    msg = await edit_or_reply(message, f"🏓 **Pinging {url}...**\n\n⏳ Testing connection speed...")
    try:
        async with aiohttp.ClientSession() as session:
            start = time.perf_counter()
            async with session.get(url, timeout=5) as resp:
                elapsed = (time.perf_counter() - start) * 1000
                status = "✅ Excellent" if elapsed < 100 else "🟡 Good" if elapsed < 300 else "🔴 Slow"
                await msg.edit(f"✅ <b>Ping successful</b>\n\n⏱️ <b>Latency:</b> <code>{elapsed:.2f} ms</code>\n🔗 <b>URL:</b> <code>{url}</code>\n📊 <b>Status:</b> {status}")
    except Exception as e:
        await msg.edit(f"❌ <b>Ping failed</b>\n\n⚠️ <b>Error:</b> <code>{str(e)}</code>\n🔗 <b>URL:</b> <code>{url}</code>\n\n💡 Check if the URL is correct and accessible.")

# TCP connectivity test
@Client.on_message(filters.command("tcp", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def tcp_test(client: Client, message: Message):
    args = message.text.split()
    if len(args) < 3:
        await edit_or_reply(message, f"❌ **Invalid format**\n\n💡 **Usage:** `{HARDCODED_PREFIXES[0]}tcp <host> <port>`\n📝 **Example:** `{HARDCODED_PREFIXES[0]}tcp google.com 443`")
        return
    host, port = args[1], int(args[2])
    msg = await edit_or_reply(message, f"🔌 **Testing TCP connection...**\n\n🎯 <b>Host:</b> <code>{host}</code>\n🔌 <b>Port:</b> <code>{port}</code>\n\n⏳ Please wait...")
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
        writer.close()
        await writer.wait_closed()
        await msg.edit(f"✅ <b>TCP connection successful</b>\n\n🎯 <b>Host:</b> <code>{host}</code>\n🔌 <b>Port:</b> <code>{port}</code>\n✅ <b>Status:</b> Reachable\n\n💡 The server is online and accepting connections.")
    except Exception as e:
        await msg.edit(f"❌ <b>TCP connection failed</b>\n\n🎯 <b>Host:</b> <code>{host}</code>\n🔌 <b>Port:</b> <code>{port}</code>\n⚠️ <b>Error:</b> <code>{str(e)}</code>\n\n💡 The server might be offline or blocking connections.")

# Async speedtest
@Client.on_message(filters.command("speed", prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def async_speedtest(client: Client, message: Message):
    msg = await edit_or_reply(message, "📡 **Running speedtest...**\n\n⏳ This may take 30-60 seconds\n🔍 Finding best server...")
    try:
        loop = asyncio.get_event_loop()
        st = speedtest.Speedtest()
        await loop.run_in_executor(None, st.get_best_server)
        download = await loop.run_in_executor(None, st.download)
        upload = await loop.run_in_executor(None, st.upload)
        
        download_mbps = download / 1_000_000
        upload_mbps = upload / 1_000_000
        
        await msg.edit(f"📡 <b>Speedtest Results</b>\n\n"
                       f"🔽 <b>Download:</b> <code>{download_mbps:.2f} Mbps</code>\n"
                       f"🔼 <b>Upload:</b> <code>{upload_mbps:.2f} Mbps</code>\n\n"
                       f"📊 <b>Quality:</b> {'Excellent ✅' if download_mbps > 50 else 'Good 🟡' if download_mbps > 10 else 'Fair 🔴'}")
    except Exception as e:
        await msg.edit(f"❌ <b>Speedtest failed</b>\n\n⚠️ <b>Error:</b> <code>{str(e)}</code>\n\n💡 Check your internet connection and try again.")

# Calculator command
@Client.on_message(filters.command(["calc", "calculate"], prefixes=HARDCODED_PREFIXES) & (filters.me | sudoers_filter()))
async def calculator(client: Client, message: Message):
    """Advanced calculator with support for mathematical expressions"""
    try:
        # Get the expression from command
        args = get_args_from_caret(message)
        
        if not args:
            help_text = """
🧮 **Calculator Help**

**Usage:** `{prefix}calc <expression>`

**Supported Operations:**
• Basic: `+`, `-`, `*`, `/`, `%`, `**` (power)
• Functions: `sqrt()`, `sin()`, `cos()`, `tan()`, `log()`, `abs()`
• Constants: `pi`, `e`

**Examples:**
• `{prefix}calc 2 + 2`
• `{prefix}calc sqrt(144)`
• `{prefix}calc 2 ** 8`
• `{prefix}calc sin(pi/2)`
• `{prefix}calc (5 + 3) * 2`
• `{prefix}calc log(100)`

**Advanced:**
• `{prefix}calc 15 % 4` (modulo)
• `{prefix}calc abs(-42)` (absolute value)
• `{prefix}calc pi * 2` (pi constant)
            """.format(prefix=HARDCODED_PREFIXES[0])
            return await edit_or_reply(message, help_text)
        
        # Join all arguments to form the expression
        expression = " ".join(args)
        original_expression = expression
        
        # Create a safe namespace with allowed functions and constants
        safe_namespace = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
            'pow': pow,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'log': math.log,
            'log10': math.log10,
            'log2': math.log2,
            'exp': math.exp,
            'floor': math.floor,
            'ceil': math.ceil,
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            'degrees': math.degrees,
            'radians': math.radians,
            'factorial': math.factorial,
            'gcd': math.gcd,
        }
        
        # Replace common notation
        expression = expression.replace('^', '**')
        expression = expression.replace('×', '*')
        expression = expression.replace('÷', '/')
        
        # Evaluate the expression safely
        try:
            # Parse the expression as an AST
            parsed = ast.parse(expression, mode='eval')
            
            # Check for dangerous operations
            for node in ast.walk(parsed):
                if isinstance(node, (ast.Import, ast.ImportFrom, ast.Call)):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            if node.func.id not in safe_namespace:
                                return await edit_or_reply(
                                    message,
                                    f"❌ **Unsafe operation detected**\n\n"
                                    f"⚠️ Function `{node.func.id}` is not allowed\n\n"
                                    f"💡 Use `{HARDCODED_PREFIXES[0]}calc` for available functions"
                                )
            
            # Evaluate the expression
            result = eval(compile(parsed, '<string>', 'eval'), {"__builtins__": {}}, safe_namespace)
            
            # Format the result
            if isinstance(result, float):
                # Round to 10 decimal places to avoid floating point errors
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # Determine result type for display
            result_type = type(result).__name__
            
            # Create response
            response = f"🧮 **Calculator**\n\n"
            response += f"📝 **Expression:** `{original_expression}`\n"
            response += f"✅ **Result:** `{result}`\n"
            
            # Add additional info for certain results
            if isinstance(result, (int, float)):
                if result > 1000000:
                    response += f"📊 **Scientific:** `{result:.2e}`\n"
                if isinstance(result, float) and not result.is_integer():
                    response += f"🔢 **Type:** Decimal\n"
                elif isinstance(result, int):
                    response += f"🔢 **Type:** Integer\n"
                    # Add binary and hex for integers
                    if 0 <= result <= 1000000:
                        response += f"💾 **Binary:** `{bin(result)}`\n"
                        response += f"🔣 **Hex:** `{hex(result)}`\n"
            
            await edit_or_reply(message, response)
            
        except ZeroDivisionError:
            await edit_or_reply(
                message,
                f"❌ **Division by zero**\n\n"
                f"📝 **Expression:** `{original_expression}`\n\n"
                f"⚠️ Cannot divide by zero\n\n"
                f"💡 Check your expression and try again"
            )
        except ValueError as e:
            await edit_or_reply(
                message,
                f"❌ **Invalid value**\n\n"
                f"📝 **Expression:** `{original_expression}`\n\n"
                f"⚠️ **Error:** `{str(e)}`\n\n"
                f"💡 Check if your values are in valid range"
            )
        except SyntaxError:
            await edit_or_reply(
                message,
                f"❌ **Syntax error**\n\n"
                f"📝 **Expression:** `{original_expression}`\n\n"
                f"⚠️ Invalid mathematical expression\n\n"
                f"💡 **Tips:**\n"
                f"• Use parentheses for grouping: `(2+3)*4`\n"
                f"• Use ** for power: `2**8`\n"
                f"• Check function syntax: `sqrt(16)`"
            )
        except NameError as e:
            await edit_or_reply(
                message,
                f"❌ **Unknown function or variable**\n\n"
                f"📝 **Expression:** `{original_expression}`\n\n"
                f"⚠️ **Error:** `{str(e)}`\n\n"
                f"💡 Use `{HARDCODED_PREFIXES[0]}calc` to see available functions"
            )
            
    except Exception as e:
        await edit_or_reply(
            message,
            f"❌ **Calculator error**\n\n"
            f"⚠️ **Error:** `{str(e)}`\n\n"
            f"💡 Use `{HARDCODED_PREFIXES[0]}calc` for help and examples"
        )

# Userbot.py Commands and Categories
userbot_commands = {
    'me': '**User Status** - Check your userbot status, current points, and account information.\n\n**Usage:** `[prefix]me` or `[prefix]me [user_id]`\n**Example:** `[prefix]me` or reply to a message with `[prefix]me`',
    'addsudo': '**Admin Control** - Add a user to the sudoers list with elevated permissions.\n\n**Usage:** `[prefix]addsudo [user_id/@username]` or reply to message\n**Example:** `[prefix]addsudo 123456789` or reply with `[prefix]addsudo`',
    'rmsudo': '**Admin Control** - Remove a user from the sudoers list.\n\n**Usage:** `[prefix]rmsudo [user_id/@username]` or reply to message\n**Example:** `[prefix]rmsudo 123456789` or reply with `[prefix]rmsudo`',
    'listsudo': '**Admin Control** - List all users in the sudoers list with their user IDs and total count.\n\n**Usage:** `[prefix]listsudo`',
    'acceptall': '**Group Management** - Accept all pending group invite requests at once.\n\n**Usage:** `[prefix]acceptall`\n**Note:** Works in groups where you have admin permissions',
    'ocr': '**Text Recognition** - Extract text from images using OCR technology.\n\n**Usage:** `[prefix]ocr` (reply to an image)\n**Example:** Reply to a screenshot with `[prefix]ocr`',
    'vc1': '**Voice Chat** - Start a group voice chat to enable voice communication.\n\n**Usage:** `[prefix]vc1`\n**Note:** Requires admin permissions in the group',
    'vc0': '**Voice Chat** - End the active group voice chat.\n\n**Usage:** `[prefix]vc0`\n**Note:** Requires admin permissions in the group',
    'ban': '**User Management** - Ban a user from the chat with optional message deletion.\n\n**Usage:** `[prefix]ban [reply|@username|user_id] [-d/--delete]`\n**Example:** `[prefix]ban @spammer -d` (bans and deletes messages)',
    'banall': '**User Management** - Ban all users from the chat (use with caution).\n\n**Usage:** `[prefix]banall`\n**Warning:** This will ban all members except admins',
    'unbanall': '**User Management** - Unban all previously banned users from the chat.\n\n**Usage:** `[prefix]unbanall`\n**Note:** Restores access for all banned users',
    'kick': '**User Management** - Remove a user from the chat (they can rejoin).\n\n**Usage:** `[prefix]kick [reply|@username|user_id]`\n**Example:** `[prefix]kick @troublemaker`',
    'mute': '**User Management** - Mute a user to prevent them from sending messages.\n\n**Usage:** `[prefix]mute [reply|@username|user_id] [-m/--media]`\n**Example:** `[prefix]mute @spammer -m` (media-only mute)',
    'unban': '**User Management** - Unban a previously banned user from the chat.\n\n**Usage:** `[prefix]unban [reply|@username|user_id]`\n**Example:** `[prefix]unban @user123`',
    'promote': '**User Management** - Promote a user with specific admin privileges.\n\n**Usage:** `[prefix]promote [reply|@username|user_id] [flags] [title]`\n**Flags:** -all (all privileges), -d (delete), -r (restrict), -i (invite), -p (pin), -c (change info), -v (video chats), -t (topics), -m (manage)\n**Example:** `[prefix]promote @user -d -r -i Moderator`',
    'pin': '**Message Management** - Pin a message to the top of the chat.\n\n**Usage:** `[prefix]pin [-s/--sound]` (reply to message)\n**Example:** `[prefix]pin -s` (pins with notification sound)',
    'unpin': '**Message Management** - Unpin the currently pinned message.\n\n**Usage:** `[prefix]unpin`\n**Note:** Removes the pinned message from the top',

    'qt': '**Quote Generator** - Create beautiful quotes from messages with custom formatting.\n\n**Usage:** `[prefix]qt [-r] [-f custom_text]` (reply to message)\n**Example:** `[prefix]qt -r` (includes reply), `[prefix]qt -f "Custom quote"`',
    'setalivetext': '**Alive Customization** - Set custom text for your userbot\'s alive status.\n\n**Usage:** `[prefix]setalivetext [text]` or reply to message\n**Example:** `[prefix]setalivetext I am online and ready!`',
    'alive': '**Status Check** - Check if your userbot is alive and operational.\n\n**Usage:** `[prefix]alive`\n**Note:** Shows current status and uptime information',
    'resetallalive': '**Alive Reset** - Reset all alive settings (text, emoji) to default values.\n\n**Usage:** `[prefix]resetallalive`\n**Note:** Removes all custom alive configurations',
    'approve': '**User Approval** - Approve a user in private chat, granting them access.\n\n**Usage:** `[prefix]approve` (in private chat)\n**Note:** Adds user to whitelist, prevents auto-blocking',
    'disapprove': '**User Disapproval** - Remove a user from approved list, they will be blocked after 5 messages.\n\n**Usage:** `[prefix]disapprove` (in private chat)\n**Note:** Removes user from whitelist',
    'rmall': '**Bulk Management** - Remove all users from the approved users list.\n\n**Usage:** `[prefix]rmall`\n**Warning:** This will remove all approved users',
    'rst': '**Message Reset** - Reset message count for a specific user in private chat.\n\n**Usage:** `[prefix]rst` (in private chat)\n**Note:** Resets their message counter to 0',
    'rstall': '**Bulk Reset** - Reset message counts for all users in private chats.\n\n**Usage:** `[prefix]rstall`\n**Warning:** This will reset all user message counters',
    'setemoji': '**Alive Customization** - Set a custom emoji for your userbot\'s alive status.\n\n**Usage:** `[prefix]setemoji [emoji]`\n**Example:** `[prefix]setemoji 🚀`',
    'tiny': '**Image Resizer** - Reduce image size by replying to any photo or sticker.\n\n**Usage:** `[prefix]tiny` (reply to image/sticker)\n**Note:** Compresses images while maintaining quality',
    'mmf': '**Image Text** - Add custom text to images by replying to any media.\n\n**Usage:** `[prefix]mmf [text]` (reply to image)\n**Example:** `[prefix]mmf Hello World` (reply to photo)',
    'kang': '**Sticker Cloner** - Clone and save stickers, videos, or photos to your collection.\n\n**Usage:** `[prefix]kang [pack_name] [emoji]` (reply to media)\n**Example:** `[prefix]kang MyPack 😀` (reply to sticker)',
    'ping': '**Ping Test** - Check bot response time and connection status.\n\n**Usage:** `[prefix]ping`\n**Note:** Shows latency and response time',
    'stats': '**Account Statistics** - View detailed statistics about your account and bot usage.\n\n**Usage:** `[prefix]stats`\n**Features:** User count, group count, message stats, uptime',
    'clone': '**Profile Cloner** - Clone another user\'s profile (name, bio, profile picture).\n\n**Usage:** `[prefix]clone [user_id/@username]`\n**Example:** `[prefix]clone @target_user`',
    'revert': '**Profile Restore** - Restore your original profile details after cloning.\n\n**Usage:** `[prefix]revert`\n**Note:** Undoes the last cloning operation',
    'raid': '**User Raid** - Initiate a raid on a specific user with multiple messages.\n\n**Usage:** `[prefix]raid [count] [user_id/@username]`\n**Example:** `[prefix]raid 10 @spammer`\n**Warning:** Use responsibly',
    'dmspam': '**DM Spam** - Spam a user in their personal messages (DM) - works in groups.\n\n**Usage:** `[prefix]dmspam [count] [message]` (reply to user)\n**Example:** Reply to a user and use `[prefix]dmspam 5 Hello`\n**Note:** Only works in group chats, sends messages to user\'s DM',
    'dmraid': '**DM Raid** - Raid a user in their personal messages (DM) with random raid messages.\n\n**Usage:** `[prefix]dmraid [count]` (reply to user)\n**Example:** Reply to a user and use `[prefix]dmraid 10`\n**Note:** Only works in group chats, sends raid messages to user\'s DM',
    'wordseek': '**WordSeek Auto-Play** - Show WordSeek auto-play info and trigger words.\n\n**Usage:** `[prefix]wordseek`\n**Note:** Use any trigger word to start auto-play',
    'gameinfo': '**WordSeek Game Info** - Show current WordSeek auto-game status and hints.\n\n**Usage:** `[prefix]gameinfo`\n**Note:** Works only when an auto-game is active',
    'invite2vc': '**Voice Chat Invite** - Invite all group members to join the voice chat.\n\n**Usage:** `[prefix]invite2vc`\n**Note:** You must be in the voice chat first',
    'spam': '**Message Spam** - Send multiple messages at once with controlled timing.\n\n**Usage:** `[prefix]spam [count] [message]`\n**Example:** `[prefix]spam 5 Hello World`\n**Warning:** Use responsibly',
    'statspam': '**Smart Spam** - Spam with 0.1s delay and auto-delete old messages.\n\n**Usage:** `[prefix]statspam [count] [message]`\n**Example:** `[prefix]statspam 10 Test message`',
    'slowspam': '**Slow Spam** - Spam messages with 2-second delay between each message.\n\n**Usage:** `[prefix]slowspam [count] [message]`\n**Example:** `[prefix]slowspam 5 Slow message`',
    'fastspam': '**Fast Spam** - Spam messages with no delay (maximum speed).\n\n**Usage:** `[prefix]fastspam [count] [message]`\n**Example:** `[prefix]fastspam 20 Fast message`\n**Warning:** Very fast, use carefully',
    'dspam': '**Delayed Spam** - Spam messages with custom delay between messages.\n\n**Usage:** `[prefix]dspam [count] [delay_seconds] [message]`\n**Example:** `[prefix]dspam 10 3 Delayed message`',
    'afk': '**AFK Mode** - Set yourself as away from keyboard with a reason.\n\n**Usage:** `[prefix]afk [reason]`\n**Example:** `[prefix]afk Going to sleep`\n**Note:** Auto-replies when mentioned',
    'unafk': '**AFK Return** - Return from AFK mode and resume normal activity.\n\n**Usage:** `[prefix]unafk`\n**Note:** Disables AFK auto-replies',
    'tagall': '**Member Tagging** - Tag group members with various filtering options.\n\n**Usage:** `[prefix]tagall [options] [message]`\n**Options:** -adm (admins only), -act (active users), -(1-4) (limit users), -usr (users without admins)\n**Example:** `[prefix]tagall -adm Hello admins!`',
    'cancel': '**Tagging Cancel** - Cancel ongoing member tagging operation.\n\n**Usage:** `[prefix]cancel`\n**Note:** Stops the current tagging process',
    'calc': '**Calculator** - Perform mathematical calculations with support for advanced functions.\n\n**Usage:** `[prefix]calc <expression>`\n**Supported:** Basic math (+, -, *, /, %, **), trigonometry (sin, cos, tan), logarithms (log, log10), square root (sqrt), constants (pi, e)\n**Examples:**\n• `[prefix]calc 2 + 2`\n• `[prefix]calc sqrt(144)`\n• `[prefix]calc sin(pi/2)`\n• `[prefix]calc 2**8`\n**Note:** Use `[prefix]calc` without arguments for full help',
    'gemini': '**AI Commands** - Access Google Gemini AI for various tasks.\n\n**Available Commands:**\n• `[prefix]chat` - General conversation\n• `[prefix]reason` - Logical problem-solving\n• `[prefix]summarize` - Text summarization\n• `[prefix]translate` - Language translation\n• `[prefix]code` - Code generation/fixing\n• `[prefix]write` - Content creation\n• `[prefix]analysis` - Data analysis\n• `[prefix]answer` - Q&A responses\n• `[prefix]complete` - Text completion\n• `[prefix]extract` - Information extraction\n\n**Usage:** `[prefix]command [text]` or reply to message\n**Example:** `[prefix]chat Hello, how are you?`',
        'chat': '**AI Chat** - Have a general conversation with Gemini AI.\n\n**Usage:** `[prefix]chat [text]` or reply to message\n**Example:** `[prefix]chat Hello, how are you?`',
        'reason': '**AI Reasoning** - Get logical problem-solving and reasoning from Gemini AI.\n\n**Usage:** `[prefix]reason [text]` or reply to message\n**Example:** `[prefix]reason Why is the sky blue?`',
        'summarize': '**AI Summarize** - Summarize long text into concise form.\n\n**Usage:** `[prefix]summarize [text]` or reply to message\n**Example:** Reply to a long message with `[prefix]summarize`',
        'translate': '**AI Translate** - Translate text to another language.\n\n**Usage:** `[prefix]translate [text]` or reply to message\n**Example:** `[prefix]translate Translate this to Spanish: Hello`',
        'code': '**AI Code** - Generate or fix code with AI assistance.\n\n**Usage:** `[prefix]code [description]` or reply to message\n**Example:** `[prefix]code Write a Python function to sort a list`',
        'write': '**AI Write** - Create content, essays, or articles.\n\n**Usage:** `[prefix]write [topic]` or reply to message\n**Example:** `[prefix]write Write a poem about nature`',
        'analysis': '**AI Analysis** - Analyze data, text, or situations.\n\n**Usage:** `[prefix]analysis [text]` or reply to message\n**Example:** `[prefix]analysis Analyze this market trend`',
        'answer': '**AI Answer** - Get direct answers to questions.\n\n**Usage:** `[prefix]answer [question]` or reply to message\n**Example:** `[prefix]answer What is quantum computing?`',
        'complete': '**AI Complete** - Complete partial text or sentences.\n\n**Usage:** `[prefix]complete [text]` or reply to message\n**Example:** `[prefix]complete Once upon a time`',
        'extract': '**AI Extract** - Extract specific information from text.\n\n**Usage:** `[prefix]extract [text]` or reply to message\n**Example:** `[prefix]extract Extract all email addresses from this text`',
    'schedule': '**Message Scheduler** - Schedule messages to be sent at specific date and time (IST).\n\n**Usage:** `[prefix]schedule [date] [time] [message]`\n**Example:** `[prefix]schedule 2024-01-01 12:00 Happy New Year!`',
    'purge': '**Message Purge** - Delete all messages from replied message to the last message.\n\n**Usage:** `[prefix]purge` (reply to starting message)\n**Warning:** This will delete all messages in the range',
    'set': '**Quick Settings** - Open settings menu in inline chat format.\n\n**Usage:** `[prefix]set`\n**Note:** Quick access to bot settings',
    'gcast': '**Global Broadcast** - Broadcast message to all chats (private/group/all).\n\n**Usage:** `[prefix]gcast [-pvt/-grp/-all] [message]` or reply to message\n**Example:** `[prefix]gcast -all Hello everyone!`',
    'addbl': '**Broadcast Blocklist** - Add chat to broadcast blocklist to exclude from broadcasts.\n\n**Usage:** `[prefix]addbl [chat_id]` or use in target chat\n**Example:** `[prefix]addbl -1001234567890`',
    'rmbl': '**Broadcast Unblock** - Remove chat from broadcast blocklist.\n\n**Usage:** `[prefix]rmbl [chat_id]` or use in target chat\n**Example:** `[prefix]rmbl -1001234567890`',
    'blist': '**Blocklist View** - Show all chats in the broadcast blocklist.\n\n**Usage:** `[prefix]blist`\n**Note:** Displays blocked chat IDs and names',
    'clr': '**Game Reset** - Clear used words from the word chain game.\n\n**Usage:** `[prefix]clr`\n**Note:** Resets the word chain game memory',
    'replyraid': '**Reply Raid** - Activate reply raid on a specific user.\n\n**Usage:** `[prefix]replyraid [user_id/@username]` or reply to message\n**Example:** `[prefix]replyraid @target_user`\n**Warning:** Use responsibly',
    'dreplyraid': '**Reply Raid Stop** - Deactivate reply raid on a specific user.\n\n**Usage:** `[prefix]dreplyraid [user_id/@username]` or reply to message\n**Example:** `[prefix]dreplyraid @target_user`',
    'sg': '**User History** - Get user history using @SangMata_beta_bot.\n\n**Usage:** `[prefix]sg` (reply to user message)\n**Note:** Shows username and name history',
    'del': '**Message Delete** - Delete the replied message.\n\n**Usage:** `[prefix]del` (reply to message)\n**Note:** Removes the specific message',
    'delall': '**Bulk Delete** - Delete all messages from the replied user.\n\n**Usage:** `[prefix]delall` (reply to user message)\n**Warning:** Deletes all messages from that user',
    'gemini_help': '**AI Help** - Get detailed information about Gemini AI commands.\n\n**Usage:** `[prefix]gemini_help`\n**Note:** Shows all available AI commands and examples',
    'pingurl': '**URL Ping** - Measure response time for a specific URL.\n\n**Usage:** `[prefix]pingurl [url]`\n**Example:** `[prefix]pingurl https://google.com`\n**Default:** Tests Google if no URL provided',
    'tcp': '**TCP Test** - Test TCP connectivity to a host and port.\n\n**Usage:** `[prefix]tcp <host> <port>`\n**Example:** `[prefix]tcp google.com 80`\n**Note:** Tests network connectivity',
    'speed': '**Speed Test** - Run comprehensive network speed test.\n\n**Usage:** `[prefix]speed`\n**Features:** Download/upload speed, latency, connection quality',
    'info': '**User Information** - Get detailed information about a user.\n\n**Usage:** `[prefix]info` (reply to message) or `[prefix]info [user_id/@username]`\n**Example:** Reply to a message with `[prefix]info`',
    'admins': '**Admin List** - List all group admins with their last message information.\n\n**Usage:** `[prefix]admins`\n**Note:** Shows admin list with activity status',
    'sessions': '**Session Info** - List all active sessions with detailed connection information.\n\n**Usage:** `[prefix]sessions`\n**Note:** Shows active userbot sessions and their status',
    'unmute': '**User Unmute** - Unmute a previously muted user.\n\n**Usage:** `[prefix]unmute [reply|@username|user_id]`\n**Example:** `[prefix]unmute @user123`',
    'eval': '**Code Evaluation** - Execute Python code safely.\n\n**Usage:** `[prefix]eval [code]`\n**Example:** `[prefix]eval print("Hello World")`\n**Warning:** Use with caution',
    'help': '**Help System** - View command details and category overview.\n\n**Usage:** `[prefix]help` (show all categories) or `[prefix]help <command>`\n**Example:** `[prefix]help ban`\n**Note:** Works with any command name',
    'react': '**Auto React** - Control automatic emoji reactions when mentioned.\n\n**Usage:** `[prefix]react <on/off/emoji_number>`\n**Options:** `on` (enable), `off` (disable), `1`-`4` (select emoji)\n**Example:** `[prefix]react on`',
    'reactlist': '**React Emojis** - Show available reaction emojis.\n\n**Usage:** `[prefix]reactlist`\n**Note:** Displays emoji options for react command',
    'unpin': '**Unpin Message** - Unpin a pinned message in the group.\n\n**Usage:** `[prefix]unpin` (reply to pinned msg) or `[prefix]unpin --all`\n**Example:** `[prefix]unpin --all` (unpin all messages)',
    'calc': '**Calculator** - Evaluate mathematical expressions.\n\n**Usage:** `[prefix]calc <expression>`\n**Supported:** +, -, *, /, %, **, sqrt, sin, cos, tan, log, pi, e\n**Example:** `[prefix]calc sqrt(144) + sin(pi/2)`',
}

userbot_categories = {
    '👤 USER INFO': ['info', 'sg', 'me', 'stats', 'sessions'],
    '🔄 PROFILE': ['clone', 'revert'],
    '💾 MEDIA SAVER': ['wow', 'link'],
    '🎨 STICKERS & MEDIA': ['qt', 'tiny', 'mmf', 'kang'],
    '🔍 TEXT RECOGNITION': ['ocr'],
    '💚 ALIVE STATUS': ['alive', 'setemoji', 'setalivetext', 'resetallalive'],
    '🗑️ MESSAGE MANAGEMENT': ['purge', 'del', 'delall'],

    '👋 WELCOME SYSTEM': ['approve', 'disapprove', 'rmall', 'rst', 'rstall'],
    '📢 BROADCASTING': ['gcast', 'addbl', 'rmbl', 'blist'],
    '👑 GROUP MANAGEMENT': ['ban', 'banall', 'unbanall', 'kick', 'mute', 'unmute', 'unban', 'promote', 'pin', 'unpin', 'admins', 'acceptall'],
    '⚙️ BOT SETTINGS': ['set'],
    '🎤 VOICE CHAT': ['vc0', 'vc1', 'invite2vc'],
    '🏷️ MEMBER TAGGING': ['tagall', 'cancel'],
    '⚔️ RAID & SPAM': ['raid', 'dmspam', 'dmraid', 'replyraid', 'dreplyraid', 'spam', 'dspam', 'statspam', 'slowspam', 'fastspam'],
    '⏰ SCHEDULING': ['schedule'],
    '👑 ADMIN CONTROL': ['addsudo', 'rmsudo', 'listsudo'],
    '🤖 AI COMMANDS': [],
    '🎮 GAMES': ['clr', 'wordseek', 'gameinfo'],
    '😴 AFK SYSTEM': ['afk', 'unafk'],
    '🌐 NETWORK TOOLS': ['ping', 'pingurl', 'tcp', 'speed', 'calc'],
    '⚙️ DEVELOPMENT': ['eval'],
    '💬 REACTIONS': ['react', 'reactlist'],
    '📖 HELP': ['help'],
}

# Update global commands and categories
commands.update(userbot_commands)
categories.update(userbot_categories)
