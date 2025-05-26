"""Surveys functionality for GoHighLevel API.

This module provides the Surveys class for managing surveys
in GoHighLevel, including questions, responses, and analytics.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class SurveyQuestion(TypedDict, total=False):
    """Type definition for survey question."""
    text: str
    type: str  # 'multiple_choice', 'text', 'rating', etc.
    required: bool
    options: Optional[List[str]]  # for multiple choice questions
    settings: Optional[Dict]  # additional question settings


class Survey(TypedDict, total=False):
    """Type definition for survey."""
    name: str
    description: str
    questions: List[SurveyQuestion]
    settings: Dict[str, any]  # branding, notifications, etc.
    status: str  # 'draft', 'active', 'closed'


class Surveys:
    """Surveys management class for GoHighLevel API.

    This class provides methods for managing surveys, including creating,
    updating, and analyzing survey responses.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Surveys class.

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
        """Get all surveys.

        Args:
            location_id (str): The ID of the location
            limit (int, optional): Number of surveys to return. Defaults to 50.
            skip (int, optional): Number of surveys to skip. Defaults to 0.

        Returns:
            List[Dict]: List of surveys

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
            f"{self.auth_data['baseurl']}/surveys",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['surveys']

    def get_submissions(self, survey_id: str) -> Dict:
        """Get a specific survey.

        Args:
            survey_id (str): The ID of the survey to retrieve

        Returns:
            Dict: Survey details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/surveys/submissions/",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['submissions']

    
