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

    def get(self, survey_id: str) -> Dict:
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
            f"{self.auth_data['baseurl']}/surveys/{survey_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['survey']

    def create(self, location_id: str, survey: Survey) -> Dict:
        """Create a new survey.

        Args:
            location_id (str): The ID of the location
            survey (Survey): Survey data
                Example:
                {
                    "name": "Customer Feedback",
                    "description": "Annual customer satisfaction survey",
                    "questions": [
                        {
                            "text": "How satisfied are you?",
                            "type": "rating",
                            "required": True,
                            "settings": {
                                "scale": 5,
                                "labels": ["Poor", "Excellent"]
                            }
                        }
                    ],
                    "settings": {
                        "branding": {
                            "logo": "https://example.com/logo.png",
                            "colors": {"primary": "#FF0000"}
                        },
                        "notifications": {
                            "email": "admin@example.com"
                        }
                    },
                    "status": "draft"
                }

        Returns:
            Dict: Created survey details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            **survey
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/surveys",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['survey']

    def update(self, survey_id: str, data: Dict) -> Dict:
        """Update a survey.

        Args:
            survey_id (str): The ID of the survey to update
            data (Dict): Updated survey data
                Example:
                {
                    "name": "Updated Survey Name",
                    "status": "active",
                    "settings": {
                        "notifications": {
                            "slack": "webhook_url"
                        }
                    }
                }

        Returns:
            Dict: Updated survey details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/surveys/{survey_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['survey']

    def delete(self, survey_id: str) -> Dict:
        """Delete a survey.

        Args:
            survey_id (str): The ID of the survey to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/surveys/{survey_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_responses(
        self,
        survey_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get survey responses.

        Args:
            survey_id (str): The ID of the survey
            limit (int, optional): Number of responses to return. Defaults to 50.
            skip (int, optional): Number of responses to skip. Defaults to 0.

        Returns:
            List[Dict]: List of survey responses

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
            f"{self.auth_data['baseurl']}/surveys/{survey_id}/responses",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['responses']

    def get_analytics(
        self,
        survey_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """Get survey analytics.

        Args:
            survey_id (str): The ID of the survey
            start_date (Optional[str], optional): Start date in ISO format. Defaults to None.
            end_date (Optional[str], optional): End date in ISO format. Defaults to None.

        Returns:
            Dict: Survey analytics data

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
            f"{self.auth_data['baseurl']}/surveys/{survey_id}/analytics",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['analytics']

    def export_responses(
        self,
        survey_id: str,
        format: str = 'csv'
    ) -> bytes:
        """Export survey responses.

        Args:
            survey_id (str): The ID of the survey
            format (str, optional): Export format ('csv' or 'xlsx'). Defaults to 'csv'.

        Returns:
            bytes: Exported file content

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {'format': format}

        response = requests.get(
            f"{self.auth_data['baseurl']}/surveys/{survey_id}/export",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.content 