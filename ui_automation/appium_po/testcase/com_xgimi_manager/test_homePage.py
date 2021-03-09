import allure
import pytest


@allure.feature('投影管家功能')
@allure.severity(allure.severity_level.BLOCKER)
class TestHomePage(object):
    @allure.story('启动进入投影管家首页')
    def test_goto_home(self, get_driver):
        self.driver = get_driver
        with allure.step('启动投影管家'):
            cur_activity = self.driver.current_activity
            print(cur_activity)
        assert cur_activity == ".ui.activitys.MainActivity"


if __name__ == '__main__':
    pytest.main(['test_homePage.py'])
