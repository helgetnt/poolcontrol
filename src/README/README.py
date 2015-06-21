#!/usr/bin/env python

import sys, os, time, shutil, threading, unittest

sys.path.append(os.getcwd())
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

##########################################################################################################################################
# sys.path.append(DIR)      >>> Moeglichkeit    >>> import file[ in DIR]
# DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ""))         >>>   /Verzeichnis des akt. Scriptes
# DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))       >>> ../Verzeichnis des akt. Scriptes
##########################################################################################################################################
def main():


    print " "
    print "==========================================="
    print "= Viel Arbeit vor dir noch liegt..... !!! ="
    print "==========================================="
    print " "


if __name__=="__main__":
    main()
