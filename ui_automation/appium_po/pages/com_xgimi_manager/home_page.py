from selenium.webdriver.common.by import By
from ui_automation.appium_po.pages.com_xgimi_newappmarket.NewAppMarket_management_page import AppManagementPage
from ui_automation.appium_po.pages.com_xgimi_manager.deepClean_page import DeepCleanPage
from ui_automation.appium_po.pages.com_xgimi_manager.netSpeedTest_page import NetSpeedTestPage
from ui_automation.appium_po.pages.com_xgimi_manager.securityScan_page import SecurityScanPage
from ui_automation.appium_po.pages.base_page import BasePage


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

    # 点击一键加速按钮
    def click_immediate_optimization_bt(self):
        self.find_element(self._immediate_optimization_bt).click()

    # 点击深度清理按钮
    def goto_deepClean(self):
        self.find_element(self._deep_cleaning_bt).click()
        return DeepCleanPage(self.driver)

    # 点击安全扫描按钮
    def goto_securityScan(self):
        self.find_element(self._security_scan_bt).click()
        return SecurityScanPage(self.driver)

    # 点击应用卸载按钮跳转应用卸载页面
    def goto_appManager(self):
        self.find_element(self._app_uninstall_bt).click()
        return AppManagementPage(self.driver)

    # 点击网络测速按钮跳转网络测速页面
    def goto_netSpeedTest(self):
        self.find_element(self._network_speed_bt).click()
        return NetSpeedTestPage(self.driver)


if __name__ == '__main__':
    pass
