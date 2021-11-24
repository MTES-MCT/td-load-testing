from locust import task, FastHttpUser
from .gql.queries import (
    me_query,
    bsd_query,
    base_form_query,
    base_dasri_query,
    base_bsda_query,
    base_bsff_query,
    base_vhu_query,
    formslifecycle_query,
    light_dasri_query,
)
from .gql.mutations import form_create, dasri_create

from .settings.locust_settings import DEFAULT_PASS, user_email_tpl
from .mixins import TDUserMixin

form_query = base_form_query.replace("#extra", "")
form_query_filter_code = base_form_query.replace("#extra", 'wasteCode: "06 01 01*"')


class UIUser(TDUserMixin, FastHttpUser):
    def on_start(self):
        self.client.post(
            "login",
            json={"email": self.email, "password": DEFAULT_PASS},
            name="ui-login",
        )

    @task
    def me(self):
        self.client.post("", json={"query": me_query}, name="ui-me")

    @task
    def bsds_archived(self):
        self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isArchivedFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-archived",
        )

    @task
    def bsds_draft(self):
        self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isDraftFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-draft",
        )

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

    @task
    def bsds_to_collect(self):
        self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isToCollectFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-to-collect",
        )

    @task
    def bsds_collected_for(self):
        self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isCollectedFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-collected-for",
        )

    @task
    def forms(self):
        self.client.post(
            "",
            json={"query": form_query, "variables": {"siret": self.siret}},
            name="ui-forms-default",
        )


class ApiUser(TDUserMixin, FastHttpUser):
    @task
    def me(self):
        self.client.post(
            "", json={"query": me_query}, headers=self.headers, name="api-me"
        )

    @task
    def forms(self):
        self.client.post(
            "",
            json={"query": form_query, "variables": {"siret": self.siret}},
            headers=self.headers,
            name="api-forms-default",
        )

    @task
    def forms_lifecycle(self):
        self.client.post(
            "",
            json={"query": formslifecycle_query, "variables": {"siret": self.siret}},
            headers=self.headers,
            name="api-forms-lifecycle",
        )

    @task
    def forms_by_waste_code(self):
        self.client.post(
            "",
            json={"query": form_query_filter_code, "variables": {"siret": self.siret}},
            headers=self.headers,
            name="api-forms-filter-waste_code",
        )

    @task
    def bsdasris_full(self):
        self.client.post(
            "",
            json={"query": base_dasri_query},
            headers=self.headers,
            name="api-bsdasris-full",
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
    def bsff(self):
        self.client.post(
            "",
            json={"query": base_bsff_query},
            headers=self.headers,
            name="api-bsff",
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
