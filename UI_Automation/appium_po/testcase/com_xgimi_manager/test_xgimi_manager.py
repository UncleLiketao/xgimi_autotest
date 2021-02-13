import sys
import os
import allure
import pytest
import time
import random
from utils.appium_server import AppiumServer
from appium import webdriver
from utils.adb_tool import AndroidDebugBridge
from appium_po.pages.com_xgimi_manager.home_page import XgimiManager

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


@allure.severity(allure.severity_level.BLOCKER)
class TestXgimiManagerHome(object):
    def setup(self):
        devices = AndroidDebugBridge().attached_devices()
        l_devices = []
        app = {"port": str(random.randint(4700, 4900)), "bport": str(random.randint(4700, 4900)),
               "systemPort": str(random.randint(4700, 4900)), "devices": devices[0]}
        l_devices.append(app)
        AppiumServer(l_devices).start_server()
        version_number = AndroidDebugBridge().get_version_number(devices[0])
        caps = {
            'platformName': 'Android',
            'deviceName': '%s' % devices[0],
            'platformVersion': '%s' % version_number,
            'appPackage': 'com.xgimi.manager',
            'appActivity': '.activitys.FirstActivity',
            "noReset": True
        }
        self.driver = webdriver.Remote('http://localhost:%s/wd/hub' % app['port'], caps)
        self.driver.implicitly_wait(15)
        self.home = XgimiManager

    @allure.feature('投影管家功能')
    @allure.story('投影管家-启动进入首页')
    def test_goto_home(self):
        cur_activity = self.driver.current_activity
        print(cur_activity)
        assert cur_activity == ".activitys.FirstActivity"

    def teardown(self):
        time.sleep(10)
        self.driver.quit()


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', '../../report/xml'])
