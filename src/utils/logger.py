import logging
import os

LOG_FILE_PATH = "logs/app.log"

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),  # Log to file
        logging.StreamHandler()              # Log to console
    ]
)

# Logger instance
logger = logging.getLogger("KenyaPowerNotifier")
