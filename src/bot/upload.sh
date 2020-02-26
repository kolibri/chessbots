#!/bin/bash

if [ -z "$DEVICE" ]; then
	echo "Target device not set. Specify it now, or recall with env-var DEVICE set."
	read DEVICE
fi

echo $DEVICE

#DEVICE=/dev/ttyUSB0






#./packages/esp8266/tools/esptool/0.4.13/esptool \
# -cd nodemcu \
# -cb 115200 \
# -ca 0x00000 \
# -cf ./build/bot.ino.bin \
# -cp $DEVICE
