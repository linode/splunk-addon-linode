"""Handler for Linode Account Notifications"""

import unittest

from .fixtures_util import request_fixture_override, MockHelper

from ..ta_linode_util import AccountNotificationsHandler, BaseLinodeEventLogger


class TestAccountNotifications(unittest.TestCase):
    """Test Account notification event collectors"""

    @staticmethod
    def test_account_notifications():
        """Test that invoices are collected and filtered correctly"""

        handler = AccountNotificationsHandler(helper=MockHelper(), fixture_mode=True)
        request_fixture_override(handler)

        collect_time = BaseLinodeEventLogger._parse_time('2016-01-01T00:01:01')
        events = handler.fetch_data(collect_time)
        assert len(events) == 2
        assert events[0]['entity']['id'] == 1234
        assert events[1]['entity']['id'] == 5678

        collect_time = BaseLinodeEventLogger._parse_time('2018-01-01T00:01:01')
        events = handler.fetch_data(collect_time)
        assert len(events) == 1
        assert events[0]['entity']['id'] == 5678

        collect_time = BaseLinodeEventLogger._parse_time('2020-01-01T00:01:01')
        events = handler.fetch_data(collect_time)
        assert len(events) == 0
