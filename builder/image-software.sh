#! /usr/bin/env bash


set -e # Exit immidiately on non-zero result

REPO_DIR="/mnt"

echo_stamp() {
  # TEMPLATE: echo_stamp <TEXT> <TYPE>
  # TYPE: SUCCESS, ERROR, INFO

  # More info there https://www.shellhacks.com/ru/bash-colors/

  TEXT="$(date '+[%Y-%m-%d %H:%M:%S]') $1"
  TEXT="\e[1m${TEXT}\e[0m" # BOLD

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

# https://gist.github.com/letmaik/caa0f6cc4375cbfcc1ff26bd4530c2a3
# https://github.com/travis-ci/travis-build/blob/master/lib/travis/build/templates/header.sh
my_travis_retry() {
  local result=0
  local count=1
  while [ $count -le 3 ]; do
    [ $result -ne 0 ] && {
      echo -e "\n${ANSI_RED}The command \"$@\" failed. Retrying, $count of 3.${ANSI_RESET}\n" >&2
    }
    # ! { } ignores set -e, see https://stackoverflow.com/a/4073372
    ! { "$@"; result=$?; }
    [ $result -eq 0 ] && break
    count=$(($count + 1))
    sleep 1
  done

  [ $count -gt 3 ] && {
    echo -e "\n${ANSI_RED}The command \"$@\" failed 3 times.${ANSI_RESET}\n" >&2
  }

  return $result
}


echo_stamp "Move /etc/ld.so.preload out of the way"
mv /etc/ld.so.preload /etc/ld.so.preload.disabled-for-build

echo_stamp "Update apt cache"
apt-get update -qq

echo_stamp "Software installing"
apt-get install -y \
cmake build-essential python-pip libusb-1.0 libusb-1.0-0-dev \
python3 python3-dev python3-numpy python3-pip git \
sox libatlas-base-dev \
&& echo_stamp "Everything was installed!" "SUCCESS" \
|| (echo_stamp "Some packages wasn't installed!" "ERROR"; exit 1)

### Install RTL-SDR
if [ -e /usr/local/bin/rtl_fm ]; then
    echo_stamp "rtl-sdr was already installed"
else
    echo_stamp "Installing rtl-sdr from osmocom..."
    # cd /tmp/
    git clone https://github.com/osmocom/rtl-sdr.git
    cd rtl-sdr/
    mkdir build
    cd build
    cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
    make
    sudo make install
    sudo ldconfig
    cd ../../
    cp ./rtl-sdr/rtl-sdr.rules /etc/udev/rules.d/
    echo_stamp "rtl-sdr install done" "SUCCESS"
fi
echo_stamp "Install wxtoimg"
dpkg -i "${REPO_DIR}/third_party/wxtoimg-armhf-2.11.2-beta.deb"
wxtoimg <<< YES
echo_stamp "wxtoimg: $(wxtoimg -- help)"

echo_stamp "Install python libs"
my_travis_retry pip3 install pandas pyorbital ephem tweepy Pillow

echo_stamp "Install nodejs"

curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs
echo_stamp "node.js version: $(node --version)" "SUCCESS"


echo_stamp "Change owner to pi"
chown -Rf pi:pi /home/pi/rpi_satellite_receiver/

echo_stamp "End of software installation"

