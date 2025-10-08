import os
import logging
import tg_bot
import graph

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

ADMIN_USERNAME = "me"
CHANNEL_LINK = "naebnet"
LIMIT = 1000
GRAPH_ROOT = "graphic"
DATA_ROOT = "data"


def main():
    os.makedirs(GRAPH_ROOT, exist_ok=True)
    os.makedirs(DATA_ROOT, exist_ok=True)

    data_file_name = os.path.join(DATA_ROOT, f"{CHANNEL_LINK}.json")
    graph_file_name = os.path.join(GRAPH_ROOT, f"{CHANNEL_LINK}.png")

    try:
        logging.info("Starting data collection...")
        tg_bot.start(
            admin=ADMIN_USERNAME,
            channel_link=CHANNEL_LINK,
            limit=LIMIT,
            save_file=data_file_name
        )
        logging.info("Data collection completed successfully.")
    except Exception as e:
        logging.error(f"Error while collecting data: {e}")
        return

    try:
        logging.info("Generating graph...")
        graph.draw(
            data_file_name=data_file_name,
            save_file_name=graph_file_name,
            graph_title=f"@{CHANNEL_LINK}"
        )
        logging.info(f"Graph saved as: {graph_file_name}")
    except Exception as e:
        logging.error(f"Error while generating graph: {e}")


if __name__ == "__main__":
    main()
