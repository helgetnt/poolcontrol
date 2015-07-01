#!/usr/bin/env python

import time
Ftime = time.time()

import sys, os, shutil
sys.path.append(os.getcwd())

from config import *
import bin.log as DataLog
tmp_last = RAM_DIR+"Sensoren_last.tmp"

Datum = time.strftime("%d.%m.%Y")                      # Datumsstempel 
Zeit = time.strftime("%H:%M:%S")                       # Zeitstempel
logfile = time.strftime("%Y-%m-%d.dat")                # Name der Logdatei
plogfile = time.strftime("%Y-%m-%d.plf")               # Pumpen-Logdatei
vlogfile = time.strftime("%Y-%m-%d.vlf")               # Ventil-Logdatei
refillfile = time.strftime("%Y-%m-%d.rf")              # Refill-Logdatei
pclog = time.strftime("%Y-%m-%d.log")                  # Poolcontrol-Logdatei
log = LOG_DIR
log2 = LOG_DIR2
ftp = FTP_DIR
ftp2 = FTP_DIR2

#from bin.log import *

##########################################################################################################################################
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

##########################################################################################################################################
def main():
    #print "=============================================================================================================================="
    #print "=============================================================================================================================="
    #a = 0    
    #while a == 0:
    #    if os.path.isfile(Controlzustand) is True:
    #        if read_file(Controlzustand) != "0":
    #            time.sleep(15)
    #            print "WW - Poolcontrol ist derzeit aktiv"
    #            print "ii - Warte 15 sec."
    #        elif read_file(Controlzustand) == "0":
    #            print "ii - Poolcontrol wird gestartet"
                #time.sleep(2)
    #            a = 1
    DataLog.write_Control__Zustand("1")
    DataLog.log_clean()
    DataLog.prepare_first(log2, pclog)
    sys.stdout = Logger(log2+pclog)
    print "=============================================================================================================================="
    print "=============================================================================================================================="
    print Datum, ' - ', Zeit
    print "======================"
    print "=....Prepare First...="
    DataLog.prepare_first(log, logfile)
    DataLog.prepare_first(log, plogfile)
    DataLog.prepare_first(log, vlogfile)
    print "======================"
    from bin.tempsensoren import tmp
    if os.path.isfile(tmp) is True:
        print "letzte Temps werden gesichert."
        shutil.copyfile(tmp, tmp_last)
    a = 0
    while a == 0:
      print "....lade Modul Temperatursensoren..."
      import bin.tempsensoren as TS
      if TS.main() == 0:
            print "....lade Module zum Manuell schalten..."
            import bin.manuell as M
            M.manuell_check()
            import bin.refill as R
            R.refill_check()
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
                if R.read_refill() == "0":
                    print "<<< Pool ist im Normalbetrieb. >>>"
                    if TP.main() == 0:
                        if int(DataLog.read_file(Pzustand)) != 0:
                            print "<<< manuell + VC >>>"
                            print "============================="
                            print "= Ventil_control startet... ="
                            print "============================="
                            VC.main()
                            a = 1
                        else:
                            print "<<< manuell >>>"
                            a = 1
                elif R.read_refill() != "0":
                    print "<<< Pool wird derzeit nachgefuellt. >>>"
                    TP.main()
                    DataLog.refill_log()
                    a = 1
            elif M.read_manuell() == "0":
                print "<<< Pumpe ist auf automatik gestellt. >>>"
                if TP.main() == 0:
                    print "============================="
                    print "= Ventil_control startet... ="
                    print "============================="
                    if VC.main() == 0:
                        print "============================="
                        print "=  Pump_control startet...  ="
                        print "============================="
                        PC.main()
                        a = 1

    print "====================="
    print "=....Prepare Last...="
    print "====================="
    DataLog.pumplog()
    DataLog.prepare_last(log, plogfile)
    DataLog.ventillog()
    DataLog.prepare_last(log, vlogfile)
    DataLog.prepare_last(log, logfile)

    x = log+refillfile
    if os.path.isfile(x) is True:
        DataLog.prepare_last(log, refillfile)

    DataLog.write_Control__Zustand("0")
    import time
    Ltime = time.time()
    RunTime = Ltime - Ftime
    print " "
    print "========================================="
    print " Durchlauf wurde in %s sec. beendet. " % (round(RunTime))
    print "========================================="


if __name__=="__main__":
    main()
