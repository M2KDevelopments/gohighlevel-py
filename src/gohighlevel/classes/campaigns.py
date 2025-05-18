"""Campaign functionality for GoHighLevel API.

This module provides the Campaign class for managing campaigns in GoHighLevel,
including creating, updating, and listing campaigns.
"""

from typing import Dict, List, Optional, TypedDict, Literal
from urllib.parse import urlencode
import requests

from .auth.authdata import Auth


class Campaign(TypedDict, total=False):
    """Type definition for a campaign."""
    id: str
    name: str
    type: str
    status: str
    trigger_type: str
    trigger_delay: Optional[int]
    trigger_delay_unit: Optional[str]
    metadata: Optional[Dict]
    created_at: str
    updated_at: str


class CreateCampaign(TypedDict, total=False):
    """Type definition for creating a campaign."""
    name: str
    type: str
    status: str
    trigger_type: str
    trigger_delay: Optional[int]
    trigger_delay_unit: Optional[str]
    metadata: Optional[Dict]


class UpdateCampaign(TypedDict, total=False):
    """Type definition for updating a campaign."""
    name: Optional[str]
    type: Optional[str]
    status: Optional[str]
    trigger_type: Optional[str]
    trigger_delay: Optional[int]
    trigger_delay_unit: Optional[str]
    metadata: Optional[Dict]


class CampaignResponse(TypedDict):
    """Type definition for a campaign response."""
    campaign: Campaign
    trace_id: str


class CampaignListResponse(TypedDict):
    """Type definition for a campaign list response."""
    campaigns: List[Campaign]
    total: int
    trace_id: str


class CampaignListParams(TypedDict, total=False):
    """Type definition for campaign list parameters."""
    page: Optional[int]
    limit: Optional[int]
    sort: Optional[str]
    order: Optional[Literal['asc', 'desc']]
    type: Optional[str]
    status: Optional[str]
    trigger_type: Optional[str]


class CampaignAPI:
    """
    Endpoints For Campaigns
    https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NTY-create-campaign
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the Campaign class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def create(self, data: CreateCampaign) -> CampaignResponse:
        """Create a campaign.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NTY-create-campaign
        
        Args:
            data (CreateCampaign): The campaign data to create
            
        Returns:
            CampaignResponse: Created campaign details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/campaigns",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get(self, campaign_id: str) -> CampaignResponse:
        """Get a campaign by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NTc-get-campaign-by-id
        
        Args:
            campaign_id (str): The ID of the campaign to retrieve
            
        Returns:
            CampaignResponse: Campaign details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/campaigns/{campaign_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def update(self, campaign_id: str, data: UpdateCampaign) -> CampaignResponse:
        """Update a campaign by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NTg-update-campaign-by-id
        
        Args:
            campaign_id (str): The ID of the campaign to update
            data (UpdateCampaign): The updated campaign data
            
        Returns:
            CampaignResponse: Updated campaign details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.patch(
            f"{self.auth_data.baseurl}/campaigns/{campaign_id}",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get_all(self, params: Optional[CampaignListParams] = None) -> CampaignListResponse:
        """List campaigns.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NTk-list-campaigns
        
        Args:
            params (Optional[CampaignListParams]): Query parameters for filtering and pagination
            
        Returns:
            CampaignListResponse: List of campaigns and pagination info
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('sort'):
                query_params['sort'] = params['sort']
            if params.get('order'):
                query_params['order'] = params['order']
            if params.get('type'):
                query_params['type'] = params['type']
            if params.get('status'):
                query_params['status'] = params['status']
            if params.get('trigger_type'):
                query_params['trigger_type'] = params['trigger_type']
                
        url = f"{self.auth_data.baseurl}/campaigns"
        if query_params:
            url = f"{url}?{urlencode(query_params)}"
            
        response = requests.get(url, headers=self.auth_data.headers)
        response.raise_for_status()
        return response.json()

    def delete(self, campaign_id: str) -> CampaignResponse:
        """Delete a campaign by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NjA-delete-campaign-by-id
        
        Args:
            campaign_id (str): The ID of the campaign to delete
            
        Returns:
            CampaignResponse: Response indicating success
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/campaigns/{campaign_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 