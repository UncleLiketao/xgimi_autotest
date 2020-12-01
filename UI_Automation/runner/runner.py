# -*- coding: utf-8 -*-
import sys
import os
import random
import platform
from utils.adb_tool import *
from datetime import datetime
from multiprocessing import Pool
from utils.device_tool import getDeviceInfo
from utils.apk_tool import ApkInfo
from utils.appium_server import AppiumServer

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def kill_adb():
    if platform.system() == "Windows":
        os.system(PATH("../utils/kill5037.bat"))
    else:
        os.popen("killall adb")
    os.system("adb start-server")


def runnerPool(getDevices):
    devices_Pool = []

    for i in range(0, len(getDevices)):
        _pool = []
        _initApp = {}
        print("=====runnerPool=========")
        print(getDevices)
        _initApp["deviceName"] = getDevices[i]["devices"]
        _initApp["udid"] = getDevices[i]["devices"]
        _initApp["platformVersion"] = getDeviceInfo(devices=_initApp["deviceName"])["release"]
        _initApp["platformName"] = "android"
        _initApp["port"] = getDevices[i]["port"]
        _initApp["automationName"] = "uiautomator2"
        _initApp["systemPort"] = getDevices[i]["systemPort"]
        _initApp["app"] = getDevices[i]["app"]
        apkInfo = ApkInfo(_initApp["app"])
        _initApp["appPackage"] = apkInfo.getApkBaseInfo()[0]
        _initApp["appActivity"] = apkInfo.getApkActivity()
        _pool.append(_initApp)
        devices_Pool.append(_initApp)

    pool = Pool(len(devices_Pool))
    pool.map(runnerCaseApp, devices_Pool)
    pool.close()
    pool.join()


def runnerCaseApp(devices):
    os.popen("allure generate report/ -o result/ --clean")
    os.popen("allure open -h 0.0.0.0 -p 8083 result/")


if __name__ == '__main__':

    kill_adb()

    devicess = AndroidDebugBridge().attached_devices()
    if len(devicess) > 0:
        l_devices = []
        for dev in devicess:
            app = {}
            app["devices"] = dev
            app["port"] = str(random.randint(4700, 4900))
            app["bport"] = str(random.randint(4700, 4900))
            app["systemPort"] = str(random.randint(4700, 4900))
            app["app"] = ""
            l_devices.append(app)

        appium_server = AppiumServer(l_devices)
        appium_server.start_server()
        runnerPool(l_devices)
        appium_server.stop_server(l_devices)

    else:
        print("没有可用的安卓设备")
