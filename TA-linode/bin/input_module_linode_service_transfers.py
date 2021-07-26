
# encoding = utf-8

import os
import sys
import time
import datetime

def validate_input(helper, definition):
    from ta_linode_util.linode_event_base import BaseLinodeEventLogger
    BaseLinodeEventLogger.validate_inputs(definition.parameters)

def collect_events(helper, ew):
    try:
        from ta_linode_util.account_service_transfers import AccountServiceTransfersHandler
        handler = AccountServiceTransfersHandler(helper, ew)
        handler.collect_events()
    except Exception as exc:
        helper.log_error('failed to collect linode account service transfers: {}'.format(exc))
        raise exc
