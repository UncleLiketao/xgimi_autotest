from appium import webdriver


def com_xgimi_manger_driver(device_name, platform_version, app_port):
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = platform_version
    desired_caps['deviceName'] = device_name
    desired_caps['appPackage'] = 'com.xgimi.manager'
    desired_caps['appActivity'] = '.activitys.FirstActivity'
    desired_caps['unicodeKeyboard'] = True
    desired_caps['resetKeyboard'] = True
    desired_caps['autoGrantPermissions'] = True
    desired_caps['noReset'] = True
    driver = webdriver.Remote('http://localhost:%s/wd/hub' % app_port, desired_caps)
    return driver

