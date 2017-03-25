from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import logging
import requests

import mailgun
import settings


logger = logging.getLogger(__file__)

alert_interval = timedelta(days=settings.ALERT_INTERVAL_DAYS)


def get_daytum_entries():
    url = 'http://daytum.com/spoutdoors/entries/'
    resp = requests.get(url)
    return resp


def get_latest_entry(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    entry = soup.select('#entry_list .edit_right span')[0]
    date_str = entry.contents[0].strip().split(',')[0]
    return {
        "date": datetime.strptime(date_str, settings.DATE_FORMAT)
    }


def do_the_thing():
    resp = get_daytum_entries()
    entry = get_latest_entry(resp)
    if datetime.now() - entry['date'] > alert_interval:
        logger.info("Sending email")
        mailgun.send_email(
            recipients=[settings.NOTIFY_EMAIL],
            subject='Get on it',
            body=settings.EMAIL_BODY.format(
                entry_date=datetime.strftime(entry['date'], settings.DATE_FORMAT)))


if __name__ == '__main__':
    do_the_thing()
