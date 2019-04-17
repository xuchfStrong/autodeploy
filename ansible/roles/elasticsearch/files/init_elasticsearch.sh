#!/bin/sh
#
# chkconfig: - 98 02
# description: Starts and stops ElasticSearch Service
#

RUNUSER=elastic
BASEDIR=/opt/bigdata/elasticsearch-6.4.3
EXECBIN=${BASEDIR}/bin/elasticsearch
CONF=${BASEDIR}/config/elasticsearch.yml
PIDFILE=${BASEDIR}/run/elasticsearch.pid
RUNGREP="${BASEDIR}/lib/elasticsearch"
RUNUID=$(id -u ${RUNUSER})

function check_root(){
  if [ $EUID -ne 0 ] && [ $EUID -ne "${RUNUID}" ]; then
    echo "This script must be run as root or ${RUNUSER}" 1>&2
    exit 1
  fi
}

status(){
  if [ -f "${PIDFILE}" ]; then
    echo "ElasticSearch Service is running"
    exit 0
  else
    echo "ElasticSearch Service is not running"
    exit 2
  fi
}

start(){
  if [ -f "${PIDFILE}" ]; then
    echo "ElasticSearch Service is already running"
  else
    echo -n "Starting ElasticSearch Service"
    if [ $EUID -eq "${RUNUID}" ]; then
      ${EXECBIN} -d -p ${PIDFILE}
    else
      sudo -u ${RUNUSER} ${EXECBIN} -d -p ${PIDFILE}
    fi
	attempt=1
	while true
    do
      if [ ! -f "${PIDFILE}" ]; then
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
  if [ ! -f "${PIDFILE}" ]; then
    echo "ElasticSearch Service is aready stopped"
  else
    echo -n "Stopping ElasticSearch Service"
	PID=$(cat ${PIDFILE} | xargs)
    kill -TERM ${PID}
    rm -f ${PIDFILE}
    attempt=1
    while true
    do
      if [ -f "${PIDFILE}" ]; then
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
