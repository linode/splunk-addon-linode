import os
import sys
import unittest

from fixtures_util import request_fixture_override, request_fixture_override_func, load_fixture

from account_invoices import AccountInvoicesHandler
from linode_event_base import BaseLinodeEventLogger

class TestAccountInvoices(unittest.TestCase):
    """Test Account invoices event collectors"""

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