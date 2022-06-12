from locust import task, HttpUser
import uuid
from locust import constant

url = "http://163.172.142.255/convert/html"
headers = {"X-Auth-Token": "8b89c4db-159d-4b7f-98b8-47dccb192b26"}
files = {
    "file": open(
        "/Users/pao/Documents/DEV/PY/load-testing/src/locustfiles/index.html", "rb"
    )
}


class User(HttpUser):
    @task
    def pdf(self):
        with open(
            "/Users/pao/Documents/DEV/PY/load-testing/src/locustfiles/index.html", "rb"
        ) as tpl:
            self.client.post(url, files={"file": tpl}, headers=headers)
