"""Calendar management functionality for GoHighLevel API.

This module provides the Calendar class for managing calendars in GoHighLevel,
including operations like creating, updating, and deleting calendars, as well as
managing calendar events, appointments, and block slots.
"""

from typing import Dict, List, Optional, Union
import requests

from .calendars_appointmentsnotes import CalendarAppointmentNote
from .calendars_events import CalendarEvent
from .calendars_groups import CalendarGroup
from .calendars_notifications import CalendarNotification
from .calendars_resources import CalendarResource


class Calendar:
    """Calendar management class for GoHighLevel API.

    This class provides methods for managing calendars, including CRUD operations
    and specialized calendar functionality like managing free slots and block slots.

    Attributes:
        appointmentnotes (CalendarAppointmentNote): Handler for calendar appointment notes
        events (CalendarEvent): Handler for calendar events
        groups (CalendarGroup): Handler for calendar groups
        notifications (CalendarNotification): Handler for calendar notifications
        resources (CalendarResource): Handler for calendar resources
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Calendar class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data
        self.appointmentnotes = CalendarAppointmentNote(self.auth_data)
        self.events = CalendarEvent(self.auth_data)
        self.groups = CalendarGroup(self.auth_data)
        self.notifications = CalendarNotification(self.auth_data)
        self.resources = CalendarResource(self.auth_data)

    def get_all(self, location_id: str, show_drafted: bool = True) -> List[Dict]:
        """Get all calendars for a location.

        Args:
            location_id (str): The ID of the location
            show_drafted (bool, optional): Whether to include drafted calendars. Defaults to True.

        Returns:
            List[Dict]: List of calendar objects

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars",
            params={
                'locationId': location_id,
                'showDrafted': str(show_drafted).lower()
            },
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['calendars']

    def get(self, calendar_id: str) -> Dict:
        """Get a specific calendar by ID.

        Args:
            calendar_id (str): The ID of the calendar to retrieve

        Returns:
            Dict: Calendar object

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

    def get_free_slots(
        self,
        calendar_id: str,
        start_date: int,
        end_date: int,
        timezone: str = "",
        user_id: str = "userId"
    ) -> Dict:
        """Get free slots for a calendar.

        Args:
            calendar_id (str): The ID of the calendar
            start_date (int): Start timestamp
            end_date (int): End timestamp
            timezone (str, optional): Timezone string. Defaults to "".
            user_id (str, optional): User ID. Defaults to "userId".

        Returns:
            Dict: Calendar free slots information

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'startDate': start_date,
            'endDate': end_date
        }
        if timezone:
            params['timezone'] = timezone
        if user_id:
            params['userId'] = user_id

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}/free-slots",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['calendar']

    def add(self, calendar: Dict) -> Dict:
        """Create a new calendar.

        Args:
            calendar (Dict): Calendar data to create

        Returns:
            Dict: Created calendar object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/calendars",
            json=calendar,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['calendar']

    def create_block_slot(
        self,
        location_id: str,
        start_time: str,
        end_time: str,
        extra: Optional[Dict] = None
    ) -> Dict:
        """Create a block slot in the calendar.

        Args:
            location_id (str): The ID of the location
            start_time (str): Start time of the block
            end_time (str): End time of the block
            extra (Optional[Dict], optional): Additional parameters like calendarId,
                title, assignedUserId. Defaults to None.

        Returns:
            Dict: Created block slot information

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            'startTime': start_time,
            'endTime': end_time,
            **(extra or {})
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/calendars/events/block-slots",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def update(self, calendar_id: str, calendar: Dict) -> Dict:
        """Update an existing calendar.

        Args:
            calendar_id (str): The ID of the calendar to update
            calendar (Dict): Updated calendar data

        Returns:
            Dict: Updated calendar object

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}",
            json=calendar,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['calendar']

    def remove(self, calendar_id: str) -> bool:
        """Delete a calendar.

        Args:
            calendar_id (str): The ID of the calendar to delete

        Returns:
            bool: True if deletion was successful

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/calendars/{calendar_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['succeeded'] 