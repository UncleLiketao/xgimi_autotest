from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class XgimiManagerPage(BasePage):
    # 一键加速按钮
    immediate_optimization_bt = (By.ID, 'com.xgimi.manager:id/immediate_optimization_bt')
    # 系统状态提示文案
    garbage_size_reminding = (By.ID, 'com.xgimi.manager:id/garbage_size_reminding')
    # 内存占用显示区域
    memory_occupancy_view = (By.ID, 'com.xgimi.manager:id/memory_occupancy_view')
    # 空间占用显示区域
    space_occupancy_view = (By.ID, 'com.xgimi.manager:id/space_occupancy_view')
    # 深度清理按钮
    deep_cleaning_bt = (By.ID, 'com.xgimi.manager:id/deep_cleaning_bt')
    # 安全扫描按钮
    security_scan_bt = (By.ID, 'com.xgimi.manager:id/security_scan_bt')
    # 应用卸载按钮
    app_uninstall_bt = (By.ID, 'com.xgimi.manager:id/app_uninstall_bt')
    # 网络测速按钮
    network_speed_bt = (By.ID, 'com.xgimi.manager:id/network_speed_bt')

    # 点击一键加速按钮
    def click_immediate_optimization_bt(self):
        self.find_element(*self.immediate_optimization_bt).click()

    # 点击深度清理按钮
    def click_deep_cleaning_bt(self):
        self.find_element(*self.deep_cleaning_bt).click()

    # 点击安全扫描按钮
    def click_security_scan_bt(self):
        self.find_element(*self.security_scan_bt).click()

    # 点击应用卸载按钮
    def click_app_uninstall_bt(self):
        self.find_element(*self.app_uninstall_bt).click()

    # 点击网络测速按钮
    def click_network_speed_bt(self):
        self.find_element(*self.network_speed_bt).click()


if __name__ == '__main__':
    pass
