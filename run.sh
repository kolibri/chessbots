#!/bin/bash

set -e
IMAGE_NAME='chessbots'
BOT_TTY=/dev/ttyUSB0
BOT_BAUD=115200

mkdir -p build/mockbot
mkdir -p build/bots

run_action() {
  action=$1
  if [[ "run" = "$action" ]]; then ## run default or command
    docker_run ${@:2}
  elif [[ "venv" = "$action" ]]; then ## run default or command
    python3 -m venv .

  elif [[ "board" = "$action" ]]; then ## run board command
    board_actions "${@:2}"
  elif [[ "bot" = "$action" ]]; then ## run bot command
    bot_actions "${@:2}"

  elif [[ "build" = "$action" ]]; then ## docker container
    docker build -t $IMAGE_NAME --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
#    docker build -t $IMAGE_NAME .

  elif [[ "help" = "$action" ]]; then ## displays help
    fn=$(basename "$0")
    echo "## Available targets:"
    grep -E 'if\s.*##' $fn | sed 's/.*"\(.*\)" = "$action".*## \(.*\)$/\1: \2/g'
  else
    run_action help
  fi
}

board_actions() {
  action=$1
  if [[ "serve" = "$action" ]]; then ## serve board on port 8031
    docker run -ti --volume $(pwd)/:/app -p 8031:8031 "$IMAGE_NAME" flask --app chessbots.board.flaskr run -p 8031 -h 0.0.0.0 --reload
#    flask_cmd run -p 8031 -h 0.0.0.0 --reload

  elif [[ "run" = "$action" ]]; then ## serve board on port 8031
    flask_cmd script "${@:2}"

  elif [[ "print" = "$action" ]]; then ## serve board on port 8031
    rm -rf build/print/
    mkdir -p build/print/
    board_actions run board_print

  elif [[ "debug" = "$action" ]]; then ## serve board on port 8031
    rm -rf build/bots/ build/mockbot/
    mkdir -p build/bots/ build/mockbot/
    board_actions run mockbot_pictures
     board_actions run test_captcha

  else
    board_actions serve
  fi
}

run_ampy () {
  docker_bot_run ampy --port $BOT_TTY -b$BOT_BAUD "$@"
}

bot_actions() {
  action=$1
    if [[ "erase" = "$action" ]]; then
    echo "Will erase now"
    docker_bot_run esptool.py --port $BOT_TTY erase_flash
  elif [[ "flash" = "$action" ]]; then
    echo "Will flash now"
    docker_bot_run esptool.py --chip esp32 --port $BOT_TTY --baud 460800 write_flash -z 0x1000 bot/micropython_esp32_camera_firmware.bin

    echo "Is the ground pin disconnected from io0 and usb cable replugged? "
#    read -p "Is the ground pin disconnected from io0 and usb cable replugged? " -n 1 -r
  elif [[ "upip" = "$action" ]]; then
    run_ampy put bot/config.py
    run_ampy run bot/install.py
  elif [[ "reset" = "$action" ]]; then
    echo "Will reset now"
    run_ampy reset
  elif [[ "copy" = "$action" ]]; then
    echo "Will copy now"
    run_ampy put bot/config.py
    run_ampy put bot/boot.py
    #run_ampy put bot/main.py
    run_ampy ls

  elif [[ "repl" = "$action" ]]; then
    echo "Will repl now"
    sudo picocom $BOT_TTY -b115200
  else
    echo "erase or flash"
    exit 1
  fi
}


flask_cmd() {
  docker_run flask --app chessbots.board.flaskr "$@"
}


docker_run() {
    set -x
    docker run -ti --volume `pwd`/:/app "$IMAGE_NAME" "$@"
    set +x
}

docker_bot_run() {
    set -x
    docker run -ti --user root --volume `pwd`/:/app --device "$BOT_TTY:$BOT_TTY" "$IMAGE_NAME" "$@"
    set +x
}

run_action "$@"
