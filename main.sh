#!/bin/bash

# Colors
YELLOW='\e[33m'
NC='\e[0m' # No Color

# Constants

WARN="${YELLOW}WARN: ${NC}"

# Directories
BIN_DIR=./env/bin

source_func() {
  source "$BIN_DIR/activate"
}

env() {
  python3 -m venv env
}

check_env() {
  if [ ! -f "$BIN_DIR/activate" ]; then
    echo -e "${WARN}Creating environment"
    env
  fi
}

check_source() {
  check_env
  if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${WARN}Source environment"
    source_func
  fi
}

check_install() {
  check_source
  if [ ! -f "$BIN_DIR/pytest" ]; then
    echo -e "${WARN}Installation not detected (using pytest as source of truth)"
    install
  fi
}

install() {
  check_source
  pip3 install -r requirements.txt 
}

test_project() {
  check_source
  for i in "${@:2}"
    do
      params="$params $i"
    done
    pytest $params
}

run() {
  check_install
  python3 app
}

case $1 in

  run)
    run
    ;;

  test)
    test_project
    ;;

  install)
    install
    ;;

  env)
    env
    ;;

  activate)
    source_func
    ;;

  *)
    echo -e "${WARN}unknown command\n"
    ;;
esac