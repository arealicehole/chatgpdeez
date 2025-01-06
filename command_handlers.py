import discord
from grok_client import GrokClient
from message_history import MessageHistory
from config import XAI_API_KEY, TOOLS_DEFINITION
from utils import extract_image_url, send_response_in_chunks
import logging

logger = logging.getLogger(__name__)

async def handle_roast_command(message: discord.Message):
    image_url = extract_image_url(message.content)
    if not image_url:
        await message.reply("Please provide an image URL for roasting.")
        return

    async with GrokClient(XAI_API_KEY) as grok:
        analysis_result = await grok.analyze_image(image_url)
        roast_prompt = f"Based on this image analysis: {analysis_result}\nNow, roast the subject of the image in the style of ChatGPDeez."
        response = await grok.get_response([{"role": "user", "content": roast_prompt}], model="grok-2-1212")
        
    await send_response_in_chunks(message, response)

async def handle_regular_conversation(message: discord.Message, bot_user: discord.ClientUser):
    if message.author.bot:
        return

    history = MessageHistory()
    conversation = await history.get_conversation_history(message.channel, bot_user)

    async with GrokClient(XAI_API_KEY) as grok:
        if any(message.attachments) or 'http' in message.content:
            image_url = extract_image_url(message.content) or message.attachments[0].url
            analysis_result = await grok.analyze_image(image_url)
            conversation.append({"role": "system", "content": f"Image analysis: {analysis_result}"})
        
        response = await grok.get_response(conversation, tools=TOOLS_DEFINITION, tool_choice="auto")
    
    await send_response_in_chunks(message, response)