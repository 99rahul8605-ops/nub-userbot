from pyrogram import Client, filters
from pyrogram.types import Message, MessageEntity
from pyrogram.enums import MessageEntityType
import asyncio
from config import *
from tools import *

def mentioned_me():
    async def func(_, __, message: Message):
        if not message.entities:
            return False

        for entity in message.entities:
            if entity.type == MessageEntityType.MENTION:
                mentioned_user = message.text[entity.offset:entity.offset + entity.length]
                if mentioned_user == f"@{__.me.username}":
                    return True
            elif entity.type == MessageEntityType.TEXT_MENTION:
                if entity.user and entity.user.id == __.me.id:
                    return True
        return False

    return filters.create(func)

react_emojis = ['👍', '♥️', '🔥', '🎉']

@Client.on_message(mentioned_me() & ~filters.bot)
async def auto_react_handler(client: Client, message: Message):
    try:
        user = await client.get_me()
        user_data = user_sessions.find_one({"user_id": user.id})
        if not user_data:
            return

        rc = user_data.get('react_control')
        if not isinstance(rc, int) or not (1 <= rc <= len(react_emojis)):
            return

        selected = react_emojis[rc - 1]

        chat = await client.get_chat(message.chat.id)
        cr = getattr(chat, "available_reactions", None)

        # Case 1: reactions disabled
        if cr is None:
            logger.debug(f"[REACTION] Disabled in chat {message.chat.id} for user {user.id}")
            return

        # Prepare usable emojis list
        if getattr(cr, "reactions", None):
            # Subset of allowed
            available = [r.emoji for r in cr.reactions if getattr(r, "emoji", None)]
        elif getattr(cr, "all_are_enabled", False):
            # All default emojis allowed, use your set
            available = react_emojis.copy()
        else:
            logger.debug(f"[REACTION] No usable reactions in chat {message.chat.id} for user {user.id}")
            return

        if not available:
            logger.debug(f"[REACTION] Empty available list in chat {message.chat.id} for user {user.id}")
            return

        # Determine which emoji to send
        emoji_to_send = selected if selected in available else available[0]

        await client.send_reaction(chat_id=message.chat.id,
                                   message_id=message.id,
                                   emoji=emoji_to_send)

    except Exception as e:
        logger.error(f"[REACTION] Auto-react error for user {client.me.id}: {e}")

# Reaction control commands with dynamic prefix
@Client.on_message(filters.command("react", prefixes=HARDCODED_PREFIXES) & filters.me)
async def react_control_command(client, message):
    """Control auto-reaction settings"""
    # Extract arguments using command args (filters.command automatically handles this)
    args = message.command[1:] if len(message.command) > 1 else []
    
    if not args:
        help_text = (
            f"\n\n╭━━ <emoji id=\"5368324170671202286\">🤖</emoji> REACTION CONTROLS ━━╮\n"
            f"\n"
            f"┃ Commands\n"
            f"┃ ▸ [prefix]react on  — enable reactions\n"
            f"┃ ▸ [prefix]react off — disable reactions\n"
            f"┃ ▸ [prefix]react 1   — set to 👍\n"
            f"┃ ▸ [prefix]react 2   — set to ❤️\n"
            f"┃ ▸ [prefix]react 3   — set to 🔥\n"
            f"┃ ▸ [prefix]react 4   — set to 🎉\n"
            f"┃ ▸ [prefix]react status\n"
            f"\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━━╯"
        )
        await message.edit(help_text)
        return
    
    command = args[0].lower()
    user_id = client.me.id
    
    if command == "on":
        user_sessions.update_one(
            {"user_id": user_id},
            {"$set": {"react_control": 1}},
            upsert=True
        )
        await message.edit(
            f"Reactions Enabled\n\n"
            f"┃ Default reaction: 👍\n"
            f"╰▸ [prefix]react <1-4> to change"
        )
        
    elif command == "off":
        user_sessions.update_one(
            {"user_id": user_id},
            {"$unset": {"react_control": ""}},
            upsert=True
        )
        await message.edit(
            f"Reactions Disabled\n\n"
            f"┃ Auto-reactions turned off\n"
            f"╰▸ [prefix]react on to re-enable"
        )
        
    elif command == "status":
        user_data = user_sessions.find_one({"user_id": user_id})
        if user_data and "react_control" in user_data:
            rc = user_data["react_control"]
            if isinstance(rc, int) and 1 <= rc <= len(react_emojis):
                selected = react_emojis[rc - 1]
                await message.edit(
                    f"╭━━ <emoji id=\"5368324170671202286\">🤖</emoji> REACTION STATUS ━━╮\n"
                    f"┃ Status: <emoji id=\"5368324170671202286\">✅</emoji> Enabled\n"
                    f"┃ Emoji: {selected}\n"
                    f"╰━━━━━━━━━━━━━━━━━━━━━╯"
                )
            else:
                await message.edit(
                    f"╭━━ <emoji id=\"5368324170671202286\">🤖</emoji> REACTION STATUS ━━╮\n"
                    f"┃ Status: <emoji id=\"5368324170671202286\">❌</emoji> Disabled\n"
                    f"╰━━━━━━━━━━━━━━━━━━━━━╯"
                )
        else:
            await message.edit(
                f"╭━━ 🤖 REACTION STATUS ━━╮\n"
                f"┃ Status: ❌ Disabled\n"
                f"╰━━━━━━━━━━━━━━━━━━━━━╯"
            )
            
    elif command.isdigit():
        try:
            reaction_num = int(command)
            if 1 <= reaction_num <= len(react_emojis):
                user_sessions.update_one(
                    {"user_id": user_id},
                    {"$set": {"react_control": reaction_num}},
                    upsert=True
                )
                selected = react_emojis[reaction_num - 1]
                await message.edit(
                    f"Reaction Updated\n\n"
                    f"┃ New Reaction: {selected}"
                )
            else:
                await message.edit(
                    f"Invalid Number\n\n"
                    f"┃ Use 1 to {len(react_emojis)}"
                )
        except ValueError:
            await message.edit(
                f"Invalid Command\n\n"
                f"┃ [prefix]react help for usage"
            )
    else:
        await message.edit(
            f"Invalid Command\n\n"
            f"┃ [prefix]react help for usage"
        )

@Client.on_message(filters.command("reactlist", prefixes=HARDCODED_PREFIXES) & filters.me)
async def react_list_command(client, message):
    """List available reactions"""
    reactions_text = f"╭━━ <emoji id=\"5368324170671202286\">🤖</emoji> AVAILABLE REACTIONS ━━╮\n\n"
    for i, emoji in enumerate(react_emojis, 1):
        reactions_text += f"┃ {str(i)}. {emoji}\n"
    
    reactions_text += f"\n╰▸ [prefix]react <number> to set"
    await message.edit(reactions_text)
