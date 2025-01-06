import os
import discord
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
XAI_API_KEY = os.getenv('XAI_API_KEY')

if not DISCORD_TOKEN or not XAI_API_KEY:
    raise ValueError("Please ensure both DISCORD_TOKEN and XAI_API_KEY are set in your .env file")

# Discord bot configuration
COMMAND_PREFIX = '!'
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.guild_messages = True
INTENTS.guilds = True
INTENTS.members = True
INTENTS.presences = True

# Grok API configuration
TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "vision_analysis",
            "description": "Analyzes an image for content or context.",
            "parameters": {
                "image_url": {
                    "type": "string",
                    "description": "URL of the image to analyze."
                }
            }
        }
    }
]

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
