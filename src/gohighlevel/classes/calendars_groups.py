"""Calendar groups functionality for GoHighLevel API.

This module provides the CalendarGroup class for managing calendar groups in GoHighLevel,
including operations like creating, updating, and deleting groups, as well as
managing group status and slug validation.
"""

from typing import Dict, List, Optional
import requests


class CalendarGroup:
    """Calendar groups management class for GoHighLevel API.

    This class provides methods for managing calendar groups, including CRUD operations
    and specialized functionality like slug validation and group status management.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the CalendarGroup class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self) -> List[Dict]:
        """Get all calendar groups.

        Returns:
            List[Dict]: List of calendar groups

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/groups",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['calendars']

    def get(self, calendar_id: str) -> Dict:
        """Get a specific calendar group by ID.

        Args:
            calendar_id (str): The ID of the calendar group to retrieve

        Returns:
            Dict: Calendar group object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['calendar']

    def verify_slug(self, location_id: str, slug: str) -> bool:
        """Validate a group slug.

        Args:
            location_id (str): The ID of the location
            slug (str): The slug to validate

        Returns:
            bool: True if the slug is available

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/calendars/groups/validate-slug",
            json={'locationId': location_id, 'slug': slug},
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['available']

    def add(self, calendar_group: Dict) -> Dict:
        """Create a new calendar group.

        Args:
            calendar_group (Dict): Calendar group data to create

        Returns:
            Dict: Created calendar group object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/calendars/groups",
            json=calendar_group,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['group']

    def update(self, group_id: str, name: str, description: str, slug: str) -> Dict:
        """Update an existing calendar group.

        Args:
            group_id (str): The ID of the group to update
            name (str): New group name
            description (str): New group description
            slug (str): New group slug

        Returns:
            Dict: Updated calendar group object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/calendars/groups/{group_id}",
            json={
                'name': name,
                'description': description,
                'slug': slug
            },
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['group']

    def remove(self, group_id: str) -> bool:
        """Delete a calendar group.

        Args:
            group_id (str): The ID of the group to delete

        Returns:
            bool: True if deletion was successful

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/calendars/groups/{group_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['succeeded']

    def set_status(self, group_id: str, is_active: bool) -> bool:
        """Enable or disable a calendar group.

        Args:
            group_id (str): The ID of the group to update
            is_active (bool): Whether the group should be active

        Returns:
            bool: True if status update was successful

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/calendars/groups/{group_id}/status",
            json={'isActive': is_active},
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['success'] 