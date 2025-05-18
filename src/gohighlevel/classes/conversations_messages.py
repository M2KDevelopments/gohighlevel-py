"""Messages functionality for conversations in GoHighLevel API.

This module provides the ConversationsMessages class for managing messages
within conversations in GoHighLevel.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class MessageData(TypedDict, total=False):
    """Type definition for message data."""
    body: str
    type: str  # 'text', 'image', 'file', etc.
    attachments: List[Dict]
    metadata: Dict


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
                    "type": "text",
                    "attachments": [{"url": "https://example.com/file.pdf"}],
                    "metadata": {"key": "value"}
                }

        Returns:
            Dict: Response containing the sent message details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/conversations/{conversation_id}/messages",
            json=message,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['message'] 