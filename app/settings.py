import os

ALERT_INTERVAL_DAYS = int(os.environ.get('ALERT_INTERVAL_DAYS', 3))

MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
MAILGUN_DOMAIN_NAME = os.environ['MAILGUN_DOMAIN_NAME']

NOTIFY_EMAIL = os.environ['NOTIFY_EMAIL']

DATE_FORMAT = '%m/%d/%Y'
EMAIL_BODY = """\
Your last entry in Daytum is from {entry_date}, which means you either haven't been exercising or you forgot to log it.  Better get on that!

Log it here: https://daytum.com/spoutdoors
"""
