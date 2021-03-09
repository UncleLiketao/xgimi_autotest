import allure
import pytest
from ui_automation.appium_po.pages.com_xgimi_manager.home_page import XgimiManager


@allure.feature('投影管家功能')
@allure.severity(allure.severity_level.BLOCKER)
class TestNetSpeedTest(object):
    @allure.story('点击跳转到网络测速页面')
    def test_goto_netSpeedTest(self, get_driver):
        self.driver = get_driver
        page = XgimiManager(self.driver)
        page.goto_netSpeedTest()
        with allure.step('启动投影管家'):
            cur_activity = self.driver.current_activity
            print(cur_activity)
        assert cur_activity == ".ui.activitys.NetWorkSpeedAcitivity"


if __name__  == '__main__':
    pytest.main(['test_homePage.py'])
