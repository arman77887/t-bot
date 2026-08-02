from anthropic import AsyncAnthropic
from typing import List, Dict, Any

from config import Config
from logger.logger import logger


class ClaudeHandler:

    def __init__(self):

        self.api_key = Config.CLAUDE_API_KEY

        if self.api_key:

            self.client = AsyncAnthropic(
                api_key=self.api_key
            )

        else:

            self.client = None

            logger.warning(
                "Claude API key not found"
            )

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-sonnet-latest"
    ) -> Dict[str, Any]:

        if not self.client:

            return {
                "error": "Claude API key not configured"
            }

        try:

            system = ""
            user_messages = []

            for msg in messages:

                if msg["role"] == "system":
                    system = msg["content"]

                else:

                    user_messages.append(msg)

            response = await self.client.messages.create(

                model=model,

                system=system,

                max_tokens=2048,

                messages=user_messages

            )

            return {

                "content": response.content[0].text

            }

        except Exception as e:

            logger.error(f"Claude Error: {e}")

            return {

                "error": str(e)

            }
