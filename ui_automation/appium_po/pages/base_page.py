# -*- encoding: utf-8 -*-
import datetime
from time import sleep
from selenium.webdriver.common.by import By
from ui_automation.utils.Logger import logger
from ui_automation.appium_po.pages.web_driver_wait_page import WebDriverWaitPage
from selenium.webdriver.support.ui import WebDriverWait


class BasePage(object):
    def __init__(self, driver, timeout=10, poll_frequency=0.5, ignored_exceptions=None):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWaitPage(
            self.driver, timeout, poll_frequency, ignored_exceptions)

    def find_element(self, loc):
        """重写查找单个元素方法"""
        if self.wait.web_until_visibility_of_element_located(loc):
            return self.driver.find_element(*loc)
        else:
            self.logger.warning(f'未找到元素, 查找方法为：{loc[0]}，查找元素为：{loc[1]}')
            screen_name = self.get_screen('screen_shot/')
            self.logger.warning(f'已截图，路径：{screen_name}')

    def find_elements(self, loc, all_element=True):
        """查找所有元素"""
        if all_element:
            if self.wait.web_until_visibility_of_all_elements_located(loc):
                return self.driver.find_elements(*loc)
            else:
                self.logger.warning(f'未找到元素, 查找方法为：{loc[0]}，查找元素为：{loc[1]}')
                screen_name = self.get_screen('screen_shot/')
                self.logger.warning(f'已截图，路径：{screen_name}')
        else:
            if self.wait.web_until_visibility_of_any_elements_located(loc):
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
        if self.wait.web_until_element_to_be_clickable(loc):
            self.find_element(loc).click()

    def get_toast(self, toast_message):
        message = '//*[@text=\'{}\']'.format(toast_message)
        # 获取toast提示框内容
        toast_element = WebDriverWait(self.driver, 5).until(
            lambda x: x.find_element_by_xpath(message))
        return toast_element.text

    def is_toast_exist(self, text):
        """is toast exist, return True or False
        :Agrs:
            - text   - 页面上看到的文本内容
        :Usage:
            is_toast_exist("看到的内容")
        """
        toast_loc = (By.XPATH, ".//*[contains(@text,'%s')]" % text)
        if self.wait.web_until_not_presence_of_element_located(toast_loc):
            return True
        else:
            self.logger.warning('toast不存在')
            screen_name = self.get_screen('screen_shot/')
            self.logger.warning(f'已截图，路径：{screen_name}')
            return False

    def get_screen(self, path):
        """截图"""
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        screen_shot = path + 'a_' + now + '.png'
        self.driver.get_screenshot_as_file(screen_shot)
        return screen_shot

    def input_text(self, loc, text):
        """
            封装输入操作函数
        """
        self.fm = self.find_element(loc)
        self.fm.clear()  # 需要先清空输入框，防止有默认内容
        self.fm.send_keys(text)

    def back(self, times=1):
        '''模拟点击返回。

        Args:
            times: 点击次数，默认单击。
        '''
        command = {'command': 'input', 'args': ['keyevent', '4']}
        for _ in range(times):
            self.driver.execute_script('mobile:shell', command)
            # self.driver.press_keycode(keycode)  # 古法不好用

    def press_keycode(self, keycode: int, repeat: int = 1):
        '''发送按键键值

        发送某个按键键值，可重复发送。有延时，比back温和些。

        Args:
            keycode: 键值
            repeat: 重复次数
        '''
        for _ in range(repeat):
            self.driver.press_keycode(keycode)
            sleep(0.5)


if __name__ == '__main__':
    pass
