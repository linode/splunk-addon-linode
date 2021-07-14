"""Module for collecting Linode Account Logins"""

from datetime import datetime

from .linode_event_base import BaseLinodeEventLogger


class AccountLoginsHandler(BaseLinodeEventLogger):
    """Handler for collecting Linode Account Logins"""

    _time_attr = 'datetime'

    def fetch_data(self, after_date: datetime):
        result = self._get_paginated('/account/logins')
        return self._filter_new_events(result, after_date)
