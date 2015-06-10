#!/usr/bin/env python
### Pump_control.py ###

import sys
import os
import shutil
import threading
import unittest
import csv
import time
import datetime

sys.path.append(os.getcwd())
#from config_test import *
from config import *
from time import *
from timestring import *
#import time as T
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

def prepare_first():                  ###
    a = 0
    while a != 3:
        if os.path.isfile(Pzustand) is False:
            sh(Poff)
            write_Pzustand(0)
        elif os.path.isfile(Pzustand) is True:
            if os.path.isfile(Ventilzustand) is False:
                read_Vzustand = '0'
            a = 3

def show_plf():
    file1 = str(LOG_DIR+max(dat))[:-4]+'.plf'
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
        #erg = str(erg)[:-7]
    f1.close()
    return erg 
         
def write_Pzustand(OnOff):         ###
    k = Pzustand
    q = str(OnOff)
    control = open(k,"w")
    control.write(q)
    control.close()

def read_Vzustand():              ###
    v = Ventilzustand
    fobj_in = open(v,"r")
    for line in fobj_in:
        inhalt = line
    fobj_in.close()
    return inhalt
            
def read_Pzustand():              ###
    x = Pzustand
    pfobj_in = open(x,"r")
    for line in pfobj_in:
        inhalt = line
    pfobj_in.close()
    return inhalt

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
    if n == "1":
          if read_Pzustand() == "0":
            print "Pumpe wird jetzt eingeschaltet !!!"
          sh(Pon)
          #sleep(1)
          #sh(Pon)
          #sleep(1)
          #sh(Pon)
          write_Pzustand(1)
            
    if n == "0":
          print "Pumpe wird jetzt ausgeschaltet !!!"
          sh(Poff)
          #sleep(1)
          #sh(Poff)
          #sleep(1)
          #sh(Poff)
          write_Pzustand(0)

def Schalter():
    init = False
    rPump = int(read_Pzustand())
    rVZst = int(read_Vzustand())
    print "ii - PumpenSchalter"
    print "-------------------"
    if PZon >= Zeit:                    ### ...Zeit vor Beginn.
        if rPump != 0:                # Pumpzustand steht nicht auf 0
            Pumpe("0")
        print "1... Es ist Ruhezeit !!!"
        init = False
    elif PZoff <= Zeit:                 ### ...Zeit nach Ende.
        if rPump != 0:                # Pumpzustand steht nicht  auf 0
            Pumpe("0")
        print "2... Es ist Ruhezeit !!!"
        init = False
    elif PZon <= Zeit:                  ### Pumpe ist im Zeitrahmen an
      if PZoff >= Zeit:                 ###
        if rVZst != 0:                    # Ventil steht nicht komplett auf zirkulieren.
            if rPump == 0:                # Pumpzustand steht  auf 0
                Pumpe("1")
                print "rPump=0 Beginn Pumpzeit seit %s ...jetzt %s" % (PZon, Zeit)
                init = True
            else:                         # Pumpzustand steht  auf 1
                init = True
        elif rVZst == 0:                  # Ventil steht auf zirkulieren
            if PZgelaufen < PZmind:               # Pumpe ist weniger gelaufen, als sie muss
                if PZrest <= Zeit:                ### Restlaufzeit der Pumpe
                    Pumpe("1")
                    print "Pumpe befindet sich in der Restlaufzeit."
                    init = False                  # sorgt fuer eine Wiederholung des Einschaltbefehls
            elif rPump != 0:
                Pumpe("0")
                print "Pumpe aus..."
                init = False
    if init == False:
        if PZgelaufen < PZmind:               # Pumpe ist weniger gelaufen, als sie muss
            if PZrest <= Zeit:                ### Restlaufzeit der Pumpe
                if PZoff >= Zeit:
                    Pumpe("1")
                    print "Beginn Pumpzeit (zum Ende) um %s bis %s" % (PZrest, PZoff)
        else:
            print "ii - Pumpe ist schon aus."
    if init == True:
        print "ii - Pumpe ist schon an."

prepare_first()
##########################################################################################################################################
PZon    = datetime.strptime(str(Date(PZon)), Zeitformat)
PZoff   = datetime.strptime(str(Date(PZoff)), Zeitformat)
PZmind = PZmind()
#########################################################
#PZgelaufen = timedelta(seconds=int(read_Pzeit()))
#PZgelaufen = datetime.fromtimestamp(float(str(show_plf())),'%H:%M:%S')
PZgelaufen = show_plf()
PZmuss     = timedelta(seconds=0)
PZrest     = timedelta(seconds=0)
#Pump_must  = timedelta(seconds=0)
#Pump_do    = timedelta(seconds=0)
if PZmind > PZgelaufen:
    PZmuss = PZmind - PZgelaufen
#if PZoff > PZmuss:
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
    print " Pumpenzustand                    (read_Pzustand):" , read_Pzustand()
    print " Ventilzustand                    (read_Vzustand):" , read_Vzustand()
    print "----------------------------------------------------------------------------------------- "
    print " "

def main():
    #write_Ptmp(0)
    Time_print()
    Schalter()
    #Time_print()
    return 0

if __name__=="__main__":
    main()
