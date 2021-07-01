import json
import os
import sys
import unittest

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ta_linode_util'))

from account_events import AccountEventsHandler
from account_invoices import AccountInvoicesHandler
from account_logins import AccountLoginsHandler
from account_notifications import AccountNotificationsHandler
from account_payments import AccountPaymentsHandler
from account_service_transfers import AccountServiceTransfersHandler
from linode_event_base import BaseLinodeEventLogger

class TestAccountEvents(unittest.TestCase):
    def request_fixture_override(self, handler, fixture_handler):
        def f(url, *args, **kwargs):
            return fixture_handler('get', url, *args, **kwargs)

        handler._get = f

    def load_fixture(self, fixture_name):
        with open(os.path.join(FIXTURES_DIR, fixture_name)) as f:
            content = f.read()

        return json.loads(content)

    def fixture_func(self, fixture_content):
        return lambda method, url, *args, **kwargs: fixture_content

    def test_account_events(self):
        time_str = '2017-01-01T00:01:01'
        t = BaseLinodeEventLogger._parse_time(time_str)

        def test_account_request(method, url, *args, **kwargs):
            assert kwargs['filters'] == {
                'created': {
                    '+gt': time_str
                }
            }
            return self.load_fixture('account_events.json')

        handler = AccountEventsHandler(fixture_mode=True)
        self.request_fixture_override(handler, test_account_request)
        events = handler.fetch_data(t)

        assert len(events) == 1

        event = events[0]
        assert event['action'] == 'ticket_create'
        assert event['id'] == 123
        assert event['username'] == 'exampleUser'

    def test_account_invoices(self):
        fixture = self.load_fixture('account_invoices.json')

        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')

        handler = AccountInvoicesHandler(fixture_mode=True)
        self.request_fixture_override(handler,
                                      lambda method, url, *args, **kwargs: fixture)

        events = handler.fetch_data(t)
        assert len(events) == 2
        assert events[0]['id'] == 123
        assert events[1]['id'] == 456

        t = BaseLinodeEventLogger._parse_time('2018-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 1
        assert events[0]['id'] == 456

        t = BaseLinodeEventLogger._parse_time('2020-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 0

    def test_account_logins(self):
        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')

        handler = AccountLoginsHandler(fixture_mode=True)
        self.request_fixture_override(handler,
                                      lambda method, url, *args, **kwargs:
                                      self.load_fixture('account_logins.json'))

        events = handler.fetch_data(t)
        assert len(events) == 2
        assert events[0]['id'] == 1234
        assert events[0]['ip'] == '192.0.2.0'

        assert events[1]['id'] == 5678
        assert events[1]['ip'] == '192.0.1.0'

        t = BaseLinodeEventLogger._parse_time('2018-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 1
        assert events[0]['id'] == 5678

        t = BaseLinodeEventLogger._parse_time('2020-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 0

    def test_account_notifications(self):
        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')

        handler = AccountNotificationsHandler(fixture_mode=True)
        self.request_fixture_override(handler,
                                      self.fixture_func(
                                          self.load_fixture('account_notifications.json')))

        events = handler.fetch_data(t)
        assert len(events) == 2
        assert events[0]['entity']['id'] == 1234
        assert events[1]['entity']['id'] == 5678

        t = BaseLinodeEventLogger._parse_time('2018-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 1
        assert events[0]['entity']['id'] == 5678

        t = BaseLinodeEventLogger._parse_time('2020-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 0

    def test_account_payments(self):
        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')

        handler = AccountPaymentsHandler(fixture_mode=True)
        self.request_fixture_override(handler,
                                      self.fixture_func(
                                        self.load_fixture('account_payments.json')))

        events = handler.fetch_data(t)
        assert len(events) == 2
        assert events[0]['id'] == 123
        assert events[1]['id'] == 456

        t = BaseLinodeEventLogger._parse_time('2018-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 1
        assert events[0]['id'] == 456

        t = BaseLinodeEventLogger._parse_time('2020-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 0

    def test_account_service_transfers(self):
        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')

        handler = AccountServiceTransfersHandler(fixture_mode=True)
        self.request_fixture_override(handler,
                                      self.fixture_func(
                                        self.load_fixture('account_service_transfers.json')))

        events = handler.fetch_data(t)
        assert len(events) == 2
        assert events[0]['token'] == '123'
        assert events[1]['token'] == '456'

        t = BaseLinodeEventLogger._parse_time('2018-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 1
        assert events[0]['token'] == '456'

        t = BaseLinodeEventLogger._parse_time('2020-01-01T00:01:01')
        events = handler.fetch_data(t)
        assert len(events) == 0
