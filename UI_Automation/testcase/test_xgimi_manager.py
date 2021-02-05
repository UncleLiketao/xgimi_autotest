import sys
import os
import pytest
import allure
import time
import random
from utils.appium_server import AppiumServer
from appium import webdriver
from pages.xgimi_manager_page import XgimiManagerPage
from pages.base_page import BasePage
from utils.adb_tool import AndroidDebugBridge

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


@allure.feature('测试投影管家')
class TestXgimiManager:
    def setup_method(self):
        devices = AndroidDebugBridge().attached_devices()
        l_devices = []
        app = { "port": str(random.randint(4700, 4900)), "bport": str(random.randint(4700, 4900)),
                "systemPort": str(random.randint(4700, 4900)), "devices": devices[0] }
        l_devices.append(app)
        AppiumServer(l_devices).start_server()
        version_number = AndroidDebugBridge().get_version_number(devices[0])
        desired_caps = {
            'platformName': 'Android',
            'deviceName': '%s' % devices[0],
            'platformVersion': '%s' % version_number,
            'appPackage': 'com.xgimi.manager',
            'appActivity': '.ui.activitys.MainActivity',
        }
        try:
            self.driver = webdriver.Remote('http://localhost:%s/wd/hub' % app['port'], desired_caps)
            time.sleep(3)
            self.base_page = BasePage(self.driver)
            self.xgimi_manager_page = XgimiManagerPage(self.base_page)
        except Exception:
            BasePage.get_screen('../screen_shot')

    def teardown_method(self):
        print("断开连接")

    @allure.story('打开投影管家')
    def test_app_uninstall_bt(self):
        cur_activity = self.driver.current_activity
        print(cur_activity)
        assert cur_activity == ".ui.activitys.MainActivity"


if __name__ == '__main__':
    pytest.main(['-s', '-q', "--alluredir", "../result", 'test_xgimi_manager.py'])
