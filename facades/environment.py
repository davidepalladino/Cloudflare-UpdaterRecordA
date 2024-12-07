import os

from dotenv import load_dotenv
from utils.messages import *


class Environment:
    """
    Handles the loading and validation of environment variables required for Cloudflare API operations.

    Attributes:
        _ENTRY_ZONE_ID (str): The environment variable key for the Cloudflare Zone ID.
        _ENTRY_EMAIL (str): The environment variable key for the Cloudflare account email.
        _ENTRY_API_KEY (str): The environment variable key for the Cloudflare API key.

    Raises:
        EnvironmentError: If any required environment variable is missing.

    Methods:
        get_zone_id() -> str:
            Returns the Cloudflare Zone ID.
        get_email() -> str:
            Returns the Cloudflare account email.
        get_api_key() -> str:
            Returns the Cloudflare API key.
    """

    _ENTRY_ZONE_ID: str = 'ZONE_ID'
    _ENTRY_EMAIL: str = 'EMAIL'
    _ENTRY_API_KEY: str = 'API_KEY'

    _zone_id: str
    _email: str
    _api_key: str

    def __init__(self):
        """
        Initializes the Environment object by loading and validating the required environment variables.

        Raises:
            EnvironmentError: If any of the required environment variables (ZONE_ID, EMAIL, API_KEY) are not set.
        """
        load_dotenv()

        errors: list = []

        self._zone_id = os.getenv(self._ENTRY_ZONE_ID)
        if self._zone_id is None:
            errors.append(self._ENTRY_ZONE_ID)

        self._email = os.getenv(self._ENTRY_EMAIL)
        if self._email is None:
            errors.append(self._ENTRY_EMAIL)

        self._api_key = os.getenv(self._ENTRY_API_KEY)
        if self._api_key is None:
            errors.append(self._ENTRY_API_KEY)

        if len(errors) > 0:
            raise EnvironmentError(ERROR_MISSED_ENV.format(', '.join(errors)))

    def get_zone_id(self) -> str:
        """
        Retrieves the Cloudflare Zone ID.

        Returns:
            str: The Zone ID retrieved from the environment variables.
        """
        return self._zone_id

    def get_email(self) -> str:
        """
        Retrieves the Cloudflare account email.

        Returns:
            str: The email retrieved from the environment variables.
        """
        return self._email

    def get_api_key(self) -> str:
        """
        Retrieves the Cloudflare API key.

        Returns:
            str: The API key retrieved from the environment variables.
        """
        return self._api_key