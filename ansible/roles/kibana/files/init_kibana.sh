#!/bin/sh
#
# chkconfig: - 98 02
# description: Starts and stops Kibana Service
#

RUNUSER=elastic
BASEDIR=/opt/bigdata/kibana-6.4.3-linux-x86_64
EXECBIN=${BASEDIR}/bin/kibana
CONF=${BASEDIR}/config/kibana.yml
LOGFILE=${BASEDIR}/logs/kibana.log
PIDFILE=${BASEDIR}/run/kibana.pid
RUNGREP="${BASEDIR}/bin/../node/bin/node"
RUNUID=$(id -u ${RUNUSER})

function check_root(){
  if [ $EUID -ne 0 ] && [ $EUID -ne "${RUNUID}" ]; then
    echo "This script must be run as root or ${RUNUSER}" 1>&2
    exit 1
  fi
}

status(){
  #PID=$(ps aux | grep -w ${RUNGREP} | grep -Ewv 'nohup|grep' | awk '{print $2}' | xargs)
  if [ -f "${PIDFILE}" ]; then
    echo "Kibana Service is running"
    exit 0
  else
    echo "Kibana Service is not running"
    exit 2
  fi
}

start(){
  #PID=$(ps aux | grep -w ${RUNGREP} | grep -Ewv 'nohup|grep' | awk '{print $2}' | xargs)
  if [ -f "${PIDFILE}" ]; then
    echo "Kibana Service is already running"
  else
    echo -n "Starting Kibana Service"
    if [ $EUID -eq "${RUNUID}" ]; then
      nohup ${EXECBIN} >> ${LOGFILE} 2>&1 &
    else
      sudo -u ${RUNUSER} nohup ${EXECBIN} >> ${LOGFILE} 2>&1 &
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
  #PID=$(ps aux | grep -w ${RUNGREP} | grep -Ewv 'nohup|grep' | awk '{print $2}' | xargs)
  if [ ! -f "${PIDFILE}" ]; then
    echo "Kibana Service is aready stopped"
  else
    echo -n "Stopping Kibana Service"
	PID=$(cat ${PIDFILE} | xargs)
    kill -TERM ${PID}
    rm ${PIDFILE}
    attempt=1
    while true
    do
      if [ -f "${PIDFILE}" ]; then
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
