
from pyrogram.raw.functions.contacts import GetBlocked
from config import *
from tools import *

@Client.on_message(filters.command("approve") & filters.private & filters.me)
@retry()
async def approve_user(client, message):
    print("Approving user...")
    chat_id = message.chat.id
    try:
        await client.unblock_user(chat_id)
        print(f"User {chat_id} unblocked.")
    except Exception as e:
        print(f"Error unblocking user {chat_id}: {e}")

    user_data = user_sessions.find_one({"user_id": client.me.id})
    if user_data:
        white_listed = user_data.get('white_listed', [])
        if chat_id not in white_listed:
            user_sessions.update_one(
                {"user_id": client.me.id},
                {"$push": {"white_listed": chat_id}}
            )
            print(f"User {chat_id} added to whitelist.")
            await message.edit_text("You have been approved and added to the whitelist.")
        else:
            print(f"User {chat_id} is already in the whitelist.")
            await message.edit_text("You are already in the whitelist.")
    else:
        user_sessions.insert_one({
            "user_id": client.me.id,
            "white_listed": [chat_id]
        })
        print(f"User {chat_id} added to whitelist (new entry).")
        await message.edit_text("You have been approved and added to the whitelist.")

@Client.on_message(filters.command("addbl") & filters.me)
@retry()
async def add_to_blacklist(client, message):
    chat_id = message.chat.id
    chat = message.chat
    user_data = user_sessions.find_one({"user_id": client.me.id})

    if user_data:
        blocked_list = user_data.get('blocked_list', [])
        if chat_id in blocked_list:
            await message.edit_text(f"{chat.title or chat.first_name} is already in the blacklist.")
            return

        user_sessions.update_one(
            {"user_id": client.me.id},
            {"$push": {"blocked_list": chat_id}}
        )
        await message.edit_text(f"{chat.title or chat.first_name} added to blacklist.")

    else:
        user_sessions.insert_one({
            "user_id": client.me.id,
            "blocked_list": [chat_id]
        })
        await message.edit_text(f"{chat.title or chat.first_name} added to blacklist (new entry).")

@Client.on_message(filters.command("rmbl") & filters.me)
@retry()
async def remove_from_blacklist(client, message: Message):
    user_id = client.me.id
    user_data = user_sessions.find_one({"user_id": user_id})

    blocked_list = user_data.get("blocked_list", [])

    if len(message.command) > 1:  # Chat ID provided as argument
        target_chat_id_str = message.command[1]
        try:
            target_chat_id = int(target_chat_id_str)
        except ValueError:
            await message.reply("Invalid chat ID. Please provide a valid integer.")
            return
        try:
            target_chat = await client.get_chat(target_chat_id)
            chat_title_or_name = target_chat.title or target_chat.first_name
        except Exception as e:
            chat_title_or_name = None

        if target_chat_id in blocked_list:
            user_sessions.update_one({"user_id": user_id}, {"$pull": {"blocked_list": target_chat_id}})
            await message.reply(f"{chat_title_or_name} removed from blacklist.")
        else:
            await message.reply(f"{target_chat_id} not found in blacklist.")

    else:  # Remove current chat from blacklist
        chat_id = message.chat.id
        try:
            chat = await client.get_chat(chat_id)
            chat_title_or_name = chat.title or chat.first_name
        except Exception as e:
            await message.reply(f"Error fetching chat information: {e}")
            return

        if chat_id in blocked_list:
            user_sessions.update_one({"user_id": user_id}, {"$pull": {"blocked_list": chat_id}})
            await message.reply(f"{chat_title_or_name} removed from blacklist.")
        else:
            await message.reply(f"{chat_title_or_name} not found in blacklist.")

@Client.on_message(filters.command("blist") & filters.me)
@retry()
async def show_blacklist(client, message):
    user_data = user_sessions.find_one({"user_id": client.me.id})
    if user_data:
        blocked_list = user_data.get("blocked_list", [])
        if blocked_list:
            await message.reply(f"Blacklisted chats:<blockquote> {', '.join(map(str, blocked_list))}</blockquote>")
        else:
            await message.reply("Blacklist is empty.")
    else:
        await message.reply("No blacklist found for this bot.")

