"""
This script is used to test the functionality of chat history object.
Tests performed:
- Create new conversation                       
- Add messages to the existing chat history    
- Retrieve chat history by session ID          
- Retrieve chat history by user ID                          
- Update field in chat history                 
- Delete chat history by session ID
- Delete chat history by user ID
- Delete all chat histories
- Delete all entries (chat histories, documents, etc.)
"""

import os
import sys
from uuid import uuid4

# Add to system path the '../' directory
_current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(_current_dir, "../"))

from src.config.config import ENCRYPTION_KEY
from src.utils.encryption import encrypt_word
from src.infra.document_store import DocumentStore
from src.chatbot.chatbot_entities import MessageRole

# -------------------------------
# Constants
# -------------------------------
user_email = "support-team@caspian.ai"
user_id = encrypt_word(user_email, ENCRYPTION_KEY)

# -------------------------------
# Initializations
# -------------------------------
document_store = DocumentStore()


# -------------------------------
# Create new test conversations
# -------------------------------
question = "Test Message"
input_intent = "rag"
n_new_conversations = 2

for i in range(n_new_conversations):
    session_id = str(uuid4())
    message_id = str(uuid4())
    document_store.add_message_to_history(
        session_id=session_id,
        message_id=message_id,
        user_id=user_id,
        role=MessageRole.USER,
        content=question,
        intent=input_intent,
    )

# -------------------------------
# Add messages to the existing chat history
# -------------------------------
answer = "Test Message"
response_message_id = str(uuid4())
reference = {}

n_msgs_to_add = 10

for i in range(n_msgs_to_add): 
    document_store.add_message_to_history(
            session_id=session_id,
            question_id=message_id,
            message_id=response_message_id,
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content=answer,
            reference={}
        )

# -------------------------------
# Retrieve chat history by session ID
# -------------------------------
# session_id = "6449f152-c480-41de-8fa4-e88f91a203fa"
chat_history = document_store.get_chat_history(
    user_id=user_id,
    session_id=session_id,
    # num_conversation_pairs=3
    )
chat_history.dict()

# -------------------------------
# Retrieve chat history by user ID
# -------------------------------
user_chat_history = document_store.get_history_by_user_id(user_id=user_id)
user_chat_history

# -------------------------------
# Update field in chat history
# -------------------------------
# session_id = "7f7f98d2-2da8-4b86-9008-90f4fc0868c3"
topic = "Update Topic Name"
deleted = True

document_store.update_field(
    key="topic",
    value=topic,
    session_id=session_id,
    user_id=user_id
)

document_store.update_field(
    key="deleted",
    value=deleted,
    session_id=session_id,
    user_id=user_id
)


# -------------------------------
# Delete chat history by session ID
# -------------------------------
# session_id = "7f7f98d2-2da8-4b86-9008-90f4fc0868c3"
document_store.delete_chat_history_by_session_id(user_id, session_id)



# -------------------------------
# Delete chat history by user ID
# -------------------------------
document_store.delete_chat_history_by_user_id(user_id)


# -------------------------------
# Delete all chat histories
# -------------------------------
document_store.delete_all_chats()


# -------------------------------
# Delete all entries (chat histories, documents, etc.)
# -------------------------------
document_store.drop_all_entries()