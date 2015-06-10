#!/usr/bin/env python

import sys, os, time, shutil, threading, unittest

sys.path.append(os.getcwd())

from config import *
from bin.tempsensoren import sensorcheck as sensorcheck

##########################################################################################################################################
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
##########################################################################################################################################
def write_Control__Zustand(on_off):
    k = Controlzustand
    control = open(k,"w")
    control.write(on_off)
    control.close()

def main():
    print "=============================================================================================================================="
    print "==============================================================================================================================" 
    sys.stdout = Logger(LOG)
    write_Control__Zustand("2")
    sensorcheck()
    a = 0
    while a == 0: 
      print "....lade Modul zum Manuell schalten..."
      import bin.manuell as M
      M.manuell_check()
      print "....lade Modul Ventil_control..."
      import bin.Ventil_control as VC
      print "....lade Modul Pump_control..."
      import bin.Pump_control as PC
      print "....lade Modul Temp_protokoll..."
      import bin.Temp_protokoll as TP
      print "============================="
      print "= Temp_Protokoll startet... ="
      print "============================="

      if M.read_manuell() != "0":
        print "<<< Pumpe ist auf manuell gestellt. >>>"
        if TP.main() == 0 and int(PC.read_Pzustand()) == 1:
            print "<<< manuell + VC >>>"
            VC.main()
            a = 1
        elif TP.main() == 0 and int(PC.read_Pzustand()) == 0:
            print "<<< manuell >>>"
            a = 1
      elif M.read_manuell() == "0":
        print "<<< Pumpe ist auf automatik gestellt. >>>"
        if TP.main() == 0:
          #time.sleep(1)
          print "============================="
          print "= Ventil_control startet... ="
          print "============================="

          if VC.main() == 0:
            #time.sleep(1)
            print "============================="
            print "=  Pump_control startet...  ="
            print "============================="
            PC.main()
            a = 1

    #time.sleep(1)
    write_Control__Zustand("0")
    print " "
    print "======================"
    print "= Durchlauf beendet. ="
    print "======================"

if __name__=="__main__":
    main()
