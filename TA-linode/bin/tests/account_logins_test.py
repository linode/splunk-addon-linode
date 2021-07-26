"""Handler for Linode Account Logins"""

import unittest

from .fixtures_util import request_fixture_override, MockHelper

from ..ta_linode_util import AccountLoginsHandler, BaseLinodeEventLogger


class TestAccountLogins(unittest.TestCase):
    """Test Account login event collectors"""

    @staticmethod
    def test_account_logins():
        """Test that logins are collected correctly"""

        handler = AccountLoginsHandler(helper=MockHelper(), fixture_mode=True)
        request_fixture_override(handler)

        collect_time = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')
        events = handler.fetch_data(collect_time)
        assert len(events) == 2
        assert events[0]['id'] == 1234
        assert events[0]['ip'] == '192.0.2.0'

        assert events[1]['id'] == 5678
        assert events[1]['ip'] == '192.0.1.0'

        collect_time = BaseLinodeEventLogger._parse_time('2018-01-01T00:01:01')
        events = handler.fetch_data(collect_time)
        assert len(events) == 1
        assert events[0]['id'] == 5678

        collect_time = BaseLinodeEventLogger._parse_time('2020-01-01T00:01:01')
        events = handler.fetch_data(collect_time)
        assert len(events) == 0
