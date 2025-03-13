import os
import logging
import asyncio
import aiohttp
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize the bot client
app = Client(
    "ai_image_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# AI Image Generation Handler
def setup_ai_handler(app: Client):
    @app.on_message(filters.command(["ai"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def image_command(client: Client, message: Message):
        try:
            # Retrieve the prompt entered by the user
            prompt = message.text.split(" ", 1)[1]  # Example: /ai Batman

            # Send a loading message with bold text
            loading_msg = await app.send_message(
                message.chat.id, "⏳ **Generating images, please wait...**", parse_mode=ParseMode.MARKDOWN
            )

            api_url = f"https://death-image.ashlynn.workers.dev/?prompt={prompt}&image=3&dimensions=tall&safety=true"

            # Fetch image URLs (each request has its own session)
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    data = await response.json()

            # Check if "images" key exists and has URLs
            if "images" in data and isinstance(data["images"], list) and data["images"]:
                image_paths = []

                # Download images asynchronously (each image has its own session)
                for i, img_url in enumerate(data["images"]):
                    image_path = f"temp_image_{i}.jpg"
                    image_paths.append(image_path)

                    async with aiohttp.ClientSession() as session:
                        async with session.get(img_url) as img_response:
                            if img_response.status == 200:
                                async with aiofiles.open(image_path, "wb") as f:
                                    await f.write(await img_response.read())

                # Prepare media group
                media_group = [
                    InputMediaPhoto(image_paths[i], caption=f"🖼 **Prompt:** `{prompt}`\n\n**Here are the generated images.**")
                    if i == 0 else InputMediaPhoto(image_paths[i])
                    for i in range(len(image_paths))
                ]

                # Send images as an album (grouped together)
                await app.send_media_group(message.chat.id, media_group)

                # Delete downloaded images after sending
                for img in image_paths:
                    os.remove(img)

            else:
                await app.send_message(
                    message.chat.id, "❌ **No images were found for the given prompt.**", parse_mode=ParseMode.MARKDOWN
                )

            # Delete the loading message after sending the images
            await loading_msg.delete()

        except IndexError:
            await app.send_message(
                message.chat.id, "⚠️ **Please provide a prompt.**\n\n**Example:** `/ai Batman`", parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            await app.send_message(
                message.chat.id, f"❌ **Error:** `{str(e)}`", parse_mode=ParseMode.MARKDOWN
            )

# Register AI handler
setup_ai_handler(app)

# Run bot
if __name__ == "__main__":
    app.run()
