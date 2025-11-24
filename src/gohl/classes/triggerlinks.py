"""TriggerLinks functionality for GoHighLevel API.

This module provides the TriggerLinks class for managing trigger links
in GoHighLevel, including creation, tracking, and analytics.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class TriggerLinkConfig(TypedDict, total=False):
    """Type definition for trigger link configuration."""
    name: str
    description: str
    type: str  # 'form', 'survey', 'workflow', etc.
    targetId: str  # ID of the target resource
    settings: Dict[str, any]  # link settings
    expiresAt: Optional[str]  # expiration date in ISO format
    tags: List[str]


class TriggerLinks:
    """TriggerLinks management class for GoHighLevel API.

    This class provides methods for managing trigger links, including
    creating, tracking, and analyzing link performance.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the TriggerLinks class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        location_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all trigger links.

        Args:
            location_id (str): The ID of the location
            limit (int, optional): Number of links to return. Defaults to 50.
            skip (int, optional): Number of links to skip. Defaults to 0.

        Returns:
            List[Dict]: List of trigger links

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'locationId': location_id,
            'limit': limit,
            'skip': skip
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/triggerlinks",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['triggerLinks']

    def get(self, link_id: str) -> Dict:
        """Get a specific trigger link.

        Args:
            link_id (str): The ID of the trigger link to retrieve

        Returns:
            Dict: Trigger link details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/triggerlinks/{link_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['triggerLink']

    def create(self, location_id: str, config: TriggerLinkConfig) -> Dict:
        """Create a new trigger link.

        Args:
            location_id (str): The ID of the location
            config (TriggerLinkConfig): Link configuration
                Example:
                {
                    "name": "Customer Survey Link",
                    "description": "Link to customer feedback survey",
                    "type": "survey",
                    "targetId": "survey123",
                    "settings": {
                        "redirectUrl": "https://example.com/thank-you",
                        "trackingEnabled": True
                    },
                    "expiresAt": "2024-12-31T23:59:59Z",
                    "tags": ["feedback", "customer"]
                }

        Returns:
            Dict: Created trigger link details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            **config
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/triggerlinks",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['triggerLink']

    def update(self, link_id: str, data: Dict) -> Dict:
        """Update a trigger link.

        Args:
            link_id (str): The ID of the trigger link to update
            data (Dict): Updated link data
                Example:
                {
                    "name": "Updated Link Name",
                    "settings": {
                        "trackingEnabled": False
                    },
                    "expiresAt": "2025-12-31T23:59:59Z"
                }

        Returns:
            Dict: Updated trigger link details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/triggerlinks/{link_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['triggerLink']

    def delete(self, link_id: str) -> Dict:
        """Delete a trigger link.

        Args:
            link_id (str): The ID of the trigger link to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/triggerlinks/{link_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_analytics(
        self,
        link_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """Get analytics for a trigger link.

        Args:
            link_id (str): The ID of the trigger link
            start_date (Optional[str], optional): Start date in ISO format. Defaults to None.
            end_date (Optional[str], optional): End date in ISO format. Defaults to None.

        Returns:
            Dict: Link analytics data

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {}
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        response = requests.get(
            f"{self.auth_data['baseurl']}/triggerlinks/{link_id}/analytics",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['analytics']

    def get_clicks(
        self,
        link_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get click data for a trigger link.

        Args:
            link_id (str): The ID of the trigger link
            limit (int, optional): Number of clicks to return. Defaults to 50.
            skip (int, optional): Number of clicks to skip. Defaults to 0.

        Returns:
            List[Dict]: List of click events

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
            f"{self.auth_data['baseurl']}/triggerlinks/{link_id}/clicks",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['clicks'] 