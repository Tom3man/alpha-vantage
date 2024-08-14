import json
import logging
import random
import time
from abc import ABC
from typing import Dict, Optional, Tuple

import requests
from orb.common.vpn.pia import PiaVpn, VPNConnectionError

from alpha_vantage import REPO_PATH

log = logging.getLogger(__name__)


class APIKeyManager(ABC):
    """
    Singleton class for managing API keys and handling API requests with rate limiting.

    The APIKeyManager ensures that only one instance of the class exists and provides methods
    to manage API keys, rotate expired keys, make API requests, and handle VPN-based IP address changes.

    Attributes:
        _instance (APIKeyManager): The singleton instance of the class.
        API_LIMIT (int): Maximum allowed requests per API key.
        STATE_FILE (str): The path to the JSON file where the state of active and expired API keys is saved.
        active_keys (Dict[str, int]): Dictionary of active API keys with their remaining usage counts.
        expired_keys (Dict[str, int]): Dictionary of expired API keys.
        api_key (str): The currently active API key.
        pia (PiaVpn): Instance of the PiaVpn class to manage VPN connections.
    """

    _instance = None  # Class-level attribute to hold the singleton instance
    API_LIMIT: int = 25
    STATE_FILE: str = f"{REPO_PATH}/api_keys.json"

    def __new__(cls, *args, **kwargs):
        """
        Implement the Singleton pattern by overriding the __new__ method.
        This method ensures only one instance of the class is created.

        Returns:
            APIKeyManager: The singleton instance of the class.
        """
        if cls._instance is None:
            log.debug("Creating the Singleton instance for APIKeyManager.")
            cls._instance = super(APIKeyManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialise the APIKeyManager with an optional API key. If no key is provided, one will be set automatically.

        Args:
            api_key (Optional[str]): An optional API key to start with.
                                      If not provided, a key will be set automatically.
        """
        if self._initialized:
            return

        self.active_keys, self.expired_keys = self.load_api_keys(api_limit=self.API_LIMIT)
        self.ensure_active_keys()

        if api_key and api_key in self.active_keys:
            self.api_key = api_key
            log.info(f"Starting with provided API key: {self.api_key}")
        else:
            self.set_key()

        self.pia = PiaVpn()
        self._initialized = True

    def load_api_keys(self, api_limit: int) -> Tuple[Dict[str, int], Dict[str, int]]:
        """
        Load API keys from a JSON configuration file and return dictionaries of active and
        expired keys with usage counts.

        Args:
            api_limit (int): The initial usage count for each API key.

        Returns:
            Tuple[Dict[str, int], Dict[str, int]]: Dictionaries of active and expired API keys with their usage counts.
        """
        log.debug("Loading API keys from configuration file.")
        with open(self.STATE_FILE, 'r') as file:
            config = json.load(file)
        active_keys = {api_key: api_limit for api_key in config.get('active_keys', [])}
        expired_keys = {api_key: api_limit for api_key in config.get('expired_keys', [])}

        log.info(f"Loaded {len(active_keys)} active API keys and {len(expired_keys)} expired API keys.")
        return active_keys, expired_keys

    def ensure_active_keys(self):
        """
        Ensure that there are active API keys available. If not, swap expired keys with active keys in both
        memory and the JSON file.
        """
        if len(self.active_keys) == 0:
            log.warning("No active API keys available. Swapping expired keys with active keys.")
            self.active_keys, self.expired_keys = self.expired_keys, self.active_keys
            self.save_api_keys()
            log.info(
                f"Swapped keys. Now {len(self.active_keys)} active keys and {len(self.expired_keys)} expired keys.")

    def save_api_keys(self):
        """
        Save the current state of active and expired API keys to a JSON file.
        """
        with open(self.STATE_FILE, 'w') as file:
            json.dump(
                {'active_keys': list(self.active_keys.keys()), 'expired_keys': list(self.expired_keys.keys())}, file)
        log.info("Saved current state of API keys.")

    def set_key(self):
        """
        Set the API key to the one with the maximum available requests. If no keys are available, raises an exception.
        """
        self.ensure_active_keys()
        if not self.active_keys:
            log.error("No available requests for any API key.")
            raise RuntimeError("No requests available for any API key")

        max_value = max(self.active_keys.values())
        max_keys = [key for key, value in self.active_keys.items() if value == max_value]

        self.api_key = random.choice(max_keys)
        log.info(f"API key set to: {self.api_key} with {max_value} requests remaining.")

    def remove_key(self):
        """
        Remove the current API key from the active keys, move it to expired keys, and log the action.
        """
        log.info(f"Removing API key: {self.api_key} due to exhaustion of requests.")
        self.expired_keys[self.api_key] = self.API_LIMIT  # Move the key to expired_keys
        del self.active_keys[self.api_key]
        self.save_api_keys()

    def update_key_usage(self):
        """
        Update the usage count for the current API key and handle key rotation if needed.
        """
        current_count = self.active_keys[self.api_key]
        new_count = current_count - 1

        if new_count == 0:
            self.remove_key()
            if self.active_keys:
                self.set_key()
            else:
                log.error("All API keys exhausted.")
                raise RuntimeError("All API keys exhausted")
        else:
            self.active_keys[self.api_key] = new_count
            log.info(f"Requests remaining for API key {self.api_key}: {new_count}")
            self.save_api_keys()

    def change_ip_address(self) -> None:
        """
        Change IP address using PIA VPN. Logs the VPN connection status and handles errors.

        Raises:
            VPNConnectionError: If the VPN connection or IP address change fails.
        """
        try:
            log.info("Attempting to change IP address using PIA VPN.")
            if self.pia.vpn_status() != 'Connected':
                self.pia.connect()
                log.info("Connected to PIA VPN.")
            else:
                self.pia.set_region(region='random')
                log.info("VPN region changed to a random location.")
        except Exception as e:
            log.error(f"Failed to change IP address using PIA VPN: {e}")
            raise VPNConnectionError(f"Failed to change IP address using PIA VPN: {e}")

    def make_request(self, url: str) -> Dict:
        """
        Make an API request using the current API key. Decrease the count of available requests for the API key.
        Automatically resets or removes the key if no requests remain. Handles rate limits and API response errors.

        Args:
            url (str): The URL to which the API request is made.

        Returns:
            dict: Parsed JSON data from the API response.

        Raises:
            RuntimeError: If no API keys are available or if the API response is an error.
        """
        self.ensure_active_keys()

        if not self.active_keys:
            log.error("Attempted to make a request with no available API keys.")
            raise RuntimeError("No API keys available")

        try:
            log.info(f"Making API request to {url} using key {self.api_key}.")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            log.info(f"Successful API call to {url} with key {self.api_key}.")
            log.info(f"Requests remaining for API key {self.api_key}: {self.active_keys[self.api_key]}")

            if 'Information' in data:
                log.warning(f"API limit or other information received: {data['Information']}")
                self.remove_key()
                self.set_key()
                self.change_ip_address()
                time.sleep(8)
                return self.make_request(url=url)

            self.update_key_usage()
            return data

        except requests.HTTPError as e:
            log.error(f"HTTP error occurred during API request: {e}")
            raise
        except ValueError as e:
            log.error(f"Invalid JSON response received from API: {e}")
            raise RuntimeError("Invalid JSON response") from e
        except Exception as e:
            log.error(f"Unexpected error occurred: {e}")
            raise
