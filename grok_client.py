import aiohttp
import asyncio
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GrokClient:
    def __init__(self, api_key: str, base_url: str = "https://api.x.ai/v1/chat/completions"):
        self.api_key = api_key
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_response(self, messages: List[Dict[str, str]], model: str = "grok-2-1212", 
                           tools: Optional[List[Dict]] = None, tool_choice: Optional[str] = None, 
                           temperature: float = 0.7, max_retries: int = 3) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        if tools:
            data["tools"] = tools
        if tool_choice:
            data["tool_choice"] = tool_choice

        for attempt in range(max_retries):
            try:
                async with self.session.post(self.base_url, headers=headers, json=data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        raise Exception("Max retries reached")

    async def analyze_image(self, image_url: str, timeout: int = 30) -> str:
        logger.debug(f"Starting image analysis for URL: {image_url}")
        image_url = image_url.replace("&format=webp", "&format=png")
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                            "detail": "high"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Analyze this image for roasting purposes."
                    }
                ]
            }
        ]
        try:
            logger.debug("Sending request to Grok API")
            result = await asyncio.wait_for(
                self.get_response(messages, model="grok-2-vision-1212"),
                timeout=timeout
            )
            logger.debug(f"Received response from Grok API: {result}")
            return result
        except asyncio.TimeoutError:
            logger.error(f"Image analysis timed out after {timeout} seconds")
            return "Image analysis timed out. Your image is probably too complex for my tiny AI brain."
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}", exc_info=True)
            return f"Error analyzing image: {str(e)}"