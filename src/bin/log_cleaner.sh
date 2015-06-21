#! /bin/bash

dir=${0::-17}
conf="config.py"

source $dir$conf


case "$1" in
  LogClean)
    echo "ii - Alte Logfiles werden entfernt."
    find $RAM_DIR${LOG_DIR:8} -mtime +6 -exec rm {} \;

  PC-LogBackup)
    echo "ii - Altes APP-Log wurde entfernt."
    find $RAM_DIR${LOG_DIR2:8} -mtime +6 -exec rm {} \;

