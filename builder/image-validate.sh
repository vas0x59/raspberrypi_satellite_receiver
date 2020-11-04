#! /usr/bin/env bash

set -ex

cd /home/pi/catkin_ws/src/clover/builder/test/
./test.sh

echo "Move /etc/ld.so.preload back to its original position"
mv /etc/ld.so.preload.disabled-for-build /etc/ld.so.preload

