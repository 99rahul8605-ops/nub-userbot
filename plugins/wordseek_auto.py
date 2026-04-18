"""
WordSeek Auto-Player Plugin for Userbot
Automatically plays WordSeek Telegram bot games with intelligent solving
"""

import asyncio
import json
import re
import logging
from typing import Dict, Optional
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from plugins.game_solver import get_solver
from tools import *
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Active game states: {chat_id: game_state}
ACTIVE_GAMES: Dict[int, Dict] = {}

# Configuration
CONFIG = {
    'AUTO_DELAY': 4.0,  # Seconds between guesses
    'MAX_GUESSES': 30,
    'MIN_WORD_CONFIDENCE': 0.3,
    'DEBUG_MODE': False,
}

# Trigger words - auto-play only starts when user types one of these
TRIGGER_WORDS = {
    'STARE',
    'SLATE',
    'CRATE',
    'TRADE',
    'BLAZE',
    'CRANE',
    'FLARE',
    'GRACE',
    'SHADE',
    'TRACE',
}

def init_game_state(chat_id: int) -> Dict:
    """Initialize a new game state"""
    return {
        'chat_id': chat_id,
        'known_letters': {},  # {char: [wrong_positions]}
        'excluded_letters': set(),
        'position_hints': {},  # {pos: char}
        'guesses_made': 0,
        'attempts_left': 30,
        'game_active': True,
        'word_solution': None,
        'used_words': [],  # Store all guessed words
        'patterns': {},  # {word: feedback_pattern}
        'waiting_for_reply': False,  # Flag to prevent sending multiple words
        'last_sent_word': None,  # Track the last sent word
    }


def safe_text_preview(text: Optional[str], limit: int = 150) -> str:
    """Safely render text for logging without surrogate slicing errors."""
    if not text:
        return ""
    try:
        clean = text.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")
    except Exception:
        clean = str(text)
    if len(clean) > limit:
        return f"{clean[:limit]}…"
    return clean


def parse_feedback_from_message(message_text: str) -> Optional[dict]:
    """
    Extract all words and their emoji feedback from bot message
    Looks for patterns like: 🟩 🟩 🟥 🟩 🟥 𝗕𝗘𝗔𝗡𝗦
    Returns: {word: feedback_string} dict
    """
    logger.debug(f"[PARSE] Attempting to parse message: {repr(safe_text_preview(message_text, 200))}")
    results = {}
    
    # Pattern: 5 emojis (with or without spaces) followed by a word
    # Match emojis and extract the word after them
    lines = message_text.split('\n')
    logger.debug(f"[PARSE] Split into {len(lines)} lines")
    
    for i, line in enumerate(lines):
        logger.debug(f"[PARSE] Line {i}: {repr(safe_text_preview(line, 200))}")
        # Pattern: emojis followed by a word (including bold Unicode characters)
        # Look for: 🟩 🟩 🟥 🟩 🟥 𝗕𝗘𝗔𝗡𝗦 or 🟩 🟩 🟥 🟩 🟥 BEANS
        emoji_pattern = r'(🟩|🟨|🟥)\s*(🟩|🟨|🟥)\s*(🟩|🟨|🟥)\s*(🟩|🟨|🟥)\s*(🟩|🟨|🟥)\s+([\w\U0001D400-\U0001D7FF]+)'
        match = re.search(emoji_pattern, line)
        
        if match:
            # Reconstruct the feedback string from captured groups
            feedback = ''.join(match.groups()[:5])
            word_raw = match.group(6)
            
            # Convert bold Unicode letters to regular ASCII if needed
            # Bold Unicode letters: 𝗔-𝗭 (U+1D5D4 - U+1D5ED)
            word_ascii = ''
            for char in word_raw:
                # Check if it's a bold Unicode letter
                code = ord(char)
                if 0x1D5D4 <= code <= 0x1D5ED:  # Bold capital A-Z
                    word_ascii += chr(code - 0x1D5D4 + ord('A'))
                elif 0x1D5EE <= code <= 0x1D607:  # Bold lowercase a-z
                    word_ascii += chr(code - 0x1D5EE + ord('a'))
                else:
                    word_ascii += char.upper()
            
            word = word_ascii.upper()
            results[word] = feedback
            logger.info(f"[PARSE] ✓ Parsed: {word} → {feedback} (raw: {word_raw})")
        else:
            logger.debug(f"[PARSE] ✗ No match on line {i}")
    
    logger.info(f"[PARSE] Final results: {results if results else 'None'}")
    return results if results else None


