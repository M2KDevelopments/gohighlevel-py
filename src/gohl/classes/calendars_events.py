"""Calendar events functionality for GoHighLevel API.

This module provides the CalendarEvent class for managing calendar events and appointments
in GoHighLevel, including operations like creating, updating, and deleting events,
as well as managing block slots.
"""

import requests
from typing import Dict, List, Optional, TypedDict, Union


class BlockSlot(TypedDict):
    """Type definition for calendar block slot data."""
    calendar_id: str
    start_time: str
    end_time: str
    title: str
    assigned_user_id: str


class CalendarEvent:
    """Calendar events management class for GoHighLevel API.

    This class provides methods for managing calendar events and appointments,
    including CRUD operations and specialized functionality like managing block slots.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the CalendarEvent class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        location_id: str,
        start_time: str,
        end_time: str,
        extra: Optional[Dict] = None
    ) -> List[Dict]:
        """Get all calendar events for a location.

        Args:
            location_id (str): The ID of the location
            start_time (str): Start time for events range
            end_time (str): End time for events range
            extra (Optional[Dict], optional): Additional parameters like userId,
                groupId, calendarId. Defaults to None.

        Returns:
            List[Dict]: List of calendar events

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'locationId': location_id,
            'startTime': start_time,
            'endTime': end_time
        }

        if extra:
            if extra.get('userId'):
                params['userId'] = extra['userId']
            if extra.get('groupId'):
                params['groupId'] = extra['groupId']
            if extra.get('calendarId'):
                params['calendarId'] = extra['calendarId']

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/events",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['events']

    def get_block_slots(
        self,
        location_id: str,
        start_time: str,
        end_time: str,
        extra: Optional[Dict] = None
    ) -> List[Dict]:
        """Get all block slots for a location.

        Args:
            location_id (str): The ID of the location
            start_time (str): Start time for block slots range
            end_time (str): End time for block slots range
            extra (Optional[Dict], optional): Additional parameters like userId,
                groupId, calendarId. Defaults to None.

        Returns:
            List[Dict]: List of block slots

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'locationId': location_id,
            'startTime': start_time,
            'endTime': end_time
        }

        if extra:
            if extra.get('userId'):
                params['userId'] = extra['userId']
            if extra.get('groupId'):
                params['groupId'] = extra['groupId']
            if extra.get('calendarId'):
                params['calendarId'] = extra['calendarId']

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/blocked-slots",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['events']

    def get_appointments(self, event_id: str) -> Dict:
        """Get appointments for an event.

        Args:
            event_id (str): Event ID or Instance ID. For recurring appointments
                send masterEventId to modify original series.

        Returns:
            Dict: Event appointment information

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/calendars/events/appointments/{event_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['event']

    def add_appointment(
        self,
        location_id: str,
        contact_id: str,
        start_time: str,
        calendar: Dict
    ) -> Dict:
        """Create a new appointment.

        Args:
            location_id (str): The ID of the location
            contact_id (str): The ID of the contact
            start_time (str): Start time of the appointment
            calendar (Dict): Calendar appointment data

        Returns:
            Dict: Created appointment information

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            'contactId': contact_id,
            'startTime': start_time,
            **calendar
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/calendars/events/appointments",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def update_appointment(self, event_id: str, event: Dict) -> Dict:
        """Update an existing appointment.

        Args:
            event_id (str): The ID of the event to update
            event (Dict): Updated appointment data

        Returns:
            Dict: Updated appointment information

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/calendars/events/appointments/{event_id}",
            json=event,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def update_block_slot(self, event_id: str, slot: BlockSlot) -> BlockSlot:
        """Update a block slot.

        Args:
            event_id (str): The ID of the block slot to update
            slot (BlockSlot): Updated block slot data

        Returns:
            BlockSlot: Updated block slot information

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/calendars/events/block-slots/{event_id}",
            json={
                'calendarId': slot['calendar_id'],
                'startTime': slot['start_time'],
                'endTime': slot['end_time'],
                'title': slot['title'],
                'assignedUserId': slot['assigned_user_id']
            },
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return BlockSlot(**response.json())

    def remove(self, event_id: str) -> bool:
        """Delete an event.

        Args:
            event_id (str): The ID of the event to delete

        Returns:
            bool: True if deletion was successful

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/calendars/events/{event_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['succeeded'] 