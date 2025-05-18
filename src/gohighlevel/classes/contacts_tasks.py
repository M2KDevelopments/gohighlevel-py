from typing import Optional, Dict, Any, List
import requests

from .auth.authdata import Auth

class Task:
    """
    Endpoints For Contacts for Tasks
    https://highlevel.stoplight.io/docs/integrations/db572d519b209-get-all-tasks
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def get_all(self, contact_id: str) -> List[Dict[str, Any]]:
        """
        Get all Tasks
        Documentation - https://highlevel.stoplight.io/docs/integrations/db572d519b209-get-all-tasks
        
        Args:
            contact_id: The contact ID to get tasks for
            
        Returns:
            List of tasks
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/tasks",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['tasks']

    def get(self, contact_id: str, task_id: str) -> Dict[str, Any]:
        """
        Get Task
        Documentation - https://highlevel.stoplight.io/docs/integrations/c4d36fb259656-get-task
        
        Args:
            contact_id: The contact ID
            task_id: The task ID to retrieve
            
        Returns:
            Task information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/tasks/{task_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['task']

    def add(self, contact_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Task
        Documentation - https://highlevel.stoplight.io/docs/integrations/fa57d1470b87c-create-task
        
        Args:
            contact_id: The contact ID
            task: Task information to create
            
        Returns:
            Created task information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/tasks",
            json=task,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['task']

    def update(self, contact_id: str, task_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Task
        Documentation - https://highlevel.stoplight.io/docs/integrations/82e1223e90ec9-update-task
        
        Args:
            contact_id: The contact ID
            task_id: The task ID to update
            task: Updated task information
            
        Returns:
            Updated task information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.put(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/tasks/{task_id}",
            json=task,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['task']

    def remove(self, contact_id: str, task_id: str) -> bool:
        """
        Delete Task
        Documentation - https://highlevel.stoplight.io/docs/integrations/506ee1741ec7e-delete-task
        
        Args:
            contact_id: The contact ID
            task_id: The task ID to delete
            
        Returns:
            True if successful
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/tasks/{task_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True)

    def completed(self, contact_id: str, task_id: str) -> Dict[str, Any]:
        """
        Complete Task
        Documentation - https://highlevel.stoplight.io/docs/integrations/b03d53971d208-update-task-completed
        
        Args:
            contact_id: The contact ID
            task_id: The task ID to mark as completed
            
        Returns:
            Updated task information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.put(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/tasks/{task_id}/completed",
            json={},
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 