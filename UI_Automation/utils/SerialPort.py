"""
@author: jack.tang
@date: 2020/12/30
"""
from time import sleep

import serial


class SerialPort:
    def __init__(self, port='COM4', baudrate=115200):
        self.ser = serial.Serial(port, baudrate)

    def send_data(self, cmd):
        cmd = cmd + "\n"
        self.ser.write(cmd.encode("utf-8"))

    def read_data(self, wait_time=0.5):
        data = ""
        sleep(wait_time)
        try:
            count = self.ser.inWaiting()  # 读取串口中缓存字符个数
            if count > 0:
                data = data + self.ser.read(count).decode("utf-8")
        except UnicodeDecodeError:
            raise Exception("UnicodeDecodeError:%s" % UnicodeDecodeError)
        return data.strip()  # 返回串口读取得数据并去掉前后空格

    def __del__(self):
        self.ser.close()

