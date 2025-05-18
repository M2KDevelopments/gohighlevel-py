"""Opportunities functionality for GoHighLevel API.

This module provides the Opportunities class for managing opportunities
in GoHighLevel, including pipeline management and deal tracking.
"""

from typing import Dict, List, Optional, TypedDict
import requests

from .opportunities_pipelines import Pipelines
from .opportunities_notes import Notes


class OpportunityData(TypedDict, total=False):
    """Type definition for opportunity data."""
    name: str
    description: Optional[str]
    value: float
    currency: str
    pipelineId: str
    stageId: str
    status: str  # 'open', 'won', 'lost'
    assignedTo: Optional[str]  # user ID
    contactId: Optional[str]
    companyId: Optional[str]
    priority: Optional[str]  # 'low', 'medium', 'high'
    tags: Optional[List[str]]
    customFields: Optional[Dict[str, any]]
    dueDate: Optional[str]  # ISO date string


class Opportunities:
    """Opportunities management class for GoHighLevel API.

    This class provides methods for managing opportunities, including
    pipeline management, deal tracking, and opportunity analytics.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Opportunities class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data
        self.pipelines = Pipelines(auth_data)
        self.notes = Notes(auth_data)

    def get_all(
        self,
        location_id: str,
        pipeline_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all opportunities.

        Args:
            location_id (str): The ID of the location
            pipeline_id (Optional[str], optional): Filter by pipeline ID. Defaults to None.
            stage_id (Optional[str], optional): Filter by stage ID. Defaults to None.
            status (Optional[str], optional): Filter by status. Defaults to None.
            limit (int, optional): Number of opportunities to return. Defaults to 50.
            skip (int, optional): Number of opportunities to skip. Defaults to 0.

        Returns:
            List[Dict]: List of opportunities

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
        if pipeline_id:
            params['pipelineId'] = pipeline_id
        if stage_id:
            params['stageId'] = stage_id
        if status:
            params['status'] = status

        response = requests.get(
            f"{self.auth_data['baseurl']}/opportunities",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['opportunities']

    def get(self, opportunity_id: str) -> Dict:
        """Get a specific opportunity.

        Args:
            opportunity_id (str): The ID of the opportunity to retrieve

        Returns:
            Dict: Opportunity details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/opportunities/{opportunity_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['opportunity']

    def create(self, location_id: str, data: OpportunityData) -> Dict:
        """Create a new opportunity.

        Args:
            location_id (str): The ID of the location
            data (OpportunityData): Opportunity data
                Example:
                {
                    "name": "Enterprise Deal",
                    "description": "Potential enterprise client",
                    "value": 50000.00,
                    "currency": "USD",
                    "pipelineId": "pipe123",
                    "stageId": "stage1",
                    "status": "open",
                    "assignedTo": "user123",
                    "contactId": "contact456",
                    "priority": "high",
                    "tags": ["enterprise", "q4"],
                    "customFields": {
                        "industry": "technology",
                        "source": "referral"
                    },
                    "dueDate": "2024-12-31T23:59:59Z"
                }

        Returns:
            Dict: Created opportunity details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        opportunity_data = {
            'locationId': location_id,
            **data
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/opportunities",
            json=opportunity_data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['opportunity']

    def update(self, opportunity_id: str, data: Dict) -> Dict:
        """Update an opportunity.

        Args:
            opportunity_id (str): The ID of the opportunity to update
            data (Dict): Updated opportunity data
                Example:
                {
                    "name": "Updated Deal Name",
                    "value": 75000.00,
                    "status": "won",
                    "priority": "medium"
                }

        Returns:
            Dict: Updated opportunity details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/opportunities/{opportunity_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['opportunity']

    def delete(self, opportunity_id: str) -> Dict:
        """Delete an opportunity.

        Args:
            opportunity_id (str): The ID of the opportunity to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/opportunities/{opportunity_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_analytics(
        self,
        location_id: str,
        pipeline_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """Get opportunity analytics.

        Args:
            location_id (str): The ID of the location
            pipeline_id (Optional[str], optional): Filter by pipeline ID. Defaults to None.
            start_date (Optional[str], optional): Start date in ISO format. Defaults to None.
            end_date (Optional[str], optional): End date in ISO format. Defaults to None.

        Returns:
            Dict: Opportunity analytics data

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {'locationId': location_id}
        if pipeline_id:
            params['pipelineId'] = pipeline_id
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        response = requests.get(
            f"{self.auth_data['baseurl']}/opportunities/analytics",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['analytics'] 