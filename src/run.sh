#!/bin/bash

set -e

helptext () {
  echo "# ./run.sh board-run   # runs flask app"
  echo "# ./run.sh board-clean # removes json caches"
  echo "# ./run.sh ocv-detect  # run image detection"
  echo "# ./run.sh ocv-crop    # crops test images"

  echo "# ./run.sh cmd service command # run command in docker compose container"
  echo "# ./run.sh docker-build        # build containers with args"
  echo "# run with CMD_DOCKER=false to run commands not in container."
}

run_action () {
  ACTION=$1

  if [[ "cmd" = $ACTION ]]
  then
    run_compose_cmd ${@:2}

  elif [[ "board-run" = $ACTION ]]
  then
    cd ./board && FLASK_APP=flaskr flask run -p 8031 --reload

  elif [[ "board-clean" = $ACTION ]]
  then
    rm -rf ./board/flaskr/bot_cache/*

  elif [[ "ocv-detect" = $ACTION ]]
  then
    run_compose_cmd ocv python detect_position.py ${@:2}

  elif [[ "ocv-crop" = $ACTION ]]
  then
    run_compose_cmd ocv python crop_testboard.py ${@:2}

  elif [[ "docker-build" = $ACTION ]]; then
    docker-compose build ${@:2}

  elif [[ "help" = $ACTION ]]; then
    helptext
  else
    echo "There was no action to perform."
    echo "Maybe, this will help you consider, what you want to perform"

    helptext
    exit 1
  fi
}

run_compose_cmd () {
    docker-compose run $@
}

run_action $@