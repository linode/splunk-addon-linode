"""Rest endpoint for Account Events"""

from ta_linode_declare import add_local_paths
add_local_paths()

from splunktaucclib.rest_handler.endpoint import (
    RestModel,
    DataInputModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

from linode_base import EVENT_REST_FIELDS

util.remove_http_proxy_env_vars()

fields = EVENT_REST_FIELDS
model = RestModel(fields, name=None)

endpoint = DataInputModel(
    'linode_account_events',
    model,
)

if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )
