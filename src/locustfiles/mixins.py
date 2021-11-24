import random
from .settings.locust_settings import user_email_tpl
from locust import constant


class TDUserMixin:
    # wait_time = constant(1)

    def __init__(self, environment):
        super().__init__(environment)
        i = random.randint(1, 1000)
        self.siret = f"{i:014d}" if i <= 100 else f"{1:014d}"
        self.email = user_email_tpl.format(i)
        token = f"token_{i}"
        self.headers = {"Authorization": f"bearer {token}"}
        print(self.email, self.siret)
