#!/bin/bash

#Script para startar uma instancia do uwsgi

UWSGI=`which uwsgi`
CURRENT_PATH=`pwd`
PORT="8944"
echo "Iniciando a instancia de aplicação saude"

if [ ! -d "log" ]; then
    mkdir "log"
fi

if [ ! -d "lock" ]; then
    mkdir "lock"
fi


if [ -e "lock/uwsgi.pid" ]; then
    PID=`cat "lock/uwsgi.pid"`

    if [ -e /proc/$PID/cmdline ]; then
        echo "Já esta em execução";
        exit 1;
    fi

fi

uwsgi -s 127.0.0.1:$PORT -M 4 -t 30 -A 4 -p 4 -d log/uwsgi.log --pythonpath $CURRENT_PATH --module supportcenter.wsgi --pidfile lock/uwsgi.pid --harakiri 120
