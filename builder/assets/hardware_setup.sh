#! /usr/bin/env bash

set -e # Exit immidiately on non-zero result

echo_stamp() {
  # TEMPLATE: echo_stamp <TEXT> <TYPE>
  # TYPE: SUCCESS, ERROR, INFO

  # More info there https://www.shellhacks.com/ru/bash-colors/

  TEXT="$(date '+[%Y-%m-%d %H:%M:%S]') $1"
  TEXT="\e[1m$TEXT\e[0m" # BOLD

  case "$2" in
    SUCCESS)
    TEXT="\e[32m${TEXT}\e[0m";; # GREEN
    ERROR)
    TEXT="\e[31m${TEXT}\e[0m";; # RED
    *)
    TEXT="\e[34m${TEXT}\e[0m";; # BLUE
  esac
  echo -e ${TEXT}
}

##################################################
# Configure hardware interfaces
##################################################

# 1. Enable sshd
echo_stamp "Turn on sshd"
touch /boot/ssh
# /usr/bin/raspi-config nonint do_ssh 0

# 6. Enable hardware UART
echo_stamp "Turn on UART"
# Temporary solution
# https://github.com/RPi-Distro/raspi-config/pull/75
/usr/bin/raspi-config nonint do_serial 1
/usr/bin/raspi-config nonint set_config_var enable_uart 1 /boot/config.txt
/usr/bin/raspi-config nonint set_config_var dtoverlay pi3-disable-bt /boot/config.txt
systemctl disable hciuart.service

# After adding to Raspbian OS
# https://github.com/RPi-Distro/raspi-config/commit/d6d9ecc0d9cbe4aaa9744ae733b9cb239e79c116
#/usr/bin/raspi-config nonint do_serial 2

# 7. Enable V4L driver http://robocraft.ru/blog/electronics/3158.html
#echo "bcm2835-v4l2" >> /etc/modules
# echo_stamp "#7 Turn on v4l2 driver"
# if ! grep -q "^bcm2835-v4l2" /etc/modules;
# then printf "bcm2835-v4l2\n" >> /etc/modules
# fi

echo_stamp "End of configure hardware interfaces"