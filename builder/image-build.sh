#! /usr/bin/env bash

set -e # Exit immidiately on non-zero result
# source img-tool
SOURCE_IMAGE="https://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2020-02-14/2020-02-13-raspbian-buster-lite.zip"

export DEBIAN_FRONTEND=${DEBIAN_FRONTEND:='noninteractive'}
export LANG=${LANG:='C.UTF-8'}
export LC_ALL=${LC_ALL:='C.UTF-8'}


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

REPO_DIR="/mnt"
SCRIPTS_DIR="${REPO_DIR}/builder"
IMAGES_DIR="${REPO_DIR}/images"

[[ ! -d ${SCRIPTS_DIR} ]] && (echo_stamp "Directory ${SCRIPTS_DIR} doesn't exist" "ERROR"; exit 1)
[[ ! -d ${IMAGES_DIR} ]] && mkdir ${IMAGES_DIR} && echo_stamp "Directory ${IMAGES_DIR} was created successful" "SUCCESS"
[[ ! -d ${CONFIG_DIR} ]] && mkdir ${CONFIG_DIR} && echo_stamp "Directory ${CONFIG_DIR} was created successful" "SUCCESS"

if [[ -z ${TRAVIS_TAG} ]]; then IMAGE_VERSION="$(cd ${REPO_DIR}; git log --format=%h -1)"; else IMAGE_VERSION="${TRAVIS_TAG}"; fi

REPO_URL="$(cd ${REPO_DIR}; git remote --verbose | grep origin | grep fetch | cut -f2 | cut -d' ' -f1 | sed 's/git@github\.com\:/https\:\/\/github.com\//')"
REPO_NAME="$(basename -s '.git' ${REPO_URL})"
echo_stamp "REPO_NAME=${REPO_NAME}" "INFO"
IMAGE_NAME="${REPO_NAME}_${IMAGE_VERSION}.img"
echo_stamp "IMAGE_NAME=${IMAGE_NAME}" "INFO"
IMAGE_PATH="${IMAGES_DIR}/${IMAGE_NAME}"
echo_stamp "IMAGE_PATH=${IMAGE_PATH}" "INFO"

# get_image() {
#   # TEMPLATE: get_image <IMAGE_PATH> <RPI_DONWLOAD_URL>
#   local BUILD_DIR=$(dirname $1)
#   local RPI_ZIP_NAME=$(basename $2)
#   local RPI_IMAGE_NAME=$(echo ${RPI_ZIP_NAME} | sed 's/zip/img/')

#   if [ ! -e "${BUILD_DIR}/${RPI_ZIP_NAME}" ]; then
#     echo_stamp "Downloading original Linux distribution"
#     wget --progress=dot:giga -O ${BUILD_DIR}/${RPI_ZIP_NAME} $2
#     echo_stamp "Downloading complete" "SUCCESS" \
#   else echo_stamp "Linux distribution already donwloaded"; fi

#   echo_stamp "Unzipping Linux distribution image" \
#   && unzip -p ${BUILD_DIR}/${RPI_ZIP_NAME} ${RPI_IMAGE_NAME} > $1 \
#   && echo_stamp "Unzipping complete" "SUCCESS" \
#   || (echo_stamp "Unzipping was failed!" "ERROR"; exit 1)
# }

# get_image ${IMAGE_PATH} ${SOURCE_IMAGE}
img-tool ${IMAGE_PATH} load ${SOURCE_IMAGE}

# img-resize ${IMAGE_PATH} max '6G'
img-tool ${IMAGE_PATH} size 6000000000

if [[ ! -z ${TRAVIS_TAG} ]]; then
  cd ${REPO_DIR}
  REMOTE_BRANCH="$(git branch -r --contains ${TRAVIS_TAG} | sed -n 1p | cut -d ' ' -f 5)"
  BRANCH="$(echo ${REMOTE_BRANCH} | cut -d '/' -f 2)"
  echo_stamp "Checkout to ${REMOTE_BRANCH} from ${TRAVIS_TAG}" "INFO"
  git branch ${BRANCH} ${REMOTE_BRANCH}
  git checkout ${BRANCH}
  cd /
fi

shopt -s dotglob

echo_stamp "Mount loop-image: ${IMAGE_PATH}"
DEV_IMAGE=$(losetup -Pf ${IMAGE_PATH} --show)
sleep 0.5

MOUNT_POINT=$(mktemp -d --suffix=.builder_image)
echo_stamp "Mount dirs ${MOUNT_POINT} & ${MOUNT_POINT}/boot"
mount "${DEV_IMAGE}p2" ${MOUNT_POINT}
mount "${DEV_IMAGE}p1" ${MOUNT_POINT}/boot

mkdir -p ${MOUNT_POINT}'/home/pi/raspberrypi_satellite_receiver/'
for dir in ${REPO_DIR}/*; do
  if [[ $dir != *"images" && $dir != *"imgcache" ]]; then
    cp -r $dir ${MOUNT_POINT}'/home/pi/raspberrypi_satellite_receiver/'$(basename $dir)
  fi;
done

umount -fR ${MOUNT_POINT}
losetup -d ${DEV_IMAGE}


img-tool ${IMAGE_PATH} copy ${SCRIPTS_DIR}'/assets/init_rpi.sh' '/root/'
img-tool ${IMAGE_PATH} copy ${SCRIPTS_DIR}'/assets/hardware_setup.sh' '/root/'

echo_stamp "image-init.sh"
img-tool ${IMAGE_PATH} exec ${SCRIPTS_DIR}'/image-init.sh' ${IMAGE_VERSION} ${SOURCE_IMAGE} \
&& echo_stamp "Init - OK" "SUCCESS" \
|| (echo_stamp "Init - ERROR" "ERROR"; exit 1)

echo_stamp "image-software.sh"
img-tool ${IMAGE_PATH} exec ${SCRIPTS_DIR}'/image-software.sh' \
&& echo_stamp "Software - OK" "SUCCESS" \
|| (echo_stamp "Software - ERROR" "ERROR"; exit 1)

echo_stamp "image-network.sh"
img-tool ${IMAGE_PATH} exec ${SCRIPTS_DIR}'/image-network.sh' \
&& echo_stamp "Network config - OK" "SUCCESS" \
|| (echo_stamp "Network config - ERROR" "ERROR"; exit 1)

echo_stamp "image-validate.sh"
img-tool ${IMAGE_PATH} exec ${SCRIPTS_DIR}'/image-validate.sh' \
&& echo_stamp "validate - OK" "SUCCESS" \
|| (echo_stamp "validate - ERROR" "ERROR"; exit 1)

img-tool ${IMAGE_PATH} size $(img-tool ${IMAGE_PATH} size | grep "IMG_MIN_SIZE" | cut -b 15-)

echo_stamp "DONE"