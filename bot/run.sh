#!/bin/bash

set -e

IMAGE_NAME='chessbots-bot'

BOT_TTY=/dev/ttyUSB0
#BAUD=115200
#sudo chown ko $DEV_PATH


bot_action () {
  ACTION=$1
  if [[ "run" = "$ACTION" ]]; then
    docker_run "${@:2}"

  elif [[ "compile" = "$ACTION" ]]; then
   docker run -ti --volume `pwd`/:/app "$IMAGE_NAME" arduino-cli compile --dump-profile --fqbn esp32:esp32:esp32cam --build-path ./build chessbot

  elif [[ "upload" = "$ACTION" ]]; then
    echo "upload"
   docker run -ti --volume `pwd`/:/app --device "$BOT_TTY:$BOT_TTY" "$IMAGE_NAME" arduino-cli upload -p $BOT_TTY --input-dir ./build --fqbn esp32:esp32:esp32cam chessbot

  elif [[ "repl" = "$ACTION" ]]; then
    echo "Will repl now"
    sudo picocom $BOT_TTY -b115200
  elif [[ "build" = "$ACTION" ]]; then
#    docker build -t $IMAGE_NAME --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) --no-cache .
    docker build -t $IMAGE_NAME --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
  else
    echo "erase or flash"
    exit 1
  fi
}

docker_run() {
    set -x
    docker run -ti --volume `pwd`/:/app --device "$BOT_TTY:$BOT_TTY" "$IMAGE_NAME" "$@"
    set +x
}
bot_action "$@"


