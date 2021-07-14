"""Module for collecting Linode Account Invoices"""

from datetime import datetime

from .linode_event_base import BaseLinodeEventLogger


class AccountInvoicesHandler(BaseLinodeEventLogger):
    """Handler for collecting Linode Account Invoices"""

    _time_attr = 'date'

    def fetch_data(self, after_date: datetime):
        result = self._get_paginated('/account/invoices')
        return self._filter_new_events(result, after_date)
