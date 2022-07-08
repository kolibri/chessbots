#!/bin/bash

set -e

helptext () {
  echo "# ./run.sh board up        # run board flask app"
  echo "# ./run.sh board run cmd   # run board flask command"
  echo "# ./run.sh board test      # run board tests"
  echo "# ./run.sh docker-build    # build containers with args"
}

run_action () {
  APP=$1
  if [[ "board" = $APP ]]; then
    ACTION=$2
    if [[ "run" == $ACTION ]]; then
      time run_cmd board flask script ${@:3}
    elif [[ "test" == $ACTION ]]; then
      time run_cmd board pytest
    elif [[ "up" == $ACTION ]]; then
      docker-compose up -d board
    else
      echo "targets: run, up, test"
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

run_cmd () {
    docker-compose run $@
}

run_action $@