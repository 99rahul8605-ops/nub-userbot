import os

# Telegram API credentials
API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

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

GROUP = os.getenv('GROUP', 'nub_coder_s')
CHANNEL = os.getenv('CHANNEL', 'nub_coders')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
SESSION_STR = os.getenv('SESSION_STR', '')
USERBOT_USERNAME = os.getenv('USERBOT_USERNAME', '')
apps= {}