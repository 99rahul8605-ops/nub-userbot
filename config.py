import os

# Telegram API credentials
# Required: Get these from https://my.telegram.org
API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')

# Gemini API configuration
# Optional: Get from https://aistudio.google.com/app/apikey (needed for AI features)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Optional: NUBYTDLP API Key for YouTube downloads
NUBYTDLP_API = os.getenv('NUBYTDLP_API', '')

# Global variables
clients = {}
RAIDS = {}
conversations = {}
chat_queues = {}
active_streams = {}
last_response_time = {}
used_words = {}
active = {}
songs_client = {}
IGNORE_DURATION = 5
StartTime = time.time()

ggg = os.getcwd()
from fonts import *
from pyrogram import Client, filters
from convopyro import Conversation

# Optional: Your support group username (without @)
GROUP = os.getenv('GROUP', 'nub_coder_s')

# Optional: Your updates channel username (without @)
CHANNEL = os.getenv('CHANNEL', 'nub_coders')

# Optional: Get from @BotFather on Telegram (used for inline bot features)
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# Required: Your Pyrogram String Session
SESSION_STR = os.getenv('SESSION_STR', '')

# Optional: The username of your userbot account (without @) to use in menus
USERBOT_USERNAME = os.getenv('USERBOT_USERNAME', '')
apps= {}