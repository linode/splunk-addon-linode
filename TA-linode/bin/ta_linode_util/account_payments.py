"""Module for collecting Linode Account Payments"""

from datetime import datetime

from .linode_event_base import BaseLinodeEventLogger


class AccountPaymentsHandler(BaseLinodeEventLogger):
    """Handler for collecting Linode Account Payments"""

    _time_attr = 'date'

    def fetch_data(self, after_date: datetime):
        result = self._get_paginated('/account/payments')
        return self._filter_new_events(result, after_date)
