from openai import AsyncOpenAI
from typing import Dict, Any, List

from config import Config
from logger.logger import logger


class GrokHandler:

    def __init__(self):

        if Config.GROK_API_KEY:
            self.client = AsyncOpenAI(
                api_key=Config.GROK_API_KEY,
                base_url="https://api.x.ai/v1"
            )
        else:
            self.client = None
            logger.warning("Grok API key not configured")

    async def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:

        if not self.client:
            return {
                "error": "Grok API key not configured"
            }

        try:

            response = await self.client.chat.completions.create(
                model="grok-4",
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
