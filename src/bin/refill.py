#!/usr/bin/env python

import sys, os, time, shutil

sys.path.append(os.getcwd())
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from config import *

##########################################################################################################################################
def read_refill():
    j = Pool_refill
    mfobj_in = open(j,"r")
    for line in mfobj_in:
        inhalt = line
    mfobj_in.close()
    return inhalt

def write_refill(lq):         ###
    k = Pool_refill
    q = str(lq)
    control = open(k,"w")
    control.write(q)
    control.close()

def refill_check():
    a = 0
    while a == 0:
        if os.path.isfile(Pool_refill) is False:
            robj_out = open(Pool_refill,"w")
            robj_out.write("0")
            robj_out.close()
            man = 0
            a = 1
        elif os.path.isfile(Pool_refill) is True:
            man = read_refill()
            a = 1
    return man

def main():
    import manuell as M
    refill_check()
    for arg in sys.argv[1:]:
        if arg == "0":
            write_refill("0")
            M.write_manuell("0")
        elif arg == "1":
            write_refill("1")
            M.write_manuell("1")
    if refill_check() == "0":
        S = "Pool ist im Normalbetrieb."
    if refill_check() == "1":
        S = "Pool wird derzeit nachgefuellt."
    print "ii -  %s" % S

if __name__=="__main__":
    main()
