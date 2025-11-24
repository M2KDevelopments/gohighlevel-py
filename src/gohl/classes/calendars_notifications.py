"""Calendar notifications functionality for GoHighLevel API.

This module provides the CalendarNotification class for managing calendar notifications
in GoHighLevel, including operations like creating, updating, and deleting notifications.
"""

import requests
from typing import Dict, List, Optional, TypedDict, Union, Literal


class NotificationFilter(TypedDict, total=False):
    """Type definition for notification filter parameters."""
    alt_id: str
    alt_type: Literal['calendar'] | str
    deleted: bool
    is_active: bool
    limit: int
    skip: int


class CalendarNotification:
    """Calendar notifications management class for GoHighLevel API.

    This class provides methods for managing calendar notifications, including CRUD operations
    and specialized functionality for bulk notification management.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the CalendarNotification class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        calendar_id: str,
        extra: Optional[NotificationFilter] = None
    ) -> List[Dict]:
        """Get all notifications for a calendar.

        Args:
            calendar_id (str): The ID of the calendar
            extra (Optional[NotificationFilter], optional): Additional filter parameters.
                Defaults to None.

        Returns:
            List[Dict]: List of calendar notifications

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {}
        if extra:
            if 'alt_id' in extra:
                params['altId'] = extra['alt_id']
            if 'alt_type' in extra:
                params['altType'] = extra['alt_type']
            if 'deleted' in extra:
                params['deleted'] = str(extra['deleted']).lower()
            if 'is_active' in extra:
                params['isActive'] = str(extra['is_active']).lower()
            if 'limit' in extra:
                params['limit'] = extra['limit']
            if 'skip' in extra:
                params['skip'] = extra['skip']

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}/notifications",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get(self, calendar_id: str, notification_id: str) -> Dict:
        """Get a specific calendar notification.

        Args:
            calendar_id (str): The ID of the calendar
            notification_id (str): The ID of the notification to retrieve

        Returns:
            Dict: Calendar notification object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}/notifications/{notification_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def add(self, calendar_id: str, notifications: List[Dict]) -> List[Dict]:
        """Create new calendar notifications.

        Args:
            calendar_id (str): The ID of the calendar
            notifications (List[Dict]): List of notification objects to create

        Returns:
            List[Dict]: List of created notification objects

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}/notifications/",
            json=notifications,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def update(self, calendar_id: str, notification_id: str, notification: Dict) -> Dict:
        """Update an existing calendar notification.

        Args:
            calendar_id (str): The ID of the calendar
            notification_id (str): The ID of the notification to update
            notification (Dict): Updated notification data

        Returns:
            Dict: Updated notification object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}/notifications/{notification_id}",
            json=notification,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['calendar']

    def remove(self, calendar_id: str, notification_id: str) -> str:
        """Delete a calendar notification.

        Args:
            calendar_id (str): The ID of the calendar
            notification_id (str): The ID of the notification to delete

        Returns:
            str: Success message

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}/notifications/{notification_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['message'] 