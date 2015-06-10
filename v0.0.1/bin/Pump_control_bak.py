#!/usr/bin/env python
### Pump_control.py ###

import sys, os, shutil, threading, unittest

sys.path.append(os.getcwd())
#from config_test import *
from config import *

from timestring import *
import time as T
Tformat = "%H:%M:%S"
Dformat = "%Y-%m-%d"

from datetime import *
Zeit = datetime.now()
Zeitformat = "%Y-%m-%d %H:%M:%S"
sh = os.system
####################################################################################################################################

def prepare_first():                  ###
    x = Pzeit
    z = Pzustand
    a = 0
    while a != 2:
        if os.path.isfile(x) is False:
            write_Pzeit(0)
        elif os.path.isfile(x) is True:
            a = 1
            while a != 2:
                if os.path.isfile(z) is False:
                    sh(Poff)
                    write_Pzustand(0)
                elif os.path.isfile(z) is True:
                    a = 2

def write_Pzustand(OnOff):         ###
    k = Pzustand
    q = str(OnOff)
    control = open(k,"w")
    control.write(q)
    control.close()

def write_Pzeit(Laufzeit):         ###
    k = Pzeit
    q = str(Laufzeit)
    control = open(k,"w")
    control.write(q)
    control.close()

prepare_first()

def read_Vzustand():              ###
    v = Ventilzustand
    fobj_in = open(v,"r")
    for line in fobj_in:
        inhalt = line
    fobj_in.close()
    return inhalt
            
def read_Pzeit():                 ###
    x = Pzeit
    fobj_in = open(x,"r")
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

def write_Ptmp(pumpON):         ###
    k = P_temp
    q = str(pumpON)
    control = open(k,"w")
    control.write(q)
    control.close()

def read_Ptmp():                 ###
    x = P_temp
    fobj_in = open(x,"r")
    for line in fobj_in:
        inhalt = line
    fobj_in.close()
    return inhalt

def Pcount(key):                   ###
    a = 0
    y = P_temp
    while a != 1:
        if os.path.isfile(y) is False:
           write_Ptmp(0)
        elif os.path.isfile(y) is True:
           a = 1
    ############
    pz = int(read_Pzeit())
    rt = int(round(T.time()))
    if key is True:
        if int(read_Ptmp()) == 0:
            write_Ptmp(rt)

    elif key is False:
        if int(read_Ptmp()) != 0:
            newpz = (rt - int(read_Ptmp())) + pz
            write_Pzeit(int(newpz))

def datecheck():
    t = datetime.fromtimestamp(float(read_Ptmp()))
    a = datetime.fromtimestamp(T.time())
    tf = t.strftime(Dformat)
    af = a.strftime(Dformat)
    if af > tf:
        if int(read_Ptmp()) != 0:
            print "Zeitstempel der Pumpe wird auf 0 gesetzt !!!"
            write_Ptmp(0)

def Pumpe(an):                 ###
    if an == "1":
          #a = str(read_Pzustand())
          #if a != 1:
          print "Pumpe wird jetzt eingeschaltet !!!"
          sh(Pon)
          Pcount(True)
          write_Pzustand(1)
            
    else: print "Pumpe wird jetzt ausgeschaltet."; sh(Poff); Pcount(False); write_Pzustand(0)
          #sh(Poff)
          #Countup_PZon(False)
          #write_Pzustand(0)
        

def Schalter():
    rPZ   = int(read_Pzeit())
    rPump = int(read_Pzustand())
    rVZst = int(read_Vzustand())
    if PZon >= Zeit:                    ### ...Zeit vor Beginn.
        datecheck()
        if rPump != 0:                # Pumpzustand steht nicht auf 0
            Pumpe("0")
        print "1... Es ist Ruhezeit !!!"
    elif PZoff <= Zeit:                 ### ...Zeit nach Ende.
        if rPump != 0:                # Pumpzustand steht nicht  auf 0
            Pumpe("0")
        print "2... Es ist Ruhezeit !!!"

    elif PZon <= Zeit:                  ### Pumpe ist im Zeitrahmen an
      if PZoff >= Zeit:                 ###
        if rVZst != 0:                    # Ventil steht nicht komplett auf zirkulieren.
            if rPZ == 0:                  # Pumpzeit steht auf 0
                Pumpe("1")
                print "Beginn Pumpzeit (CountUP =  %s) seit %s ...jetzt %s" % (rPZ, PZon, Zeit)
            elif rPump == 0:                # Pumpzustand steht  auf 0
                Pumpe("1")
                print "Beginn Pumpzeit (CountUP =  %s) seit %s ...jetzt %s" % (rPZ, PZon, Zeit)
        elif rVZst == 0:                  # Ventil steht auf zirkulieren
            Pumpe("0")
            print "Pumpe aus..."
        elif PZrest <= Zeit:                ### Restlaufzeit der Pumpe
            #if rVZst != 0:
                Pumpe("1")
                print "Beginn Pumpzeit (zum Ende) um %s bis %s" % (PZrest, PZoff)

##########################################################################################################################################
rPZ = int(read_Pzeit())
#########################################################
PZon    = datetime.strptime(str(Date(PZon)), Zeitformat)
PZoff   = datetime.strptime(str(Date(PZoff)), Zeitformat)
PZmind = PZmind()
#########################################################
PZgelaufen = timedelta(seconds=int(read_Pzeit()))
PZmuss     = PZmind - PZgelaufen
PZrest     = PZoff - PZmuss
Pump_must  = PZon + PZmuss
Pump_do    = Zeit + PZmuss
##########################################################################################################################################

def Time_print():                  ###
    PZlaufen = timedelta(seconds=Timecheck())
    PZmuss   = PZmind - PZlaufen
    if PZlaufen > PZmind:
        PZmuss = "Mindestlaufzeit erreicht..."
    print "PZon  ", PZon
    print "PZoff ", PZoff
    print "----------------------------------------------------------------------------------------- "
    print " Zeit,die die Pumpe laufen muss.         (PZmind):" , PZmind
    print " Es ist jetzt.                             (Zeit):" , Zeit.strftime(Zeitformat)
    print " Pumpe muss teoretisch an sein bis... (Pump_must):" , Pump_must
    print " Pumpe muss noch bis an sein.           (Pump_do):" , Pump_do.strftime(Zeitformat)
    print " Pumpe ist so lang gelaufen.         (PZgelaufen):" , PZgelaufen
    print " Pumpe muss JETZT einschalten            (PZrest):" , PZrest
    print " Pumpe muss noch so lang laufen.         (PZmuss):" , PZmuss
    print " Pumpe ist schon so lang an.           (PZlaufen):" , PZlaufen
    print " Pumpenzustand                    (read_Pzustand):" , read_Pzustand()
    print " Ventilzustand                    (read_Vzustand):" , read_Vzustand()
    print "----------------------------------------------------------------------------------------- "
    print " "

def Timecheck():
    pz = int(read_Pzeit())
    if pz == 0:
        rt = int(round(T.time()))
        PZlaufen = (rt - int(read_Ptmp()))
        return PZlaufen
       

def main():
    prepare_first()         ###
    Schalter()
    #PZgelaufen = Timecheck()
    Time_print()
    return 0

if __name__=="__main__":
    main()
