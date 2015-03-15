# -*- coding: utf-8 -*-

import sys
major_ver = sys.version_info[0]
if major_ver == 2:
    from test_run import *
    from test_config import *
    from test_generator import *
