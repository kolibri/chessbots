#!/bin/bash

DEVICE=/dev/ttyUSB0

./packages/esp8266/tools/esptool/0.4.13/esptool -cd nodemcu -cb 115200 -ca 0x00000 -cf ./build/chessbot.ino.bin -cp $DEVICE