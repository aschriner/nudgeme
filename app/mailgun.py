import requests

from app import settings


def send_email(recipients, subject, body):
    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(settings.MAILGUN_DOMAIN_NAME),
        auth=("api", settings.MAILGUN_API_KEY),
        data={
            "from": "NudgeBot <mailgun@{}>".format(settings.MAILGUN_DOMAIN_NAME),
            "to": recipients,
            "subject": subject,
            "text": body
        })
