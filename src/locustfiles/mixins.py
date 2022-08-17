import random
from .settings.locust_settings import user_email_tpl

from .gql.queries import base_forms_query
import structlog

logger = structlog.get_logger()
forms_query = base_forms_query.replace("#extra", "")

form_query_filter_draft = base_forms_query.replace("#extra", "status: DRAFT")


class TDUserMixin:
    def __init__(self, environment):
        super().__init__(environment)
        i = random.randint(1, 1000)
        self.siret = f"{i:014d}" if i <= 100 else f"{1:014d}"
        self.email = user_email_tpl.format(i)
        self.token = f"token_{i}"
        self.headers = None
        self.bsddIds = []
        self.editableBsddIds = []

    def get_user_forms(self):
        res_all = self.all_forms()
        try:
            forms = res_all.json()["data"]["forms"]
            self.bsddIds = [el["id"] for el in forms]
        except (KeyError, TypeError):
            logger.error("initial-all-forms", response=res_all.json())
        res_draft = self.draft_forms()

        try:
            forms = res_draft.json()["data"]["forms"]

            self.editableBsddIds = [el["id"] for el in forms]
        except (KeyError, TypeError):
            logger.error("initial-drafts-forms", response=res_draft.json())

    def all_forms(self, name="base-all-forms"):

        res = self.client.post(
            "",
            json={"query": forms_query, "variables": {"siret": self.siret}},
            headers=self.headers,
            name=name,
        )
        return res

    def draft_forms(self, name="base-draft-forms"):
        res = self.client.post(
            "",
            json={"query": form_query_filter_draft, "variables": {"siret": self.siret}},
            headers=self.headers,
            name=name,
        )
        return res
