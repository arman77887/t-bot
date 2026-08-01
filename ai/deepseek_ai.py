from openai import AsyncOpenAI
from typing import Dict, Any, List

from config import Config
from logger.logger import logger


class DeepSeekHandler:

    def __init__(self):

        if Config.DEEPSEEK_API_KEY:

            self.client = AsyncOpenAI(
                api_key=Config.DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com"
            )

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
                model="deepseek-chat",
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
