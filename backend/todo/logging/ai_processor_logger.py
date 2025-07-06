import logging
import os

# Ensure the log directory exists
os.makedirs("logs", exist_ok=True)

# Set up logger
logger = logging.getLogger("task_ai_logger")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers if already configured
if not logger.handlers:
    handler = logging.FileHandler("logs/ai_processor.log")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
