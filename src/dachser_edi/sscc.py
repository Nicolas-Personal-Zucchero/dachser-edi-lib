import logging
from typing import Optional, Dict, List
import requests

class SSCCGenerator:
    _BASE_URL = "https://api-gateway.dachser.com"
    _MAX_SSCCS_PER_REQUEST = 100

    def __init__(self, token: str, logger: Optional[logging.Logger] = None) -> None:
        self._headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "X-API-Key": token,
        }
        self._logger = logger or logging.getLogger(__name__)

    def _handle_api_error(self, response: requests.Response) -> None:
        status = response.status_code
        if status in (400, 413, 500):
            try:
                data = response.json()
                self._logger.error("API Error: %s", data.get('message', 'Unknown error'))
                for detail in data.get("details", []):
                    self._logger.error("\t- %s", detail)
            except ValueError:
                self._logger.error("API Error %d: Unparseable JSON response", status)
        elif status == 401:
            self._logger.error("Unauthorized: Check your API token.")
        elif status == 429:
            self._logger.error("Rate limit exceeded: Too many requests.")
        else:
            self._logger.error("Unexpected HTTP error: %d", status)

    def get_ssccs(self, count: int, use_prefix: bool = True) -> Optional[List[str]]:
        if not (1 <= count <= self._MAX_SSCCS_PER_REQUEST):
            self._logger.error("Validation Error: count must be between 1 and %d", self._MAX_SSCCS_PER_REQUEST)
            return None

        payload = {
            "count": count,
            "usePrefix": use_prefix
        }

        endpoint = f"{self._BASE_URL}/rest/v2/ssccs"

        try:
            response = requests.post(
                endpoint,
                headers=self._headers,
                json=payload,
                timeout=10.0 
            )
        except requests.RequestException as e:
            self._logger.error("Network request failed: %s", e)
            return None

        if response.status_code == 200:
            data = response.json()
            return data.get("ssccs")

        self._handle_api_error(response)
        return None