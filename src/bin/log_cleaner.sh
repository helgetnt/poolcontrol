#! /bin/bash

dir=${0::-18}
conf="config.py"

source $dir$conf


case "$1" in
  test)
    echo ""
    echo "$dir$conf"
    echo "$dir"
    echo ""
    ;;
  LogClean)
    echo "ii - Alte Logfiles werden entfernt."
    find $RAM_DIR${LOG_DIR:8} -mtime +6 -exec rm {} \;
    ;;
  PC-LogBackup)
    echo "ii - Altes APP-Log wurde entfernt."
    find $RAM_DIR${LOG_DIR2:8} -mtime +6 -exec rm {} \;
    ;;
 *)
    echo "------------------------------------------------------------------------"
    echo "Optionen: LogClean | PC-LogBackup | test" >&2
    echo "------------------------------------------------------------------------"
    echo "LogClean        |entfernt alle Dateien die älter als eine Woche sind"
    echo "                |aus -> $RAM_DIR${LOG_DIR:8}"
    echo ""
    echo "PC-LogBackup    |entfernt alle Dateien die älter als eine Woche sind"
    echo "                |aus -> $RAM_DIR${LOG_DIR2:8}"
    echo ""
    echo "test            |echo -> Config & Config_dir"
    exit 3
    ;;
esac
