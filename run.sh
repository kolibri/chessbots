#!/bin/bash

set -e
IMAGE_NAME='chessbots'

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
    flask_cmd run -p 8031 -h 0.0.0.0 --reload

  elif [[ "run" = "$action" ]]; then ## serve board on port 8031
    flask_cmd script "${@:2}"

  elif [[ "build" = "$action" ]]; then ## serve board on port 8031
    rm -rf build/bots/ build/mockbot/
    mkdir -p build/bots/ build/mockbot/
    board_actions run mockbot_pictures
    board_actions run test_captcha_to_txt


  else
    board_actions serve
  fi
}

bot_actions() {
  action=$1

}

flask_cmd() {
  docker_run flask --app chessbots.board.flaskr "$@"
}


docker_run() {
    set -x
    docker run -ti --volume `pwd`/:/app -p 8031:8031 "$IMAGE_NAME" "$@"
    set +x
}

run_action "$@"
