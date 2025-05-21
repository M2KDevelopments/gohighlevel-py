from typing import Optional, Dict, Any, List, Union, Tuple, TypedDict, Literal
import requests

from .auth.authdata import Auth
from .contacts_tasks import Task
from .contacts_notes import Note
from .contacts_campaigns import Campaign
from .contacts_workflows import ContactsWorkflows
from .contacts_tags import Tag
from .contacts_appointments import Appointment

class ContactSearchFilterSort(TypedDict):
    field: str
    direction: Literal["desc", "asc"]

class SearchRange(TypedDict, total=False):
    gte: Optional[str]
    gt: Optional[str]
    lte: Optional[str]
    lt: Optional[str]

class SearchSimpleFilter(TypedDict):
    field: str
    operator: Literal["eq", "not_exists", "range", "exists", "not_contains", "contains", "not_eq"]
    value: Union[str, bool, SearchRange]

class SearchComplexFilter(TypedDict):
    group: Literal["OR", "AND"]
    filters: List[SearchSimpleFilter]

class ContactSearchFilter(TypedDict):
    location_id: str
    page_limit: int
    page: Optional[int]
    search_after: Optional[List[str]]
    filters: List[Union[SearchComplexFilter, SearchSimpleFilter]]
    sort: List[ContactSearchFilterSort]

