#! /usr/bin/env bash

set -ex

cd /home/pi/rpi_satellite_receiver/builder/test/
./test.sh

echo "Move /etc/ld.so.preload back to its original position"
mv /etc/ld.so.preload.disabled-for-build /etc/ld.so.preload

