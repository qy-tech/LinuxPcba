# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
from functools import partial
from tkinter import *

import Utils
from ConfigOptions import ConfigOptions
from ReadCpuInfoThread import ReadCpuInfoThread
from Utils import logger as logging
from constant import const


class GUITest:
    """
    工厂测试工具
    """

    def __init__(self, config=None):
        self.autoTest = 0
        self.grids = []
        self.testCaseButtons = {}
        self.configOptions = config
        self.testCase = []
        self.testCaseEnable = {}
        self.currentIndex = 0
        self.currentItem = ''

        self.window = None
        self.messageLabel = NONE
        self.toplevel = None
        self.successButton = None
        self.failButton = None

        self.readCpuInfoThread = ReadCpuInfoThread()
        self.readCpuInfoThread.setDaemon(True)
        self.readCpuInfoThread.set_flag(False)
        self.readCpuInfoThread.start()

    def init_config(self):
        """
        从配置文件中加载相关配置
        """
        testCaseStatus = self.configOptions.config[const.TEST_CASE]
        self.testCase = self.configOptions.config[const.TEST_CASE_LIST][const.TEST_CASE_LIST].split(' ')
        logging.debug('testCase {}'.format(self.testCase))

        for index, key in enumerate(testCaseStatus):
            logging.debug('testCase {} {}'.format(key, testCaseStatus[key]))
            val = IntVar()
            val.set(testCaseStatus[key])
            self.testCaseEnable[key] = val
            if index < len(self.grids):
                self.grids[index].config(state=DISABLED if testCaseStatus[key] == "0" else NORMAL)
        logging.debug('testCaseEnable {}'.format(self.testCaseEnable))
        logging.debug('auto test {}'.format(self.autoTest))

    def start(self):
        """
        启动测试主界面
        """
        self.window = Tk(className='Factory test')
        self.window.resizable(0, 0)
        self.init_config()
        self.create_grid()
        self.create_menu()
        Utils.resize_window(self.window)
        self.window.mainloop()

    def create_grid(self):
        """
        根据测试项生成测试界面
        """
        for index, item in enumerate(self.testCase[:-1]):
            button = Button(
                self.window,
                text=item,
                font='Helvetica 16 bold',
                width=16,
                height=4,
                state='normal',
                highlightbackground='#3E4149',
                command=partial(self.on_item_click_listener, index, item),
            )
            button.grid(row=index // 2, column=index % 2, sticky=W, padx=5, pady=5)
            self.grids.append(button)

    def create_menu(self):
        """
        测试界面菜单部分
        """
        menu = Menu(self.window)
        self.window.config(menu=menu)

        # menu file
        fileMenu = Menu(menu, tearoff=False)
        fileMenu.add_command(label='Reset config', command='')
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.window.quit)
        menu.add_cascade(label='File', menu=fileMenu)

        # menu test case
        testCaseMenu = Menu(menu, tearoff=False)
        for index, item in enumerate(self.testCase):
            if index == len(self.testCase) - 1:
                testCaseMenu.add_separator()
            testCaseMenu.add_checkbutton(
                label=item,
                onvalue=1,
                offvalue=0,
                variable=self.testCaseEnable[item],
                command=partial(self.set_test_case_enable, index, item)
            )
        menu.add_cascade(label=const.TEST_CASE, menu=testCaseMenu)

        # Auto Test
        # menu.add_command(label='Auto test', command=partial(self.start_auto_test))
        # Agin test
        menu.add_command(label='Aging test', command=partial(self.test_aging, const.AGING))

    def set_test_case_enable(self, index, item):
        """
        设置测试项是否可用
        """
        value = str(self.testCaseEnable[item].get())
        self.configOptions.config[const.TEST_CASE][item] = value
        self.configOptions.save_config()
        self.grids[index].config(state=DISABLED if value == "0" else NORMAL)

    def start_auto_test(self):
        """
        启动自动测试
        """

    def test_aging(self, title):
        """
        启动老化测试，并展示 CPU 相关信息
        stressapptest -M 1200 -s 300000
        memtester 1G 5
        """
        os.system('stressapptest -M 1200 -s 300000 &')
        os.system('memtester 1G 5 &')
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel = None

        self.toplevel = Toplevel()
        self.toplevel.title(title)
        self.messageLabel = Label(self.toplevel, width=40, height=20)
        self.messageLabel.pack()

        self.readCpuInfoThread.set_flag(True)
        self.readCpuInfoThread.set_ui(self.messageLabel)
        self.toplevel.protocol('WM_DELETE_WINDOW', self.stop_read_cpu_info_thread)
        self.toplevel.update()
        Utils.resize_window(self.toplevel)

    def stop_read_cpu_info_thread(self):
        """
        停止读取 CPU 相关信息
        """
        self.readCpuInfoThread.set_flag(False)
        # 查找 stressapptest 相关进程并关闭
        os.system("pidof stressapptest | xargs kill -9 &")
        # 查找 memtester 相关进程并关闭
        os.system("pidof memtester | xargs kill -9 &")
        self.toplevel.destroy()

    def on_test_case_click_listener(self, item):
        """
        点击测试项目执行相关的命令
        """
        logging.debug('test case name {}'.format(item))
        try:
            path = self.configOptions.config[const.TEST_CASE_PATH][item]
        except KeyError as _:
            path = ''
        logging.debug('test case path {}'.format(path))
        result, message = Utils.run_shell_command(Utils.commands(item, path))
        switchAutoCheck = {
            const.WIFI: 'inet addr' in message,
            const.BLUETOOTH: 'hci' in message,
            const.USB_NETWORK: 'inet addr' in message,
            const.NFC: 'success' in message,
            const.HUMIDITY: message.strip(),
            const.TEMPERATURE: message.strip(),
            const.PRESSURE: message.strip(),
            const.MAX44009: message.strip(),
            const.VL53L1X: message.strip(),
            const.XM132: message.strip(),
        }
        if item in switchAutoCheck.keys():
            logging.debug('result is {} auto check is {}'.format(result, switchAutoCheck.get(item, False)))
            color = const.COLOR_SUCCESS if (result and switchAutoCheck.get(item, False)) else const.COLOR_ERROR
            self.testCaseButtons[item].config(bg=color)

    def test_wifi_bt(self):
        """
        显示 WIIF 和 Bluetooth 以及 4G 5G 测试模块
        """
        logging.debug('test wifi bt')
        self.create_test_case_button(const.WIFI, 0, 2)
        # self.create_test_case_button(const.BLUETOOTH, 1, 2)
        self.create_test_case_button(const.USB_NETWORK, 2, 2)

    def test_rtc(self):
        """
        显示 RTC 测试模块，RTC 测试直接判断相关节点是否存在即可
        """
        logging.debug('test rtc')
        try:
            rtcPath = self.configOptions.config[const.TEST_CASE_PATH][const.RTC]
        except KeyError as _:
            rtcPath = '/dev/rtc1'
        self.on_result_click_listener(os.path.exists(rtcPath))

    def test_relay(self):
        """
        显示继电器测试模块，首先判断是否有对应的 GPIO 口如果没有就创建
        :return:
        """
        logging.debug('test relay')
        try:
            relay54 = self.configOptions.config[const.TEST_CASE_PATH][const.RELAY54]
        except KeyError as _:
            relay54 = "54"
        try:
            relay55 = self.configOptions.config[const.TEST_CASE_PATH][const.RELAY55]
        except KeyError as _:
            relay55 = "55"

        Utils.check_and_create_gpio(relay54)
        Utils.check_and_create_gpio(relay55)

        self.create_test_case_button(const.RELAY54, 0, 2)
        self.create_test_case_button(const.RELAY55, 1, 2)

    def test_sound(self):
        """
        测试声卡是否正常，分为录音和放音功能
        """
        logging.debug('test sound')
        # self.create_test_case_button(const.SOUND_RECORD, 0, 2)
        self.create_test_case_button(const.SOUND_PLAY, 1, 2)

    def test_nfc(self):
        """
        测试 NFC 模块是否正常
        """
        logging.debug('test nfc')

        self.create_test_case_button(const.NFC, 0, 2)

    def test_camera(self):
        """
        测试摄像头是否正常
        """
        logging.debug('test_camera')
        self.create_test_case_button(const.CAMERA, 0, 2)

    def test_rgb(self):
        """
        测试 RGB 灯是否正常，首先判断节点是否存在，如果不存在就创建对应的节点
        """
        logging.debug('test_rgb')
        try:
            ledR = self.configOptions.config[const.TEST_CASE_PATH][const.LED_R]
        except KeyError as _:
            ledR = "32"
        try:
            ledG = self.configOptions.config[const.TEST_CASE_PATH][const.LED_G]
        except KeyError as _:
            ledG = "33"
        try:
            ledB = self.configOptions.config[const.TEST_CASE_PATH][const.LED_B]
        except KeyError as _:
            ledB = "45"
        Utils.check_and_create_gpio(ledR)
        Utils.check_and_create_gpio(ledG)
        Utils.check_and_create_gpio(ledB)

        self.create_test_case_button(const.LED_R, 0, 2)
        self.create_test_case_button(const.LED_G, 1, 2)
        self.create_test_case_button(const.LED_B, 2, 2)

    def test_sensor(self):
        """
        测试 Sensor 是否正常
        """
        logging.debug('test_sensor')
        self.create_test_case_button(const.VL53L1X, 0, 1)
        self.create_test_case_button(const.XM132, 1, 1)
        self.create_test_case_button(const.MAX44009, 2, 1)
        self.create_test_case_button(const.HUMIDITY, 0, 2)
        self.create_test_case_button(const.TEMPERATURE, 1, 2)
        self.create_test_case_button(const.PRESSURE, 2, 2)

    def on_result_click_listener(self, result):
        """
        根据测试结果改变相关界面并保存结果到测试日志
        :param result: 测试结果
        """
        logging.debug('{} test {}'.format(self.currentItem, result))
        color = const.COLOR_SUCCESS if result else const.COLOR_ERROR
        resultMessage = const.SUCCESS if result else const.ERROR
        self.grids[self.currentIndex].config(bg=color)
        self.configOptions.save_log('{} test {}\n'.format(self.currentItem, resultMessage))
        self.toplevel.destroy()
        self.toplevel = None

    def create_test_case_button(self, text, row, column):
        button = Button(
            self.toplevel,
            text=text,
            font="Helvetica 10 bold",
            width=8,
            height=2,
            state="normal",
            highlightbackground="#3E4149",
            command=partial(self.on_test_case_click_listener, text)
        )
        button.grid(row=row, column=column, padx=10, pady=10)
        self.testCaseButtons[text] = button

    def on_item_click_listener(self, index, item):
        """
        点击屏幕上的条目时触发的事件
        """
        logging.debug('on item click {} {}'.format(index, item))
        self.currentIndex = index
        self.currentItem = item

        if self.toplevel:
            self.toplevel.destroy()

        self.toplevel = Toplevel()
        self.toplevel.title(item)

        # Python字典中还可以包括函数或Lambda表达式
        # 使用字典形式实现其他的语言 switch 效果避免if else 嵌套
        switch = {
            const.WIFI_BT: self.test_wifi_bt,
            const.RTC: self.test_rtc,
            const.RELAY: self.test_relay,
            const.SOUND: self.test_sound,
            const.NFC: self.test_nfc,
            const.CAMERA: self.test_camera,
            const.RGB: self.test_rgb,
            const.SENSOR: self.test_sensor,
        }
        self.successButton = Button(
            self.toplevel,
            text=const.SUCCESS,
            font="Helvetica 10 bold",
            width=8,
            height=2,
            state="normal",
            highlightbackground="#3E4149",
            command=partial(self.on_result_click_listener, True)
        )
        self.successButton.grid(row=3, column=0, padx=10, pady=10)

        self.failButton = Button(
            self.toplevel,
            text=const.ERROR,
            font="Helvetica 10 bold",
            width=8,
            height=2,
            state="normal",
            highlightbackground="#3E4149",
            command=partial(self.on_result_click_listener, False)
        )
        self.failButton.grid(row=3, column=3, padx=10, pady=10)
        method = switch.get(item)
        if method:
            method()
        if self.toplevel:
            self.toplevel.update()
            Utils.resize_window(self.toplevel)


def main():
    Utils.check_and_authorization()
    gui = GUITest(ConfigOptions())
    gui.start()


if __name__ == '__main__':
    main()
