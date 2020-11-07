#! /usr/bin/env bash

set -e

cd /home/pi/raspberrypi_satellite_receiver/builder/tests/
./test.sh
cd /home/pi
# echo "Move /etc/ld.so.preload back to its original position"
# mv /etc/ld.so.preload.disabled-for-build /etc/ld.so.preload