def is_game_over_message(text: str) -> bool:
    """Check if message indicates game is over"""
    game_over_keywords = [
        'Congrats! You guessed it correctly.',
        'game over',
        'the word was',
        'Correct Word:',
        'congratulations',
        'won',
        'lost',
        'no more guesses',
        'out of attempts',
    ]
    
    return any(keyword in text for keyword in game_over_keywords)


def is_game_started_message(text: str) -> bool:
    """Check if message indicates a game has started"""
    start_keywords = [
        'game started',
        'guess the 5',
        'new game',
        'start a new game',
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in start_keywords)


async def wait_for_bot_response(client: Client, chat_id: int, user_message_id: int, timeout: int = 10):
    """
    Wait for supported game bot response with feedback
    Checks if bot has already responded by comparing message IDs
    Returns the bot's message or None if timeout
    """
    try:
        start_time = asyncio.get_event_loop().time()
        logger.info(f"[WAIT] Starting to wait for bot response after message ID {user_message_id}")
        
        check_count = 0
        while True:
            check_count += 1
            # Search for latest messages in chat (not filtering by user since that might fail)
            found_bot_message = False
            latest_msg = None
            
            async for message in client.search_messages(
                chat_id=chat_id,
                limit=10  # Check last 10 messages
            ):
                # Check if this message is from a supported game bot
                if message.from_user and (message.from_user.username or '').lower() in ['wordseekbot', 'crocodilegameenn_bot']:
                    # Check if bot message is newer than user's message
                    if message.id > user_message_id:
                        # Store the latest message (first match since results are in reverse chronological order)
                        if latest_msg is None:
                            latest_msg = message
                            logger.debug(f"[WAIT] Check #{check_count}: Latest bot message ID {message.id}, user message ID {user_message_id}")
                            logger.debug(f"[WAIT] Message preview: {repr(safe_text_preview(message.text, 150))}")
                        # Break after finding latest message - no need to check older ones
                        break
            
            # Only check win condition in the latest message
            if latest_msg:
                # Check if it contains feedback or game over message
                has_emoji = '🟩' in latest_msg.text or '🟨' in latest_msg.text or '🟥' in latest_msg.text
                has_game_over = ('congrats' in latest_msg.text.lower() or 'word was' in latest_msg.text.lower() or
                               'correct word' in latest_msg.text.lower() or 'game over' in latest_msg.text.lower())
                
                logger.debug(f"[WAIT] Latest message check - has_emoji: {has_emoji}, has_game_over: {has_game_over}")
                
                if has_emoji or has_game_over:
                    logger.info(f"[WAIT] ✓ Valid bot response found (ID: {latest_msg.id})")
                    logger.info(f"[WAIT] Full message text:\n{safe_text_preview(latest_msg.text, 2000)}")
                    found_bot_message = True
                    return latest_msg
                else:
                    logger.debug(f"[WAIT] Latest bot message doesn't match criteria")
            
            if not found_bot_message:
                logger.debug(f"[WAIT] Check #{check_count}: No new messages from supported game bots found")
                
            # Check timeout
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= timeout:
                logger.warning(f"[WAIT] Timeout after {check_count} checks waiting for bot response")
                logger.info(f"[WAIT] Last check - searching last 10 messages for debug...")
                async for msg in client.search_messages(chat_id=chat_id, limit=10):
                    username = msg.from_user.username if msg.from_user else 'None'
                    logger.info(
                        f"[WAIT] Debug msg: ID={msg.id}, from={username}, "
                        f"text={repr(safe_text_preview(msg.text, 50)) if msg.text else 'N/A'}"
                    )
                return None
            
            # Wait a bit before checking again
            await asyncio.sleep(1.0)  # Increased from 0.5 to 1.0 second
        
    except Exception as e:
        logger.error(f"[WAIT] Error waiting for response: {e}", exc_info=True)
        return None


