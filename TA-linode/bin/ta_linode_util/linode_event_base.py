import json
import os
from datetime import datetime
import sys
from pathlib import Path

BIN_DIR = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())
sys.path.append(os.path.join(BIN_DIR, 'deps'))
sys.path.append(os.path.join(BIN_DIR, 'ta_linode_util'))

from typing import Optional, List, Dict, Any

from linode_api4 import LinodeClient
from linode_api4.objects import DATE_FORMAT

from datetime import datetime

class BaseLinodeEventLogger:
    _time_attr = '_time'

    def __init__(self, helper=None, ew=None, token=None, fixture_mode=False):
        linode_token = token

        if helper is not None and token is None:
            linode_token = helper.get_arg('linode_api_token')

        self._helper = helper
        self._ew = ew

        if not fixture_mode:
            self._client = LinodeClient(linode_token)

    @staticmethod
    def _parse_time(t: str) -> datetime:
        return datetime.strptime(t, DATE_FORMAT)

    @staticmethod
    def _format_time(t: datetime) -> str:
        return datetime.strftime(t, DATE_FORMAT)

    # Override for fixtures
    def _get(self, *args, **kwargs) -> Optional[Any]:
        return self._client.get(*args, **kwargs)

    def _get_old_datetime(self) -> Optional[datetime]:
        old_datetime = self._helper.get_check_point('last_event')

        if old_datetime is None:
            old_datetime = datetime.now()
            self._set_datetime(old_datetime)
            return old_datetime

        return BaseLinodeEventLogger._parse_time(old_datetime)

    def _set_datetime(self, new_time: datetime):
        self._helper.save_check_point('last_event', BaseLinodeEventLogger._format_time(new_time))

    def _filter_new_events(self, events: List[Dict[Any, str]], last_time: datetime):
        return [event for event in events
                if event[self._time_attr] is not None and
                BaseLinodeEventLogger._parse_time(event[self._time_attr]) > last_time]

    def _get_newest_event_timestamp(self, events: List[Dict[Any, str]]) -> datetime:
        return max(BaseLinodeEventLogger._parse_time(event[self._time_attr]) for event in events)

    def fetch_data(self, after_date: datetime) -> Any:
        pass

    def collect_events(self):
        old_datetime = self._get_old_datetime()
        events = self.fetch_data(old_datetime)

        if len(events) < 1:
            return

        self._set_datetime(self._get_newest_event_timestamp(events))

        for event in events:
            e = self._helper.new_event(
                data=json.dumps(event),
                time=self._parse_time(event[self._time_attr]).timestamp()
            )

            self._ew.write_event(e)
