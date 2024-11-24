"""Module containing intent related entities"""

from enum import Enum


class Intent(str, Enum):
    """
    Enum class for defining various types of intents.

    Attributes:
        DEFAULT (str): Represents the default intent when no specific type is determined.
        EXTRACTION (str): Represents an intent for extraction purposes.
        RFPChat (str): Represents an intent for RFP chat purposes.
        RFPSimilarity (str): Represents an intent for RFP similarity purposes.
    """

    DEFAULT = "default"
    RFPChat_EXTRACTION = "rfp_chat_extraction"
    RFPSimilarity_EXTRACTION = "rfp_similar_extraction"
    RFPChat = "rfp_chat"
    RFPSimilarity = "rfp_similar"
    RFPRAISE = "rfp_raise"
    RFPReferenze = "rfp_referenze"
