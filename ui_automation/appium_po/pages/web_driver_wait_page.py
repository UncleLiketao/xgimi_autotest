"""
@author: jack.tang  
@date: 2020/12/19 
"""
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverWaitPage:
    def __init__(self, driver: webdriver, timeout=10, poll_frequency=0.5, ignored_exceptions=None):
        self.driver = driver
        self.timeout = timeout
        self.poll_frequency = poll_frequency
        self.ignored_exceptions = ignored_exceptions

    def web_until_visibility_of_element_located(self, locator):
        """判定该元素是否可见"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.visibility_of_element_located(locator))

    def web_until_visibility_of_all_elements_located(self, locator):
        """判定所有是否可见"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.visibility_of_all_elements_located(locator))

    def web_until_visibility_of_any_elements_located(self, locator):
        """判定任意一个是否可见"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.visibility_of_any_elements_located(locator))

    def web_util_presence_of_element_located(self, locator):
        """检查该元素是否存在于页面的DOM中"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.presence_of_element_located(locator))

    def web_util_text_to_be_present_in_element(self, locator, text):
        """判断对象是否包含给定text"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.text_to_be_present_in_element(locator, text))

    def web_util_text_to_be_present_in_element_value(self, locator, text):
        """判断对象是否包含给定text(定位元素不存在返回False)"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.text_to_be_present_in_element_value(locator, text))

    def web_util_invisibility_of_element_located(self, locator):
        """判定该元素是否不存在"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.invisibility_of_element_located(locator))

    def web_util_invisibility_of_element(self, locator):
        """判定元素是否不可见"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.invisibility_of_element(locator))

    def web_util_element_to_be_clickable(self, locator):
        """判定元素是否可点击"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.element_to_be_clickable(locator))

    def web_util_staleness_of(self, locator):
        """判断元素是否被移除"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.staleness_of(locator))

    def web_util_element_to_be_selected(self, locator):
        """判定元素是否被选择"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.element_to_be_selected(locator))

    def web_util_element_selection_state_to_be(self, locator, is_selected):
        """判定元素选中状态是否与预期一致"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until(
            EC.element_selection_state_to_be(locator, is_selected))

    def web_until_not_visibility_of_element_located(self, locator):
        """判定该元素是否不可见"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until_not(
            EC.visibility_of_element_located(locator))

    def web_util_not_presence_of_element_located(self, locator):
        """检查该元素是否不存在于页面的DOM中"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until_not(
            EC.presence_of_element_located(locator))

    def web_util_not_text_to_be_present_in_element(self, locator, text):
        """判断对象是否不包含给定text"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until_not(
            EC.text_to_be_present_in_element(locator, text))

    def web_util_not_text_to_be_present_in_element_value(self, locator, text):
        """判断对象是否不包含给定text(定位元素不存在返回False)"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until_not(
            EC.text_to_be_present_in_element_value(locator, text))

    def web_util_not_element_to_be_clickable(self, locator):
        """判定元素是否不可点击"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until_not(
            EC.element_to_be_clickable(locator))

    def web_util_not_staleness_of(self, locator):
        """判断元素是否没被移除"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until_not(
            EC.staleness_of(locator))

    def web_util_not_element_to_be_selected(self, locator):
        """判定元素是否没被选择"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until_not(
            EC.element_to_be_selected(locator))

    def web_util_not_element_selection_state_to_be(self, locator, is_selected):
        """判定元素选中状态不是与预期一致"""
        return WebDriverWait(self.driver, self.timeout, self.poll_frequency, self.ignored_exceptions).until_not(
            EC.element_selection_state_to_be(locator, is_selected))
