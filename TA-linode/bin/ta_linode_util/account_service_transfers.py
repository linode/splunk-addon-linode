import json
import os
from datetime import datetime
import sys
from pathlib import Path

BIN_DIR = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())
sys.path.append(os.path.join(BIN_DIR, 'deps'))
sys.path.append(os.path.join(BIN_DIR, 'ta_linode_util'))

from linode_event_base import BaseLinodeEventLogger


class AccountServiceTransfersHandler(BaseLinodeEventLogger):
    _time_attr = 'created'

    def fetch_data(self, after_date: datetime):
        response = self._get('/account/service-transfers')

        if response is None or 'data' not in response:
            raise Exception('invalid response from linode api')

        result = self._filter_new_events(response['data'], after_date)

        return result