@Client.on_message(filters.command("disapprove") & filters.private & filters.me)
@retry()
async def disapprove_user(client, message):
    chat_id = message.chat.id
    user_data = user_sessions.find_one({"user_id": client.me.id})
    if user_data:
        white_listed = user_data.get('white_listed', [])
        if chat_id in white_listed:
            user_sessions.update_one(
                {"user_id": client.me.id},
                {
                    "$pull": {"white_listed": chat_id},
                    "$set": {f"users.{chat_id}": 0}
                }
            )
            print(f"User {chat_id} removed from whitelist and user count reset.")
            await message.edit_text("You have been removed from the whitelist and your message count has been reset.")
        else:
            print(f"User {chat_id} is not in the whitelist.")
            await message.edit_text("You are not in the whitelist.")
    else:
        print(f"No data found for user_id {client.me.id}.")
        await message.edit_text("No data found for the bot user.")

@Client.on_message(filters.command("rmall") & filters.private & filters.me)
@retry()
async def remove_all_whitelisted_users(client, message):
    print("Removing all whitelisted users...")

    result = user_sessions.update_one(
        {"user_id": client.me.id},
        {"$set": {"white_listed": []}}
    )
    
    if result.modified_count > 0:
        print("All whitelisted users removed.")
        await message.edit_text("All whitelisted users have been removed.")
    else:
        print("No whitelisted users to remove.")
        await message.edit_text("There were no whitelisted users to remove.")

@Client.on_message(filters.command("rstall") & filters.private & filters.me)
@retry()
async def reset_all_users_count(client, message):
    print("Resetting all users' counts to 0...")
    
    user_data = user_sessions.find_one({"user_id": client.me.id})
    if user_data:
        users = user_data.get('users', {})
        for user_id in users.keys():
            if user_id != "total_user_count":  # Ensure we don't reset the total_user_count field
                user_sessions.update_one(
                    {"user_id": client.me.id},
                    {"$set": {f"users.{user_id}": 0}}
                )
        print("All users' counts have been reset to 0.")
        await message.edit_text("All users' message counts have been reset to 0.")
    else:
        print(f"No data found for user_id {client.me.id}.")
        await message.edit_text("No data found for the bot user.")

@Client.on_message(filters.command("rst") & filters.private & filters.me)
@retry()
async def reset_user_count(client, message):
    print("Resetting user count for specific chat...")
    chat_id = str(message.chat.id)  # Ensure chat_id is a string to match MongoDB keys

    user_data = user_sessions.find_one({"user_id": client.me.id})
    if user_data:
        users = user_data.get('users', {})
        if chat_id in users:
            user_sessions.update_one(
                {"user_id": client.me.id},
                {"$set": {f"users.{chat_id}": 0}}
            )
            print(f"User count for {chat_id} has been reset to 0.")
            await message.edit_text(f"Your message count has been reset to 0.")
        else:
            print(f"No count found for {chat_id}.")
            await message.edit_text("No count found for your chat ID.")
    else:
        print(f"No data found for user_id {client.me.id}.")
        await message.edit_text("No data found for the bot user.")

async def get_all_blocked_users(client):
    blocked_users = []
    offset = 0
    limit = 100  # Adjust as needed

    while True:
        blocked = await client.invoke(
            GetBlocked(
                offset=offset,
                limit=limit
            )
        )
        blocked_users.extend(blocked.blocked)
        offset += len(blocked.blocked)

        if len(blocked.blocked) < limit:  # Break if we've fetched all blocked users
            break

    return [user.peer_id.user_id for user in blocked_users if user.peer_id]  # Extract user IDs

async def categorize_blocked_users(client, blocked_user_ids):
    users = []
    bots = []

    if blocked_user_ids:
        # Fetch all user details using get_users
        user_details = await client.get_users(blocked_user_ids)
        for user in user_details:
            if user.is_bot:
                bots.append(user.id)
            else:
                users.append(user.id)

    return users, bots