class Contacts:
    """
    Endpoints For Contacts
    https://highlevel.stoplight.io/docs/integrations/e957726e8625d-contacts-api
    https://public-api.gohighlevel.com/#0097b747-33c2-452f-8c78-aab5ab36c071
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data
        self.appointments = Appointment(auth_data)
        self.campaigns = Campaign(auth_data)
        self.workflows = ContactsWorkflows(auth_data)
        self.tasks = Task(auth_data)
        self.notes = Note(auth_data)
        self.tags = Tag(auth_data)

    def get(self, location_id: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get contacts. [Deprecated]
        Documentation - https://highlevel.stoplight.io/docs/integrations/dbe4f3a00a106-search-contacts
        
        Args:
            location_id: The location ID
            filters: Optional filters including query, startAfter, startAfterId, limit
            
        Returns:
            Dictionary containing count and contacts list
        """
        headers = self.auth_data.headers if self.auth_data else None
        filters = filters or {}
        
        query_params = []
        if filters.get('query'): query_params.append(f"query={filters['query']}")
        if filters.get('startAfter'): query_params.append(f"startAfter={filters['startAfter']}")
        if filters.get('startAfterId'): query_params.append(f"startAfterId={filters['startAfterId']}")
        if filters.get('limit'): query_params.append(f"limit={filters['limit']}")
        
        query_string = f"locationId={location_id}"
        if query_params:
            query_string += "&" + "&".join(query_params)
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts?{query_string}" if self.auth_data else "",
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        return {
            'count': data['count'],
            'contacts': data['contacts']
        }

    def search(self, query: str = '', order: str = 'desc', 
               sort_by: str = 'date_added', limit: int = 20) -> Dict[str, Any]:
        """
        Get Contacts and Search contacts. For both App and API version
        Documentation - https://highlevel.stoplight.io/docs/integrations/dbe4f3a00a106-search-contacts
        Documentation - https://public-api.gohighlevel.com/#dac71866-cddd-48e9-ba77-99fd293594fa
        
        Args:
            query: Search query string
            order: Sort order ('asc' or 'desc')
            sort_by: Field to sort by ('date_added' or 'date_updated')
            limit: Number of results to return
            
        Returns:
            Dictionary containing total and contacts list
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
        
        headers = self.auth_data.headers 
        if self.auth_data.use_api_key:
            response = requests.get(
                f"{self.auth_data.baseurl}/contacts/?limit={limit}&query={query}&sortBy={sort_by}&order={order}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {
                'total': data['meta']['total'],
                'contacts': data['contacts']
            }
        else:
            response = requests.post(
                f"{self.auth_data.baseurl}/contacts/search/",
                json={},
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {
                'total': data['total'],
                'contacts': data['contacts']
            }

    def search_with_filters(self, query: ContactSearchFilter) -> Dict[str, Any]:
        """
        Get Searched contacts using filters.
        Documentation - https://highlevel.stoplight.io/docs/integrations/dbe4f3a00a106-search-contacts
        Documentation on Filters - https://doc.clickup.com/8631005/d/h/87cpx-158396/6e629989abe7fad
        
        Args:
            query: A ContactSearchFilter object containing search parameters including:
                  - location_id: The location ID to search in
                  - page_limit: Maximum number of results per page
                  - page: Optional page number
                  - search_after: Optional list of values to search after
                  - filters: List of search filters (simple or complex)
                  - sort: List of sort criteria
                  
        Returns:
            Dictionary containing total and contacts list
        
        Example:
            filter_query = {
                'location_id': 'abc123',
                'page_limit': 10,
                'filters': [{
                    'field': 'email',
                    'operator': 'contains',
                    'value': '@example.com'
                }],
                'sort': [{
                    'field': 'dateAdded',
                    'direction': 'desc'
                }]
            }
            results = contacts.search_with_filters(filter_query)
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/contacts/search/",
            json=query,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        data = response.json()
        return {
            'total': data['total'],
            'contacts': data['contacts']
        }

    def lookup(self, email: str = "", phone: str = "") -> List[Dict[str, Any]]:
        """
        Search contact by email or phone number. Only For API version
        Documentation - https://public-api.gohighlevel.com/#5f4bde90-5179-43b2-b38d-f09b7bb771ad
        
        Args:
            email: Email to search for
            phone: Phone number to search for
            
        Returns:
            List of matching contacts
        """
        if not self.auth_data or not self.auth_data.use_api_key:
            raise ValueError("You need to use an API key to call this function. "
                           "Look at the documentation here https://public-api.gohighlevel.com/#5f4bde90-5179-43b2-b38d-f09b7bb771ad")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts/lookup?email={email}&phone={phone}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['contacts']

    def get_by_business_id(self, business_id: str) -> Dict[str, Any]:
        """
        Get Contacts By BusinessId
        Documentation: https://highlevel.stoplight.io/docs/integrations/8efc6d5a99417-get-contacts-by-business-id
        
        Args:
            business_id: The business ID to get contacts for
            
        Returns:
            Dictionary containing total, count and contacts list
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts/business/{business_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        data = response.json()
        total = data['count']
        return {
            'total': total,
            'count': total,
            'contacts': data['contacts']
        }

    def get_one(self, contact_id: str) -> Dict[str, Any]:
        """
        Get Contacts By Id. For other GHL App and API version
        Documentation: https://highlevel.stoplight.io/docs/integrations/00c5ff21f0030-get-contact
        
        Args:
            contact_id: The contact ID to retrieve
            
        Returns:
            Contact information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts/{contact_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['contact']

    def create(self, contact: Dict[str, Any], location_id: str = "") -> Dict[str, Any]:
        """
        Creates a new contact with the provided information. For other GHL App and API version
        Documentation: https://public-api.gohighlevel.com/#5fbc2b83-603d-4974-81c3-7d8658a79594
        
        Args:
            contact: The contact information including email, name, phone, company, and source
            location_id: Optional location ID
            
        Returns:
            The newly created contact
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        location = location_id or self.auth_data.location_id
        body = contact if self.auth_data.use_api_key else {**contact, 'locationId': location}
        
        response = requests.post(
            f"{self.auth_data.baseurl}/contacts/",
            json=body,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['contact']

    def update(self, id: str, contact: Dict[str, Any], location_id: str = "") -> Dict[str, Any]:
        """
        Update contact. For other GHL App and API version
        Documentation: https://highlevel.stoplight.io/docs/integrations/9ce5a739d4fb9-update-contact
        Documentation: https://public-api.gohighlevel.com/#1c7060e2-ebaf-4b5b-9248-be0292689bba
        
        Args:
            id: Contact ID to update
            contact: Updated contact information
            location_id: Optional location ID
            
        Returns:
            The updated contact
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        location = location_id or self.auth_data.location_id
        body = contact if self.auth_data.use_api_key else {**contact, 'locationId': location}
        
        response = requests.put(
            f"{self.auth_data.baseurl}/contacts/{id}",
            json=body,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['contact']

    def remove(self, id: str) -> bool:
        """
        Remove contact. For other GHL App and API version
        Documentation: https://highlevel.stoplight.io/docs/integrations/28ab84e9522b6-delete-contact
        Documentation: https://public-api.gohighlevel.com/#546cdf6c-3367-4569-b3c4-46d9c13a71ba
        
        Args:
            id: Contact ID to remove
            
        Returns:
            True if successful
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/contacts/{id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True) 