from src.logging.logger import logger
from src.dbs.redisdb import RedisChatHistoryHelper
from src.config.config import (
    CHATBOT_HISTORY_DB_TYPE,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT
)

# ----------------------------------------
# Constants
# ----------------------------------------
_HISTORY_STORE = None


# ----------------------------------------
# Chatbot Initialization Functions
# ----------------------------------------
def _init_history_store(collection: str) -> RedisChatHistoryHelper:
    """
    Initializes and returns the chatbot history store based on the runtime environment.

    If the runtime is 'cloud', it initializes an Azure Cosmos DB store using the given
    connection string, database name, and session-specific collection.

    If the runtime is 'local', it initializes a Redis store.

    If neither condition is met, it raises a ValueError indicating an unsupported runtime.

    Args:
        session_id (str): The session identifier to be used as the collection name in the database.

    Returns:
        RedisChatHistoryHelper: The initialized history store instance.

    Raises:
        ValueError: If the runtime environment is neither 'cloud' nor 'local'.
    """

    if CHATBOT_HISTORY_DB_TYPE == "redis":
        logger.info("Initializing Redis history store...")
        history_store = RedisChatHistoryHelper(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            collection=collection,
        )
        logger.info("Initialized Redis history store.")
    # TODO: currently, it is not supported
    # elif CHATBOT_HISTORY_DB_TYPE == "cosmos":
    #     logger.info("Initializing Azure Cosmos history store...")
    #     history_store = AzureCosmosLangchainHelper(
    #         connection_string=DOCUMENT_STORE_CONNECTION_STRING,
    #         database=CHATBOT_HISTORY_DATABASE_NAME,
    #         collection=collection,
    #     )
    #     logger.info("Initialized Azure Cosmos history store.")
    else:
        raise ValueError(
            f"Unsupported CHATBOT_HISTORY_DB_TYPE environment value. CHATBOT_HISTORY_DB_TYPE value: {CHATBOT_HISTORY_DB_TYPE}"
        )
    return history_store

# NOTE: currently it is not used bcs we do not change the collection name. Do not delete it, it may be useful in the future
# def _update_history_store(session_id: str) -> Union[AzureCosmosLangchainHelper, RedisChatHistoryHelper]:
#     """
#     Updates and returns the chatbot history store based on the runtime environment and session ID.

#     This function checks the runtime environment and the given session ID to decide whether
#     to initialize a new history store or return the existing one. Depending on the runtime,
#     it either initializes an Azure Cosmos DB store or a Redis store.

#     - If the runtime is 'cloud' and the session ID differs from the current collection,
#       it initializes a new Azure Cosmos DB store using the provided connection string,
#       database name, and session-specific collection.
#     - If the runtime is 'local' and the session ID differs from the current collection,
#       it initializes a new Redis store with the specified host, port, database, and session ID.
#     - If neither condition is met, it returns the existing history store without reinitializing it.

#     Args:
#         session_id (str): The session identifier used as the collection name in the database.

#     Returns:
#         Union[AzureCosmosLangchainHelper, RedisChatHistoryHelper]: The updated or existing history store instance.
#     """

#     # TODO: pycharm signals a "cannot find reference" error. Restructure conditions
#     if _CHATBOT_HISTORY_DB_TYPE == "cosmos" and session_id != _HISTORY_STORE.collection_name:
#         logger.info("Updating Azure Cosmos history store with new session_id...")
#         updated_history_store = AzureCosmosLangchainHelper(
#             connection_string=_DOCUMENT_STORE_CONNECTION_STRING,
#             database=_CHATBOT_HISTORY_DATABASE_NAME,
#             collection=session_id,
#         )
#         logger.info("Updated Azure Cosmos history store.")
#         return updated_history_store
#     elif _CHATBOT_HISTORY_DB_TYPE == "redis" and session_id != _HISTORY_STORE.session_id:
#         # logger.info("Updating Redis history store with new session_id...")
#         # updated_history_store = RedisChatHistoryHelper(
#         #     host=_REDIS_HOST,
#         #     port=_REDIS_PORT,
#         #     db=_REDIS_DB,
#         #     session_id=session_id
#         # )
#         # logger.info("Updated Redis history store.")
#         # return updated_history_store
#         raise ValueError("Redis is not supported in the current configuration. Please refer to the documentation for supported configurations.")
#     else:
#         return _HISTORY_STORE  # Return the existing history store if no conditions are met


def init_chatbot_history_store(collection: str) -> RedisChatHistoryHelper:
    """
    Initializes or updates and returns the chatbot history store based on the runtime environment.

    This function checks if the history store is already initialized. If not, it initializes a new
    history store based on the runtime environment ('cloud' or 'local'). If the store is already
    initialized, it updates the store based on the session ID and runtime environment.

    - If the runtime is 'cloud', it initializes an Azure Cosmos DB store using the given
      connection string, database name, and session-specific collection.
    - If the runtime is 'local', it initializes a Redis store.
    - If the store is already initialized, it checks the session ID and updates the store
      accordingly without reinitializing if the session ID matches the existing collection.

    Args:
        session_id (str): The session identifier used as the collection name in the database.

    Returns:
        RedisChatHistoryHelper: The initialized or updated/existing history store instance.
    """
    global _HISTORY_STORE

    if not _HISTORY_STORE:
        _HISTORY_STORE = _init_history_store(collection)
    # NOTE: with current configuration, we do not change the collection name
    # else:
    #     _HISTORY_STORE = _update_history_store(collection)
    return _HISTORY_STORE