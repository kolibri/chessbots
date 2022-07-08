#!/bin/bash

set -e

DEV_PATH=/dev/ttyUSB0
BAUD=115200
sudo chown ko $DEV_PATH

run_ampy () {
  ampy --port $DEV_PATH -b$BAUD $@
}

run_action () {
  ACTION=$1
  if [[ "erase" = $ACTION ]]; then
    echo "Will erase now"

    esptool.py --port $DEV_PATH erase_flash
  elif [[ "flash" = $ACTION ]]; then
    echo "Will flash now"
    esptool.py --chip esp32 --port $DEV_PATH --baud 460800 write_flash -z 0x1000 micropython_esp32_camera_firmware.bin

    read -p "Is the ground pin disconnected from io0 and usb cable replugged? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
#      run_action reset
      run_action upip
    fi
  elif [[ "upip" = $ACTION ]]; then
    run_ampy put src/config.py
    run_ampy run src/install.py
  elif [[ "reset" = $ACTION ]]; then
    echo "Will reset now"
    run_ampy reset
  elif [[ "copy" = $ACTION ]]; then
    echo "Will copy now"
    run_ampy put src/config.py
    run_ampy put src/boot.py
    #run_ampy put src/main.py
    run_ampy ls

  elif [[ "repl" = $ACTION ]]; then
    echo "Will repl now"
    picocom $DEV_PATH -b115200
  else
    echo "erase or flash"
    exit 1
  fi
}

run_action $@


