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





