import http.client
import json

from typing import Union

class Cloudflare:
    """
    A class for interacting with the Cloudflare API to manage DNS records.

    Attributes:
        _connection (http.client.HTTPSConnection): HTTPS connection to the Cloudflare API.
        _zone_id (str): The ID of the Cloudflare zone.
        _headers (dict): Authentication headers for the API requests.
    """

    _connection = http.client.HTTPSConnection("api.cloudflare.com")
    _zone_id: str
    _headers: dict

    def __init__(self, zone_id: str, email: str, api_key: str):
        """
        Initializes the Cloudflare object.

        Args:
            zone_id (str): The ID of the Cloudflare zone to manage.
            email (str): The email associated with the Cloudflare account.
            api_key (str): The API key for authenticating with the Cloudflare API.
        """
        self._zone_id = zone_id
        self._headers = {
            'Content-Type': "application/json",
            'X-Auth-Email': email,
            'X-Auth-Key': api_key
        }

    def get_record(self, name) -> Union[object, None]:
        """
        Retrieves a DNS record by name from the Cloudflare zone.

        Args:
            name (str): The name of the DNS record to retrieve.

        Returns:
            Union[object, None]: The DNS record if found, otherwise None.
        """
        self._connection.request(
            method="GET",
            url="/client/v4/zones/{0}/dns_records?type=A&name={1}".format(self._zone_id, name),
            headers=self._headers
        )
        result = self._connection.getresponse()
        data = json.loads(result.read().decode("utf-8"))

        try:
            return data['result'][0]
        except IndexError:
            return None

    def update_record(self, record_id: str, public_ip: str) -> list[str]:
        """
        Updates a DNS record with a new IP address.

        Args:
            record_id (str): The ID of the DNS record to update.
            public_ip (str): The new IP address to set for the DNS record.

        Returns:
            list[str]: A list of error messages, if any occurred during the update.
        """
        body = "{\n \"content\": \"" + public_ip + "\" \n}"
        self._connection.request(
            method="PATCH",
            url="/client/v4/zones/{0}/dns_records/{1}".format(self._zone_id, record_id),
            body=body,
            headers=self._headers
        )

        result = self._connection.getresponse()
        data = json.loads(result.read().decode("utf-8"))

        return data['errors']