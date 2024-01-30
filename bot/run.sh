#!/bin/bash

set -e

IMAGE_NAME='chessbots-bot'

BOT_TTY=/dev/ttyUSB0
BAUD=115200
sudo chown ko:users $BOT_TTY


bot_action () {
  ACTION=$1
  if [[ "run" = "$ACTION" ]]; then
    docker_run "${@:2}"

  elif [[ "erase" = "$ACTION" ]]; then
   esptool erase_flash

  elif [[ "flash" = "$ACTION" ]]; then
   esptool write_flash -z 0x1000 micropython_esp32_camera_firmware.bin

  elif [[ "upip" = $ACTION ]]; then
    run_ampy put config.py
    run_ampy run install.py

  elif [[ "copy" = $ACTION ]]; then
    run_ampy put config.py
    run_ampy put mcp23017.py
    run_ampy put boot.py

  elif [[ "reset" = $ACTION ]]; then
    run_ampy reset


  elif [[ "repl" = $ACTION ]]; then
    picocom $BOT_TTY -b115200


#  elif [[ "compile" = "$ACTION" ]]; then
#   docker run -ti --volume `pwd`/:/app "$IMAGE_NAME" arduino-cli compile --dump-profile --fqbn esp32:esp32:esp32cam --build-path ./build chessbot

#  elif [[ "upload" = "$ACTION" ]]; then 
#    echo "upload"
#   docker run -ti --volume `pwd`/:/app --device "$BOT_TTY:$BOT_TTY" "$IMAGE_NAME" arduino-cli upload -p $BOT_TTY --input-dir ./build --fqbn esp32:esp32:esp32cam chessbot

#  elif [[ "repl" = "$ACTION" ]]; then
#    echo "Will repl now"
#    sudo picocom $BOT_TTY -b115200
  elif [[ "build" = "$ACTION" ]]; then
    docker build -t $IMAGE_NAME --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
  elif [[ "build-noc" = "$ACTION" ]]; then
    docker build -t $IMAGE_NAME --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) --no-cache .
  else
    echo "no command"
    exit 1
  fi
}

docker_run() {
    set -x
    docker run -ti --volume `pwd`/:/app --device "$BOT_TTY:$BOT_TTY" "$IMAGE_NAME" "$@"
    set +x
}

esptool() {
  docker_run esptool.py --chip esp32 --port $BOT_TTY "$@"
}

run_ampy () {
  docker_run ampy --port $BOT_TTY -b$BAUD "$@"
}

bot_action "$@"


