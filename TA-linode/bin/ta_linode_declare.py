# encode = utf-8

"""
This module is used to filter and reload PATH.
"""

import os
import sys
import re

if sys.version_info[0] < 3:
    PY_VERSION = "aob_py2"
else:
    PY_VERSION = "aob_py3"

TA_NAME = 'TA-linode'
TA_LIB_NAME = 'ta_linode'
pattern = re.compile(r"[\\/]etc[\\/]apps[\\/][^\\/]+[\\/]bin[\\/]?$")


def add_local_paths():
    """Adds local dependency paths to the system path"""
    new_paths = [path for path in sys.path if not pattern.search(path) or TA_NAME in path]
    new_paths.insert(0, os.path.sep.join([os.path.dirname(__file__), TA_LIB_NAME]))
    new_paths.insert(0, os.path.sep.join([os.path.dirname(__file__), TA_LIB_NAME, PY_VERSION]))
    new_paths.insert(0, os.path.sep.join([os.path.dirname(__file__), 'deps']))
    sys.path = new_paths