async def play_game_loop(client: Client, chat_id: int, initial_message_id: int):
    """
    Main game loop - waits for bot responses and sends next guesses
    """
    if chat_id not in ACTIVE_GAMES:
        logger.warning(f"[LOOP] No active game for chat {chat_id}")
        return
    
    game = ACTIVE_GAMES[chat_id]
    last_user_message_id = initial_message_id
    
    while game['game_active'] and game['attempts_left'] > 0:
        # Wait for bot response
        bot_message = await wait_for_bot_response(client, chat_id, last_user_message_id)
        
        if not bot_message:
            logger.warning(f"[LOOP] No bot response received, stopping game")
            ACTIVE_GAMES.pop(chat_id, None)
            break
        
        # Check if game is over
        if is_game_over_message(bot_message.text):
            logger.info(f"[LOOP] Game ended in chat {chat_id}")
            logger.info(f"[LOOP] Bot message: {bot_message.text[:100]}")
            
            # Extract solution word
            solution_pattern = r'(?:word was:|correct word:)\s*(\w{5})'
            match = re.search(solution_pattern, bot_message.text.lower())
            if match:
                game['word_solution'] = match.group(1)
                logger.info(f"[LOOP] Solution: {game['word_solution']}")
            
            # Clean up
            ACTIVE_GAMES.pop(chat_id, None)
            logger.info(f"[LOOP] Cleaned up game data for chat {chat_id}")
            break
        
        # Handle duplicate-word response (no feedback provided)
        message_lower = (bot_message.text or "").lower()
        if "someone has already guessed your word" in message_lower:
            logger.info("[LOOP] Duplicate word detected; selecting a new guess")
            if game.get('last_sent_word') and game['last_sent_word'] not in game['used_words']:
                game['used_words'].append(game['last_sent_word'])
                logger.info(f"[LOOP] Marked as used: {game['last_sent_word']}")
        else:
            # Parse feedback from bot message
            logger.debug(f"[LOOP] Bot message text: {bot_message.text}")
            feedback = parse_feedback_from_message(bot_message.text)
            
            if not feedback or not isinstance(feedback, dict):
                logger.warning(f"[LOOP] Could not parse feedback from message: {safe_text_preview(bot_message.text, 200)}")
                ACTIVE_GAMES.pop(chat_id, None)
                break
        
            # Process all words found in the message
            for word, word_feedback in feedback.items():
                # Skip if already processed
                if word in game['used_words']:
                    logger.debug(f"[LOOP] Word {word} already processed, skipping")
                    continue
                
                if len(word_feedback) != 5:
                    logger.warning(f"[LOOP] Invalid feedback length for {word}: {word_feedback}")
                    continue
            
                # Store word and pattern
                game['used_words'].append(word)
                game['patterns'][word] = word_feedback
            
                logger.info(f"[LOOP] Feedback: {word} → {word_feedback}")
            
                # Analyze feedback
                solver = get_solver()
                known_letters, excluded_letters, position_hints = solver.analyze_feedback(
                    word, word_feedback
                )
            
                # Update game state
                for ch, positions in known_letters.items():
                    if ch not in game['known_letters']:
                        game['known_letters'][ch] = []
                    for p in positions:
                        if p not in game['known_letters'][ch]:
                            game['known_letters'][ch].append(p)
                            
                game['excluded_letters'].update(excluded_letters)
                game['position_hints'].update(position_hints)
                
                # Cleanup conflicts in case earlier guesses incorrectly excluded a letter
                for ch in game['position_hints'].values():
                    game['excluded_letters'].discard(ch)
                for ch in game['known_letters']:
                    game['excluded_letters'].discard(ch)
                
                game['guesses_made'] += 1
                game['attempts_left'] -= 1
            
            logger.info(f"[LOOP] Guesses made: {game['guesses_made']}/30")
            logger.info(f"[LOOP] Used words: {game['used_words']}")
        
        # Get next guess
        await asyncio.sleep(CONFIG['AUTO_DELAY'])
        
        solver = get_solver()
        candidates = solver.filter_candidates(
            game['known_letters'],
            game['excluded_letters'],
            game['position_hints']
        )
        
        # Filter out already used words
        available_candidates = [w for w in candidates if w not in game['used_words']]
        
        if available_candidates:
            next_guess = solver.get_best_guess(available_candidates, game['position_hints'])
            game['last_sent_word'] = next_guess
            
            logger.debug(f"[LOOP] Next guess: {next_guess} ({len(available_candidates)} candidates)")
            
            # Send the word to the bot
            await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
            logger.info(f"[LOOP] Sending word: '{next_guess}'")
            sent_message = await client.send_message(chat_id, next_guess)
            last_user_message_id = sent_message.id
        else:
            logger.warning(f"[LOOP] No available candidates found!")
            ACTIVE_GAMES.pop(chat_id, None)
            break




