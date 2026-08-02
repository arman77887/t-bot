from openai import AsyncOpenAI
from typing import List, Dict, Any

from config import Config
from logger.logger import logger


class GrokHandler:

    def __init__(self):

        self.api_key = Config.GROK_API_KEY

        if self.api_key:

            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )

        else:

            self.client = None

            logger.warning("Grok API key not found")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-4"
    ) -> Dict[str, Any]:

        if not self.client:

            return {
                "error": "Grok API key not configured"
            }

        try:

            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )

            return {
                "content": response.choices[0].message.content
            }

        except Exception as e:

            logger.error(f"Grok Error: {e}")

            return {
                "error": str(e)
            }
