#!/usr/bin/env python

import sys, os, time, shutil 
sys.path.append(os.getcwd())

from config import *
from bin.log import prepare_last

pclog = time.strftime("%Y-%m-%d.log")                  # Poolcontrol-Logdatei
log2 = LOG_DIR2
sh = os.system
myc = "controller.py"
start = "sudo "+workdir+myc

##########################################################################################################################################
def main():
    sh(start)
    prepare_last(log2, pclog)
    print " "
    print "======================"
    print "= Durchlauf beendet. ="
    print "======================"


if __name__=="__main__":
    main()
