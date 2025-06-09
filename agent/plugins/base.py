from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List

class PortalPlugin(ABC):
    @abstractmethod
    def search_jobs(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        """Search for jobs and return a list of job dicts."""
        pass

    @abstractmethod
    def get_job_details(self, job: Dict[str, Any]) -> str:
        """Return job description text for a job dict."""
        pass

    @abstractmethod
    def apply_to_job(self, job: Dict[str, Any], resume: str, tailored_resume: str) -> (bool, str):
        """Attempt to apply to a job. Returns (success, reason)."""
        pass
