#!/bin/bash
# /usr/local/bin/init.sh
DIR=/mnt/disk

function check_and_create_gpio() {
  GPIO_LIST=(32 33 45 54 55)
  GPIO_EXPORT=/sys/class/gpio/export
  for item in ${GPIO_LIST[*]}; do
    gpioValue=/sys/class/gpio/gpio${item}/value
    gpioDirection=/sys/class/gpio/gpio${item}/direction
    if [ ! -f "$gpioValue" ]; then
      echo $item >$GPIO_EXPORT
      echo out >$gpioDirection
      chmod 0666 $gpioValue
      chmod 0666 $gpioDirection
    fi
  done
}

function authorization_test_dev() {
  DEV_LIST=(
    /sys/bus/iio/devices/iio:device1/in_humidityrelative_input
    /sys/bus/iio/devices/iio:device2/in_temp_input
    /sys/bus/iio/devices/iio:device2/in_pressure_input
    /sys/bus/iio/devices/iio:device3/in_temp_input
    /sys/bus/iio/devices/iio:device3/in_pressure_input
    /dev/vl53l1x-dev
    /dev/xm132-dev
    /sys/bus/iio/devices/iio:device2/in_illuminance_input
  )

  for item in ${DEV_LIST[*]}; do
    echo "$item"
    chmod 0777 $item
  done
}

function start_factory_test() {
  # copy FactoryTest
  if [ -e "$DIR/config.ini" ]; then
    cp $DIR/config.ini /tmp/config.ini
    chmod 777 /tmp/config.ini
  fi

  if [ -e "$DIR/FactoryTest" ]; then
    chmod 777 $DIR/FactoryTest
    cp $DIR/FactoryTest /tmp/FactoryTest
    chmod 777 /tmp/FactoryTest
    kill -9 $(ps -ef | grep FactoryTest | awk '$0 !~/grep/ {print $1}')
    kill -9 $(ps -ef | grep stressapptest | awk '$0 !~/grep/ {print $1}')
    #expect /usr/local/bin/init_expect.sh
    su linaro -c "DISPLAY=:0.0 /tmp/FactoryTest"
  fi
}

# 创建测试所需的 GPIO
check_and_create_gpio
# 修改测试节点权限
authorization_test_dev

mkdir $DIR

mount /dev/$1 $DIR

sync
# 开启工厂测试
start_factory_test

umount $DIR