@Client.on_message(
    filters.text
    & (filters.user(['wordseekbot', 'crocodilegameenn_bot']) | filters.group)
    & ~filters.incoming
    & filters.command(list(TRIGGER_WORDS), prefixes="")
)
async def auto_play_handler(client: Client, message: Message):
    """Handle auto-play of WordSeek game - trigger words and user input"""
    chat_id = message.chat.id
    text = message.text.strip().upper()
    
    # Skip bot commands
    if text.startswith('/'):
        return
    
    # User sending trigger word
    if text in TRIGGER_WORDS and chat_id not in ACTIVE_GAMES:
        logger.info(f"[AUTO-GAME] Trigger word '{text}' detected, starting auto-play")
        ACTIVE_GAMES[chat_id] = init_game_state(chat_id)
        game = ACTIVE_GAMES[chat_id]
        game['last_sent_word'] = text
        
        logger.info(f"[AUTO-GAME] Sending first word: {text}")
        # The word will be sent as the user's message, we just need to wait for bot reply
        
        # Start game loop with the user's message ID
        await play_game_loop(client, chat_id, message.id)
        return
    
    # Skip if no active game
    if chat_id not in ACTIVE_GAMES:
        return


@Client.on_message(filters.command('gameinfo', prefixes=HARDCODED_PREFIXES))
async def show_game_info(client: Client, message: Message):
    """Show current game information"""
    chat_id = message.chat.id
    
    if chat_id not in ACTIVE_GAMES:
        await message.reply("No active auto-game.")
        return
    
    game = ACTIVE_GAMES[chat_id]
    
    info = f"""
📊 **Game Information**
━━━━━━━━━━━━━━━━━━━
• **Status:** {'Active' if game['game_active'] else 'Ended'}
• **Guesses Made:** {game['guesses_made']}/30
• **Attempts Left:** {game['attempts_left']}
• **Confirmed Letters:** {len(game['position_hints'])}
• **Excluded Letters:** {len(game['excluded_letters'])}
• **Known Letters:** {len(game['known_letters'])}

📍 **Position Hints:**
{', '.join(f'{k}: {v}' for k, v in sorted(game['position_hints'].items())) if game['position_hints'] else 'None'}

🚫 **Excluded:** {', '.join(sorted(game['excluded_letters'])) if game['excluded_letters'] else 'None'}
    """
    
    await message.reply(info)


@Client.on_message(filters.command('wordseek',prefixes=HARDCODED_PREFIXES) & filters.me)
async def wordseek_info(client: Client, message: Message):
    """Show WordSeek auto-play info and trigger words"""
    words = ", ".join(sorted(TRIGGER_WORDS))
    info = (
        "🎮 **WordSeek Auto-Play**\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "• **How to start:** Send any trigger word below\n"
        f"• **Trigger words:** {words}\n"
        "• **Note:** The bot will auto-guess after the first word"
    )
    await message.reply(info)


# Manual guess submission
@Client.on_message(
    filters.text & 
    ~filters.regex(r"^/") & 
    ~filters.incoming
)
async def manual_guess(client: Client, message: Message):
    """Handle manual word guesses in auto-game"""
    chat_id = message.chat.id
    
    # Check if game is won
    if "Congrats! You guessed it correctly." in message.text:
        logger.info(f"[AUTO-GAME] Game won in chat {chat_id}")
        
        # Clean up saved things for this chat
        if chat_id in ACTIVE_GAMES:
            ACTIVE_GAMES.pop(chat_id, None)
            logger.info(f"[AUTO-GAME] Cleaned up game data for chat {chat_id}")
        
        return
    
    if chat_id not in ACTIVE_GAMES:
        return
    
    word = message.text.strip().lower()
    
    # Validate 5-letter word
    if not (len(word) == 5 and word.isalpha()):
        return
    
    game = ACTIVE_GAMES[chat_id]
    game._last_guess = word
    
    logger.info(f"[AUTO-GAME] Manual guess: {word}")


def setup_auto_player(client: Client, config_updates: Optional[Dict] = None):
    """Initialize auto-player with optional config updates"""
    global CONFIG
    
    if config_updates:
        CONFIG.update(config_updates)
    
    logger.info("[AUTO-GAME] Auto-player initialized")
    logger.info(f"[AUTO-GAME] Config: {CONFIG}")


# Export for use
__all__ = [
    'start_auto_game',
    'auto_play_handler',
    'manual_guess',
    'show_game_info',
    'setup_auto_player',
    'ACTIVE_GAMES',
    'CONFIG',
]
