"""Credentials for GoHighLevel API.

This module provides the Credentials class for storing API credentials
including client ID, client secret, and other authentication settings.
"""

from typing import List, Optional


class Credentials:
    """Credentials container for GoHighLevel API.
    
    Documentation: https://highlevel.stoplight.io/docs/integrations/0443d7d1a4bd0-overview
    """
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None,
                 redirect_uri: Optional[str] = None, scopes: Optional[List[str]] = None,
                 is_white_label: bool = False, api_key: Optional[str] = None):
        """Initialize Credentials.
        
        Args:
            client_id (Optional[str]): OAuth client ID
            client_secret (Optional[str]): OAuth client secret
            redirect_uri (Optional[str]): OAuth redirect URI
            scopes (Optional[List[str]]): List of OAuth scopes
            is_white_label (bool): Whether to use white label domain
            api_key (Optional[str]): API key for direct authentication
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes or []
        self.is_white_label = is_white_label
        self.api_key = api_key 