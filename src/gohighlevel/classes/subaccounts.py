"""SubAccounts functionality for GoHighLevel API.

This module provides the SubAccounts class for managing sub-accounts (formerly locations)
in GoHighLevel, including creating, updating, and managing sub-accounts.
"""

from typing import Dict, List, Optional, Union, TypedDict
import requests

from .auth.authdata import Auth
from .subaccounts_customvalues import CustomValue
from .subaccounts_customfields import CustomField
from .contacts_tags import Tag


class SearchTask(TypedDict, total=False):
    """Type definition for search task parameters."""
    contact_id: str
    completed: bool
    assigned_to: List[str]
    query: str
    limit: int
    skip: int
    business_id: str


class SubAccounts:
    """
    Endpoints For Subaccounts
    https://highlevel.stoplight.io/docs/integrations/e283eac258a96-sub-account-formerly-location-api
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the SubAccounts class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data
        self.custom_fields = CustomField(auth_data)
        self.custom_values = CustomValue(auth_data)
        self.tags = Tag(auth_data)

    def get(self, location_id: str) -> Dict:
        """Get a sub-account by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/d777490312af4-get-sub-account-formerly-location
        
        Args:
            location_id (str): The ID of the sub-account/location to retrieve
            
        Returns:
            Dict: Sub-account details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/location/{location_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['location']

    def get_timezones(self, location_id: str) -> Dict:
        """Get all timezones for a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            
        Returns:
            Dict: Timezone information
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/location/{location_id}/timezones",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def search_task(self, location_id: str, search: SearchTask) -> List[Dict]:
        """Search for tasks in a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            search (SearchTask): Search parameters
            
        Returns:
            List[Dict]: List of matching tasks
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/location/{location_id}/tasks/search",
            json={
                'contactId': search.get('contact_id'),
                'completed': search.get('completed'),
                'assignedTo': search.get('assigned_to'),
                'query': search.get('query'),
                'limit': search.get('limit'),
                'skip': search.get('skip'),
                'businessId': search.get('business_id')
            },
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['tasks']

    def search(self, limit: int = 10, order: str = 'asc', skip: int = 0,
              company_id: Optional[str] = None, email: Optional[str] = None) -> List[Dict]:
        """Search for sub-accounts.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/12f3fb56990d3-search
        
        Args:
            limit (int): Number of results to return (default: 10)
            order (str): Sort order ('asc' or 'desc') (default: 'asc')
            skip (int): Number of results to skip (default: 0)
            company_id (Optional[str]): Filter by company ID
            email (Optional[str]): Filter by email
            
        Returns:
            List[Dict]: List of matching sub-accounts
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        params = {
            'limit': limit,
            'order': order,
            'skip': skip
        }
        if company_id:
            params['companyId'] = company_id
        if email:
            params['email'] = email
            
        response = requests.get(
            f"{self.auth_data.baseurl}/location/search",
            params=params,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['locations']

    def create(self, data: Dict) -> Dict:
        """Create a new sub-account.
        
        Args:
            data (Dict): The sub-account data to create
            
        Returns:
            Dict: Created sub-account details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/location",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def update(self, location_id: str, data: Dict) -> Dict:
        """Update a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location to update
            data (Dict): The updated sub-account data
            
        Returns:
            Dict: Updated sub-account details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.put(
            f"{self.auth_data.baseurl}/location/{location_id}",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def delete(self, location_id: str, delete_twilio_account: bool = False) -> Dict:
        """Delete a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location to delete
            delete_twilio_account (bool): Whether to delete the associated Twilio account
            
        Returns:
            Dict: Response indicating success
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/location/{location_id}",
            params={'deleteTwilioAccount': str(delete_twilio_account).lower()},
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 