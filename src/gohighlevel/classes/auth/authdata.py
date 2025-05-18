"""Authentication data for GoHighLevel API.

This module provides the Auth class for storing authentication information
including tokens, headers, and other authentication-related data.
"""

from typing import Dict, Optional


class Auth:
    """Authentication data container for GoHighLevel API."""
    
    def __init__(self, access_token: str, refresh_token: Optional[str] = None,
                 location_id: Optional[str] = None, company_id: Optional[str] = None,
                 expires_in: Optional[int] = None, user_type: Optional[str] = None,
                 use_api_key: bool = False, baseurl: Optional[str] = None,
                 scope: Optional[str] = None, headers: Optional[Dict] = None):
        """Initialize Auth.
        
        Args:
            access_token (str): The access token for API authentication
            refresh_token (Optional[str]): The refresh token for getting new access tokens
            location_id (Optional[str]): The ID of the location
            company_id (Optional[str]): The ID of the company
            expires_in (Optional[int]): Token expiration time in seconds
            user_type (Optional[str]): Type of user
            use_api_key (bool): Whether to use API key authentication
            baseurl (Optional[str]): Base URL for API requests
            scope (Optional[str]): OAuth scope
            headers (Optional[Dict]): Custom headers for API requests
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.location_id = location_id
        self.company_id = company_id
        self.expires_in = expires_in
        self.user_type = user_type
        self.use_api_key = use_api_key
        self.baseurl = baseurl
        self.scope = scope
        self.headers = headers or {
            'Version': '2021-04-15',
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        } 