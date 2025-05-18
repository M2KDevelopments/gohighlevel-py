"""Calendar resources functionality for GoHighLevel API.

This module provides the CalendarResource class for managing calendar resources
in GoHighLevel, including operations like creating, updating, and deleting resources
such as equipment and rooms.
"""

import requests
from typing import Dict, List, Optional, Literal, Union


ResourceType = Literal['equipments', 'rooms']


class CalendarResource:
    """Calendar resources management class for GoHighLevel API.

    This class provides methods for managing calendar resources, including CRUD operations
    for equipment and room resources.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the CalendarResource class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self, resource_type: ResourceType) -> List[Dict]:
        """List all calendar resources of a specific type.

        Args:
            resource_type (ResourceType): Type of resource ('equipments' or 'rooms')

        Returns:
            List[Dict]: List of calendar resources

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/resources/{resource_type}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get(self, resource_id: str, resource_type: ResourceType) -> Dict:
        """Get a specific calendar resource.

        Args:
            resource_id (str): The ID of the resource to retrieve
            resource_type (ResourceType): Type of resource ('equipments' or 'rooms')

        Returns:
            Dict: Calendar resource object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/resources/{resource_type}/{resource_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def add(self, resource_type: ResourceType, resource: Dict) -> Dict:
        """Create a new calendar resource.

        Args:
            resource_type (ResourceType): Type of resource ('equipments' or 'rooms')
            resource (Dict): Resource data to create

        Returns:
            Dict: Created resource object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/calendars/resources/{resource_type}",
            json=resource,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['note']

    def update(self, resource_id: str, resource_type: ResourceType, resource: Dict) -> Dict:
        """Update an existing calendar resource.

        Args:
            resource_id (str): The ID of the resource to update
            resource_type (ResourceType): Type of resource ('equipments' or 'rooms')
            resource (Dict): Updated resource data

        Returns:
            Dict: Updated resource object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/calendars/resources/{resource_type}/{resource_id}",
            json=resource,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['note']

    def remove(self, resource_id: str, resource_type: ResourceType) -> bool:
        """Delete a calendar resource.

        Args:
            resource_id (str): The ID of the resource to delete
            resource_type (ResourceType): Type of resource ('equipments' or 'rooms')

        Returns:
            bool: True if deletion was successful

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/calendars/resources/{resource_type}/{resource_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['succeeded'] 