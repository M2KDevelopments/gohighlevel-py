"""Email functionality for conversations in GoHighLevel API.

This module provides the ConversationsEmail class for managing email communications
within conversations in GoHighLevel.
"""

from typing import Dict, List, Optional
import requests


class ConversationsEmail:
    """Email management class for conversations in GoHighLevel API.

    This class provides methods for sending and managing emails within conversations.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the ConversationsEmail class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def send(self, conversation_id: str, email: Dict) -> Dict:
        """Send an email in a conversation.

        Args:
            conversation_id (str): The ID of the conversation
            email (Dict): Email data containing subject, body, and recipients
                Example:
                {
                    "subject": "Meeting Follow-up",
                    "body": "Thank you for your time today...",
                    "to": ["recipient@example.com"],
                    "cc": ["cc@example.com"],  # Optional
                    "bcc": ["bcc@example.com"]  # Optional
                }

        Returns:
            Dict: Response containing the sent email details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/conversations/{conversation_id}/email",
            json=email,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['email'] 