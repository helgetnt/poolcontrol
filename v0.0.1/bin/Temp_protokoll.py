#!/usr/bin/env python 

import sys, os, time, shutil
import ConfigParser

sys.path.append(os.getcwd())
from config import *
#from tempsensoren import TSens as TS

from time import *
lt = localtime()
Datum = strftime("%d.%m.%Y")            # Datumsstempel 
Zeit = strftime("%H:%M:%S")             # Zeitstempel
logfile = strftime("%Y-%m-%d.dat")      # Name der Logdatei
log = LOG_DIR
ftp = FTP_DIR

####################################################################################################################################
#sensorcheck()

#stemp1 = str(stemp1(Faktor_Protokoll))
#stemp2 = str(stemp2(Faktor_Protokoll))
#stemp3 = str(stemp3(Faktor_Protokoll))
####################################################################################################################################
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
        if c != '1':
            print "Poolcontrol ist derzeit aktiv. Warte 20sec......"    # ...zum testen
            sleep(20)
            #print "nochmal testen.........."
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

   ### ...Zeit bis hier rund 30 Sekunden !!! ###
##########################################################################################################################################

def main():
#    if read_poolcontrol == '0':
#        from tempsensoren import sensorcheck  
#        sensorcheck()

    check_poolcontrol()

#    tmp = RAM_DIR+"Sensoren.tmp"
#    if os.path.isfile(tmp) is False:
#        stemp1 = stemp1
#        stemp2 = stemp2
#        stemp3 = stemp3
#    if os.path.isfile(tmp) is True:
#        conf = ConfigParser.ConfigParser()
#        conf.read(tmp)
#        stemp1 = float(conf.get("sensors", "temp1"))
#        stemp2 = float(conf.get("sensors", "temp2"))
#        stemp3 = float(conf.get("sensors", "temp3"))

#    print('Sensor    | Temperatur')			### Zum Testen...
#    print('----------------------')			### Ausgabe
#    print 'Sensor_1 -> ' , stemp1			    ### in
#    print 'Sensor_2 -> ' , stemp2			    ### Terminal
#    print 'Sensor_3 -> ' , stemp3			    ### ...Ende.

    prepare_first()
    printLog()
    prepare_last()
    return 0



if __name__=="__main__":
    main()

