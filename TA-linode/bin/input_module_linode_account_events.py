
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
        from ta_linode_util.account_events import AccountEventsHandler
        handler = AccountEventsHandler(helper, ew)
        handler.collect_events()
    except Exception as exc:
        helper.log_error('failed to collect linode account events: {}'.format(exc))
        raise exc
