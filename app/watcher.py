from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import logging
import requests

from app import mailgun
from app import settings


logger = logging.getLogger(__file__)

alert_interval = timedelta(days=settings.ALERT_INTERVAL_DAYS)


def get_daytum_entries():
    url = 'http://daytum.com/spoutdoors/entries/'
    resp = requests.get(url)
    return resp


def get_latest_entry(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    entry = soup.select('#entry_list .edit_row')[0]
    name = entry.select('.entry_name a')[0].contents[0]
    date_str = entry.select('.edit_right span')[0].contents[0].strip().split(',')[0]
    return {
        "date": datetime.strptime(date_str, settings.DATE_FORMAT),
        "name": name
    }


def process_entry(entry):
    if datetime.now() - entry['date'] > alert_interval:
        logger.info("Sending email")
        mailgun.send_email(
            recipients=[settings.NOTIFY_EMAIL],
            subject='Get on it',
            body=get_email_body(entry),
            )

def get_email_body(entry):
    return settings.EMAIL_BODY.format(
        entry_day=entry['date'].strftime('%A'),
        entry_date=entry['date'].strftime(settings.DATE_FORMAT),
        entry_name=entry['name'])

def do_the_thing():
    resp = get_daytum_entries()
    entry = get_latest_entry(resp)
    process_entry(entry)


if __name__ == '__main__':
    do_the_thing()
