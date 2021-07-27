"""Base Module for creating Linode event collectors"""

from datetime import datetime
from typing import Optional, List, Dict, Any
import json
import os
import sys
from pathlib import Path


def add_deps_path():
    """Workaround to import local dependencies above top-level package"""

    bin_dir = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())
    sys.path.append(os.path.join(bin_dir, 'deps'))


add_deps_path()

from linode_api4 import LinodeClient
from linode_api4.objects import DATE_FORMAT

APP_ROOT = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent.absolute())

class BaseLinodeEventLogger:
    """Base class for Linode event loggers"""

    _time_attr = '_time'

    def __init__(self, helper=None, ew=None, token=None, fixture_mode=False):

        self._helper = helper
        self._ew = ew

        if not fixture_mode:
            linode_token = token or helper.get_arg('linode_api_token')

            manifest = self._get_app_manifest()
            addon_version = manifest.get('info').get('id').get('version')

            self._client = LinodeClient(linode_token,
                                        user_agent='SplunkAddonLinode/{version} '
                                                   'https://github.com/linode/splunk-addon-linode'
                                        .format(version=addon_version))

            meta = list(self._helper.get_input_stanza().values())[0]
            self._last_event_checkpoint = '{}_{}_last_event'\
                .format(meta['sourcetype'], meta['name'])

    @staticmethod
    def _parse_time(to_parse: str) -> datetime:
        return datetime.strptime(to_parse, DATE_FORMAT)

    @staticmethod
    def _format_time(to_format: datetime) -> str:
        return datetime.strftime(to_format, DATE_FORMAT)

    @staticmethod
    def validate_inputs(params: Dict[str, Any]):
        """Raises an error if any of the specified inputs are invalid"""

        interval = params.get('interval')
        if int(interval) < 300:
            raise ValueError('Interval must be at least 300 seconds to prevent API rate limiting')

        start_date = params.get('start_date')

        try:
            if start_date is not None:
                BaseLinodeEventLogger._parse_time(start_date)
        except ValueError:
            raise ValueError('Incorrect date format, should be YYYY-MM-DDTHH:MM:SS')

    @staticmethod
    def _get_app_manifest():
        """Get a dict of all app manifest info"""

        app_manifest = os.path.join(APP_ROOT, 'app.manifest')
        with open(app_manifest, 'r') as file:
            result = json.load(file)

        return result

    # Override for fixtures
    def _get(self, *args, **kwargs) -> Optional[Any]:
        return self._client.get(*args, **kwargs)

    def _get_paginated(self, endpoint: str, **kwargs):
        result = []

        resp = self._get('{}?page_size=100&page=1'.format(endpoint), **kwargs)
        result += resp['data']

        num_pages = resp.get('pages')
        if num_pages is None:
            raise Exception('expected "pages" in response')

        self._helper.log_debug('Paginated request to endpoint {} of {} pages has started'
                               .format(endpoint, num_pages))

        for page in range(2, num_pages + 1):
            resp = self._get('{}?page_size=100&page={}'.format(endpoint, page), **kwargs)
            result += resp['data']
            self._helper.log_debug('Made paginated request {} of {} to endpoint {}'
                                   .format(page, num_pages, endpoint))

        self._helper.log_debug('Completed paginated request to endpoint {}'.format(endpoint))

        return result

    def _get_old_datetime(self) -> Optional[datetime]:
        old_datetime = self._helper.get_check_point(self._last_event_checkpoint)

        if old_datetime is None:
            config_start_time = self._helper.get_arg('start_date')

            # Override the start time with the user-defined start time
            if config_start_time is not None:
                old_datetime = self._parse_time(config_start_time)
            else:
                old_datetime = datetime.now()

            self._set_datetime(old_datetime)
            return old_datetime

        return BaseLinodeEventLogger._parse_time(old_datetime)

    def _set_datetime(self, new_time: datetime):
        self._helper.save_check_point(self._last_event_checkpoint,
                                      BaseLinodeEventLogger._format_time(new_time))

    def _filter_new_events(self, events: List[Dict[Any, str]], last_time: datetime):
        return [event for event in events
                if event[self._time_attr] is not None and
                BaseLinodeEventLogger._parse_time(event[self._time_attr]) > last_time]

    def _get_newest_event_timestamp(self, events: List[Dict[Any, str]]) -> datetime:
        return max(BaseLinodeEventLogger._parse_time(event[self._time_attr]) for event in events)

    def fetch_data(self, after_date: datetime) -> Any:
        """Method to fetch a list of events for the event collector"""
        pass

    def collect_events(self):
        """Method to collect and write the events to Splunk"""

        old_datetime = self._get_old_datetime()
        events = self.fetch_data(old_datetime)

        if len(events) < 1:
            return

        new_datetime = self._get_newest_event_timestamp(events)

        self._helper.log_info('Collected Linode events from {0} to {1}'.format(
            old_datetime.strftime(DATE_FORMAT),
            new_datetime.strftime(DATE_FORMAT)
        ))

        self._set_datetime(new_datetime)

        self._helper.log_info('New checkpoint date set to {}'.format(
            new_datetime
        ))

        for event in events:
            splunk_event = self._helper.new_event(
                data=json.dumps(event),
                time=self._parse_time(event[self._time_attr]).timestamp()
            )

            self._ew.write_event(splunk_event)
