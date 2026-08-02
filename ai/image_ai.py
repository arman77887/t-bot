from openai import AsyncOpenAI
from config import Config
from logger.logger import logger


class ImageAI:

    def __init__(self):

        self.api_key = Config.OPENAI_API_KEY

        if self.api_key:

            self.client = AsyncOpenAI(
                api_key=self.api_key
            )

        else:

            self.client = None

            logger.warning(
                "OpenAI API key not found"
            )

    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024"
    ):

        if not self.client:

            return {
                "error": "OpenAI API key not configured"
            }

        try:

            response = await self.client.images.generate(

                model="gpt-image-1",

                prompt=prompt,

                size=size

            )

            return {

                "url": response.data[0].url

            }

        except Exception as e:

            logger.error(f"Image Error: {e}")

            return {

                "error": str(e)

            }
