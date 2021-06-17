import json
import os
from typing import Optional, List, Dict, Any

from linode_api4 import LinodeClient
from linode_api4.objects import DATE_FORMAT

from datetime import datetime

import sys
sys.path.append(os.path.join(os.environ['SPLUNK_HOME'], 'etc','apps','TA-linode','bin','ta_linode_util'))


from linode_event_base import BaseLinodeEventLogger


class AccountEventsHandler(BaseLinodeEventLogger):
    def fetch_data(self, after_date: datetime):
        response = self._client.get('/account/events', filters={
            'created': {
                '+gt': self._format_time(after_date)
            }
        })

        if response is None or 'data' not in response:
            raise Exception('invalid response from linode api')

        return response['data']

    def collect_events(self):
        old_datetime = self._get_old_datetime()

        events = self.fetch_data(old_datetime)

        if len(events) < 1:
            return

        self._set_datetime(self._get_newest_event_timestamp(events))
        for event in events:
            e = self._helper.new_event(
                data=json.dumps(event),
                time=self._parse_time(event['created']).timestamp()
            )

            self._ew.write_event(e)
