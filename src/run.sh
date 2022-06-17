#!/bin/bash

set -e

helptext () {
  echo "# ./run.sh board up        # runs board flask app"
  echo "# ./run.sh board run cmd   # runs board flask command"
  echo "# ./run.sh docker-build    # build containers with args"
}

run_action () {
  APP=$1
  if [[ "board" = $APP ]]; then
    ACTION=$2
    if [[ "run" == $ACTION ]]; then
      time run_board_cmd flask script ${@:3}
    elif [[ "test" == $ACTION ]]; then
      time run_board_cmd pytest
      docker-compose up -d board
    elif [[ "up" == $ACTION ]]; then
      docker-compose up -d board
    else
      echo "targets: run, up"
    fi

  elif [[ "docker-build" = $APP ]]; then
    docker-compose build ${@:2}

  elif [[ "help" = $APP ]]; then
    helptext
  else
    echo "There was no action to perform."
    echo "Maybe, this will help you consider, what you want to perform"

    helptext
    exit 1
  fi
}

run_board_cmd () {
    docker-compose run board $@
}

run_action $@