import json
import os
from datetime import datetime
import sys

sys.path.append(os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', 'TA-linode', 'bin', 'deps'))
sys.path.append(os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', 'TA-linode', 'bin', 'ta_linode_util'))

from linode_event_base import BaseLinodeEventLogger


class AccountPaymentsHandler(BaseLinodeEventLogger):
    _time_attr = 'date'

    def fetch_data(self, after_date: datetime):
        response = self._client.get('/account/payments')

        if response is None or 'data' not in response:
            raise Exception('invalid response from linode api')

        result = self._filter_new_events(response['data'], after_date)

        return result
