"""Modular Input for Linode Account Invoices"""

from ta_linode_declare import add_local_paths
add_local_paths()

import sys

from linode_base import ModInputLinodeBase

from linode_events.account_invoices import AccountInvoicesHandler

class ModInputLinodeAccountInvoices(ModInputLinodeBase):
    """Collect Linode Account Invoices"""

    def __init__(self):
        super(ModInputLinodeAccountInvoices, self)\
            .__init__("linode_account_invoices", "Linode Account Invoices")

    def collect_events(self, event_writer):
        """write out the events"""
        handler = AccountInvoicesHandler(self, event_writer)
        handler.collect_events()

if __name__ == "__main__":
    exitcode = ModInputLinodeAccountInvoices().run(sys.argv)
    sys.exit(exitcode)
