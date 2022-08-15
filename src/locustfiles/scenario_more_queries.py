from locust import task, FastHttpUser, constant
from .gql.queries import (
    me_query,
    bsd_query,
    base_form_query,
    base_forms_query,
    base_dasri_query,
    base_bsda_query,
    base_bsff_query,
    base_vhu_query,
    formslifecycle_query,
    light_dasri_query,
)
from .gql.mutations import form_create, dasri_create, form_update
import random
from .settings.locust_settings import DEFAULT_PASS
from .mixins import TDUserMixin

forms_query = base_forms_query.replace("#extra", "")

form_query_filter_code = base_forms_query.replace("#extra", 'wasteCode: "06 01 01*"')
form_query_filter_draft = base_forms_query.replace("#extra", "status: DRAFT")
form_query = base_form_query  # .replace("#extra", "")

REDIRECT_LOGIN_URL = "http://ui-td.test/"


def random_custom_id():
    return "".join([str(random.randint(1, 9)) for _ in range(6)])


class UIUser(TDUserMixin, FastHttpUser):
    wait_time = constant(0.5)

    def on_start(self):
        with self.client.post(
            "login",
            json={"email": self.email, "password": DEFAULT_PASS},
            name="ui-login",
            catch_response=True,
        ) as res:
            if res.url == REDIRECT_LOGIN_URL:
                res.success()

        res_all = self.all_forms()
        forms = res_all.json()["data"]["forms"]
        self.bsddIds = [el["id"] for el in forms]

        res_draft = self.draft_forms()

        try:
            forms = res_draft.json()["data"]["forms"]

            self.editableBsddIds = [el["id"] for el in forms]
        except KeyError:
            print(res_draft.json())

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

    @task(10)
    def form_update(self):
        if not self.editableBsddIds:
            return
        custom_id = random_custom_id()

        bsd_id = random.choice(self.editableBsddIds)

        res = self.client.post(
            "",
            json={
                "query": form_update,
                "variables": {"updateFormInput": {"customId": custom_id, "id": bsd_id}},
            },
            name="ui-form-update",
        )
        try:
            if res.json()["data"]["updateForm"]["customId"] != custom_id:
                print(
                    "api-form-update",
                    res.json()["data"]["updateForm"]["customId"] == custom_id,
                    bsd_id,
                    custom_id,
                    self.email,
                )
        except KeyError:
            print("api-form-update error", res.json()["errors"])

    @task(5)
    def form(self):
        if not self.bsddIds:
            return

        self.client.post(
            "",
            json={
                "query": form_query,
                "variables": {"id": random.choice(self.bsddIds)},
            },
            name="ui-form",
        )


class ApiUser(TDUserMixin, FastHttpUser):
    wait_time = constant(0.5)

    @task
    def me(self):
        self.client.post(
            "", json={"query": me_query}, headers=self.headers, name="api-me"
        )

    def on_start(self):
        res = self.forms()
        forms = res.json()["data"]["forms"]
        self.bsddIds = [el["id"] for el in forms]

        res = self.draft_forms()

        forms = res.json()["data"]["forms"]
        self.editableBsddIds = [el["id"] for el in forms]

    @task(10)
    def forms(self):
        return self.all_forms(name="api-forms-default")

    @task(5)
    def form(self):
        if not self.bsddIds:
            return

        self.client.post(
            "",
            json={
                "query": form_query,
                "variables": {"id": random.choice(self.bsddIds)},
            },
            headers=self.headers,
            name="api-form",
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

    #
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

    #
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

    @task(20)
    def form_update(self):
        if not self.editableBsddIds:
            return
        custom_id = random_custom_id()
        bsd_id = random.choice(self.editableBsddIds)
        self.client.post(
            "",
            json={
                "query": form_update,
                "variables": {"updateFormInput": {"customId": custom_id, "id": bsd_id}},
            },
            name="api-form-update",
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
