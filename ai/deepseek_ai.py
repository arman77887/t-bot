import asyncio
from typing import Dict, Any, List

from openai import AsyncOpenAI

from config import Config
from logger.logger import logger


class DeepSeekHandler:

    def __init__(self):
        self.api_key = Config.DEEPSEEK_API_KEY

        if self.api_key:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com/v1"
            )
            self.model = "deepseek-chat"
            logger.info("DeepSeek handler initialized successfully")
        else:
            self.client = None
            logger.warning("DeepSeek API key not configured")

    async def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:

        if not self.client:
            return {
                "error": "DeepSeek API key not configured"
            }

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            return {
                "content": response.choices[0].message.content,
                "model": self.model
            }

        except Exception as e:
            logger.exception(f"DeepSeek API error: {e}")
            return {
                "error": str(e)
            }
