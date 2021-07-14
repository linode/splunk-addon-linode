"""Base Modular Input for Linode Account Events"""

from ta_linode_declare import add_local_paths
add_local_paths()

import os
import json

import modinput_wrapper.base_modinput
from solnlib.packages.splunklib import modularinput as smi
from splunktaucclib.rest_handler.endpoint import (
    field,
    validator
)

from linode_events.linode_event_base import BaseLinodeEventLogger

bin_dir = os.path.basename(__file__)

EVENT_REST_FIELDS = [
    field.RestField(
        'interval',
        required=True,
        encrypted=False,
        default=None,
        validator=validator.Pattern(
            regex=r"""^\-[1-9]\d*$|^\d*$""",
        )
    ),
    field.RestField(
        'index',
        required=True,
        encrypted=False,
        default='default',
        validator=validator.String(
            min_len=1,
            max_len=80,
        )
    ),
    field.RestField(
        'linode_account',
        required=True,
        encrypted=False,
        default=None,
        validator=None
    ),
    field.RestField(
        'start_date',
        required=False,
        encrypted=False,
        default=None,
        validator=validator.String(
            min_len=0,
            max_len=8192,
        )
    ),

    field.RestField(
        'disabled',
        required=False,
        validator=None
    )

]


class ModInputLinodeBase(modinput_wrapper.base_modinput.BaseModInput):
    """Base Input Module"""

    def __init__(self, name, title, single_instance=False):
        self._name = name
        self._title = title

        super(ModInputLinodeBase, self).__init__("ta_linode", name, single_instance)
        self.global_checkbox_fields = None

    def get_scheme(self):
        """overloaded splunklib modularinput method"""
        scheme = super(ModInputLinodeBase, self).get_scheme()
        scheme.title = self._title
        scheme.description = ("Go to the add-on\'s configuration UI and "
                              "configure modular inputs under the Inputs menu.")
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True

        scheme.add_argument(smi.Argument("name", title="Name",
                                         description="",
                                         required_on_create=True))
        scheme.add_argument(smi.Argument("linode_account", title="Linode Account",
                                         description="",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("start_date", title="Start Date",
                                         description="If specified, the event "
                                                     "collector will collect all events"
                                                     " that occurred after the given date.",
                                         required_on_create=False,
                                         required_on_edit=False))
        return scheme

    def get_app_name(self):
        """Gets the name of the App"""

        return "TA-linode"

    def validate_input(self, definition):
        """Validate the input definition"""
        BaseLinodeEventLogger.validate_inputs(definition.parameters)

    def collect_events(self, event_writer):
        """Write the events to Splunk"""
        pass

    def get_account_fields(self):
        """Gets the account fields"""
        account_fields = []
        account_fields.append("linode_account")
        return account_fields

    def get_checkbox_fields(self):
        """Gets the checkbox fields"""
        checkbox_fields = []
        return checkbox_fields

    def get_global_checkbox_fields(self):
        """Gets the global checkbox fields"""

        if self.global_checkbox_fields is None:
            checkbox_name_file = os.path.join(bin_dir, 'global_checkbox_param.json')
            try:
                if os.path.isfile(checkbox_name_file):
                    with open(checkbox_name_file, 'r') as file:
                        self.global_checkbox_fields = json.load(file)
                else:
                    self.global_checkbox_fields = []
            except Exception as exc:
                self.log_error('Get exception when loading global checkbox parameter names. '
                               + str(exc))
                self.global_checkbox_fields = []
        return self.global_checkbox_fields
