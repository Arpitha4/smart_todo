import os
import sys
from scripts.config.app_configuration import TemplateDetails
from scripts.logging.logger import logger


class DjangoManager:
    """Handles environment setup, logging, and Django command execution."""

    def __init__(self):
        self.config = self._read_config()
        self._set_env()

    def _read_config(self):
        """Reads configuration from a key=value formatted file."""
        config_path = os.path.join(TemplateDetails.FOLDER_NAME, TemplateDetails.FILE_NAME)
        try:
            with open(config_path) as f:
                config = dict(
                    line.strip().split('=', 1)
                    for line in f if line.strip() and not line.startswith('#')
                )
                logger.info("Configuration loaded from %s", config_path)
                return config
        except Exception as e:
            logger.exception("Error reading configuration file: %s", e)
            sys.exit(1)

    def _set_env(self):
        """Set the DJANGO_SETTINGS_MODULE environment variable."""
        settings_module = self.config.get('DJANGO_SETTINGS_MODULE', 'smart_todo.settings')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        logger.info("Environment set with DJANGO_SETTINGS_MODULE = %s", settings_module)

    def run(self):
        """Execute Django command-line interface."""
        try:
            from django.core.management import execute_from_command_line
            logger.info("Executing Django command: %s", ' '.join(sys.argv))
            execute_from_command_line(sys.argv)
        except ImportError:
            logger.exception("Django import failed.")
            raise ImportError("Couldn't import Django.") from None
        except Exception:
            logger.exception("Unexpected error occurred while running Django.")
            sys.exit(1)

    def app(self):
        """Entry point."""
        try:
            manager = DjangoManager().run()
        except Exception as e:
            logger.exception("Failed to start DjangoManager: %s", e)
