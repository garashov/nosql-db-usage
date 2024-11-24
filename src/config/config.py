"""
This notebook is designed to configure and initialize environment variables for various services utilized in our project.
It extracts configurations from the `CONFIG` object and sets up necessary parameters, credentials, and settings for seamless
integration and interaction with different APIs and services.
"""

from src.config import CONFIG

# ----------------------------------------------
# Logging
# ----------------------------------------------
LOGGER_LEVEL = CONFIG["logging.logging_level"]
LOGGER_LEVEL_PDFMINER = CONFIG["logging.logging_level_pdfminer"]
LOGGER_LEVEL_PYMONGO = CONFIG["logging.logging_level_pymongo"]

# ----------------------------------------------
# Utils
# ----------------------------------------------
ENCRYPTION_KEY = str.encode(CONFIG["utils.encryption_key"])

# ----------------------------------------------
# DB Types
# ----------------------------------------------
CHATBOT_HISTORY_DB_TYPE = CONFIG["db_types.chatbot_history_db"]
DOCUMENT_STORE_DB_TYPE = CONFIG["db_types.document_store_db"]
VECTOR_STORE_DB_TYPE = CONFIG["db_types.vector_store_db"]

# ----------------------------------------------
# Redis
# ----------------------------------------------
REDIS_TTL = CONFIG["redis.ttl"]
REDIS_HOST = CONFIG["redis.host"]
REDIS_PORT = CONFIG["redis.port"]
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
REDIS_DB = CONFIG["redis.db"]
REDIS_INDEX_NAME = CONFIG["redis.index_name"]
REDIS_PARENT_INDEX_NAME = CONFIG["redis.parent_index_name"]
REDIS_COLLECTION_NAME = CONFIG["redis.chatbot_history_collection"]


# ----------------------------------------------
# DB Configuration
# ----------------------------------------------
CHATBOT_HISTORY_COLLECTION_NAME = (
    REDIS_COLLECTION_NAME if CHATBOT_HISTORY_DB_TYPE == "redis"
    else None
)