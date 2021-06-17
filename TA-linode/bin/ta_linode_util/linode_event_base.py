from typing import Optional, List, Dict, Any

from linode_api4 import LinodeClient
from linode_api4.objects import DATE_FORMAT

from datetime import datetime

class BaseLinodeEventLogger:
    def __init__(self, helper, ew):
        self._helper = helper
        self._ew = ew
        self._client = LinodeClient(helper.get_arg('linode_api_token'))

    @staticmethod
    def _parse_time(t: str) -> datetime:
        return datetime.strptime(t, DATE_FORMAT)

    @staticmethod
    def _format_time(t: datetime) -> str:
        return datetime.strftime(t, DATE_FORMAT)

    def _get_old_datetime(self) -> Optional[datetime]:
        old_datetime = self._helper.get_check_point('last_event')

        if old_datetime is None:
            old_datetime = datetime.now()
            self._set_datetime(old_datetime)
            return old_datetime

        return BaseLinodeEventLogger._parse_time(old_datetime)

    def _set_datetime(self, new_time: datetime):
        self._helper.save_check_point('last_event', BaseLinodeEventLogger._format_time(new_time))

    @staticmethod
    def _filter_new_events(events: List[Dict[Any, str]], last_time: datetime, time_attr: str = 'created'):
        return [event for event in events
                if BaseLinodeEventLogger._parse_time(event[time_attr]) > last_time]

    @staticmethod
    def _get_newest_event_timestamp(events: List[Dict[Any, str]], time_attr: str = 'created') -> datetime:
        return max(BaseLinodeEventLogger._parse_time(event[time_attr]) for event in events)

    def fetch_data(self, after_date: datetime):
        return

    def collect_events(self):
        return
