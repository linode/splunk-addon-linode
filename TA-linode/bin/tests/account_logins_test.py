import os
import sys
import unittest

from fixtures_util import request_fixture_override, request_fixture_override_func, load_fixture

from account_logins import AccountLoginsHandler
from linode_event_base import BaseLinodeEventLogger

class TestAccountLogins(unittest.TestCase):
    """Test Account login event collectors"""

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