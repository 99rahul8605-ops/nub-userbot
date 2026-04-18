
from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from tools import *

@Client.on_message(filters.command("me") & filters.me)
@retry()
async def inline_handler(client, message):
    try:
        # Get inline bot results
        results = await client.get_inline_bot_results(app.me.username, query="")
        
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
            await message.reply("No inline results found.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")


@Client.on_message(filters.command("set") & filters.me)
@retry()
async def inline_handler1(client, message):
    try:
        # Get inline bot results
        results = await client.get_inline_bot_results(app.me.username, query="")

        if results.results:
            # Get the first result ID
            first_result_id = results.results[1].id

            # Send the first inline result
            await client.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=results.query_id,
                result_id=first_result_id
            )
        else:
            await message.reply("No inline results found.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

