"""
This script is used to create Redis helpers for chat history storage.
"""
import json
import redis
from uuid import UUID
from typing import Optional, Union, List

from src.logging.logger import logger
from src.chatbot.chatbot_entities import ChatbotHistory, ChatbotHistoryItem


class RedisChatHistoryHelper:
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection
        self.history_store = redis.Redis(
            connection_pool=redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        )

    def add(
        self,
        message: ChatbotHistoryItem,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> None:
        """
        Adds a new message to a Redis entry identified by session_id. If the entry does not
        exist, it is created with the given session_id, user_id, and topic based on the content
        of the first message. If the first message contains a request to "summarize the uploaded file",
        the topic is set to "File Uploaded"; otherwise, the topic is set to the message content.

        Args:
            message (ChatbotHistoryItem): The message to be added to the session. Must be
                                        serializable to a dictionary.
            session_id (str): The unique identifier for the session in Redis.
            user_id (Optional[str]): An optional user identifier to be included in the session.

        Returns:
            None: The function does not return a value but logs the action performed.
        """
        key = f"{self.collection}/{user_id}/{session_id}"

        # Check if the session exists in Redis
        session_data = self.history_store.get(key)


        if not session_data:
            # If session does not exist, create new history with metadata
            content = message.dict().get("content", "")
            session_metadata = {
                "session_id": session_id,
                "user_id": user_id,
                "topic": content,
                "deleted": False,
                "messages": [message.dict()],  # Initialize with the first message
            }
            # Save the new session as a serialized JSON string
            self.history_store.set(key, json.dumps(session_metadata))
            logger.info(f"Inserted new session for session_id: {session_id}.")
        else:
            # If session exists, update the messages list
            session_metadata = json.loads(session_data)
            session_metadata["messages"].append(message.dict())
            
            # Save the updated session back to Redis
            self.history_store.set(key, json.dumps(session_metadata))
            logger.info(f"Updated existing session for session_id: {session_id}.")


    def get_history_by_session_id(
        self,
        user_id: str,
        session_id: Union[UUID, str],
        num_conversation_pairs: Optional[int] = None,  # Allow None as default
    ) -> Optional[ChatbotHistory]:
        """
        Retrieves the chatbot history for a specific session ID from Redis.

        This function fetches either all messages or a specified number of recent conversation pairs from the chatbot history.

        Args:
            session_id (Union[UUID, str]): The unique identifier of the chatbot session.
            num_conversation_pairs (Optional[int]): The number of conversation pairs to retrieve. Defaults to None (all messages).

        Returns:
            Optional[ChatbotHistory]: The chatbot history for the given session ID, if available.
        """
        key = f"{self.collection}/{user_id}/{session_id}"
        session_data = self.history_store.get(key)

        if not session_data:
            logger.info(f"No history found for session_id: {session_id}.")
            return None

        # Deserialize the session data
        session_metadata = json.loads(session_data)

        # Retrieve the messages
        messages = session_metadata.get("messages", [])

        # If num_conversation_pairs is provided, slice the last N conversation pairs (2 messages per pair)
        if num_conversation_pairs is not None and num_conversation_pairs > 0:
            num_last_entries = num_conversation_pairs * 2
            messages = messages[-num_last_entries:]

        # Convert messages to ChatbotHistory format
        return ChatbotHistory(
            session_id=session_id,
            history=[ChatbotHistoryItem(**item) for item in messages],
        )


    def get_history_by_user_id(self, user_id: str) -> Optional[List[dict]]:
        """
        Retrieves the full chatbot history for a specific user ID from Redis.

        This function fetches all session data from all sessions for the given user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[List[dict]]: A list of session dictionaries for the given user ID, if available.
        """
        # Scan all keys to find those belonging to this user
        pattern = f"{self.collection}/{user_id}/*"
        keys = self.history_store.scan_iter(match=pattern)

        user_sessions = []

        for key in keys:
            session_data = self.history_store.get(key)
            if not session_data:
                continue
            
            session_metadata = json.loads(session_data)
            if session_metadata.get("user_id") == user_id:
                # Add the entire session dictionary, not just the messages
                user_sessions.append(session_metadata)

        if not user_sessions:
            logger.info(f"No history found for user_id: {user_id}.")
            return None

        return user_sessions


    def update_field(self, key: str, value: str, user_id: str, session_id: str) -> None:
        """
        Updates a specific field of an existing session identified by session_id in Redis.
        This function updates fields that are not part of the 'messages' list. For updates
        within 'messages', a separate method should be used.

        Args:
            key (str): The field name to be updated.
            value (str): The new value to set for the specified field.
            session_id (str): The unique identifier for the session in Redis.

        Returns:
            None: The function does not return a value, but logs a message indicating whether the session was updated.
        """
        redis_key = f"{self.collection}/{user_id}/{session_id}"
        
        # Retrieve the session data
        session_data = self.history_store.get(redis_key)

        if not session_data:
            logger.warning(f"No session found for session_id: {session_id}.")
            return

        # Deserialize session data
        session_metadata = json.loads(session_data)

        # Update the specified field
        session_metadata[key] = value

        # Save updated session back to Redis
        self.history_store.set(redis_key, json.dumps(session_metadata))
        logger.info(f"Updated {key} for session_id {session_id} to '{value}'.")


    def delete_chat_history_by_session_id(self, user_id: str, session_id: str) -> Optional[bool]:
        """
        Deletes a specific session from Redis using the session ID.

        Args:
            session_id (str): The unique identifier of the session to be deleted.

        Returns:
            Optional[bool]: True if the session was deleted successfully, 
                            False if the session was not found, 
                            None if an error occurred during deletion.
        """
        key = f"{self.collection}/{user_id}/{session_id}"

        try:
            # Attempt to delete the session from Redis
            result = self.history_store.delete(key)

            if result > 0:
                logger.info(f"Session with session_id {session_id} deleted successfully.")
                return True  # Session was deleted successfully
            else:
                logger.info(f"No session found with session_id {session_id}.")
                return False  # Session was not found
        except Exception as e:
            # Log the exception or handle it as needed
            logger.error(f"An error occurred while deleting the session: {e}")
            return None  # Return None if an error occurred


    def delete_chat_history_by_user_id(self, user_id: str) -> Optional[int]:
        """
        Deletes all sessions associated with a specific user_id in Redis.

        Args:
            user_id (str): The unique identifier of the user whose sessions are to be deleted.

        Returns:
            Optional[int]: The number of sessions deleted, or None if an error occurred during deletion.
        """
        pattern = f"{self.collection}/{user_id}/*"  # Pattern matches all sessions for the given user_id

        try:
            # Scan all keys in Redis that match the user_id pattern
            keys = self.history_store.scan_iter(match=pattern)

            deleted_count = 0  # Counter for the number of sessions deleted

            for key in keys:
                # Delete the key (session) for the given user_id
                self.history_store.delete(key)
                deleted_count += 1  # Increment the deleted session count

            # Log and return the number of deleted sessions
            if deleted_count > 0:
                logger.info(f"Deleted {deleted_count} sessions for user_id {user_id}.")
                return deleted_count  # Return the number of deleted sessions
            else:
                logger.info(f"No sessions found for user_id {user_id}.")
                return 0  # No sessions found for the user_id

        except Exception as e:
            # Log the exception or handle it as needed
            logger.error(f"An error occurred while deleting sessions for user_id {user_id}: {e}")
            return None  # Return None if an error occurred


    def delete_all_chats(self) -> Optional[int]:
        """
        Deletes all chat sessions from Redis.

        Args:
            None

        Returns:
            Optional[int]: The number of sessions deleted, or None if an error occurred during deletion.
        """
        pattern = f"{self.collection}/*"  # Adjust the pattern based on your Redis key structure

        try:
            # Scan all keys in Redis
            keys = self.history_store.scan_iter(match=pattern)
            
            deleted_count = 0  # Counter for the number of sessions deleted

            for key in keys:
                # Delete each key (session)
                self.history_store.delete(key)
                deleted_count += 1  # Increment the deleted session count

            # Log and return the number of deleted sessions
            if deleted_count > 0:
                logger.info(f"Deleted {deleted_count} chat sessions.")
                return deleted_count  # Return the number of deleted sessions
            else:
                logger.info("No chat sessions found.")
                return 0  # No chat sessions found

        except Exception as e:
            # Log the exception or handle it as needed
            logger.error(f"An error occurred while deleting all chat sessions: {e}")
            return None  # Return None if an error occurred
        
    def drop_all_entries(self) -> Optional[int]:
        """
        Drop all entries from the store.

        Args:
            None

        Returns:
            Optional[int]: The number of entries deleted, or None if an error occurred during deletion.
        """
        try:
            # Initialize the counter for deleted entries
            deleted_count = 0

            # Iterate through all keys in the store and delete them
            for key in self.history_store.scan_iter():
                self.history_store.delete(key)
                deleted_count += 1  # Increment the counter for each deleted entry

            # Log and return the number of entries deleted
            if deleted_count > 0:
                logger.info(f"Dropped {deleted_count} entries from the store.")
                return deleted_count  # Return the number of deleted entries
            else:
                logger.info("No entries found to drop.")
                return 0  # No entries found

        except Exception as e:
            # Log the exception and return None if an error occurs
            logger.error(f"An error occurred while dropping entries from the store: {e}")
            return None