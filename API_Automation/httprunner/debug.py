# Debug enter

import os
import sys

PACKAGE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(PACKAGE_DIR, '..'))
sys.path.insert(0, ROOT_DIR)

from httprunner.report import gen_html_report
from httprunner.api import HttpRunner


runner = HttpRunner(
    failfast=True,
    save_tests=False,
    log_level='INFO'
)

runner.run(r".\API_Automation\testsuites\GMUI\launcher3.0_testsuite.yml")
summary = runner.summary
print("OK")