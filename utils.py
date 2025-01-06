import asyncio
import discord

def extract_image_url(content: str) -> str:
    words = content.split()
    for word in words:
        if word.startswith('http') and ('png' in word or 'jpg' in word or 'jpeg' in word):
            return word
    return None

async def send_response_in_chunks(message: discord.Message, response: str):
    chunk_size = 1900
    for i in range(0, len(response), chunk_size):
        chunk = response[i:i + chunk_size]
        await message.reply(chunk)
        await asyncio.sleep(0.5)

async def convert_webp_url_to_png(url: str) -> str:
    return url.replace("&format=webp", "&format=png")
