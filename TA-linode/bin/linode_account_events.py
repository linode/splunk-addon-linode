"""Modular Input for Linode Account Events"""

from ta_linode_declare import add_local_paths
add_local_paths()

import sys

from linode_base import ModInputLinodeBase

from linode_events.account_events import AccountEventsHandler


class ModInputLinodeAccountEvents(ModInputLinodeBase):
    """Collect Linode Account Events"""

    def __init__(self):
        super(ModInputLinodeAccountEvents, self)\
            .__init__("linode_account_events", "Linode Account Events")

    def collect_events(self, event_writer):
        """write out the events"""
        handler = AccountEventsHandler(self, event_writer)
        handler.collect_events()

if __name__ == "__main__":
    exitcode = ModInputLinodeAccountEvents().run(sys.argv)
    sys.exit(exitcode)
