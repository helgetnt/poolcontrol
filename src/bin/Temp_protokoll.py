#!/usr/bin/env python 

import sys, os, time, shutil
import ConfigParser

sys.path.append(os.getcwd())
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from config import *
from log import *

from time import *
lt = localtime()
Datum = strftime("%d.%m.%Y")            # Datumsstempel 
Zeit = strftime("%H:%M:%S")             # Zeitstempel
logfile = strftime("%Y-%m-%d.dat")      # Name der Logdatei
log = LOG_DIR
ftp = FTP_DIR

####################################################################################################################################
def read_poolcontrol():
    if os.path.isfile(Controlzustand) is False:
        pc = open(Controlzustand,"a")
        pc.write("0")
        pc.close
        inhalt = "0"

    elif os.path.isfile(Controlzustand) is True:
        fobj_in = open(Controlzustand,"r")
        for line in fobj_in:
            inhalt = line
        fobj_in.close()
    return inhalt

def check_poolcontrol():
    a = 0
    while a != 1:
        if read_poolcontrol() != '0':
            print "Poolcontrol ist derzeit aktiv. Warte 10sec......"    # ...zum testen
            sleep(10)
        elif read_poolcontrol() == '0':
            print "Poolcontrol ist inaktiv. Starte Job......"           # ...zum testen
        a = 1

####################################################################################################################################
if read_poolcontrol() == 0:
    import tempsensoren as TS
    TS.sensorcheck()

tmp = RAM_DIR+"Sensoren.tmp"
if os.path.isfile(tmp) is False:
    import tempsensoren as TS
    stemp1 = str(TS.stemp1(Faktor))
    stemp2 = str(TS.stemp2(Faktor))
    stemp3 = str(TS.stemp3(Faktor))
if os.path.isfile(tmp) is True:
    conf = ConfigParser.ConfigParser()
    conf.read(tmp)
    stemp1 = conf.get("sensors", "temp1")
    stemp2 = conf.get("sensors", "temp2")
    stemp3 = conf.get("sensors", "temp3")

####################################################################################################################################
def printLog():
        x = log+logfile
        fobj_out = open(x,"a")                                                                          # Logdatei oeffnen
        fobj_out.write(Datum + "-" + Zeit + " " + stemp1 + " " + stemp2 + " " + stemp3 + "\n")          # Daten in Logdatei schreiben
        fobj_out.close()                                                                                # Logdatei schliessen
        print "Logfile wurde komplettiert !!!"                                          # ...zum testen
        
##########################################################################################################################################
def main():
    write_Control__Zustand("3")
    printLog()
    return 0



if __name__=="__main__":
    main()

