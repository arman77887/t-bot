import asyncio
from typing import Dict, Any, List

import google.generativeai as genai

from config import Config
from logger.logger import logger


class GeminiHandler:

    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )
        else:
            self.model = None
            logger.warning("Gemini API key not configured")

    async def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:

        if not self.model:
            return {
                "error": "Gemini API key not configured"
            }

        try:

            prompt = ""

            for msg in messages:

                role = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "system":
                    prompt += f"System: {content}\n"

                elif role == "assistant":
                    prompt += f"Assistant: {content}\n"

                else:
                    prompt += f"User: {content}\n"

            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )

            return {
                "content": response.text
            }

        except Exception as e:

            logger.exception(e)

            return {
                "error": str(e)
            }
