"""Modular Input for Linode Account Logins"""

from ta_linode_declare import add_local_paths
add_local_paths()

import sys

from linode_base import ModInputLinodeBase

from linode_events.account_logins import AccountLoginsHandler

class ModInputLinodeAccountLogins(ModInputLinodeBase):
    """Collect Linode Account Logins"""

    def __init__(self):
        super(ModInputLinodeAccountLogins, self)\
            .__init__("linode_account_logins", "Linode Account Logins")

    def collect_events(self, event_writer):
        """write out the events"""
        handler = AccountLoginsHandler(self, event_writer)
        handler.collect_events()

if __name__ == "__main__":
    exitcode = ModInputLinodeAccountLogins().run(sys.argv)
    sys.exit(exitcode)
