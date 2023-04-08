#!/bin/bash

set -e

run_action() {
  action=$1
  if [[ "board" = "$action" ]]; then
    cd ./board && ./run.sh "${@:2}"
  elif [[ "bot" = "$action" ]]; then
    cd ./bot && ./run.sh "${@:2}"
  elif [[ "frontend" = "$action" ]]; then
    cd ./frontend && ./run.sh "${@:2}"


  elif [[ "help" = "$action" ]]; then ## displays help
    fn=$(basename "$0")
    echo "## Available targets:"
    grep -E 'if\s.*##' $fn | sed 's/.*"\(.*\)" = "$action".*## \(.*\)$/\1: \2/g'
  else
    run_action help
  fi
}


docker_run() {
    set -x
    docker run -ti --volume `pwd`/:/app "$IMAGE_NAME" "$@"
    set +x
}


run_action "$@"
