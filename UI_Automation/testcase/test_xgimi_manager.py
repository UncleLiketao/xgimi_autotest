import sys
import os
import pytest
from pages.BasePage import BasePage
from pages.XgimiManagerPage import XgimiManagerPage
from appium import webdriver
import time
import logging
import allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


@allure.feature('测试投影管家')
class Test_xgimi_manager(object):
    def setup_method(self, method):
        self.logger = logging.getLogger()
        desired_caps = {
            'platformName': 'Android',
            'deviceName': '192.168.4.10:5555',
            'platformVersion': '8.0',
            'appPackage': 'com.xgimi.manager',
            'appActivity': '.ui.activitys.MainActivity',
        }
        self.logger.info('启动app')
        try:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            time.sleep(3)
            self.base_page = BasePage(self.driver)
            self.xgimi_manager_page = XgimiManagerPage(self.base_page)
        except Exception:
            BasePage.get_screen('screen_shot/')

    def teardown_method(self, method):
        print("断开连接")

    @allure.story('跳转到应用卸载页面')
    def test_app_uninstall_bt(self):
        self.xgimi_manager_page.click_app_uninstall_bt()
        cur_activity = self.driver.current_activity
        print(cur_activity)
        assert cur_activity=="com.xgimi.appmanager.view.AppManagerActivity"
        self.logger.info('测试结束=====================================')


if __name__=='__main__':
    pytest.main(['-s', '-q', '--alluredir', '../result', 'demo_case.py'])
