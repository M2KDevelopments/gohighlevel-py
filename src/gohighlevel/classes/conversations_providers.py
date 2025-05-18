"""Providers functionality for conversations in GoHighLevel API.

This module provides the ConversationsProviders class for managing conversation
providers in GoHighLevel.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class ProviderFilter(TypedDict, total=False):
    """Type definition for provider filters."""
    type: str  # 'sms', 'email', 'facebook', etc.
    status: str  # 'active', 'inactive'


class ConversationsProviders:
    """Providers management class for conversations in GoHighLevel API.

    This class provides methods for managing conversation providers,
    including retrieving and updating provider settings.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the ConversationsProviders class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        location_id: str,
        filters: Optional[ProviderFilter] = None
    ) -> List[Dict]:
        """Get all conversation providers for a location.

        Args:
            location_id (str): The ID of the location
            filters (Optional[ProviderFilter], optional): Filter criteria for providers.
                Defaults to None.

        Returns:
            List[Dict]: List of conversation providers

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {'locationId': location_id}
        if filters:
            params.update(filters)

        response = requests.get(
            f"{self.auth_data['baseurl']}/conversations/providers",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['providers']

    def get(self, provider_id: str) -> Dict:
        """Get a specific conversation provider.

        Args:
            provider_id (str): The ID of the provider to retrieve

        Returns:
            Dict: Provider details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/conversations/providers/{provider_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['provider']

    def update(self, provider_id: str, data: Dict) -> Dict:
        """Update a conversation provider's settings.

        Args:
            provider_id (str): The ID of the provider to update
            data (Dict): Updated provider settings
                Example:
                {
                    "status": "active",
                    "settings": {
                        "autoReply": True,
                        "signature": "Best regards,\\nSupport Team"
                    }
                }

        Returns:
            Dict: Updated provider details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/conversations/providers/{provider_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['provider'] 