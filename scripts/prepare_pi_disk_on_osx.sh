#!/bin/sh

set -e

source "`dirname "$0"`/../.env"

if [ $# -lt 1 ]
then
  echo "Check for your USB stick, and call the script with the device name!"
  echo "example: $0 disk42"
  echo 
  diskutil list
  exit 1
fi

set -x

IMG_PATH=./raspbian_lite_latest.img

if [ ! -f $IMG_PATH ]
then
    ZIP_PATH=./raspbian_lite_latest.zip
    ZIP_URL="https://downloads.raspberrypi.org/raspbian_lite_latest"
    if [ ! -f $ZIP_PATH ]
    then
        curl -L -o $ZIP_PATH $ZIP_URL
    fi
    unzip -p $ZIP_PATH \*.img | cat > $IMG_PATH
fi

if [ $# -eq 1 ]
then
    diskutil unmountDisk /dev/$1
    sudo dd if=$IMG_PATH of=/dev/r$1 bs=1m
    sleep 10 # wait for image mount
    touch /Volumes/boot/ssh

    if [ -n $WIFI_NAME -a -n $WIFI_PASS ]
    then
        (cat <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={
    ssid="$WIFI_NAME"
    psk="$WIFI_PASS"
}
EOF
    ) > /Volumes/boot/wpa_supplicant.conf
    fi
fi
set +xe
