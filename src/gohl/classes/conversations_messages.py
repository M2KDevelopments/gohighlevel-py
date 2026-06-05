"""Messages functionality for conversations in GoHighLevel API.

This module provides the ConversationsMessages class for managing messages
within conversations in GoHighLevel.
"""

from enum import Enum
from typing import Dict, List, Optional, TypedDict, Union
import requests


class MessageType(str, Enum):
    """Allowed message channel types for the conversations API."""
    SMS = "SMS"
    EMAIL = "Email"
    WHATSAPP = "WhatsApp"
    GMB = "GMB"
    IG = "IG"
    FB = "FB"
    CUSTOM = "Custom"
    LIVE_CHAT = "Live_Chat"
    CALL = "Call"


def _validate_message_type(message: Dict) -> None:
    """Validate that ``message['type']`` is a known :class:`MessageType`.

    Accepts either a ``MessageType`` member or its string value.

    Raises:
        ValueError: If ``type`` is missing or not a valid message type.
    """
    type_value = message.get("type")
    if type_value is None:
        raise ValueError("Message 'type' is required")
    if type_value not in {t.value for t in MessageType}:
        valid = ", ".join(sorted(t.value for t in MessageType))
        raise ValueError(
            f"Invalid message type {type_value!r}. Must be one of: {valid}"
        )


class MessageData(TypedDict, total=False):
    """Type definition for message data."""
    body: str
    type: Union[MessageType, str]
    attachments: List[Dict]
    metadata: Dict


class InboundMessageData(TypedDict, total=False):
    """Type definition for an inbound message.

    Either ``conversationId`` or ``contactId`` is required, along with
    ``type`` and ``conversationProviderId``.
    """
    type: Union[MessageType, str]
    conversationId: str
    contactId: str
    conversationProviderId: str
    message: str
    attachments: List[str]
    html: str
    subject: str
    emailFrom: str
    emailTo: str
    date: str
    call: Dict
    altId: str
    direction: str


class ConversationsMessages:
    """Messages management class for conversations in GoHighLevel API.

    This class provides methods for managing messages within conversations,
    including retrieving and sending messages.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the ConversationsMessages class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
            self,
            conversation_id: str,
            limit: int = 50,
            skip: int = 0
    ) -> List[Dict]:
        """Get all messages in a conversation.

        Args:
            conversation_id (str): The ID of the conversation
            limit (int, optional): Number of messages to return. Defaults to 50.
            skip (int, optional): Number of messages to skip. Defaults to 0.

        Returns:
            List[Dict]: List of messages in the conversation

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'limit': limit,
            'skip': skip
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/conversations/{conversation_id}/messages",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['messages']

    def add(self, conversation_id: str, message: MessageData) -> Dict:
        """Send a message in a conversation.

        Args:
            conversation_id (str): The ID of the conversation
            message (MessageData): Message data containing body and type
                Example:
                {
                    "body": "Hello! How can I help you today?",
                    "type": "SMS",
                    "attachments": [{"url": "https://example.com/file.pdf"}],
                    "metadata": {"key": "value"}
                }

        Returns:
            Dict: Response containing the sent message details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing or ``type`` is invalid
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        _validate_message_type(message)

        response = requests.post(
            f"{self.auth_data['baseurl']}/conversations/{conversation_id}/messages",
            json=message,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['message']

    def add_inbound(self, message: InboundMessageData) -> Dict:
        """Add an inbound message to a conversation.

        See https://marketplace.gohighlevel.com/docs/ghl/conversations/add-an-inbound-message

        Unlike :meth:`add`, the target is identified inside the payload
        (``conversationId`` or ``contactId``) rather than in the URL.

        Args:
            message (InboundMessageData): Inbound message payload. Requires
                ``type`` and ``conversationProviderId``, plus either
                ``conversationId`` or ``contactId``.
                Example:
                {
                    "type": "SMS",
                    "conversationId": "conv_1",
                    "conversationProviderId": "provider_1",
                    "message": "Hello! How can I help you today?",
                    "attachments": ["https://example.com/file.pdf"]
                }

        Returns:
            Dict: Response describing the created message (``conversationId``,
                ``messageId``, etc.)

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing or ``type`` is invalid
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        _validate_message_type(message)

        response = requests.post(
            f"{self.auth_data['baseurl']}/conversations/messages/inbound",
            json=message,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()
