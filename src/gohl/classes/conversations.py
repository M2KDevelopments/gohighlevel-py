"""Conversations functionality for GoHighLevel API.

This module provides the Conversations class for managing conversations in GoHighLevel,
including operations like getting, updating, and searching conversations.
"""

from typing import Dict, List, Optional, TypedDict, Union
import requests

from .conversations_email import ConversationsEmail
from .conversations_messages import ConversationsMessages
from .conversations_providers import ConversationsProviders


class DateRange(TypedDict):
    """Type definition for date range filter."""
    startDate: str
    endDate: str


class ConversationFilters(TypedDict, total=False):
    """Type definition for conversation search filters."""
    status: str
    dateRange: DateRange


class Conversations:
    """Conversations management class for GoHighLevel API.

    This class provides methods for managing conversations, including operations
    for retrieving, updating, and searching conversations.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Conversations class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data
        self.email = ConversationsEmail(auth_data)
        self.messages = ConversationsMessages(auth_data)
        self.providers = ConversationsProviders(auth_data)

    def get_all(
        self,
        location_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all conversations for a location.

        Args:
            location_id (str): The ID of the location
            limit (int, optional): Number of conversations to return. Defaults to 50.
            skip (int, optional): Number of conversations to skip. Defaults to 0.

        Returns:
            List[Dict]: List of conversations

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'locationId': location_id,
            'limit': limit,
            'skip': skip
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/conversations",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['conversations']

    def get(self, conversation_id: str) -> Dict:
        """Get a specific conversation.

        Args:
            conversation_id (str): The ID of the conversation to retrieve

        Returns:
            Dict: Conversation object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/conversations/{conversation_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['conversation']

    def update(self, conversation_id: str, data: Dict) -> Dict:
        """Update a conversation.

        Args:
            conversation_id (str): The ID of the conversation to update
            data (Dict): Updated conversation data

        Returns:
            Dict: Updated conversation object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/conversations/{conversation_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['conversation']

    def search(
        self,
        location_id: str,
        query: str,
        filters: Optional[ConversationFilters] = None
    ) -> List[Dict]:
        """Search conversations.

        Args:
            location_id (str): The ID of the location
            query (str): Search query string
            filters (Optional[ConversationFilters], optional): Search filters.
                Defaults to None.

        Returns:
            List[Dict]: List of matching conversations

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            'query': query
        }
        if filters:
            data['filters'] = filters

        response = requests.post(
            f"{self.auth_data['baseurl']}/conversations/search",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['conversations'] 