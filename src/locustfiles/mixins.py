import random
import time
from json import JSONDecodeError

import structlog

from .gql.queries import base_forms_query
from .settings.locust_settings import user_email_tpl

logger = structlog.get_logger()
forms_query = base_forms_query.replace("#extra", "")
form_query_filter_draft = base_forms_query.replace("#extra", "status: DRAFT")


class LTException(Exception):
    pass


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

    def fill_editable_forms(self):
        res_all = self.all_forms()
        try:
            forms = res_all.json()["data"]["forms"]
            self.bsddIds = [el["id"] for el in forms]
        except (KeyError, TypeError, AttributeError, JSONDecodeError):
            logger.error("initial-all-forms")
            raise LTException

    def fill_draft_forms(self):

        res_draft = self.draft_forms()

        try:
            forms = res_draft.json()["data"]["forms"]

            self.editableBsddIds = [el["id"] for el in forms]
        except (KeyError, TypeError, AttributeError, JSONDecodeError):
            logger.error("initial-drafts-forms")
            raise LTException

    def get_user_forms(self):
        """Get each user forms to make queries on editable or draft forms"""
        for _ in range(3):
            try:
                self.fill_editable_forms()
                break
            except LTException:
                logger.msg("Waiting 3s before retrying")
                time.sleep(3)
        for _ in range(3):
            try:
                self.fill_draft_forms()
                return
            except LTException:
                logger.msg("Waiting 3s before retrying")
                time.sleep(3)

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
