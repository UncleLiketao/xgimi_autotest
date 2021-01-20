# -*- encoding: utf-8 -*-
import datetime
import time

from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By

from utils.Logger import logger
from pages.WebDriverWaitPage import WebDriverWaitPage


class BasePage(object):
    def __init__(self, driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWaitPage(self.driver, timeout, poll_frequency, ignored_exceptions)

    def find_element(self, loc):
        """重写查找单个元素方法"""
        if self.wait.web_util_invisibility_of_element(self.driver):
            return self.driver.find_element(*loc)
        else:
            self.logger.warning(f'未找到元素, 查找方法为：{loc[0]}，查找元素为：{loc[1]}')
            screen_name = self.get_screen('screen_shot/')
            self.logger.warning(f'已截图，路径：{screen_name}')

    def find_elements(self, loc, all_element=True):
        """查找所有元素"""
        if all_element:
            if self.wait.web_until_visibility_of_all_elements_located:
                return self.driver.find_elements(*loc)
            else:
                self.logger.warning(f'未找到元素, 查找方法为：{loc[0]}，查找元素为：{loc[1]}')
                screen_name = self.get_screen('screen_shot/')
                self.logger.warning(f'已截图，路径：{screen_name}')
        else:
            if self.wait.web_until_visibility_of_any_elements_located:
                return self.driver.find_elements(*loc)
            else:
                self.logger.warning(f'未找到元素, 查找方法为：{loc[0]}，查找元素为：{loc[1]}')
                screen_name = self.get_screen('screen_shot/')
                self.logger.warning(f'已截图，路径：{screen_name}')

    def find_element_and_send_keys(self, loc, value):
        """输入文本"""
        self.find_element(loc).send_keys(value)

    def find_element_and_send_click(self, loc):
        """点击按钮"""
        if self.wait.web_util_element_to_be_clickable(loc):
            self.find_element(loc).click()

    def is_toast_exist(self, text):
        """is toast exist, return True or False
        :Agrs:
            - text   - 页面上看到的文本内容
        :Usage:
            is_toast_exist("看到的内容")
        """
        toast_loc = (By.XPATH, ".//*[contains(@text,'%s')]" % text)
        if self.wait.web_util_not_presence_of_element_located(toast_loc):
            return True
        else:
            self.logger.warning('toast不存在')
            screen_name = self.get_screen('screen_shot/')
            self.logger.warning(f'已截图，路径：{screen_name}')
            return False

    def get_size(self):
        """获取屏幕大小"""
        try:
            size = self.driver.get_window_size()
            return size
        except NoSuchWindowException:
            self.logger.warning("无能获取到屏幕大小")
            self.get_screen('screen_shot/')

    def swipe_to_left(self):
        """左滑"""
        window_size = self.get_size()
        if window_size:
            width = window_size.get("width")
            height = window_size.get("height")
            self.driver.swipe(width * 0.9, height * 0.5, width * 0.1, height * 0.5)
            time.sleep(0.5)

    def swipe_to_right(self):
        """右滑"""
        window_size = self.get_size()
        if window_size:
            width = window_size.get("width")
            height = window_size.get("height")
            self.driver.swipe(width * 0.1, height * 0.5, width * 0.9, height * 0.5)
            time.sleep(0.5)

    def swipe_to_up(self):
        """上滑"""
        window_size = self.get_size()
        if window_size:
            width = window_size.get("width")
            height = window_size.get("height")
            self.driver.swipe(width * 0.5, height * 0.9, width * 0.5, height * 0.1)
            time.sleep(0.5)

    def swipe_to_down(self):
        """下滑、下拉刷新"""
        window_size = self.get_size()
        if window_size:
            width = window_size.get("width")
            height = window_size.get("height")
            self.driver.swipe(width * 0.5, height * 0.4, width * 0.5, height * 0.9)
            time.sleep(1)

    def get_screen(self, path):
        """截图"""
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        screen_shot = path + 'a_' + now + '.png'
        self.driver.get_screenshot_as_file(screen_shot)
        return screen_shot


if __name__ == '__main__':
    pass
