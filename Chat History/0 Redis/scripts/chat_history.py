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
from src.chatbot import chatbot_repository
from src.chatbot.chatbot_entities import MessageRole


# -------------------------------
# Create new test conversations
# -------------------------------
question = "Test Message"
user_email = "support-team@caspian.ai"
user_id = encrypt_word(user_email, ENCRYPTION_KEY)
input_intent = "rag"
n_new_conversations = 1

for i in range(n_new_conversations):
    session_id = str(uuid4())
    message_id = str(uuid4())
    chatbot_repository.add_message_to_history(
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
user_email = "support-team@caspian.ai"
user_id = encrypt_word(user_email, ENCRYPTION_KEY)
reference = {}

n_msgs_to_add = 10

for i in range(n_msgs_to_add): 
    chatbot_repository.add_message_to_history(
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
user_email = "support-team@caspian.ai"
user_id = encrypt_word(user_email, ENCRYPTION_KEY)
session_id = "6449f152-c480-41de-8fa4-e88f91a203fa"
chat_history = chatbot_repository.get_chat_history(
    user_id=user_id,
    session_id=session_id,
    num_conversation_pairs=3
    )
chat_history.dict()

# -------------------------------
# Retrieve chat history by user ID
# -------------------------------
user_email = "support-team@caspian.ai"
user_id = encrypt_word(user_email, ENCRYPTION_KEY)
user_chat_history = chatbot_repository.get_history_by_user_id(user_id=user_id)
user_chat_history

# -------------------------------
# Update field in chat history
# -------------------------------
user_email = "support-team@caspian.ai"
user_id = encrypt_word(user_email, ENCRYPTION_KEY)
session_id = "7f7f98d2-2da8-4b86-9008-90f4fc0868c3"
topic = "Update Topic Name"
deleted = True

chatbot_repository.update_field(
    key="topic",
    value=topic,
    session_id=session_id,
    user_id=user_id
)

chatbot_repository.update_field(
    key="deleted",
    value=deleted,
    session_id=session_id,
    user_id=user_id
)


# -------------------------------
# Delete chat history by session ID
# -------------------------------
user_email = "support-team@caspian.ai"
user_id = encrypt_word(user_email, ENCRYPTION_KEY)
session_id = "7f7f98d2-2da8-4b86-9008-90f4fc0868c3"
chatbot_repository.delete_chat_history_by_session_id(user_id, session_id)



# -------------------------------
# Delete chat history by user ID
# -------------------------------
user_email = "support-team@caspian.ai"
user_id = encrypt_word(user_email, ENCRYPTION_KEY)
chatbot_repository.delete_chat_history_by_user_id(user_id)


# -------------------------------
# Delete all chat histories
# -------------------------------
chatbot_repository.delete_all_chats()


# -------------------------------
# Delete all entries (chat histories, documents, etc.)
# -------------------------------
chatbot_repository.drop_all_entries()