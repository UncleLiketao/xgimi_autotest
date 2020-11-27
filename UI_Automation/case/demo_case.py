import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pytest
from pages.BasePage import BasePage
from pages.XgimiManagerPage import XgimiManagerPage
from appium import webdriver
import time
import logging
import allure


@allure.feature('测试登录功能')
def setup_method(self, method):
    self.logging_util.setup_logging()
    self.logger = logging.getLogger()
    desired_caps = {
        'platformName': 'Android',
        # 'deviceName': '127.0.0.1:5554',  # 手机设备名称，通过adb devices查看
        'deviceName': '127.0.0.1:62001',  # 手机设备名称，通过adb devices查看
        'platformVersion': '5.1.1',  # android系统的版本号
        'appPackage': 'com.aiosign.dzonesign',  # apk包名
        # apk的launcherActivity
        'appActivity': 'com.aiosign.dzonesign.view.AppStartActivity',
    }
    self.logger.info('启动app')















# desired_caps = { }
# desired_caps['platformName'] = 'Android'
# desired_caps['platformVersion'] = '8.0'
# desired_caps['deviceName'] = '192.168.4.10:5555'
# desired_caps['appPackage'] = 'com.xgimi.manager'
# desired_caps['appActivity'] = '.ui.activitys.MainActivity'
#
# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
#
# wait = WebDriverWait(driver, 10, 0.5)
# wait.until(EC.presence_of_element_located((By.ID, "app_uninstall_bt")))
# driver.find_element_by_id("com.xgimi.manager:id/app_uninstall_bt").click()
# wait.until(EC.invisibility_of_element_located((By.ID, "com.xgimi.manager:id/app_uninstall_bt")))
# cur_activity = driver.current_activity
# print(cur_activity)
#
# driver.quit()
