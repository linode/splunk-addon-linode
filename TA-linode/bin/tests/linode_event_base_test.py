"""Handler for linode_event_base module"""

import unittest

from ..ta_linode_util import BaseLinodeEventLogger


class TestLinodeEventBase(unittest.TestCase):
    """Test for linode_event_base module"""

    @staticmethod
    def test_get_app_manifest():
        """Test that the app manifest is parsed correctly"""

        logger = BaseLinodeEventLogger(fixture_mode=True)
        manifest = logger._get_app_manifest()

        assert manifest is not None
        assert manifest.get('info').get('id').get('version') is not None
