import logging
import os

# Basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.dirname(MODULE_PATH)

DATABASE_PATH = f"{os.getenv('DATABASE_PATH')}/market_mystic"
