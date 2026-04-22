from wi_crash_engine.core.base_provider import BaseProvider
import requests

class MilwaukeePDProvider(BaseProvider):
    """
    Provider for Milwaukee Police Department crash records.
    Implements authentication, record fetching, and normalization.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://milwaukee.gov/api/v1/crash-records/"
        self.session = requests.Session()

    def authenticate(self, api_key=None):
        if api_key:
            self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key required for authentication.")
        # Example: Set API key in session headers
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def fetch_records(self, params=None):
        url = self.base_url + "search"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def normalize(self, raw_data):
        # Implement normalization logic to standard schema (e.g., Pydantic model)
        return raw_data
