#!/bin/bash

arduino-builder \
  -dump-prefs \
  -logger=machine \
  -hardware /usr/share/arduino/hardware \
  -hardware ./packages \
  -tools ./packages \
  -libraries ./libs \
  -fqbn=esp8266:esp8266:nodemcuv2:CpuFrequency=80,VTable=flash,FlashSize=4M1M,LwIPVariant=v2mss536,Debug=Disabled,DebugLevel=None____,FlashErase=none,UploadSpeed=115200 \
  -ide-version=10805 \
  -build-path `pwd`/build \
  -warnings=none \
  -build-cache `pwd` cache \
  -prefs=build.warn_data_percentage=75 \
  -prefs=runtime.tools.esptool.path=./packages/esp8266/tools/esptool/0.4.13 \
  -prefs=runtime.tools.mkspiffs.path=./packages/esp8266/tools/mkspiffs/0.2.0 \
  -prefs=runtime.tools.xtensa-lx106-elf-gcc.path=./packages/esp8266/tools/xtensa-lx106-elf-gcc/1.20.0-26-gb404fb9-2 \
  chessbot.ino
#  -verbose \


arduino-builder \
  -compile \
  -logger=machine \
  -hardware /usr/share/arduino/hardware \
  -hardware ./packages \
  -tools ./packages \
  -libraries ./libs \
  -fqbn=esp8266:esp8266:nodemcuv2:CpuFrequency=80,VTable=flash,FlashSize=4M1M,LwIPVariant=v2mss536,Debug=Disabled,DebugLevel=None____,FlashErase=none,UploadSpeed=115200 \
  -ide-version=10805 \
  -build-path `pwd`/build \
  -warnings=none \
  -build-cache `pwd`/cache \
  -prefs=build.warn_data_percentage=75 \
  -prefs=runtime.tools.esptool.path=./packages/esp8266/tools/esptool/0.4.13 \
  -prefs=runtime.tools.mkspiffs.path=./packages/esp8266/tools/mkspiffs/0.2.0 \
  -prefs=runtime.tools.xtensa-lx106-elf-gcc.path=./packages/esp8266/tools/xtensa-lx106-elf-gcc/1.20.0-26-gb404fb9-2 \
  chessbot.ino
#  -verbose \
