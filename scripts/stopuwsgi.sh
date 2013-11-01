#!/bin/bash

if [ -e "lock/uwsgi.pid" ]; then
echo "Parando serviço de aplicação"
PID=`cat lock/uwsgi.pid`
kill -3 $PID
rm -Rf "lock/uwsgi.pid"
fi