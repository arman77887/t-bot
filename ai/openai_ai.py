import asyncio
from typing import Dict, Any, List

from openai import AsyncOpenAI

from config import Config
from logger.logger import logger


class OpenAIHandler:

    def __init__(self):

        if Config.OPENAI_API_KEY:
            self.client = AsyncOpenAI(
                api_key=Config.OPENAI_API_KEY
            )
        else:
            self.client = None
            logger.warning("OpenAI API key not configured")

    async def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:

        if not self.client:
            return {
                "error": "OpenAI API key not configured"
            }

        try:

            response = await self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                temperature=0.7
            )

            return {
                "content": response.choices[0].message.content
            }

        except Exception as e:

            logger.exception(e)

            return {
                "error": str(e)
            }
