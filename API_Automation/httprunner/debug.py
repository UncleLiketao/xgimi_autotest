# Debug enter

import os
import sys
import pprint

PACKAGE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(PACKAGE_DIR, '..'))
if sys.path[0] != ROOT_DIR:
    sys.path.insert(0, ROOT_DIR)

from httprunner.report import gen_html_report
from httprunner.ext.dubbotelnet.runner import DubboRunner

from httprunner.api import HttpRunner


runner = DubboRunner()
os.chdir(os.path.dirname(__file__))
summary = runner.run(r"D:\workspace\projects\github\xgimi_autotest\API_Automation\testcases\GMUI\rpc媒资接口\get_res_info_success.yml")


# runner = HttpRunner()
# summary = runner.run(r"D:\workspace\projects\github\xgimi_autotest\API_Automation\testcases\GMUI\Launcher3.0接口\get_res_info_success.yml")

print(sys.path)
print("OKKKKKKKKKKKKKKKKKKKK")
