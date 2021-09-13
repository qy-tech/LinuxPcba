# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import threading
import time


class ReadCpuInfoThread(threading.Thread):
    def __init__(self, ui=None):
        threading.Thread.__init__(self)
        self.Flag = True
        self.ui = ui

    def run(self):
        while True:
            if self.Flag and self.ui:
                self.show_message()
            else:
                time.sleep(2)

    def set_flag(self, flag):
        self.Flag = flag

    def set_ui(self, ui):
        self.ui = ui

    def show_message(self):

        temp = os.popen('cat /sys/class/thermal/thermal_zone0/temp &').readlines()
        freq0 = os.popen(
            'cat /sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq &'
        ).readlines()
        freq4 = os.popen(
            'cat /sys/devices/system/cpu/cpufreq/policy4/scaling_cur_freq &'
        ).readlines()
        if temp:
            temp = int(temp[0]) / 1000
        if freq0:
            freq0 = int(freq0[0]) / 1000
        if freq4:
            freq4 = int(freq4[0]) / 1000

        # temp = random.randint(50, 100)
        # freq0 = random.randint(1024, 1400)
        # freq4 = random.randint(1024, 1800)
        text = 'temp: {}℃\ncpu0freq: {}M\ncpu4freq: {}M'.format(temp, freq0, freq4)
        try:
            if self.ui and text:
                self.ui.config(text=text)
        except Exception as _:
            pass
        time.sleep(2)
