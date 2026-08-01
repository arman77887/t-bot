from typing import Dict, Any

from config import Config
from logger.logger import logger


class ImageAIHandler:

    def __init__(self):
        self.openai_key = Config.OPENAI_API_KEY
        self.gemini_key = Config.GEMINI_API_KEY

    async def generate(
        self,
        prompt: str,
        provider: str = "openai"
    ) -> Dict[str, Any]:

        try:

            if provider == "openai":

                if not self.openai_key:
                    return {
                        "error": "OpenAI API key not configured"
                    }

                return {
                    "error": "OpenAI image generation will be added in next update."
                }

            elif provider == "gemini":

                if not self.gemini_key:
                    return {
                        "error": "Gemini API key not configured"
                    }

                return {
                    "error": "Gemini image generation will be added in next update."
                }

            return {
                "error": "Unknown provider"
            }

        except Exception as e:

            logger.exception(e)

            return {
                "error": str(e)
            }
