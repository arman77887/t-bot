import asyncio
from typing import Dict, Any, List

from anthropic import AsyncAnthropic

from config import Config
from logger.logger import logger


class ClaudeHandler:

    def __init__(self):
        self.api_key = Config.CLAUDE_API_KEY

        if self.api_key:
            self.client = AsyncAnthropic(api_key=self.api_key)
            self.model = "claude-3-haiku-20240307"
            logger.info("Claude handler initialized successfully")
        else:
            self.client = None
            logger.warning("Claude API key not configured")

    async def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:

        if not self.client:
            return {
                "error": "Claude API key not configured"
            }

        try:
            # Claude এর জন্য মেসেজ ফরম্যাট আলাদা
            system_message = None
            formatted_messages = []

            for msg in messages:
                if msg.get("role") == "system":
                    system_message = msg.get("content")
                else:
                    formatted_messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })

            response = await self.client.messages.create(
                model=self.model,
                system=system_message,
                messages=formatted_messages,
                max_tokens=1024
            )

            return {
                "content": response.content[0].text,
                "model": self.model
            }

        except Exception as e:
            logger.exception(f"Claude API error: {e}")
            return {
                "error": str(e)
            }
