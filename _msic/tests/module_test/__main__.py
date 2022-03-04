import sys
import os

import sys
MODULE = os.path.abspath(os.path.join(__file__,'..','..'))
MODULE not in sys.path and sys.path.insert(0,MODULE)
print(MODULE)

from module_test.view import log
log.call()


