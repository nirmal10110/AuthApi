import os
from typing import List
from requests import Response, post
from libs.strings import gettext


MAILGUN_API_KEY = "03060f3e21e1886d90e4c14f85e2cbd5-8b34de1b-83169072"
MAILGUN_DOMAIN = "sandboxa2e05a9713c348b79b6aba4e215e7677.mailgun.org"
DATABASE_URL = "sqlite:///data.db"


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    """Call to Mailgun API for sending email with required fields"""
    # MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    # MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", None)

    FROM_TITLE = "Visa Mail Confirmation"
    FROM_EMAIL = f"do-not-reply@{MAILGUN_DOMAIN}"

    @classmethod
    def send_email(
            cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        if MAILGUN_API_KEY is None:
            raise MailGunException(gettext("mailgun_failed_load_api_key"))

        if MAILGUN_DOMAIN is None:
            raise MailGunException(gettext("mailgun_failed_load_domain"))

        response = post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            raise MailGunException(gettext("mailgun_error_send_email"))

        return response

