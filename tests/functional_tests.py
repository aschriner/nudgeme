from datetime import datetime
import os
from unittest import TestCase, mock

from app.watcher import get_latest_entry, get_email_body, process_entry


class TestFunctionalTests(TestCase):
    def get_test_response(self):
        path = os.path.join(os.path.dirname(__file__), 'test_response.html')
        with open(path, 'r') as fin:
            response_content = fin.read()
        response = mock.MagicMock()
        response.content = response_content
        return response

    def test_get_entry(self):
        response = self.get_test_response()
        entry = get_latest_entry(response)
        expected_last_entry_date = datetime(year=2017, month=4, day=20)
        self.assertEqual(entry['date'], expected_last_entry_date)

    @mock.patch('app.mailgun.send_email')
    def test_process_entry(self, mock_send_email):
        entry = {
            "date": datetime(year=2000, month=1, day=1),
            "name": "eating donuts"
        }
        process_entry(entry)
        self.assertTrue(mock_send_email.called)

    def test_format_email_body(self):
        entry = {
            "date": datetime(year=2000, month=1, day=1),
            "name": "eating donuts"
        }
        get_email_body(entry) # make sure no formatting/key errors
