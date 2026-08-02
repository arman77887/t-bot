from openai import AsyncOpenAI
from typing import List, Dict, Any
from config import Config
from logger.logger import logger


class OpenAIHandler:

    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY

        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("OpenAI API key not found")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4.1-mini"
    ) -> Dict[str, Any]:

        if not self.client:
            return {
                "error": "OpenAI API key not configured"
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

            logger.error(f"OpenAI Error: {e}")

            return {
                "error": str(e)
            }
