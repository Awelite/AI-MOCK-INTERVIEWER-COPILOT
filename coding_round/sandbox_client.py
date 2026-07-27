import requests


class SandboxClient:

    BASE_URL = "http://127.0.0.1:8000"

    def get_problem(
        self,
        slug
    ):

        response = requests.get(
            f"{self.BASE_URL}/coding/problem/{slug}"
        )

        return response.json()