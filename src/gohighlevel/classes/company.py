"""Company functionality for GoHighLevel API.

This module provides the Company class for managing companies in GoHighLevel,
including creating, updating, and listing companies.
"""

from typing import Dict, List, Optional, TypedDict, Literal
from urllib.parse import urlencode
import requests

from .auth.authdata import Auth


class Company(TypedDict, total=False):
    """Type definition for a company."""
    id: str
    name: str
    website: Optional[str]
    description: Optional[str]
    industry: Optional[str]
    employees: Optional[int]
    annual_revenue: Optional[float]
    address: Optional[Dict[str, str]]
    phone: Optional[str]
    email: Optional[str]
    social_links: Optional[Dict[str, str]]
    tags: Optional[List[str]]
    custom_fields: Optional[Dict]
    metadata: Optional[Dict]
    created_at: str
    updated_at: str


class CreateCompany(TypedDict, total=False):
    """Type definition for creating a company."""
    name: str
    website: Optional[str]
    description: Optional[str]
    industry: Optional[str]
    employees: Optional[int]
    annual_revenue: Optional[float]
    address: Optional[Dict[str, str]]
    phone: Optional[str]
    email: Optional[str]
    social_links: Optional[Dict[str, str]]
    tags: Optional[List[str]]
    custom_fields: Optional[Dict]
    metadata: Optional[Dict]


class UpdateCompany(TypedDict, total=False):
    """Type definition for updating a company."""
    name: Optional[str]
    website: Optional[str]
    description: Optional[str]
    industry: Optional[str]
    employees: Optional[int]
    annual_revenue: Optional[float]
    address: Optional[Dict[str, str]]
    phone: Optional[str]
    email: Optional[str]
    social_links: Optional[Dict[str, str]]
    tags: Optional[List[str]]
    custom_fields: Optional[Dict]
    metadata: Optional[Dict]


class CompanyResponse(TypedDict):
    """Type definition for a company response."""
    company: Company
    trace_id: str


class CompanyListResponse(TypedDict):
    """Type definition for a company list response."""
    companies: List[Company]
    total: int
    trace_id: str


class CompanyListParams(TypedDict, total=False):
    """Type definition for company list parameters."""
    page: Optional[int]
    limit: Optional[int]
    sort: Optional[str]
    order: Optional[Literal['asc', 'desc']]
    search: Optional[str]
    industry: Optional[str]
    tag: Optional[str]


class CompanyAPI:
    """
    Endpoints For Companies
    https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NjE-create-company
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the Company class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def create(self, data: CreateCompany) -> CompanyResponse:
        """Create a company.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NjE-create-company
        
        Args:
            data (CreateCompany): The company data to create
            
        Returns:
            CompanyResponse: Created company details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/companies",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get(self, company_id: str) -> CompanyResponse:
        """Get a company by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NjI-get-company-by-id
        
        Args:
            company_id (str): The ID of the company to retrieve
            
        Returns:
            CompanyResponse: Company details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/companies/{company_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def update(self, company_id: str, data: UpdateCompany) -> CompanyResponse:
        """Update a company by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NjM-update-company-by-id
        
        Args:
            company_id (str): The ID of the company to update
            data (UpdateCompany): The updated company data
            
        Returns:
            CompanyResponse: Updated company details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.patch(
            f"{self.auth_data.baseurl}/companies/{company_id}",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get_all(self, params: Optional[CompanyListParams] = None) -> CompanyListResponse:
        """List companies.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NjQ-list-companies
        
        Args:
            params (Optional[CompanyListParams]): Query parameters for filtering and pagination
            
        Returns:
            CompanyListResponse: List of companies and pagination info
            
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
            if params.get('search'):
                query_params['search'] = params['search']
            if params.get('industry'):
                query_params['industry'] = params['industry']
            if params.get('tag'):
                query_params['tag'] = params['tag']
                
        url = f"{self.auth_data.baseurl}/companies"
        if query_params:
            url = f"{url}?{urlencode(query_params)}"
            
        response = requests.get(url, headers=self.auth_data.headers)
        response.raise_for_status()
        return response.json()

    def delete(self, company_id: str) -> CompanyResponse:
        """Delete a company by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b3A6MjU2MzM2NjU-delete-company-by-id
        
        Args:
            company_id (str): The ID of the company to delete
            
        Returns:
            CompanyResponse: Response indicating success
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/companies/{company_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 