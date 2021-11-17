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
from .gql.mutations import form_create
import random
from ..locust_settings import DEFAULT_PASS, user_email_tpl


form_query = base_form_query.replace("#extra", "")
form_query_filter_code = base_form_query.replace("#extra", 'wasteCode: "06 01 01*"')


def get_count(res):
    try:
        count = res.json()["data"]["bsds"]["totalCount"]
        print(count)
    except TypeError:
        print("Error")


class TDUserMixin:
    def __init__(self, environment):
        super().__init__(environment)
        i = random.randint(1, 100)
        self.siret = f"{i:014d}"
        self.email = user_email_tpl.format(i)
        token = f"token_{i}"
        self.headers = {"Authorization": f"bearer {token}"}
        print(self.email, self.siret)


class UIUser(TDUserMixin, FastHttpUser):
    # wait_time = constant(1)
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
        self.client.post("", json={"query": form_query}, name="ui-forms-default")


class ApiUser(TDUserMixin, FastHttpUser):
    # wait_time = constant(1)

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
