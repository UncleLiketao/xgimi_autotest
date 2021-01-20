import re
from math import floor
import subprocess
import os

from exceptions.CommonException import CommonException
from utils.Logger import logger

'''
apk文件的读取信息
'''


class ApkInfo(object):
    def __init__(self, apk_path):
        self.apk_path = apk_path

    def get_apk_size(self):
        """获取app文件大小（单位：M）"""
        apk_size = floor(os.path.getsize(self.apk_path) / (1024 * 1000))
        return apk_size

    def get_apk_info(self):
        p = subprocess.Popen("aapt dump badging %s" % self.apk_path, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output.decode())
        if not match:
            raise CommonException("can't get packageinfo")
        package_name = match.group(1)
        app_key = match.group(2)
        app_version = match.group(3)

        logger.info("=====getApkInfo=========")
        logger.info('packageName:', package_name)
        logger.info('appKey:', app_key)
        logger.info('appVersion:', app_version)
        return package_name, app_key, app_version

    def get_activity(self):
        """获取activity"""
        p = subprocess.Popen("aapt dump badging %s" % self.apk_path, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        logger.info("=====getApkActivity=========")
        match = re.compile("launchable-activity: name=(\S+)").search(output.decode())
        logger.info("match=%s" % match)
        if match is not None:
            logger.info('launchable-activity:', match.group(1))
            return match.group(1)

    def get_apk_name(self):
        """获取应用名"""
        cmd = "aapt dump badging " + self.apk_path + " | grep application-label: "
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        logger.info(f'get_apk_name: {output}')
        if output != "":
            result = output.split()[0].decode()[19:-1]
        return result
