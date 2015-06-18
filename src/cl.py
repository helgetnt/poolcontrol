#!/usr/bin/env python

import sys, os, time, shutil, threading, unittest
sys.path.append(os.getcwd())

from config import *

Datum = time.strftime("%d.%m.%Y")                      # Datumsstempel 
Zeit = time.strftime("%H:%M:%S")                       # Zeitstempel
logfile = time.strftime("%Y-%m-%d.dat")                # Name der Logdatei
plogfile = time.strftime("%Y-%m-%d.plf")               # Pumpen-Logdatei
vlogfile = time.strftime("%Y-%m-%d.vlf")               # Ventil-Logdatei
refillfile = time.strftime("%Y-%m-%d.rf")               # Refill-Logdatei
global log
global ftp
global ftp2
log = LOG_DIR
ftp = FTP_DIR
ftp2 = FTP_DIR2

##########################################################################################################################################
def file_remove(file):
    while os.listdir(log):
        for f in os.listdir(log):
            f = f[:-4]
    return f

##########################################################################################################################################
def main():

    print " "
    print "==========================================="
    print "= Viel Arbeit vor dir noch liegt..... !!! ="
    print "==========================================="
    print " "


if __name__=="__main__":
    main()
