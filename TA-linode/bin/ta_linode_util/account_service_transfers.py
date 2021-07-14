"""Module for collecting Linode Account Service Transfers"""

from datetime import datetime

from .linode_event_base import BaseLinodeEventLogger


class AccountServiceTransfersHandler(BaseLinodeEventLogger):
    """Handler for collecting Linode Account Logins"""

    _time_attr = 'created'

    def fetch_data(self, after_date: datetime):
        result = self._get_paginated('/account/service-transfers')
        return self._filter_new_events(result, after_date)
