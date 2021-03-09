from selenium.webdriver.common.by import By
from appium_po.pages.com_xgimi_newappmarket.NewAppMarket_management_page import AppManagementPage
from appium_po.pages.com_xgimi_manager.deepClean_page import DeepCleanPage
from appium_po.pages.com_xgimi_manager.netSpeedTest_page import NetSpeedTestPage
from appium_po.pages.com_xgimi_manager.securityScan_page import SecurityScanPage
import random
from utils.appium_server import AppiumServer
from appium import webdriver
from utils.adb_tool import AndroidDebugBridge
from appium_po.pages.base_page import BasePage


class XgimiManager(BasePage):
    # 投影管家首页按钮
    _immediate_optimization_bt = (By.ID, 'com.xgimi.manager:id/immediate_optimization_bt')
    _deep_cleaning_bt = (By.ID, 'com.xgimi.manager:id/deep_cleaning_bt')
    _security_scan_bt = (By.ID, 'com.xgimi.manager:id/security_scan_bt')
    _app_uninstall_bt = (By.ID, 'com.xgimi.manager:id/app_uninstall_bt')
    _network_speed_bt = (By.ID, 'com.xgimi.manager:id/network_speed_bt')

    # 系统状态提示文案
    _garbage_size_reminding = (By.ID, 'com.xgimi.manager:id/garbage_size_reminding')

    # 文案显示区域
    _memory_occupancy_view = (By.ID, 'com.xgimi.manager:id/memory_occupancy_view')
    _space_occupancy_view = (By.ID, 'com.xgimi.manager:id/space_occupancy_view')

    def __init__(self, driver: webdriver):
        super().__init__(driver)
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
        self.driver.implicitly_wait(10)

    # 点击一键加速按钮
    def click_immediate_optimization_bt(self):
        self.find_element(*self._immediate_optimization_bt).click()

    # 点击深度清理按钮
    def goto_deepClean(self):
        self.find_element(*self._deep_cleaning_bt).click()
        return DeepCleanPage(self.driver)

    # 点击安全扫描按钮
    def goto_sercurityScan(self):
        self.find_element(*self._security_scan_bt).click()
        return SecurityScanPage(self.driver)

    # 点击应用卸载按钮跳转应用卸载页面
    def goto_management(self):
        self.driver.find_element_by_id('com.xgimi.manager:id/app_uninstall_bt').click()
        return AppManagementPage(self.driver)

    # 点击网络测速按钮跳转网络测速页面
    def goto_netSpeedTest(self):
        self.driver.find_element_by_id('com.xgimi.manager:id/network_speed_bt').click()
        return NetSpeedTestPage(self.driver)


if __name__ == '__main__':
    pass
