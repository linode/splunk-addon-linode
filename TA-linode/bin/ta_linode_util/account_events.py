import json
import os
from datetime import datetime
import sys
from pathlib import Path

BIN_DIR = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())
sys.path.append(os.path.join(BIN_DIR, 'deps'))
sys.path.append(os.path.join(BIN_DIR, 'ta_linode_util'))

from linode_event_base import BaseLinodeEventLogger


class AccountEventsHandler(BaseLinodeEventLogger):
    _time_attr = 'created'

    def fetch_data(self, after_date: datetime):
        return self._get_paginated('/account/events', filters={
            'created': {
                '+gt': self._format_time(after_date)
            }
        })