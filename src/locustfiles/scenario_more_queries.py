from locust import task, FastHttpUser, constant, tag
from .gql.queries import (
    me_query,
    bsd_query,
    base_form_query,
    base_forms_query,
    base_dasri_query,
    base_bsdas_query,
    base_bsffs_query,
    base_vhus_query,
    formslifecycle_query,
    light_dasri_query,
)
from .gql.mutations import form_create, dasri_create, form_update
import random
from .settings.locust_settings import DEFAULT_PASS, REDIRECT_LOGIN_URL, WAIT_TIME
from .mixins import TDUserMixin

import structlog

logger = structlog.get_logger()

forms_query = base_forms_query.replace("#extra", "")

form_query_filter_code = base_forms_query.replace("#extra", 'wasteCode: "06 01 01*"')
form_query_filter_draft = base_forms_query.replace("#extra", "status: DRAFT")
form_query = base_form_query  # .replace("#extra", "")


def random_custom_id():
    return "".join([str(random.randint(1, 9)) for _ in range(6)])


def log_response_many(res, name, sub_field=None):
    parsed = res.json()
    try:
        info = parsed["data"][name]
        if sub_field:
            info = info[sub_field]
        logger.msg(name, data=len(info))
    except Exception as e:
        logger.error(name, fail=str(e), response=parsed)


def log_response_unique(res, name):
    parsed = res.json()
    try:
        info = parsed["data"][name]["id"]

        logger.msg(name, data=info)
    except Exception as e:
        logger.error(name, fail=str(e), response=parsed)


class UIUser(TDUserMixin, FastHttpUser):
    wait_time = constant(WAIT_TIME)

    def on_start(self):
        with self.client.post(
            "login",
            json={"email": self.email, "password": DEFAULT_PASS},
            name="ui-login",
            catch_response=True,
        ) as res:
            if res.url == REDIRECT_LOGIN_URL:
                res.success()
            else:
                logger.error("login-error", email=self.email, url=res.url)

        self.get_user_forms()

    @task
    def me(self):
        self.client.post("", json={"query": me_query}, name="ui-me")

    @task
    def bsds_archived(self):
        res = self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isArchivedFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-archived",
            catch_response=True,
        )
        log_response_many(res, "bsds", "edges")

    @task
    def bsds_draft(self):
        res = self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isDraftFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-draft",
            catch_response=True,
        )
        log_response_many(res, "bsds", "edges")

    @task
    def bsds_action(self):
        res = self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isForActionFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-action",
            catch_response=True,
        )
        log_response_many(res, "bsds", "edges")

    @task
    def bsds_follow(self):
        res = self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isFollowFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-follow",
            catch_response=True,
        )
        log_response_many(res, "bsds", "edges")

    @task
    def bsds_to_collect(self):
        res = self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isToCollectFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-to-collect",
            catch_response=True,
        )
        log_response_many(res, "bsds", "edges")

    @task
    def bsds_collected_for(self):
        res = self.client.post(
            "",
            json={
                "query": bsd_query.replace("#tab", "isCollectedFor"),
                "variables": {"siret": self.siret},
            },
            name="ui-bsds-collected-for",
            catch_response=True,
        )
        log_response_many(res, "bsds", "edges")

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
        logger.msg("ui-form-update", id=bsd_id, custom_id=custom_id)
        try:
            if res.json()["data"]["updateForm"]["customId"] != custom_id:
                logger.error(
                    "api-form-update-fail",
                    bsd_id=bsd_id,
                    custom_id=custom_id,
                    user_email=self.email,
                )
        except (KeyError, TypeError):
            logger.error("api-form-update error", response=res.json()["errors"])

    @task(10)
    def form(self):
        if not self.bsddIds:
            return

        res = self.client.post(
            "",
            json={
                "query": form_query,
                "variables": {"id": random.choice(self.bsddIds)},
            },
            name="ui-form",
            catch_response=True,
        )
        log_response_unique(res, "form")


class ApiUser(TDUserMixin, FastHttpUser):
    wait_time = constant(WAIT_TIME)

    def __init__(self, environment):
        super().__init__(environment)
        self.headers = {"Authorization": f"bearer {self.token}"}

    @task
    def me(self):
        self.client.post(
            "", json={"query": me_query}, headers=self.headers, name="api-me"
        )

    def on_start(self):
        self.get_user_forms()

    @task(5)
    def forms(self):
        res = self.all_forms(name="api-forms-default")

        log_response_many(res, "forms")

    @task(10)
    def form(self):
        if not self.bsddIds:
            return

        res = self.client.post(
            "",
            json={
                "query": form_query,
                "variables": {"id": random.choice(self.bsddIds)},
            },
            headers=self.headers,
            name="api-form",
            catch_response=True,
        )
        log_response_unique(res, "form")

    @tag("slow-request")
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
        res = self.client.post(
            "",
            json={"query": form_query_filter_code, "variables": {"siret": self.siret}},
            headers=self.headers,
            name="api-forms-filter-waste_code",
            catch_response=True,
        )
        log_response_many(res, "forms")

    @task
    def bsdasris_full(self):
        res = self.client.post(
            "",
            json={"query": base_dasri_query},
            headers=self.headers,
            name="api-bsdasris-full",
            catch_response=True,
        )
        log_response_many(res, "bsdasris", "edges")

    @task
    def bsdasris_light(self):
        res = self.client.post(
            "",
            json={"query": light_dasri_query},
            headers=self.headers,
            name="api-bsdasris-light",
            catch_response=True,
        )
        log_response_many(res, "bsdasris", "edges")

    @task
    def bsvhus(self):
        res = self.client.post(
            "",
            json={"query": base_vhus_query},
            headers=self.headers,
            name="api-bsvhus",
            catch_response=True,
        )
        log_response_many(res, "bsvhus", "edges")

    @task
    def bsdas(self):
        res = self.client.post(
            "",
            json={"query": base_bsdas_query},
            headers=self.headers,
            name="api-bsdas",
            catch_response=True,
        )
        log_response_many(res, "bsdas", "edges")

    @task
    def bsff(self):
        res = self.client.post(
            "",
            json={"query": base_bsffs_query},
            headers=self.headers,
            name="api-bsff",
            catch_response=True,
        )
        log_response_many(res, "bsffs", "edges")

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
            catch_response=True,
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
            catch_response=True,
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
