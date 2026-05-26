import requests
import urllib3
from agent_utilities.exceptions import UnauthorizedError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BaseApiClient:
    def __init__(self, base_url: str, token: str, verify: bool = True):
        self.base_url = base_url.rstrip("/")
        if (
            not self.base_url.endswith("/public/v1")
            and "/public/v1" not in self.base_url
        ):
            self.base_url = f"{self.base_url}/public/v1"

        self.token = token
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": self.token, "Content-Type": "application/json"}
        )
        self.session.verify = self.verify
        self.headers = self.session.headers

        try:
            self.get_integrations()
        except Exception as e:
            if isinstance(e, UnauthorizedError):
                raise e

    def get_integrations(self) -> list:
        return []
