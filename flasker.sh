#!/bin/bash

[ -z "$1" ] && echo "usage: $0 <action>" && exit 1

PIDFILE=".flask.pid"

case "$1" in
run)
    PID=$(cat $PIDFILE)
    if [ -n "$PID" ]; then
        echo "PID file found. Is Flask running with PID $PID?"
        exit 0
    fi
    echo "Running Flask server..."
    flask run >flask.log 2>&1 &
    echo $! >"$PIDFILE"
    echo "Flask running with PID $(cat $PIDFILE)"
    ;;
stop)
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        echo "Stopping Flask server with PID $PID"
        kill $PID
        rm "$PIDFILE"
    else
        echo "No PID file found. Is Flask running?"
    fi
    ;;
*)
    echo "I don't know how to $1 a Flask server"
    exit 1
    ;;
esac
