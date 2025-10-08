import asyncio
import json
import logging
from pyrogram import Client

from config import API_ID, API_HASH, PHONE_NUMBER

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class Bot:
    def __init__(self, admin: str, channel_link: str, limit: int, save_file: str):
        self.save_file = save_file
        self.limit = limit
        self.admin = admin
        self.channel_link = channel_link
        self.data_list = []

    async def write_file(self):
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(self.data_list, f, ensure_ascii=False, indent=4)
        logging.info(f"Data successfully saved to {self.save_file}")

    async def process_data(self):
        async with Client(
            "my_account",
            api_id=API_ID,
            api_hash=API_HASH,
            phone_number=PHONE_NUMBER
        ) as app:
            try:
                await app.send_message(self.admin, "✅ Bot started. Collecting data...")
                channel = await app.get_chat(self.channel_link)
                logging.info(f"Reading channel: {channel.title} ({channel.id})")
                count_posts = 0
                async for post in app.get_chat_history(channel.id, limit=self.limit):
                    try:
                        post_data = {
                            "post_id": getattr(post, "id", None),
                            "date": str(getattr(post, "date", None)),
                            "views": getattr(post, "views", None),
                            "forwards": getattr(post, "forwards", None),
                            "text": (getattr(post, "text", "")[:500] if getattr(post, "text", None) else ""),
                            "media_type": getattr(post.media, "value", None) if getattr(post, "media", None) else None
                        }
                        self.data_list.append(post_data)
                        count_posts += 1

                        if count_posts % 1000 == 0:
                            logging.info(f"⏸ Processed {count_posts} posts, waiting 5 seconds...")
                            await asyncio.sleep(5)

                    except Exception as e:
                        logging.error(f"Error processing post")
                        continue

                await self.write_file()

                count = await app.get_chat_members_count(channel.id)
                logging.info(f"Channel subscriber count: {count}")
                logging.info("Data collection completed successfully.")

            except Exception as e:
                logging.error(f"Error during data collection: {e}")
                raise


def start(admin: str, channel_link: str, limit: int, save_file: str):
    bot = Bot(admin, channel_link, limit, save_file)
    asyncio.run(bot.process_data())
