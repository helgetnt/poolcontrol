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
    control = Controlzustand
    if os.path.isfile(control) is False:
        pc = open(control,"a")
        pc.write("0")
        pc.close
        check = "0"

    elif os.path.isfile(control) is True:
        fobj_in = open(control,"r")
        for line in fobj_in:
            check = line
        fobj_in.close()
    return check

def check_poolcontrol():
    c = read_poolcontrol()
    a = 0
    while a != 1:
        read_poolcontrol()
        if c != '0':
            print "Poolcontrol ist derzeit aktiv. Warte 10sec......"    # ...zum testen
            sleep(10)
        elif c == '0':
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
        print "Logfile wurde komplettiert !!!"                          # ...zum testen
        

def prepare_first():
    x = log+logfile
    y = ftp+logfile
    a = 0
    if os.path.isdir(log) is False:
        os.mkdir(log)
        b = open(log+logfile,"a")
        b.close()
        print "LOG_DIR & Logfile wurden erstellt !!!"                   # ...zum testen   

    if os.path.isfile(log+logfile) is False:
        b = open(log+logfile,"a")
        b.close()
        print "Logfile wurde erstellt !!!"                              # ...zum testen  

    if ftp != "":
     if os.path.isfile(ftp+logfile) == False:
       shutil.copyfile(x, y)

     while a == 0:
       if os.path.isdir(ftp) == False:
          a = 0
       elif os.path.isdir(ftp) == True:
          a = 1
          if os.path.isfile(y) is True:
            while a == 1:
              if os.path.getsize(y) > os.path.getsize(x):
                shutil.copyfile(y, x)
                print "ftp -cp-> log"                                   # ...zum testen
              elif os.path.getsize(y) == os.path.getsize(x):
                a = 2

def prepare_last():
    x = log+logfile
    y = ftp+logfile
    a = 0
    while a == 0:
        if os.path.isfile(y) is True:
            a = 1
            while a == 1:
              if os.path.getsize(x) > os.path.getsize(y):
                shutil.copyfile(x, y)
                print "log -cp-> ftp"                                   # ...zum testen
              elif os.path.getsize(x) == os.path.getsize(y):
                a = 2

##########################################################################################################################################
def main():
    write_Control__Zustand("3")
    printLog()
    return 0



if __name__=="__main__":
    main()

