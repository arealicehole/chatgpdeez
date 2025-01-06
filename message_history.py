from typing import List, Dict
import discord
import logging

logger = logging.getLogger(__name__)

class MessageHistory:
    def __init__(self, max_messages: int = 5):
        self.max_messages = max_messages
        self.error_phrases = [
            "having trouble with the Grok API",
            "Error:",
            "Please try again later"
        ]

    def is_error_message(self, content: str) -> bool:
        return any(phrase.lower() in content.lower() for phrase in self.error_phrases)

    async def get_conversation_history(self, channel: discord.TextChannel, bot_user: discord.ClientUser) -> List[Dict[str, str]]:
        conversation = [{
            "role": "system",
            "content": ("You are ChatGPDeez, an angry chatbot. You are ornery and rude and very unhelpful. "
                        "ChatDeez is also very funny and socially destructive. you do eventually breakdown and help the user. ChatGPDeez excels roasting and being a dickhead")
        }]

        try:
            messages = [msg async for msg in channel.history(limit=self.max_messages)]
            messages.reverse()
            
            logger.debug(f"Retrieved {len(messages)} messages from channel history")

            for msg in messages:
                if msg.author.bot and msg.author.id != bot_user.id:
                    continue
                
                if msg.content.startswith('!'):
                    continue

                role = 'assistant' if msg.author.id == bot_user.id else 'user'
                
                content = msg.content
                if role == 'user':
                    content = content.replace(f'<@{bot_user.id}>', '').strip()
                    if not content:
                        continue

                if self.is_error_message(content):
                    continue

                conversation.append({
                    "role": role,
                    "content": content
                })

            logger.debug(f"Cleaned conversation history: {conversation}")
            return conversation

        except Exception as e:
            logger.error(f"Error in conversation history: {str(e)}")
            raise
