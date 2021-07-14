"""Modular Input for Linode Account Notifications"""

from ta_linode_declare import add_local_paths
add_local_paths()

import sys

from linode_base import ModInputLinodeBase

from linode_events.account_notifications import AccountNotificationsHandler

class ModInputLinodeAccountNotifications(ModInputLinodeBase):
    """Collect Linode Account Notifications"""

    def __init__(self):
        super(ModInputLinodeAccountNotifications, self)\
            .__init__("linode_account_notifications", "Linode Account Notifications")

    def collect_events(self, event_writer):
        """write out the events"""
        handler = AccountNotificationsHandler(self, event_writer)
        handler.collect_events()

if __name__ == "__main__":
    exitcode = ModInputLinodeAccountNotifications().run(sys.argv)
    sys.exit(exitcode)
