"""Module for collecting Linode Account Notifications"""

from datetime import datetime

from .linode_event_base import BaseLinodeEventLogger


class AccountNotificationsHandler(BaseLinodeEventLogger):
    """Handler for collecting Linode Account Notifications"""

    _time_attr = 'when'

    def fetch_data(self, after_date: datetime):
        result = self._get_paginated('/account/notifications')
        return self._filter_new_events(result, after_date)
