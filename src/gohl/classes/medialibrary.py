"""Media Library functionality for GoHighLevel API.

This module provides the MediaLibrary class for managing media files
in GoHighLevel, including uploads, folders, and file management.
"""

from typing import Dict, List, Optional, TypedDict, BinaryIO
import requests


class MediaFolder(TypedDict, total=False):
    """Type definition for media folder."""
    name: str
    description: str
    parentId: str
    permissions: Dict[str, List[str]]  # role-based permissions


class MediaFile(TypedDict, total=False):
    """Type definition for media file."""
    name: str
    description: str
    folderId: str
    type: str  # image, video, document
    tags: List[str]
    metadata: Dict[str, str]


class MediaLibrary:
    """Media Library management class for GoHighLevel API.

    This class provides methods for managing media files and folders,
    including uploading, organizing, and retrieving media assets.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the MediaLibrary class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all_files(
        self,
        location_id: str,
        folder_id: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all media files.

        Args:
            location_id (str): The ID of the location
            folder_id (Optional[str], optional): Filter by folder ID. Defaults to None.
            limit (int, optional): Number of files to return. Defaults to 50.
            skip (int, optional): Number of files to skip. Defaults to 0.

        Returns:
            List[Dict]: List of media files

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
        if folder_id:
            params['folderId'] = folder_id

        response = requests.get(
            f"{self.auth_data['baseurl']}/media/files",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['files']

    def get_file(self, file_id: str) -> Dict:
        """Get a specific media file.

        Args:
            file_id (str): The ID of the file to retrieve

        Returns:
            Dict: Media file details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/media/files/{file_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['file']

    def upload_file(
        self,
        location_id: str,
        file: BinaryIO,
        metadata: MediaFile
    ) -> Dict:
        """Upload a new media file.

        Args:
            location_id (str): The ID of the location
            file (BinaryIO): The file to upload
            metadata (MediaFile): File metadata
                Example:
                {
                    "name": "Product Image",
                    "description": "Main product showcase image",
                    "folderId": "folder123",
                    "type": "image",
                    "tags": ["product", "showcase"],
                    "metadata": {
                        "dimensions": "1920x1080",
                        "format": "jpg"
                    }
                }

        Returns:
            Dict: Uploaded file details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        files = {'file': file}
        data = {
            'locationId': location_id,
            'metadata': metadata
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/media/files",
            files=files,
            data=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['file']

    def update_file(self, file_id: str, data: Dict) -> Dict:
        """Update a media file.

        Args:
            file_id (str): The ID of the file to update
            data (Dict): Updated file data
                Example:
                {
                    "name": "Updated Name",
                    "description": "Updated description",
                    "tags": ["new", "tags"]
                }

        Returns:
            Dict: Updated file details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/media/files/{file_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['file']

    def delete_file(self, file_id: str) -> Dict:
        """Delete a media file.

        Args:
            file_id (str): The ID of the file to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/media/files/{file_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_all_folders(
        self,
        location_id: str,
        parent_id: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all media folders.

        Args:
            location_id (str): The ID of the location
            parent_id (Optional[str], optional): Filter by parent folder ID. Defaults to None.
            limit (int, optional): Number of folders to return. Defaults to 50.
            skip (int, optional): Number of folders to skip. Defaults to 0.

        Returns:
            List[Dict]: List of media folders

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
        if parent_id:
            params['parentId'] = parent_id

        response = requests.get(
            f"{self.auth_data['baseurl']}/media/folders",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['folders']

    def create_folder(self, location_id: str, folder: MediaFolder) -> Dict:
        """Create a new media folder.

        Args:
            location_id (str): The ID of the location
            folder (MediaFolder): Folder data
                Example:
                {
                    "name": "Product Images",
                    "description": "All product related images",
                    "parentId": "parent123",
                    "permissions": {
                        "admin": ["read", "write", "delete"],
                        "user": ["read"]
                    }
                }

        Returns:
            Dict: Created folder details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            **folder
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/media/folders",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['folder']

    def update_folder(self, folder_id: str, data: Dict) -> Dict:
        """Update a media folder.

        Args:
            folder_id (str): The ID of the folder to update
            data (Dict): Updated folder data
                Example:
                {
                    "name": "Updated Folder Name",
                    "description": "Updated description"
                }

        Returns:
            Dict: Updated folder details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/media/folders/{folder_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['folder']

    def delete_folder(self, folder_id: str) -> Dict:
        """Delete a media folder.

        Args:
            folder_id (str): The ID of the folder to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/media/folders/{folder_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json() 