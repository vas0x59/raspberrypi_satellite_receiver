#! /usr/bin/env bash

set -e

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




echo_stamp "Write RaspberryPI satellite receiver Image information"

# RSR image version
echo "$1" >> /etc/rsr_version
# Origin image file name
echo "${2%.*}" >> /etc/rsr_origin

echo_stamp "Write magic script to /etc/rc.local"
MAGIC_SCRIPT="sudo /root/init_rpi.sh; sudo sed -i '/sudo \\\/root\\\/init_rpi.sh/d' /etc/rc.local && sudo reboot"
sed -i "19a${MAGIC_SCRIPT}" /etc/rc.local

# It needs for autosizer.sh & maybe that is correct
echo_stamp "Change boot partition"
sed -i 's/root=[^ ]*/root=\/dev\/mmcblk0p2/' /boot/cmdline.txt
sed -i 's/.*  \/boot           vfat    defaults          0       2$/\/dev\/mmcblk0p1  \/boot           vfat    defaults          0       2/' /etc/fstab
sed -i 's/.*  \/               ext4    defaults,noatime  0       1$/\/dev\/mmcblk0p2  \/               ext4    defaults,noatime  0       1/' /etc/fstab

echo_stamp "Set max space for syslogs"
# https://unix.stackexchange.com/questions/139513/how-to-clear-journalctl
sed -i 's/#SystemMaxUse=/SystemMaxUse=200M/' /etc/systemd/journald.conf

# echo_stamp "Move /etc/ld.so.preload out of the way"
# mv /etc/ld.so.preload /etc/ld.so.preload.disabled-for-build

echo_stamp "End of init image"


