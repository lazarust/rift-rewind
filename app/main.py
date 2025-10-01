import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting chat app container")
    logger.info("Hello from rift-rewind!")

    while True:
        logger.info("Chat app is running...")
        time.sleep(60)


if __name__ == "__main__":
    main()
