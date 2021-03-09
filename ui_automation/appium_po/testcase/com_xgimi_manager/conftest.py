import pytest
import random
from ui_automation.utils.adb_tool import AndroidDebugBridge
from ui_automation.utils.appium_server import AppiumServer
from appium import webdriver


def runnerPool(getDevices):
    devices_Pool = []
    for i in range(0, len(getDevices)):
        _pool = []
        _initApp = {}
        print("=====runnerPool=========")
        print(getDevices)
        _initApp["deviceName"] = getDevices[i]["devices"]
        _initApp["udid"] = getDevices[i]["devices"]
        _initApp["platformVersion"] = AndroidDebugBridge().get_version_number(AndroidDebugBridge().attached_devices(i))
        _initApp["platformName"] = "android"
        _initApp["port"] = getDevices[i]["port"]
        _initApp["automationName"] = "uiautomator2"
        _initApp["systemPort"] = getDevices[i]["systemPort"]
        _initApp["appPackage"] = 'com.xgimi.manager'
        _initApp["appActivity"] = '.ui.activitys.MainActivity'
        _pool.append(_initApp)
        devices_Pool.append(_initApp)
    print(devices_Pool)

@pytest.fixture(scope='class')
def get_driver():
    devices = AndroidDebugBridge().attached_devices()
    l_devices = []
    app = { "port": str(random.randint(4700, 4900)), "bport": str(random.randint(4700, 4900)),
            "systemPort": str(random.randint(4700, 4900)), "devices": devices[0] }
    l_devices.append(app)
    AppiumServer(l_devices).start_server()
    version_number = AndroidDebugBridge().get_version_number(devices[0])
    caps = {
        'platformName': 'Android',
        'deviceName': '%s' % devices[0],
        'platformVersion': '%s' % version_number,
        'appPackage': 'com.xgimi.manager',
        'appActivity': '.ui.activitys.MainActivity',
        "noReset": True
    }
    driver = webdriver.Remote('http://localhost:%s/wd/hub' % app['port'], caps)
    yield driver  # yield往上是前置条件，往下是后置条件。且yield也是个返回值跟return差不多
    driver.quit()
    AppiumServer().stop_server(l_devices)

devicess = AndroidDebugBridge().attached_devices()
if len(devicess) > 0:
    l_devices = []
    for dev in devicess:
        app = {}
        app["devices"] = dev
        app["port"] = str(random.randint(4700, 4900))
        app["bport"] = str(random.randint(4700, 4900))
        app["systemPort"] = str(random.randint(4700, 4900))
        l_devices.append(app)
runnerPool(l_devices)
appium_server = AppiumServer(l_devices)
appium_server.start_server()
appium_server.stop_server(l_devices)