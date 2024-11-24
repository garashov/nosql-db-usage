"""Module containing chatbot history related methods"""

from uuid import UUID
from typing import List, Optional, Union

from src.chatbot.chatbot_entities import ChatbotHistory, ChatbotHistoryItem, MessageRole
from src.intent.intent_entities import Intent
from src.utils.utils import generate_utc0_millisecond_timestamp
from src.infra.initializations import init_chatbot_history_store
from src.config.config import CHATBOT_HISTORY_COLLECTION_NAME
from src.logging.logger import logger


class DocumentStore:
    """
    A dynamic and extensible document store for managing data.

    The `DocumentStore` class provides a flexible framework for storing, retrieving, and managing structured data. 
    It is designed to adapt to various backend storage systems, enabling seamless integration with different 
    configurations such as Redis, CosmosDB, or any other supported storage type.

    ### Features:
    - **Backend-Agnostic Design**: 
      Supports multiple storage backends, dynamically adapting to the configuration provided during initialization.
    - **Data Management**: 
      Facilitates operations such as storing, retrieving, and updating data across different use cases.
    - **Extensibility**: 
      Built with a modular design to accommodate additional features or custom behaviors as required.

    Args:
        collection (str): The name of the collection, table, or resource being managed. 
                          Defaults to `CHATBOT_HISTORY_COLLECTION_NAME`.

    Attributes:
        collection (str): The collection or resource name managed by the store.
        history_store (object): The backend-specific store initialized based on the provided configuration.
    """
    def __init__(self, collection: str = CHATBOT_HISTORY_COLLECTION_NAME):
        self.collection = collection
        self.history_store = init_chatbot_history_store(collection=self.collection)


    def add_message_to_history(
        self,
        session_id: str,
        message_id: str,
        role: MessageRole,
        content: str,
        question_id: Optional[str] = None,
        user_id: Optional[str] = None,
        intent: Optional[Intent] = None,
        reference: dict | None = None,
    ) -> None:
        """
        Adds a single message to the chatbot history.

        This function creates a ChatbotHistoryItem from the provided parameters and adds it to the session history.

        Args:
            session_id (str): The unique identifier of the chatbot session.
            message_id (str): A unique identifier for the message.
            role (MessageRole): The role of the sender (user or assistant).
            content (str): The content of the message.
            intent (Optional[Intent]): The detected intent of the message, if any.
            reference (Optional[dict]): Any additional reference data for the message.

        """
        message: ChatbotHistoryItem = ChatbotHistoryItem(
            role=role,
            message_id=message_id,
            session_id=session_id,
            question_id=question_id,
            intent=intent,
            content=content,
            reference=reference,
            timestamp=generate_utc0_millisecond_timestamp(),  # TODO: should not be generated here!
            feedback_rating=None,  # NOTE: When we send the message, we need to populate this field with null value to then update from UI when user scores the response
        )
        self.history_store.add(message=message, session_id=session_id, user_id=user_id)


    def get_chat_history(
        self,
        user_id: str,
        session_id: Union[UUID, str],
        num_conversation_pairs: Optional[int] = None
    ) -> Optional[ChatbotHistory]:
        """
        Retrieves the chatbot history for a specific session ID from the document store.

        This function fetches a specified number of recent conversation pairs from the chatbot history.

        Args:
            user_id (str): The unique identifier of the user.
            session_id (Union[UUID, str]): The unique identifier of the chatbot session.
            num_conversation_pairs (Optional[int]): The number of conversation pairs to retrieve. Defaults to 3.

        Returns:
            Optional[ChatbotHistory]: The chatbot history for the given session ID, if available.
        """
        return self.history_store.get_history_by_session_id(session_id=session_id, user_id=user_id, num_conversation_pairs=num_conversation_pairs)


    def get_history_by_user_id(self, user_id: str) -> List[ChatbotHistoryItem]:
        """
        Retrieves the full chatbot history for a specific user ID from the document store.

        This function fetches all chatbot history items associated with a specific user ID.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            List[ChatbotHistoryItem]: A list of all ChatbotHistoryItem objects stored in the document store for the given user ID.
        """
        return self.history_store.get_history_by_user_id(user_id=user_id)


    def update_field(
            self,
            key: str,
            value: str,
            user_id: str,
            session_id: str,
        ) -> None:
        """
        Updates a field in the chat history.

        This function updates a field in the chat history for a specific session ID.

        Args:
            key (str): The field to update.
            value (str): The new value for the field.
            user_id (str): The unique identifier of the user.
            session_id (str): The unique identifier of the chatbot session.
        """
        self.history_store.update_field(key=key, value=value, user_id=user_id, session_id=session_id)


    def delete_chat_history_by_session_id(self, user_id :str, session_id: str) -> Optional[bool]:
        """
        Deletes a specific session from Redis using the session ID, after initializing the chat history store.

        This function is similar to `delete_chat_history_by_session_id`, but it initializes the
        chat history store before performing the deletion.

        Args:
            session_id (str): The unique identifier of the session to be deleted.
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[bool]: True if the session was deleted successfully, 
                            False if the session was not found, 
                            None if an error occurred during deletion.
        """       
        # Now call the original delete function on the initialized history store
        return self.history_store.delete_chat_history_by_session_id(user_id=user_id, session_id=session_id)


    def delete_chat_history_by_user_id(self, user_id: str) -> Optional[int]:
        """
        Deletes all sessions associated with a specific user_id in Redis, after initializing the chat history store.

        This function is similar to `delete_chat_history_by_user_id`, but it initializes the
        chat history store before performing the deletion.

        Args:
            user_id (str): The unique identifier of the user whose sessions are to be deleted.

        Returns:
            Optional[int]: The number of sessions deleted, or None if an error occurred during deletion.
        """        
        return self.history_store.delete_chat_history_by_user_id(user_id)


    def delete_all_chats(self) -> Optional[int]:
        """
        Deletes all chat histories within the specified collection in Redis, after initializing the chat history store.

        Args:
            None

        Returns:
            Optional[int]: The number of sessions deleted, or None if an error occurred during deletion.
        """
        return self.history_store.delete_all_chats()

    def drop_all_entries(self) -> Optional[int]:
        """
        Drops all entries from the chat history store in Redis.

        This function drops all entries from the chat history store in Redis.

        Args:
            None
        
        Returns:
            Optional[int]: The number of entries deleted, or None if an error occurred during deletion.
        """
        return self.history_store.drop_all_entries()
