#!/usr/bin/env python
### Pump_control.py ###

import sys
import os
import shutil
import csv
import time
import datetime
import ConfigParser

sys.path.append(os.getcwd())
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

#from config import *
from config import *
from log import *
from time import *
from timestring import *

Tformat = "%H:%M:%S"
Dformat = "%Y-%m-%d"

from datetime import datetime
from datetime import timedelta
Zeit = datetime.now()
Zeitformat = "%Y-%m-%d %H:%M:%S"
logZF = "%d.%m.%Y-%H:%M:%S"

sh = os.system
dat  = sorted([fn for fn in os.listdir(LOG_DIR) if any([fn.endswith('.dat')])])
last_dat = str(LOG_DIR+max(dat))

####################################################################################################################################
def prepare_first_pump():                  ###
    a = 0
    while a != 3:
        if os.path.isfile(Pzustand) is False:
            sh(Poff)
            write_zustand(Pzustand, 0)
        elif os.path.isfile(Pzustand) is True:
            if os.path.isfile(Ventilzustand) is False:
                write_zustand(Vzustand, 0)
            if os.path.isfile(Ventilzustand) is True:    
                a = 3

def show_plf():
    file1 = last_dat[:-4]+'.plf'
    f1 = open(file1, "rb")
    reader = csv.reader(f1, delimiter=" ")
    an = False
    aus = False
    init = False
    erg = timedelta(seconds=0)
    for row in reader:
        if row[1] == 'an':
            init = True
            aus = False
            if not an:
               an = True
               counter1 = strptime(row[0],logZF)
               counter3 = strptime(row[0],logZF)
            else:
               counter3 = strptime(row[0],logZF)  
        elif row[1] == 'aus':
            an = False
            if not aus:
               aus = True
               if init: 
                    counter2 = datetime.fromtimestamp(mktime(strptime(row[0],logZF))) - datetime.fromtimestamp(mktime(counter1))
                    erg = erg + counter2
        elif row[1] == 'manuell':
            init = True
            aus = False
            if not an:
                an = True
                counter1 = strptime(row[0],logZF)
                counter3 = strptime(row[0],logZF)
            else:
                counter3 = strptime(row[0],logZF)
    
    if an:
        counter2 = datetime.fromtimestamp(mktime(counter3)) - datetime.fromtimestamp(mktime(counter1))
        erg = erg + counter2
    f1.close()
    return erg 

def PZmind():                     ###
    if Pmulti == 'Sekunden':
        PZmind = timedelta(seconds=Pmin)
    elif Pmulti == 'Minuten':
        PZmind = timedelta(minutes=Pmin)
    elif Pmulti == 'Stunden':
        PZmind = timedelta(hours=Pmin)
    else:
        print " "
        print " Falsche(unbekannte) Zeiteinheit fuer Pmulti...!!!!" 
        print "     Pmulti='Stunden' ['Minuten'['Sekunden']]"
        PZmind = timedelta()
    return PZmind

def Pumpe(n):                 ###
    n = int(n)
    if n == 1:
        if read_file(Pzustand) == "0":
            print "Pumpe wird jetzt eingeschaltet !!!"
            sh(Pon)
            write_zustand(Pzustand, 1)
            
    elif n == 0:
        if read_file(Pzustand) == "1":
            print "Pumpe wird jetzt ausgeschaltet !!!"
            sh(Poff)
            write_zustand(Pzustand, 0)

    elif n > 1:
        while n > 0:
            if n > 1:
                print "ii - noch %s Einschalt-Wiederholungen" % (n)
            if n == 1:
                print "ii - noch %s Einschalt-Wiederholung" % (n)
            sh(Pon)
            sleep(1)
            n -= 1
        write_zustand(Pzustand, 1)

####################################################################################################################################
if read_file(Controlzustand) == '0':
    import tempsensoren as TS
    TS.sensorcheck()

tmp = RAM_DIR+"Sensoren.tmp"
tmp_last = RAM_DIR+"Sensoren_last.tmp"

if os.path.isfile(tmp) is False:
    import tempsensoren as TS
    stemp1 = TS.stemp1(Faktor)
    stemp2 = TS.stemp2(Faktor)
    stemp3 = TS.stemp3(Faktor)

elif os.path.isfile(tmp) is True:
    conf = ConfigParser.ConfigParser()
    conf.read(tmp)
    stemp1 = float(conf.get("sensors", "temp1"))
    stemp2 = float(conf.get("sensors", "temp2"))
    stemp3 = float(conf.get("sensors", "temp3"))

if os.path.isfile(tmp_last) is False:
    last_temp1 = stemp1
    last_temp2 = stemp2
    last_temp3 = stemp3

elif os.path.isfile(tmp_last) is True:
    conf = ConfigParser.ConfigParser()
    conf.read(tmp_last)
    last_temp1 = float(conf.get("sensors", "temp1"))
    last_temp2 = float(conf.get("sensors", "temp2"))
    last_temp3 = float(conf.get("sensors", "temp3"))

