import random
from .settings.locust_settings import user_email_tpl

from .gql.queries import base_forms_query

forms_query = base_forms_query.replace("#extra", "")

form_query_filter_draft = base_forms_query.replace("#extra", "status: DRAFT")


class TDUserMixin:
    def __init__(self, environment):
        super().__init__(environment)
        i = random.randint(1, 1000)
        self.siret = f"{i:014d}" if i <= 100 else f"{1:014d}"
        self.email = user_email_tpl.format(i)
        token = f"token_{i}"
        self.headers = {"Authorization": f"bearer {token}"}
        self.bsddIds = []
        self.editableBsddIds = []

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
            name="api-forms-draft",
        )
        return res
