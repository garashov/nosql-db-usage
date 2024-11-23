import logging

from langchain.globals import set_debug, set_verbose

from src.config.config import LOGGER_LEVEL, LOGGER_LEVEL_PDFMINER, LOGGER_LEVEL_PYMONGO

# -------------------------------
# Constants
# -------------------------------
LOGGING_LEVELS_ROUTER = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

LOGGING_LEVEL = LOGGING_LEVELS_ROUTER.get(LOGGER_LEVEL.lower() if LOGGER_LEVEL else "info")
LOGGING_LEVEL_PDFMINER = LOGGING_LEVELS_ROUTER.get(LOGGER_LEVEL_PDFMINER.lower() if LOGGER_LEVEL_PDFMINER else "info")
LOGGING_LEVEL_PYMONGO = LOGGING_LEVELS_ROUTER.get(LOGGER_LEVEL_PYMONGO.lower() if LOGGER_LEVEL_PYMONGO else "info")


# -------------------------------
# Definitions
# -------------------------------
class UserLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # Use the user from the extra context, defaulting to 'Unknown' if no user is set
        user = self.extra.get("user", "Unknown")
        # Ensure the extra dictionary is updated correctly
        kwargs["extra"] = {"user": user}
        return msg, kwargs


def assign_user(user_id):
    """Assign a user to the logger"""
    # Update the logger's user context dynamically
    logger.extra["user"] = user_id


# -------------------------------
# Configure logging
# -------------------------------
# Create a custom logger (with a custom formatter, different from the root logger that is required to be untoched for 3rd party libraries)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - [User: %(user)s] - %(message)s"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

def_logger = logging.getLogger("my_app_logger")
def_logger.setLevel(LOGGING_LEVEL)
def_logger.addHandler(stream_handler)
def_logger.propagate = False  # Prevent propagation to the root logger. This is mandatory to not trigger issue with the root logger (of 3rd partiy libraries)


# Wrap the logger with user context
logger = UserLoggerAdapter(def_logger, {"user": "NotDefined"})

# PDFMiner and PyMongo logging levels
logging.getLogger("pdfminer").setLevel(LOGGING_LEVEL_PDFMINER)
logging.getLogger("pymongo").setLevel(LOGGING_LEVEL_PYMONGO)

# LangChain logging levels
if LOGGING_LEVEL == logging.DEBUG:
    set_debug(True)
    set_verbose(True)
elif LOGGING_LEVEL == logging.INFO:
    set_debug(False)
    set_verbose(False)
else:
    set_debug(False)
    set_verbose(False)


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    # Log a message before user is assigned
    logger.info("Step 1: Initialization - No user assigned yet.")

    # Assign user and log further steps
    assign_user("User123")
    logger.info("Step 2: User assigned - User123 is now logged.")

    assign_user("User456")
    logger.info("Step 3: Another user assigned - User456 is now logged.")
