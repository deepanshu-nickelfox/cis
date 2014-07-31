import sys

from settings.production import *
if 'test' in sys.argv:
    from settings.test import *
