"""Modular Input for Linode Account Payments"""

from ta_linode_declare import add_local_paths
add_local_paths()

import sys

from linode_base import ModInputLinodeBase

from linode_events.account_payments import AccountPaymentsHandler

class ModInputLinodeAccountPayments(ModInputLinodeBase):
    """Collect Linode Account Payments"""

    def __init__(self):
        super(ModInputLinodeAccountPayments, self)\
            .__init__("linode_account_payments", "Linode Account Payments")

    def collect_events(self, event_writer):
        """write out the events"""
        handler = AccountPaymentsHandler(self, event_writer)
        handler.collect_events()

if __name__ == "__main__":
    exitcode = ModInputLinodeAccountPayments().run(sys.argv)
    sys.exit(exitcode)
