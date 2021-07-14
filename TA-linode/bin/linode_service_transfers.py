"""Modular Input for Linode Account Service Transfers"""

from ta_linode_declare import add_local_paths
add_local_paths()

import sys

from linode_base import ModInputLinodeBase

from linode_events.account_service_transfers import AccountServiceTransfersHandler

class ModInputLinodeAccountServiceTransfers(ModInputLinodeBase):
    """Collect Linode Account Service Transfers"""

    def __init__(self):
        super(ModInputLinodeAccountServiceTransfers, self)\
            .__init__("linode_account_service_transfers", "Linode Account Service Transfers")

    def collect_events(self, event_writer):
        """write out the events"""
        handler = AccountServiceTransfersHandler(self, event_writer)
        handler.collect_events()

if __name__ == "__main__":
    exitcode = ModInputLinodeAccountServiceTransfers().run(sys.argv)
    sys.exit(exitcode)
