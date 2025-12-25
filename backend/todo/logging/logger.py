import logging
import os

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
os.makedirs(log_dir, exist_ok=True)

# Full path to debug.log
log_file = os.path.join(log_dir, 'debug.log')

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
