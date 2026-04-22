from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """
    Abstract base class for all crash data providers/scrapers.
    Defines the interface for authentication, fetching, and normalization.
    """

    @abstractmethod
    def authenticate(self, *args, **kwargs):
        """
        Authenticate with the data source (API, DB, etc).
        """
        pass

    @abstractmethod
    def fetch_records(self, *args, **kwargs):
        """
        Fetch records from the data source.
        """
        pass

    @abstractmethod
    def normalize(self, raw_data):
        """
        Normalize raw data into a standard format (e.g., Pydantic model).
        """
        pass
