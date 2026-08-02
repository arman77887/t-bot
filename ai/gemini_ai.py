import asyncio
from typing import Dict, Any, List

# নতুন SDK ব্যবহার করুন
from google import genai

from config import Config
from logger.logger import logger


class GeminiHandler:

    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY

        if self.api_key:
            # নতুন ক্লায়েন্ট ইনিশিয়ালাইজ
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = "gemini-2.0-flash-exp"
            logger.info("Gemini handler initialized successfully")
        else:
            self.client = None
            self.model_name = None
            logger.warning("Gemini API key not configured")

    async def chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:

        if not self.client:
            return {
                "error": "Gemini API key not configured"
            }

        try:
            # মেসেজগুলো প্রক্রিয়াকরণ
            prompt = self._format_messages(messages)

            # নতুন API ব্যবহার করে কনটেন্ট জেনারেট
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt
            )

            return {
                "content": response.text,
                "model": self.model_name
            }

        except Exception as e:
            logger.exception(f"Gemini API error: {e}")
            return {
                "error": str(e)
            }

    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        মেসেজ লিস্টকে প্রম্পটে কনভার্ট করে
        """
        prompt = ""

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                prompt += f"System instruction: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
            else:  # user বা অন্য কোনো রোল
                prompt += f"User: {content}\n"

        return prompt.strip()
