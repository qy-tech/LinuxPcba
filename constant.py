#!/usr/bin/env python
# -*- coding: utf-8 -*-


class _Const:
    """
    自定义常量类
    """

    class ConstError(PermissionError):
        pass

    class ConstCaseError(ConstError):
        pass

    # 重写 __setattr__() 方法
    def __setattr__(self, name, value):
        if name in self.__dict__:  # 已包含该常量，不能二次赋值
            raise self.ConstError("Can't change const {0}".format(name))
        if not name.isupper():  # 所有的字母需要大写
            raise self.ConstCaseError("const name {0} is not all uppercase".format(name))
        self.__dict__[name] = value


# 将系统加载的模块列表中的 const 替换为 _const() 实例
# sys.modules[__name__] = _Const()
const = _Const()

const.WIFI = 'wifi'
const.USB_NETWORK = 'usb network'
const.BLUETOOTH = 'bluetooth'
const.RELAY54 = 'relay 54'
const.RELAY55 = 'relay 55'
const.SOUND_PLAY = 'play'
const.SOUND_RECORD = 'record'
const.NFC = 'nfc'
const.CAMERA = 'camera'
const.LED_R = 'red'
const.LED_G = 'green'
const.LED_B = 'blue'
const.HUMIDITY = 'humidity'
const.TEMPERATURE = 'temp'
const.PRESSURE = 'pressure'
const.VL53L1X = 'vl53l1x'
const.XM132 = 'xm132'
const.RGB = 'rgb'
const.SENSOR = 'sensor'
const.MAX44009 = 'MAX44009'
const.AGING = 'aging'
const.SOUND = 'sound'
const.RELAY = 'relay'
const.RTC = 'rtc'
const.WIFI_BT = 'wifi/bt'
const.AUTO_TEST = 'autotest'
const.SUCCESS = 'success'
const.ERROR = 'error'
const.COLOR_SUCCESS = 'green'
const.COLOR_ERROR = 'red'
const.TEST_CASE = 'testCase'
const.TEST_CASE_LIST = 'testCaseList'
const.TEST_CASE_PATH = 'testCasePath'
const.CHANGE_PERMISSION = 'changePermission'
