# -*- encoding: utf-8 -*-

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import datetime


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger()

    def find_element(self, *loc):
        """重写查找单个元素方法"""
        try:
            WebDriverWait(self.driver, 5, 0.5).until(
                EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except Exception:
            self.logger.error('未找到元素：%s 请检查！' % loc[1])
            screen_shot = self.get_screen('screen_shot/')
            self.logger.error('已截图，路径：%s' % screen_shot)

    def find_elements(self, *loc):
        """重写查找多个元素方法"""
        try:
            WebDriverWait(self.driver, 5, 0.5).until(
                EC.visibility_of_element_located(loc))
            return self.driver.find_elements(*loc)
        except AttributeError:
            # print('页面未找到元素')
            self.logger.error('未找到元素：%s 请检查！' % loc[1])
            screen_shot = self.get_screen('screen_shot/')
            self.logger.error('已截图，路径：%s' % screen_shot)

    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        """重写send_keys方法"""
        try:
            loc = getattr(self, "_%s" % loc)
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            self.logger.error('未找到元素：%s 请检查！' % loc[1])
            screen_shot = self.get_screen('screen_shot/')
            self.logger.error('已截图，路径：%s' % screen_shot)

    def is_toast_exist(self, text):
        """is toast exist, return True or False
        :Agrs:
            - text   - 页面上看到的文本内容
        :Usage:
            is_toast_exist("看到的内容")
        """
        try:
            toast_loc = (By.XPATH, ".//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, 5, 0.5).until(
                EC.presence_of_element_located(toast_loc))
            return True
        except Exception as e:
            print(e)
            self.logger.error('未找到元素：%s 请检查！' % text)
            screen_shot = self.get_screen('screen_shot/')
            self.logger.error('已截图，路径：%s' % screen_shot)
            return False

    def is_element_exist(self, *loc):
        try:
            WebDriverWait(self.driver, 5, 0.5).until(
                EC.visibility_of_element_located(loc))
            self.driver.find_element(*loc)
            return True
        except Exception:
            self.logger.error('未找到元素：%s 请检查！' % loc[1])
            screen_shot = self.get_screen('screen_shot/')
            self.logger.error('已截图，路径：%s' % screen_shot)
            return False

    def get_size(self):
        """获取屏幕大小"""
        try:
            size = self.driver.get_window_size()
            return size
        except Exception:
            self.get_screen('screen_shot/')
            return None

    def swipe_to_left(self):
        """左滑"""
        window_size = self.get_size()
        width = window_size.get("width")
        height = window_size.get("height")
        try:
            self.driver.swipe(width * 0.9, height * 0.5, width * 0.1, height * 0.5)
            time.sleep(0.5)
        except Exception:
            self.get_screen('screen_shot/')
        # self.driver.swipe(x*0.9, y*0.5, x*0.1, y*0.5)

    def swipe_to_right(self):
        """右滑"""
        window_size = self.get_size()
        width = window_size.get("width")
        height = window_size.get("height")
        try:
            self.driver.swipe(width * 0.1, height * 0.5, width * 0.9, height * 0.5)
            time.sleep(0.5)
        except Exception:
            self.get_screen('screen_shot/')

    def swipe_to_up(self):
        """上滑"""
        window_size = self.get_size()
        width = window_size.get("width")
        height = window_size.get("height")
        try:
            self.driver.swipe(width * 0.5, height * 0.9, width * 0.5, height * 0.1)
            time.sleep(0.5)
        except Exception:
            self.get_screen('screen_shot/')

    def swipe_to_down(self):
        """下滑、下拉刷新"""
        window_size = self.get_size()
        width = window_size.get("width")
        height = window_size.get("height")
        try:
            self.driver.swipe(width * 0.5, height * 0.4, width * 0.5, height * 0.9)
            time.sleep(1)
        except Exception:
            self.get_screen('screen_shot/')

    def get_screen(self, path):
        """截图"""
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        screen_shot = path + 'a_' + now + '.png'
        self.driver.get_screenshot_as_file(screen_shot)
        return screen_shot


if __name__ == '__main__':
    pass