@Client.on_message(filters.command("stats") & filters.me)
@retry()
async def status(client, message):
    NUB = await message.edit_text("`Collecting stats...`")
    start = datetime.datetime.now()
    u = g = sg = c = b = um = a_chat = up = blocked_bots = blocked_users = approved_users = 0
    progress_msg = ""

    # Fetch approved users from the database
    user_data = user_sessions.find_one({"user_id": client.me.id})
    approved_users_list = user_data.get('white_listed', [])

    # Get all blocked users using the Raw API
    blocked_user_ids = await get_all_blocked_users(client)
    blocked_users_list, blocked_bots_list = await categorize_blocked_users(client, blocked_user_ids)

    async for dialog in client.get_dialogs():
        um += dialog.unread_mentions_count
        up += dialog.unread_messages_count

        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
            # Check if the bot is blocked
            if dialog.chat.id in blocked_bots_list:
                blocked_bots += 1
        elif dialog.chat.type == enums.ChatType.GROUP:
            g += 1
        elif dialog.chat.type == enums.ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(client.me.id))
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chat += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1

        # Count blocked users from the blocklist
        if dialog.chat.id in blocked_users_list:
            blocked_users += 1

        # Count approved users from the database
        if dialog.chat.id in approved_users_list:
            approved_users += 1

        # Update progress message dynamically
        progress_msg = (
            f"<b>`Collecting stats...`\n"
            f"<b>`Private Messages: {u}`\n"
            f"<b>`Groups: {g}`\n"
            f"<b>`Super Groups: {sg}`\n"
            f"<b>`Channels: {c}`\n"
            f"<b>`Admin in: {a_chat} Chats`\n"
            f"<b>`Bots: {b}`\n"
            f"<b>`Blocked Bots: {len(blocked_bots_list)}`\n"
            f"<b>`Blocked Users: {len(blocked_users_list)}`\n"
            f"<b>`Approved Users: {approved_users}`\n"
            f"<b>`Unread Messages: {up}`\n"
            f"<b>`Unread Mentions: {um}`"
        )
        if random.choices([True, False], weights=[1, 10])[0]:
            await NUB.edit_text(progress_msg)

    end = datetime.datetime.now()
    ms = (end - start).seconds

    # Final message with stats
    await NUB.edit_text(
        f"""<b>`Your Stats Obtained in {ms} seconds`
<blockquote><b>`Private Messages = {u}`
<b>`Groups = {g}`
<b>`Super Groups = {sg}`<b>
<b>`Channels = {c}`<b>
<b>`Admin in Chats = {a_chat}`<b>
`<b>Bots</b> = {b}`<b>
`<b>Blocked Bots</b> = {len(blocked_bots_list)}`<b>
`<b>Blocked Users</b> = {len(blocked_users_list)}`
`<b>Approved Users</b> = {approved_users}`
`<b>Unread messages</b> {up}`
`<b>Unread mentions</b> {um}`</blockquote>"""
    )


import datetime
from pyrogram import Client, filters
from pyrogram.raw import functions
from tools import *

def format_timestamp(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%B %d, %Y, %H:%M:%S')

@Client.on_message(filters.command("sessions") & filters.me)
@retry()
async def session_handler(client, message):
    result = await client.invoke(functions.account.GetAuthorizations())
    
    session_info = "**ACTIVE SESSIONS**"
    
    # Iterate through each session and build the session info string
    for session in result.authorizations:
        session_info += (f"""
<blockquote>Device: {session.device_model}</blockquote>
<blockquote>Platform: {session.platform}</blockquote>
<blockquote>App Name: {session.app_name} (Version: {session.app_version}</blockquote>
<blockquote>Country: {session.country}</blockquote>
<blockquote>Current Session: {session.current}</blockquote>
<blockquote>Created On: {format_timestamp(session.date_created)}</blockquote>
<blockquote>Last Active: {format_timestamp(session.date_active)}</blockquote>\n\n""")
    
    # Edit the message with the session details
    await message.edit_text(session_info)
