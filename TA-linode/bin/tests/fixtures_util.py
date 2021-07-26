"""Helper functions for handling fixtures"""

import json
import os
import re
import logging

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')


def request_url_to_fixture(url: str):
    """Convert a URL path to a fixtures filename ('/account/events' -> 'account_events')"""
    params = url.split('?')

    return '_'.join([param for param in re.split('/|-', params[0]) if param != ''])


def request_fixture_override(handler, fixtures_dir=FIXTURES_DIR):
    """Override the request methods in a handler with file-based fixtures"""

    def override_func(url, *args, **kwargs):
        fixture_name = '{}.json'.format(request_url_to_fixture(url))
        fixture_path = os.path.join(fixtures_dir, fixture_name)

        return load_fixture(fixture_path)

    handler._get = override_func


def request_fixture_override_func(handler, func):
    """Override the request methods in a handler with a custom handler func"""

    def override_func(url, *args, **kwargs):
        return func('get', url, *args, **kwargs)

    handler._get = override_func


def load_fixture(fixture_path):
    """Load a fixture from the given file"""

    with open(fixture_path) as file:
        content = file.read()

    return json.loads(content)


class MockHelper:
    """Mocks the Splunk AOB 'helper' class"""

    @staticmethod
    def log(msg):
        """Mock log function"""

        logging.info(msg)

    @staticmethod
    def log_debug(msg):
        """Mock debug log function"""
        logging.debug(msg)

    @staticmethod
    def log_info(msg):
        """Mock info log function"""
        logging.info(msg)

    @staticmethod
    def log_warning(msg):
        """Mock warning log function"""
        logging.warning(msg)

    @staticmethod
    def log_error(msg):
        """Mock error log function"""
        logging.error(msg)

    @staticmethod
    def log_critical(msg):
        """Mock critical log function"""
        logging.critical(msg)
