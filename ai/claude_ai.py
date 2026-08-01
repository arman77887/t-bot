import httpx
from typing import Dict, Any, List

from config import Config
from logger.logger import logger


class ClaudeHandler:

    def __init__(self):
        self.api_key = Config.CLAUDE_API_KEY

    async def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:

        if not self.api_key:
            return {
                "error": "Claude API key not configured"
            }

        try:

            prompt = "\n".join(
                msg["content"] for msg in messages
            )

            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }

            data = {
                "model": "claude-3-5-sonnet-latest",
                "max_tokens": 2048,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            async with httpx.AsyncClient(timeout=60) as client:

                r = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=data,
                )

            r.raise_for_status()

            result = r.json()

            return {
                "content": result["content"][0]["text"]
            }

        except Exception as e:

            logger.exception(e)

            return {
                "error": str(e)
            }
