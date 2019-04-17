#!/bin/sh

PORT=8000
curr=$(cd `dirname $0`; pwd)

function check_root(){
  if [ $EUID -ne 0 ] && [ $EUID -ne "${RUNUID}" ]; then
    echo "This script must be run as root or ${RUNUSER}" 1>&2
    exit 1
  fi
}

status(){
  PID_NUM=`netstat -nlp | grep $PORT | wc -l`
  if [ $PID_NUM -ne 0 ]; then
    echo "Autodeplpy Service is running"
    exit 0
  else
    echo "Autodeplpy Service is not running"
    exit 2
  fi
}

start(){
  PID_NUM=`netstat -nlp | grep $PORT | wc -l`
  if [ $PID_NUM -ne 0 ]; then
    echo "Autodeplpy Service is already running"
  else
    echo -n "Starting Autodeplpy Service"
    cd $curr
    nohup python manage.py runserver 0:$PORT --insecure &
	attempt=1
	while true
    do
	  PID_NUM=`netstat -nlp | grep $PORT | wc -l`
      if [ $PID_NUM -eq 0 ]; then
        sleep 1
        echo -n "."
        if [ "${attempt}" -eq 30 ]; then
          echo -e "\nFAILED"
          exit 2
        fi
      else
        echo -e "\nOK"
        break
      fi
      attempt=$((${attempt}+1))
    done
  fi
}

stop(){
  PID_NUM=`netstat -nlp | grep $PORT | wc -l`
  if [ $PID_NUM -eq 0 ]; then
    echo "Autodeplpy Service is aready stopped"
  else
    echo -n "Stopping Autodeplpy Service"
	PID=`netstat -nlp | grep 8000 | awk '{print $NF}' | awk -F'/' '{print $1}'`
    kill -TERM ${PID}
    while true
    do
      PID_NUM=`netstat -nlp | grep $PORT | wc -l`
      if [ $PID_NUM -ne 0 ]; then
        sleep 1
        echo -n "."
        if [ "${attempt}" -eq 20 ]; then
          echo -e "\nFAILED"
          exit 2
        fi
      else
        echo -e "\nOK"
        break
      fi
      attempt=$((${attempt}+1))
    done
  fi
}


check_root
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    status)
        status
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart|status}"
        exit 2
esac