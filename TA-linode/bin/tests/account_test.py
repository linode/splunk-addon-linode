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
from fixtures_util import request_fixture_override, request_fixture_override_func, load_fixture


class TestAccountEvents(unittest.TestCase):
    """Test Account event collectors"""

    def test_account_events(self):
        time_str = '2017-01-01T00:01:01'
        t = BaseLinodeEventLogger._parse_time(time_str)

        def test_account_request(method, url, *args, **kwargs):
            assert kwargs['filters'] == {
                'created': {
                    '+gt': time_str
                }
            }
            return load_fixture(os.path.join(FIXTURES_DIR, 'account_events.json'))

        handler = AccountEventsHandler(fixture_mode=True)
        request_fixture_override_func(handler, test_account_request)
        events = handler.fetch_data(t)

        assert len(events) == 1

        event = events[0]
        assert event['action'] == 'ticket_create'
        assert event['id'] == 123
        assert event['username'] == 'exampleUser'

    def test_account_invoices(self):
        handler = AccountInvoicesHandler(fixture_mode=True)
        request_fixture_override(handler)

        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')
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

        handler = AccountLoginsHandler(fixture_mode=True)
        request_fixture_override(handler)

        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')
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
        handler = AccountNotificationsHandler(fixture_mode=True)
        request_fixture_override(handler)

        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')
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
        handler = AccountPaymentsHandler(fixture_mode=True)
        request_fixture_override(handler)

        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')
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
        handler = AccountServiceTransfersHandler(fixture_mode=True)
        request_fixture_override(handler)

        t = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')
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
