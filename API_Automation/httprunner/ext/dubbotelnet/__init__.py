import os
import sys

# TODO: refractor module path code
PACKAGE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(PACKAGE_DIR, '../../..'))
sys.path.insert(0, ROOT_DIR)


__version__ = "httprunner 2.5.4 dubbotelnet"