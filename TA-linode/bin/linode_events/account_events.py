"""Module for collecting Linode Account Events"""

from datetime import datetime

from .linode_event_base import BaseLinodeEventLogger


class AccountEventsHandler(BaseLinodeEventLogger):
    """Handler for collecting Linode Account Events"""

    _time_attr = 'created'

    def fetch_data(self, after_date: datetime):
        return self._get_paginated('/account/events', filters={
            'created': {
                '+gt': self._format_time(after_date)
            }
        })
