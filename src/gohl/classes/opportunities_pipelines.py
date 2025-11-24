"""Opportunity Pipelines functionality for GoHighLevel API.

This module provides the Pipelines class for managing opportunity pipelines
in GoHighLevel, including stages and pipeline configuration.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class PipelineConfig(TypedDict, total=False):
    """Type definition for pipeline configuration."""
    name: str
    description: Optional[str]
    stages: List[Dict[str, any]]  # List of stage configurations
    settings: Optional[Dict[str, any]]
    isDefault: Optional[bool]


class Pipelines:
    """Pipelines management class for GoHighLevel API.

    This class provides methods for managing opportunity pipelines,
    including stages and pipeline configuration.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Pipelines class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self, location_id: str) -> List[Dict]:
        """Get all pipelines.

        Args:
            location_id (str): The ID of the location

        Returns:
            List[Dict]: List of pipelines

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {'locationId': location_id}

        response = requests.get(
            f"{self.auth_data['baseurl']}/opportunities/pipelines",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['pipelines']

    def get(self, pipeline_id: str) -> Dict:
        """Get a specific pipeline.

        Args:
            pipeline_id (str): The ID of the pipeline to retrieve

        Returns:
            Dict: Pipeline details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/opportunities/pipelines/{pipeline_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['pipeline']

    def create(self, location_id: str, config: PipelineConfig) -> Dict:
        """Create a new pipeline.

        Args:
            location_id (str): The ID of the location
            config (PipelineConfig): Pipeline configuration
                Example:
                {
                    "name": "Sales Pipeline",
                    "description": "Main sales process pipeline",
                    "stages": [
                        {
                            "name": "Lead In",
                            "order": 1,
                            "probability": 10
                        },
                        {
                            "name": "Qualified",
                            "order": 2,
                            "probability": 30
                        },
                        {
                            "name": "Proposal",
                            "order": 3,
                            "probability": 60
                        }
                    ],
                    "settings": {
                        "autoAdvance": True,
                        "requireNotes": True
                    },
                    "isDefault": True
                }

        Returns:
            Dict: Created pipeline details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        pipeline_data = {
            'locationId': location_id,
            **config
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/opportunities/pipelines",
            json=pipeline_data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['pipeline']

    def update(self, pipeline_id: str, data: Dict) -> Dict:
        """Update a pipeline.

        Args:
            pipeline_id (str): The ID of the pipeline to update
            data (Dict): Updated pipeline data
                Example:
                {
                    "name": "Updated Pipeline Name",
                    "stages": [
                        {
                            "name": "New Stage",
                            "order": 4,
                            "probability": 80
                        }
                    ],
                    "settings": {
                        "requireNotes": False
                    }
                }

        Returns:
            Dict: Updated pipeline details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/opportunities/pipelines/{pipeline_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['pipeline']

    def delete(self, pipeline_id: str) -> Dict:
        """Delete a pipeline.

        Args:
            pipeline_id (str): The ID of the pipeline to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/opportunities/pipelines/{pipeline_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_stages(self, pipeline_id: str) -> List[Dict]:
        """Get all stages in a pipeline.

        Args:
            pipeline_id (str): The ID of the pipeline

        Returns:
            List[Dict]: List of pipeline stages

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/opportunities/pipelines/{pipeline_id}/stages",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['stages']

    def update_stage_order(
        self,
        pipeline_id: str,
        stage_order: List[Dict[str, any]]
    ) -> List[Dict]:
        """Update the order of stages in a pipeline.

        Args:
            pipeline_id (str): The ID of the pipeline
            stage_order (List[Dict[str, any]]): List of stage IDs and their new order
                Example:
                [
                    {"id": "stage1", "order": 1},
                    {"id": "stage2", "order": 2},
                    {"id": "stage3", "order": 3}
                ]

        Returns:
            List[Dict]: Updated list of stages

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/opportunities/pipelines/{pipeline_id}/stages/order",
            json={'stages': stage_order},
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['stages'] 