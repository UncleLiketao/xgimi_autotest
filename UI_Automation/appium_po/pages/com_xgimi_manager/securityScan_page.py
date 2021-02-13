from selenium.webdriver.remote.webdriver import WebDriver


class SecurityScanPage(object):
    def __init__(self, driver: WebDriver):
        self.driver = driver
    pass