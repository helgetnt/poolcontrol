#!/usr/bin/env python

import sys, os, time, shutil, threading, unittest

sys.path.append(os.getcwd())
from config import *

#from optparse import OptionParser 
#parser = OptionParser()

#Zeit = datetime.now()
#Zeitformat = "%Y-%m-%d %H:%M:%S"
#sh = os.system
##########################################################################################################################################

##########################################################################################################################################
def read_manuell():
    j = Pool_manuell 
    mfobj_in = open(j,"r")
    for line in mfobj_in:
        inhalt = line
    mfobj_in.close()
    return inhalt

def write_manuell(lq):         ###
    k = Pool_manuell
    q = str(lq)
    control = open(k,"w")
    control.write(q)
    control.close()

def manuell_check():
    a = 0
    while a == 0:
        if os.path.isfile(Pool_manuell) is False:
            robj_out = open(Pool_manuell,"w")
            robj_out.write("0")
            robj_out.close()
            man = 0
            a = 1
        elif os.path.isfile(Pool_manuell) is True:
            man = read_manuell()
            a = 1
    return man

def main():
    manuell_check()
    for arg in sys.argv[1:]:
        if arg == "0":
           write_manuell("0")
        elif arg == "1":
            write_manuell("1")
    if manuell_check() == "0":
        S = "Automatik"
    if manuell_check() == "1":
        S = "Manuell"
    print "ii - Pool ist derzeit auf %s gestellt." % S

if __name__=="__main__":
    main()