PerrTemp = errorTemp/20
errLmP = last_temp1 - stemp1
errPmL = stemp1 - last_temp1

####################################################################################################################################
def Schalter():
    init = False
    rPump = int(read_file(Pzustand))
    rVZst = int(read_file(Vzustand))
    print "ii - PumpenSchalter"
    print "-------------------"
    if rPump != 0:                # Pumpzustand steht nicht  auf 0
        init = True
    if rPump == 0:                # Pumpzustand steht auf 0
        init = False

    if PZon >= Zeit:                    ### ...Zeit vor Beginn.
        if rPump != 0:                # Pumpzustand steht nicht auf 0
            Pumpe(0)
        print "Es ist Ruhezeit !!! (Morgenmodus)"
        init = False

    if PZoff <= Zeit:                 ### ...Zeit nach Ende.
        if rPump != 0:                # Pumpzustand steht nicht  auf 0
            Pumpe(0)
        print "Es ist Ruhezeit !!! (Abendmodus)"
        init = False

    if PZon <= Zeit:                  ### Pumpe ist im Zeitrahmen an
      if PZoff >= Zeit:                 ###
        if rVZst != 0:                    # Ventil steht nicht komplett auf zirkulieren.
            if rPump == 0:                # Pumpzustand steht  auf 0
                Pumpe(1)
                print "rPump=0 Beginn Pumpzeit seit %s ...jetzt %s" % (PZon, Zeit)
                init = True
            elif rPump != 0:
                if errLmP >= PerrTemp:
                    print "ii - Es muss einen Fehler beim Einschalten der Pumpe gegeben haben."
                    print "ii - Einschalten wird %s mal wiederholt." % (PumpErr)
                    Pumpe(PumpErr)
                    init = True
            else:                         # Pumpzustand steht  auf 1
                init = True

        if rVZst == 0:                  # Ventil steht auf zirkulieren
            if PZgelaufen < PZmind:               # Pumpe ist weniger gelaufen, als sie muss
                if PZrest <= Zeit:                ### Restlaufzeit der Pumpe
                    Pumpe(1)
                    print "Pumpe befindet sich in der Restlaufzeit."
                    init = False                  # sorgt fuer eine Wiederholung des Einschaltbefehls
            elif rPump != 0:
                Pumpe(0)
                print "Pumpe aus..."
                init = False
            
    if init == True:
        print "ii - Pumpe ist an."

    elif init != True:
        if PZgelaufen < PZmind:               # Pumpe ist weniger gelaufen, als sie muss
            if PZrest <= Zeit:                ### Restlaufzeit der Pumpe
                if PZoff >= Zeit:             ### ...Zeit vor Ende.
                    Pumpe(1)
                    print "Beginn Pumpzeit (zum Ende) von %s bis %s" % (PZrest, PZoff)
        else:
            print "ii - Pumpe ist aus."

prepare_first_pump()

##########################################################################################################################################
PZon    = datetime.strptime(str(Date(PZon)), Zeitformat)
PZoff   = datetime.strptime(str(Date(PZoff)), Zeitformat)
PZmind = PZmind()
#########################################################
PZgelaufen = show_plf()
PZmuss     = timedelta(seconds=0)
PZrest     = timedelta(seconds=0)
if PZmind > PZgelaufen:
    PZmuss = PZmind - PZgelaufen
    PZrest = PZoff - PZmuss
Pump_must = PZon + PZmuss
Pump_do = Zeit + PZmuss

##########################################################################################################################################
def Time_print():                  ###
    print "PZon  ", PZon
    print "PZoff ", PZoff
    print "----------------------------------------------------------------------------------------- "
    print " Es ist jetzt.                             (Zeit):" , Zeit.strftime(Zeitformat)
    print "----------------------------------------------------------------------------------------- "
    print " Zeit,die die Pumpe laufen muss.         (PZmind):" , PZmind
    print " Pumpe muss teoretisch an sein bis... (Pump_must):" , Pump_must
    print " Pumpe muesste jetzt noch an sein bis...(Pump_do):" , str(Pump_do)[:-7]   #Pump_do #.strftime(Zeitformat)
    print " Pumpe ist so lang gelaufen.         (PZgelaufen):" , PZgelaufen
    print " Pumpe muss JETZT einschalten            (PZrest):" , PZrest
    print " Pumpe muss noch so lang laufen.         (PZmuss):" , PZmuss
#    print " Pumpe ist schon so lang an.           (PZlaufen):" , PZlaufen
    print " Pumpenzustand                    (read_Pzustand):" , read_file(Pzustand)
    print " Ventilzustand                    (read_Vzustand):" , read_file(Vzustand)
    print "----------------------------------------------------------------------------------------- "
    print " "

def main():
    Time_print()
    Schalter()
    return 0

if __name__=="__main__":
    main()
