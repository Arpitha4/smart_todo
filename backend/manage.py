import logging
from main import DjangoManager

logging.basicConfig(level=logging.INFO)

def run_application():
    """Main function to run the application."""
    try:
        DjangoManager().manage()
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)


if __name__ == '__main__':
    run_application()
