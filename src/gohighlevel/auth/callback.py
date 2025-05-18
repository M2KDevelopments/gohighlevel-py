"""Callback information for OAuth flow.

This module provides the CallbackInfo class for handling OAuth callback
information including authorization code and refresh token.
"""

from typing import Optional


class CallbackInfo:
    """Container for OAuth callback information."""
    
    def __init__(self, code: Optional[str] = None, refresh_token: Optional[str] = None):
        """Initialize CallbackInfo.
        
        Args:
            code (Optional[str]): The authorization code from OAuth callback
            refresh_token (Optional[str]): The refresh token for token refresh
        """
        self.code = code
        self.refresh_token = refresh_token

    def get_code(self):
        return self.code

    def get_refresh_token(self):
        return self.refresh_token
