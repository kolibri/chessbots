#!/bin/bash

set -e

run_action () { ## run with $ ./run.sh +
  APP=$1
  if [[ "board" = $APP ]]; then ## 'board' actions:
    ACTION=$2
    if [[ "run" == $ACTION ]]; then ## 'run' command
      run_cmd board flask script ${@:3}
    elif [[ "test" == $ACTION ]]; then ## 'test' o_O
      run_cmd board pytest ${@:3}
    elif [[ "up" == $ACTION ]]; then ## start'up' webserver
      docker-compose up -d board
    else
      echo "targets: run, up, test"
    fi

  elif [[ "build" = $APP ]]; then ## build container
    docker-compose build ${@:2}

  elif [[ "help" = $APP ]]; then ## this 'help' command
    # todo. do the fancy sed help thing...
    #fgrep -h "##" $0 | fgrep -v fgrep | sed -e "s/\\$$//' | sed -e 's/(.*)##//"
    echo "Help"
  else
    echo "There was no action to perform."
    echo "Maybe, this will help you consider, what you want to perform"

    run_action help
    exit 1
  fi
}

run_cmd () {
#    docker-compose run $@
    docker-compose run --rm --user "$(id -u):$(id -g)" $@

}

time run_action $@
#sudo chown ko:ko -R ./
