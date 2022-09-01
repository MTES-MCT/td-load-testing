from locust import HttpUser, task

from .gql.mutations import dasri_create, form_create
from .gql.queries import (base_bsda_query, base_form_query, base_vhu_query,
                          bsd_query, light_dasri_query, me_query)
from .mixins import TDUserMixin
from .settings.locust_settings import DEFAULT_PASS

form_query = base_form_query.replace("#extra", "")


class UIUser(TDUserMixin, HttpUser):
    def on_start(self):
        self.client.post(
            "login",
            {"email": self.email, "password": DEFAULT_PASS},
            name="ui-login",
        )

    @task
    def me(self):
        self.client.post("", json={"query": me_query}, name="ui-me")

    @task
    def bsds_action(self):
        self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isForActionFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-action",
        )

    @task
    def bsds_follow(self):
        self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isFollowFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-follow",
        )


class ApiUser(TDUserMixin, HttpUser):
    @task
    def me(self):
        self.client.post(
            "", json={"query": me_query}, headers=self.headers, name="api-me"
        )

    @task
    def bsdasris_light(self):
        self.client.post(
            "",
            json={"query": light_dasri_query},
            headers=self.headers,
            name="api-bsdasris-light",
        )

    @task
    def bsvhus(self):
        self.client.post(
            "",
            json={"query": base_vhu_query},
            headers=self.headers,
            name="api-bsvhus",
        )

    @task
    def bsdas(self):
        self.client.post(
            "",
            json={"query": base_bsda_query},
            headers=self.headers,
            name="api-bsdas",
        )

    @task
    def form_create(self):
        self.client.post(
            "",
            json={
                "query": form_create,
                "variables": {
                    "createFormInput": {"emitter": {"company": {"siret": self.siret}}}
                },
            },
            name="api-form-create",
            headers=self.headers,
        )

    @task
    def dasri_create(self):
        self.client.post(
            "",
            json={
                "query": dasri_create,
                "variables": {
                    "input": {
                        "waste": {"adr": "lorem", "code": "18 01 03*"},
                        "emitter": {
                            "company": {
                                "siret": self.siret,
                                "name": "lorem",
                                "address": "rue x",
                                "phone": "123",
                                "mail": "user@test.fr",
                                "contact": "john doe",
                            },
                            "emission": {
                                "packagings": [
                                    {
                                        "type": "BOITE_CARTON",
                                        "volume": 22,
                                        "quantity": 88,
                                    }
                                ]
                            },
                        },
                    },
                },
            },
            name="api-dasri-create",
            headers=self.headers,
        )
