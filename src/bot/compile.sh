#!/bin/bash
# copied ./arduino15/packages into ./packages
# currently no way to move installation of packages outside of arduino ide
# seems to be hardcoded to dotfiles

set -x

mkdir -p `pwd`/build
mkdir -p `pwd`/cache
rm -rf `pwd`/build/*
rm -rf `pwd`/cache/*

#arduino-builder \
#  -compile \
#  -logger=machine \
#  -hardware /usr/share/arduino/hardware \
#  -hardware ./packages \
#  -tools ./packages \
#  -libraries ./external_libs \
#  -libraries ./libs \
#  -fqbn=esp8266:esp8266:nodemcuv2:CpuFrequency=80,VTable=flash,FlashSize=4M1M,LwIPVariant=v2mss536,Debug=Disabled,DebugLevel=None____,FlashErase=none,UploadSpeed=115200 \
#  -ide-version=10805 \
#  -build-path `pwd`/build \
#  -warnings=none \
#  -build-cache `pwd`/cache \
#  -prefs=build.warn_data_percentage=75 \
#  -prefs=runtime.tools.esptool.path=./packages/esp8266/tools/esptool/0.4.13 \
#  -prefs=runtime.tools.mkspiffs.path=./packages/esp8266/tools/mkspiffs/0.2.0 \
#  -prefs=runtime.tools.xtensa-lx106-elf-gcc.path=./packages/esp8266/tools/xtensa-lx106-elf-gcc/1.20.0-26-gb404fb9-2 \
#  bot.ino
#  -verbose \

/usr/share/arduino/arduino-builder \
 -compile \
 -logger=machine \
 -hardware /usr/share/arduino/hardware \
 -hardware /home/ko/.arduino15/packages \
 -tools /usr/share/arduino/tools-builder \
 -tools /home/ko/.arduino15/packages \
 -libraries /home/ko/Arduino/libraries \
 -fqbn=esp8266:esp8266:generic:xtal=80,vt=flash,exception=legacy,ssl=all,ResetMethod=nodemcu,CrystalFreq=26,FlashFreq=40,FlashMode=dout,eesz=1M64,led=2,sdk=nonosdk_190703,ip=lm2f,dbg=Disabled,lvl=None____,wipe=none,baud=115200 \
 -ide-version=10809 \
 -build-path ./build \
 -warnings=none \
 -build-cache ./cache \
 -prefs=build.warn_data_percentage=75 \
 -prefs=runtime.tools.mkspiffs.path=/home/ko/.arduino15/packages/esp8266/tools/mkspiffs/2.5.0-4-b40a506 \
 -prefs=runtime.tools.mkspiffs-2.5.0-4-b40a506.path=/home/ko/.arduino15/packages/esp8266/tools/mkspiffs/2.5.0-4-b40a506 \
 -prefs=runtime.tools.mklittlefs.path=/home/ko/.arduino15/packages/esp8266/tools/mklittlefs/2.5.0-4-69bd9e6 \
 -prefs=runtime.tools.mklittlefs-2.5.0-4-69bd9e6.path=/home/ko/.arduino15/packages/esp8266/tools/mklittlefs/2.5.0-4-69bd9e6 \
 -prefs=runtime.tools.xtensa-lx106-elf-gcc.path=/home/ko/.arduino15/packages/esp8266/tools/xtensa-lx106-elf-gcc/2.5.0-4-b40a506 \
 -prefs=runtime.tools.xtensa-lx106-elf-gcc-2.5.0-4-b40a506.path=/home/ko/.arduino15/packages/esp8266/tools/xtensa-lx106-elf-gcc/2.5.0-4-b40a506 \
 -prefs=runtime.tools.python3.path=/home/ko/.arduino15/packages/esp8266/tools/python3/3.7.2-post1 \
 -prefs=runtime.tools.python3-3.7.2-post1.path=/home/ko/.arduino15/packages/esp8266/tools/python3/3.7.2-post1 \
 -verbose ./bot.ino

set +x
