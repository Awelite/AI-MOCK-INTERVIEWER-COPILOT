import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

LANGUAGE_MAP = {
    "python": 71,
    "cpp": 54
}


class Judge0Client:
    def __init__(self):
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    def run_code(
        self,
        code,
        language,
        stdin=""
    ):

        language_id = LANGUAGE_MAP.get(
            language
        )

        for attempt in range(3):
            try:
                from config import JUDGE0_URL
                response = self.session.post(
                    f"{JUDGE0_URL}/submissions?wait=true",
                    json={
                        "source_code": code,
                        "language_id": language_id,
                        "stdin": stdin
                    },
                    timeout=30
                )
                return response.json()
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                if attempt == 2:
                    return {"error": f"Judge0 execution failed after retries: {str(e)}"}
                time.sleep(1)
            except Exception as e:
                return {"error": f"Judge0 unexpected error: {str(e)}"}