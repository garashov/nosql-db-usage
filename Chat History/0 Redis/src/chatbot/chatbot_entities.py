"""Module containing chatbot related entities"""

import uuid
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ChatbotResponse(BaseModel):
    """
    Model for representing a chatbot response.

    This class is used to structure the response data of a chatbot.

    Attributes:
        answer (str): The answer or response provided by the chatbot.
    """

    answer: str


class ChatbotRequest(BaseModel):
    """
    Model for representing a chatbot request.

    This class is used to structure the request data for a chatbot.

    Attributes:
        question (str): The question or input provided to the chatbot.
    """

    question: str


class MessageRole(str, Enum):
    """
    Enumeration for defining the role of a message in a chat interaction.

    This Enum classifies a message as either being from the 'user' or from the 'assistant'.

    Attributes:
        USER (str): Represents a user-sent message.
        ASSISTANT (str): Represents an assistant-sent message.
    """

    USER = "user"
    ASSISTANT = "assistant"


class ChatbotHistoryItem(BaseModel):
    """
    Pydantic model for representing a conversation item (individual message) stored inside the database.

    Attributes:
        role (str): The role of the message sender (user or assistant).
        content (str): The content of the message.
        message_id (str): A UUID identifier for the message.
        intent (Intent | None): The use case of the message.
        reference (dict | None): Additional references found by the LLM extracted as sources to generate the message.
        timestamp (int): UNIX millisecond-granular timestamp.
    """

    role: str
    content: str
    message_id: str
    question_id: Optional[str] = None
    intent: Optional[str] = None
    reference: Optional[dict] = None
    timestamp: int | None
    feedback_rating: int | None


class ChatbotHistory(BaseModel):
    """
    Pydantic model for representing a whole conversation (all exchanged messages) stored inside the database.

    This class is used to store and manage the history of a chatbot session, including all exchanged messages.

    Attributes:
        session_id (uuid.UUID): A UUID for the conversation.
        history (List[ChatbotHistoryItem]): A list of ChatbotHistoryItem objects representing all exchanged messages.
    """

    session_id: uuid.UUID
    history: list[ChatbotHistoryItem]


class ChatbotRequestDetailed(BaseModel):
    """
    Extended model for representing a detailed chatbot request.

    This class extends the basic ChatbotRequest model to include additional details.

    Attributes:
        question (str): The question or input provided to the chatbot.
        answer (str): The answer or response provided by the chatbot.
    """

    question: str
    answer: str
