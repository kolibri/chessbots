#!/bin/bash

set -e

frontend_actions() {
  action=$1
  if [[ "dev" = "$action" ]]; then ## run default or command
    npm run start
  elif [[ "build" = "$action" ]]; then ## run default or command
    npm run build
    cp -r ./build/* ../board/flaskr/public/
    #mv ./frontend/build/static/js/main*.js ./flaskr/public/dashboard.js
  else
    echo "No valid frontent action"
  fi
}

frontend_actions "$@"
