#!/bin/bash

./packages/esp8266/tools/esptool/0.4.13/esptool \
    -vv \
    -cd \
    nodemcu \
    -cb \
    115200 \
    -cp \
    /dev/ttyUSB0 \
    -ca \
    0x00000 \
    -cf \
    `pwd`/build/chessbot.ino.bin \


