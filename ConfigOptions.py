# -*- coding: utf-8 -*-
# !/usr/bin/env python
import configparser
import os
from datetime import datetime

from constant import const


class ConfigOptions:
    """
    配置选项
    """

    def __init__(self):
        self.config_file_path = '/tmp/config.ini'
        self.log_file_path = '/tmp/{}_log.txt'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
        self.config = configparser.ConfigParser()

        self._init_config()

    def _init_config(self):
        """
        初始化配置文件
        """
        if not os.path.exists(self.config_file_path):
            self.config[const.TEST_CASE_PATH] = {
                const.RTC: '/dev/rtc1',
                const.RELAY54: '54',
                const.RELAY55: '55',
                const.LED_R: '33',
                const.LED_G: '45',
                const.LED_B: '32',
                const.VL53L1X: '/dev/vl53l1x-dev',
                const.XM132: '/dev/xm132-dev',
                const.MAX44009: '/sys/bus/iio/devices/iio:device2/in_illuminance_input',
                const.HUMIDITY: '/sys/bus/iio/devices/iio:device1/in_humidityrelative_input',
                const.TEMPERATURE: '/sys/bus/iio/devices/iio:device*/in_temp_input',
                const.PRESSURE: '/sys/bus/iio/devices/iio:device*/in_pressure_input',
            }
            self.config[const.TEST_CASE] = {
                const.WIFI_BT: '1',
                const.RTC: '1',
                const.RELAY: '1',
                const.SOUND: '1',
                const.NFC: '1',
                const.CAMERA: '1',
                const.RGB: '1',
                const.SENSOR: '1',
                const.AUTO_TEST: '0',
            }
            self.config[const.TEST_CASE_LIST] = {
                const.TEST_CASE_LIST: ' '.join([
                    const.WIFI_BT,
                    const.RTC,
                    const.RELAY,
                    const.SOUND,
                    const.NFC,
                    const.CAMERA,
                    const.RGB,
                    const.SENSOR,
                    const.AUTO_TEST])
            }
            self.save_config()
        else:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                self.config.read_file(f)

    def save_config(self):
        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def save_log(self, message):
        """
        将测试结果写入到文件中
        """
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(message)
