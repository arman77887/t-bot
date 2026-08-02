import asyncio
from typing import Dict, Any, List

import aiohttp

from config import Config
from logger.logger import logger


class GrokHandler:

    def __init__(self):
        self.api_key = Config.GROK_API_KEY

        if self.api_key:
            self.base_url = "https://api.x.ai/v1/chat/completions"
            self.model = "grok-beta"
            logger.info("Grok handler initialized successfully")
        else:
            self.api_key = None
            logger.warning("Grok API key not configured")

    async def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:

        if not self.api_key:
            return {
                "error": "Grok API key not configured"
            }

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 1024
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        return {
                            "error": f"Grok API error: {error_text}"
                        }

                    data = await response.json()
                    return {
                        "content": data["choices"][0]["message"]["content"],
                        "model": self.model
                    }

        except Exception as e:
            logger.exception(f"Grok API error: {e}")
            return {
                "error": str(e)
            }
