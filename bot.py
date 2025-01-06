import discord
from discord.ext import commands
from config import COMMAND_PREFIX, INTENTS
from command_handlers import handle_roast_command, handle_regular_conversation
import logging

logger = logging.getLogger(__name__)

def setup_bot() -> commands.Bot:
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=INTENTS)

    @bot.event
    async def on_ready():
        logger.info(f'{bot.user} has connected to Discord!')

    @bot.event
    async def on_message(message):
        # Ignore messages from any bot, including this one
        if message.author.bot:
            return

        # Only respond to messages that mention the bot
        if bot.user not in message.mentions:
            return

        logger.info(f"Processing message from {message.author}: {message.content}")

        async with message.channel.typing():
            try:
                if message.content.lower().startswith('!roast'):
                    await handle_roast_command(message)
                else:
                    await handle_regular_conversation(message, bot.user)
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}", exc_info=True)
                await message.reply("I encountered an error. Please try again later.")
    
    return bot
