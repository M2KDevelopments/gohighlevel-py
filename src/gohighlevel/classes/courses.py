"""Courses functionality for GoHighLevel API.

This module provides the Courses class for managing courses and their content
in GoHighLevel.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class CourseFilter(TypedDict, total=False):
    """Type definition for course filters."""
    status: str  # 'published', 'draft'
    categoryId: str
    search: str


class CourseContent(TypedDict, total=False):
    """Type definition for course content."""
    title: str
    description: str
    type: str  # 'video', 'text', 'quiz', etc.
    content: Dict
    order: int
    isRequired: bool


class Course:
    """Courses management class for GoHighLevel API.

    This class provides methods for managing courses, including creating,
    updating, and retrieving courses and their content.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Courses class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        location_id: str,
        filters: Optional[CourseFilter] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all courses for a location.

        Args:
            location_id (str): The ID of the location
            filters (Optional[CourseFilter], optional): Filter criteria for courses.
                Defaults to None.
            limit (int, optional): Number of courses to return. Defaults to 50.
            skip (int, optional): Number of courses to skip. Defaults to 0.

        Returns:
            List[Dict]: List of courses

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
        if filters:
            params.update(filters)

        response = requests.get(
            f"{self.auth_data['baseurl']}/courses",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['courses']

    def get(self, course_id: str) -> Dict:
        """Get a specific course.

        Args:
            course_id (str): The ID of the course to retrieve

        Returns:
            Dict: Course details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/courses/{course_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['course']

    def add(self, location_id: str, course: Dict) -> Dict:
        """Create a new course.

        Args:
            location_id (str): The ID of the location
            course (Dict): Course data
                Example:
                {
                    "title": "Marketing Basics",
                    "description": "Learn marketing fundamentals",
                    "categoryId": "category_id",
                    "status": "draft",
                    "thumbnail": "https://example.com/thumbnail.jpg"
                }

        Returns:
            Dict: Created course details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        course['locationId'] = location_id
        response = requests.post(
            f"{self.auth_data['baseurl']}/courses",
            json=course,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['course']

    def update(self, course_id: str, data: Dict) -> Dict:
        """Update a course.

        Args:
            course_id (str): The ID of the course to update
            data (Dict): Updated course data
                Example:
                {
                    "title": "Updated Marketing Course",
                    "description": "Updated description",
                    "status": "published"
                }

        Returns:
            Dict: Updated course details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/courses/{course_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['course']

    def delete(self, course_id: str) -> Dict:
        """Delete a course.

        Args:
            course_id (str): The ID of the course to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/courses/{course_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_content(self, course_id: str) -> List[Dict]:
        """Get content for a specific course.

        Args:
            course_id (str): The ID of the course

        Returns:
            List[Dict]: List of course content items

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/courses/{course_id}/content",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['content']

    def add_content(self, course_id: str, content: CourseContent) -> Dict:
        """Add content to a course.

        Args:
            course_id (str): The ID of the course
            content (CourseContent): Content data
                Example:
                {
                    "title": "Introduction",
                    "description": "Course introduction",
                    "type": "video",
                    "content": {
                        "url": "https://example.com/video.mp4",
                        "duration": 300
                    },
                    "order": 1,
                    "isRequired": True
                }

        Returns:
            Dict: Created content details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/courses/{course_id}/content",
            json=content,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['content'] 