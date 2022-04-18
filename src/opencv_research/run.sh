#!/bin/bash

set -e

helptext () {
  echo "# ./run.sh build # run image detection"
  echo "# ./run.sh docker-build"
  echo "# run with CMD_DOCKER=false to run commands not in container."
}

run_action () {
  ACTION=$1

  if [[ "cmd" = $ACTION ]]
  then
    run_cmd ${@:2}

  elif [[ "build" = $ACTION ]]
  then
    run_cmd python detect_position.py ${@:2}

  elif [[ "crop" = $ACTION ]]
  then
    run_cmd python crop_testboard.py ${@:2}

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

CMD_DOCKER="${CMD_DOCKER: true}"

run_cmd () {
  if [ "$CMD_DOCKER" == false ]; then
    (cd ./app && $@)
  else
    docker-compose run app $@
  fi
}

run_action $@