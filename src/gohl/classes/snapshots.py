"""Snapshots functionality for GoHighLevel API.

This module provides the Snapshots class for managing snapshots
in GoHighLevel, including backup and restore functionality.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class SnapshotConfig(TypedDict, total=False):
    """Type definition for snapshot configuration."""
    name: str
    description: str
    type: str  # 'full', 'partial'
    includedData: List[str]  # data types to include
    retention: int  # days to keep
    schedule: Optional[Dict[str, str]]  # for automated snapshots


class Snapshots:
    """Snapshots management class for GoHighLevel API.

    This class provides methods for managing snapshots, including
    creating backups and restoring data.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Snapshots class.

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
        """Get all snapshots.

        Args:
            location_id (str): The ID of the location
            limit (int, optional): Number of snapshots to return. Defaults to 50.
            skip (int, optional): Number of snapshots to skip. Defaults to 0.

        Returns:
            List[Dict]: List of snapshots

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
            f"{self.auth_data['baseurl']}/snapshots",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['snapshots']

    def get(self, snapshot_id: str) -> Dict:
        """Get a specific snapshot.

        Args:
            snapshot_id (str): The ID of the snapshot to retrieve

        Returns:
            Dict: Snapshot details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/snapshots/{snapshot_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['snapshot']

    def create(self, location_id: str, config: SnapshotConfig) -> Dict:
        """Create a new snapshot.

        Args:
            location_id (str): The ID of the location
            config (SnapshotConfig): Snapshot configuration
                Example:
                {
                    "name": "Weekly Backup",
                    "description": "Full weekly backup",
                    "type": "full",
                    "includedData": ["contacts", "campaigns", "forms"],
                    "retention": 30,
                    "schedule": {
                        "frequency": "weekly",
                        "day": "sunday",
                        "time": "00:00"
                    }
                }

        Returns:
            Dict: Created snapshot details

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
            f"{self.auth_data['baseurl']}/snapshots",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['snapshot']

    def delete(self, snapshot_id: str) -> Dict:
        """Delete a snapshot.

        Args:
            snapshot_id (str): The ID of the snapshot to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/snapshots/{snapshot_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def restore(
        self,
        snapshot_id: str,
        target_location_id: str,
        data_types: Optional[List[str]] = None
    ) -> Dict:
        """Restore data from a snapshot.

        Args:
            snapshot_id (str): The ID of the snapshot to restore from
            target_location_id (str): The ID of the location to restore to
            data_types (Optional[List[str]], optional): Specific data types to restore.
                Defaults to None (restores all data types).

        Returns:
            Dict: Restore operation details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'targetLocationId': target_location_id
        }
        if data_types:
            data['dataTypes'] = data_types

        response = requests.post(
            f"{self.auth_data['baseurl']}/snapshots/{snapshot_id}/restore",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['restore']

    def get_restore_status(self, restore_id: str) -> Dict:
        """Get the status of a restore operation.

        Args:
            restore_id (str): The ID of the restore operation

        Returns:
            Dict: Restore operation status

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/snapshots/restore/{restore_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['status']

    def schedule_snapshot(
        self,
        location_id: str,
        schedule: Dict[str, str],
        config: SnapshotConfig
    ) -> Dict:
        """Schedule automated snapshots.

        Args:
            location_id (str): The ID of the location
            schedule (Dict[str, str]): Schedule configuration
                Example:
                {
                    "frequency": "weekly",
                    "day": "sunday",
                    "time": "00:00"
                }
            config (SnapshotConfig): Snapshot configuration

        Returns:
            Dict: Scheduled snapshot details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            'schedule': schedule,
            **config
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/snapshots/schedule",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['schedule']

    def update_schedule(
        self,
        schedule_id: str,
        schedule: Dict[str, str]
    ) -> Dict:
        """Update a snapshot schedule.

        Args:
            schedule_id (str): The ID of the schedule to update
            schedule (Dict[str, str]): Updated schedule configuration
                Example:
                {
                    "frequency": "daily",
                    "time": "02:00"
                }

        Returns:
            Dict: Updated schedule details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/snapshots/schedule/{schedule_id}",
            json=schedule,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['schedule'] 