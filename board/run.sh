#!/bin/bash

set -e
IMAGE_NAME='chessbots-control-board'

mkdir -p build/mockbot
mkdir -p build/bots


board_actions() {
  action=$1
  if [[ "serve" = "$action" ]]; then ## serve board app on port 8031
    docker run -ti --volume $(pwd)/:/app -p 8031:8031 "$IMAGE_NAME" flask --app flaskr.flaskr run -p 8031 -h 0.0.0.0 --reload
#    flask_cmd run -p 8031 -h 0.0.0.0 --reload

  elif [[ "run" = "$action" ]]; then ## run board script
#    echo "${@:2}"
    flask_cmd script "${@:2}"

  elif [[ "print" = "$action" ]]; then ## create print images
    rm -rf build/print/
    mkdir -p build/print/
    board_actions run board_print

  elif [[ "debug" = "$action" ]]; then ## run debug script (kinda "tests")
    rm -rf build/bots/ build/mockbot/
    mkdir -p build/bots/ build/mockbot/
    board_actions run mockbot_pictures
     board_actions run test_captcha

  elif [[ "build" = "$action" ]]; then ## run debug script (kinda "tests")
#    docker build -t $IMAGE_NAME --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) --no-cache .
    docker build -t $IMAGE_NAME --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .

  else
    board_actions serve
  fi
}


flask_cmd() {
  docker_run flask --app flaskr.flaskr "$@"
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

board_actions "$@"
