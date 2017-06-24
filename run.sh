#!/usr/bin/env bash

debug='false'

while getopts 'd' flag; do
  case "${flag}" in
    d) debug='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done

if [ "`ps -edaf | grep mongo | grep -v grep &> /dev/null`" == 0 ]; then
   mongod #start db deamon
fi

if $debug; then
    export FLASK_DEBUG=1
else
    export FLASK_DEBUG=0
fi

./app.py