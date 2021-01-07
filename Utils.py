# -*- coding: utf-8 -*-
# !/usr/bin/env python
import logging
import os
import subprocess
import sys

from constant import const

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename='/tmp/FactoryTest.log',
                    filemode='a')

logger = logging.getLogger()


def run_shell_command(command):
    """
    运行 shell 命令获取执行结果
    :param command: 要执行的命令
    :return: 命令运行的输出结果
    """
    logging.debug('run command [{}]'.format(command))
    # with os.popen(command) as r:
    #     result = r.read()
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    outMessage = str(result.stdout.read(), encoding="utf-8")
    errMessage = str(result.stderr.read(), encoding='utf-8')
    logging.debug('[{}] result is [{}]'.format(command, errMessage if errMessage else outMessage))
    success = not errMessage
    message = errMessage if errMessage else outMessage
    return success, message


def resize_window(window):
    window.update()
    curWidth = window.winfo_reqwidth()
    curHeight = window.winfo_reqheight()
    scnWidth, scnHeight = window.maxsize()
    newGeometry = '{}x{}+{}+{}' \
        .format(curWidth, curHeight,
                (scnWidth - curWidth) // 2,
                (scnHeight - curHeight) // 2)
    window.geometry(newGeometry)


def check_and_create_gpio(gpio):
    gpioPath = '/sys/class/gpio/gpio{}/value'.format(gpio)
    createGpioCommand = 'echo {0} > /sys/class/gpio/export; ' \
                        'echo out > /sys/class/gpio/gpio{0}/direction'.format(gpio)
    if not os.path.exists(gpioPath):
        run_shell_command(createGpioCommand)


def commands(item, path):
    switch = {
        const.WIFI: 'busybox ifconfig wlan0',
        const.BLUETOOTH: 'hcitool dev',
        const.USB_NETWORK: 'busybox ifconfig usb0',
        const.RELAY54: 'echo 1 > /sys/class/gpio/gpio{0}/value; sleep 1; echo 0 > /sys/class/gpio/gpio{0}/value',
        const.RELAY55: 'echo 1 > /sys/class/gpio/gpio{0}/value; sleep 1; echo 0 > /sys/class/gpio/gpio{0}/value',
        const.SOUND_PLAY: 'aplay ' + get_real_path('resource/audio.wav'),
        const.SOUND_RECORD: 'arecord -f cd -d 10 /tmp/audio.wav',
        const.NFC: get_real_path('bin/test_nfc'),
        const.CAMERA: 'cheese',
        const.LED_R: 'echo 1 > /sys/class/gpio/gpio{0}/value; sleep 1; echo 0 > /sys/class/gpio/gpio{0}/value',
        const.LED_G: 'echo 1 > /sys/class/gpio/gpio{0}/value; sleep 1; echo 0 > /sys/class/gpio/gpio{0}/value',
        const.LED_B: 'echo 1 > /sys/class/gpio/gpio{0}/value; sleep 1; echo 0 > /sys/class/gpio/gpio{0}/value',
        const.HUMIDITY: 'cat {}',
        const.TEMPERATURE: 'cat {}',
        const.PRESSURE: 'cat {}',
        const.VL53L1X: 'ls {}',
        const.XM132: 'ls {}',
        const.MAX44009: 'cat {}',
        const.CHANGE_PERMISSION: 'chmod +x {}'
    }
    return switch.get(item, '').format(path)


def get_real_path(path):
    basePath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(basePath, path)


def check_and_authorization():
    binPath = '{}/*'.format(get_real_path('bin'))
    run_shell_command(commands(const.CHANGE_PERMISSION, binPath))
