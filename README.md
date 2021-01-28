# Linux Factory Test 

Linux 工厂测试工具

## 打包

将代码克隆至目标设备，并在目标设备上安装`pyinstaller`

修改`FactoryTest.spec`下的`pathex`和`hiddenimports`为项目的绝对路径

执行打包命令`pyinstaller FactoryTest.spec`

命令执行完成后再 dist 目录下会看到可执行文件

## 运行

将 dist 目录下的`FactoryTest`可执行文件拷贝至 U盘根目录，插上 U盘即可

## 问题 

1. 蓝牙测试相关命令在terminal下运行能获取到设备，在`/etc/udev/rules.d/`检测 U盘然后执行对应脚本中执行无法获取到结果

## 配置测试项

创建配置文件`config.ini`，如果需要配置某些选项不测试直接修改`testCase`中对应的选项为 0，
此时界面上测试项目就直接显示为不可点击，如果需要配置某些测试项目不显示直接在`testCaseList`中将对应的项目移除掉。

创建或修改 `config.ini`文件后可以通过 `adb push config.ini /tmp/config.ini`将配置文件推送到设备。

```ini
[testCasePath]
red = 32
blue = 45
relay 54 = 54
green = 33
temp = /sys/bus/iio/devices/iio:device*/in_temp_input
relay 55 = 55
humidity = /sys/bus/iio/devices/iio:device1/in_humidityrelative_input
xm132 = /dev/xm132-dev
rtc = /dev/rtc1
pressure = /sys/bus/iio/devices/iio:device*/in_pressure_input
vl53l1x = /dev/vl53l1x-dev
max44009 = /sys/bus/iio/devices/iio:device2/in_illuminance_input

[testCase]
wifi/bt = 1
nfc = 1
sound = 1
rtc = 1
camera = 1
autotest = 0
rgb = 1
relay = 1
sensor = 1

[testCaseList]
testcaselist = wifi/bt rtc relay sound nfc camera rgb sensor autotest
```




