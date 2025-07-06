# scripts/logging/logger.py

import logging

logger = logging.getLogger("django_manager")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# File Handler
file_handler = logging.FileHandler('logs/debug.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Optional: Stream handler (for console output)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
