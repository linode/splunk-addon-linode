"""Rest endpoint for settings"""
from ta_linode_declare import add_local_paths
add_local_paths()

from splunktaucclib.rest_handler.endpoint import (
    field,
    RestModel,
    MultipleModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

util.remove_http_proxy_env_vars()

fields_logging = [
    field.RestField(
        'loglevel',
        required=False,
        encrypted=False,
        default='INFO',
        validator=None
    )
]
model_logging = RestModel(fields_logging, name='logging')

endpoint = MultipleModel(
    'ta_linode_settings',
    models=[
        model_logging
    ],
)

if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )
