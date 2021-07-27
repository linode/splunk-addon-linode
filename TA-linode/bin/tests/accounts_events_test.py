"""Handler for Linode Account Events"""

import os
import unittest

from .fixtures_util import request_fixture_override_func, load_fixture, FIXTURES_DIR, MockHelper

from ..ta_linode_util import BaseLinodeEventLogger, AccountEventsHandler


class TestAccountEvents(unittest.TestCase):
    """Test Account events event collectors"""

    @staticmethod
    def test_account_events():
        """Test that events are collected and filtered correctly"""

        time_str = '2017-01-01T00:01:01'
        collect_time = BaseLinodeEventLogger._parse_time(time_str)

        def test_account_request(method, url, *args, **kwargs):
            assert kwargs['filters'] == {
                'created': {
                    '+gt': time_str
                }
            }
            return load_fixture(os.path.join(FIXTURES_DIR, 'account_events.json'))

        handler = AccountEventsHandler(helper=MockHelper(), fixture_mode=True)
        request_fixture_override_func(handler, test_account_request)
        events = handler.fetch_data(collect_time)

        assert len(events) == 1

        event = events[0]
        assert event['action'] == 'ticket_create'
        assert event['id'] == 123
        assert event['username'] == 'exampleUser'
