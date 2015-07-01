#!/usr/bin/env python

import sys, os, shutil, threading
import ConfigParser
from log import *

sys.path.append(os.getcwd())
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from config import *
from time import sleep
from Pump_control import Zeit, PZon, PZoff, Pumpe

sh = os.system

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

####################################################################################################################################
maxPool = float(maxPool)
maxSolar = float(maxSolar)
max_diff_ps = float(max_diff_ps)
max_diff_sp = float(max_diff_sp)
max_diff_ls = float(max_diff_ls)
SerrTemp = errorTemp/2
max_err_diff = float(max_diff_ps)*2
errLmS = last_temp2 - stemp2
errSmL = stemp2 - last_temp2
diff_ps = stemp2 - stemp1
diff_sp = stemp1 - stemp2
diff_ls = stemp2 - stemp3
toll1 = stemp1 + float(0.2)

####################################################################################################################################
def ST100(e):
  inhalt = e
  f = max_diff_ps / 2
  if inhalt != '100':
    print "...teste ST100:"                                                     # ...zum testen
    if stemp2 >= maxSolar:
        print stemp2 , ">=" , maxSolar                                          # ...zum testen
        if inhalt == '0':
            print "Ventil wird von 0 auf 100 gestellt"                          # ...zum testen
            sh(VS100)
            write_zustand(Vzustand, 100)
        elif inhalt == '50':
            print "Ventil wird von 50 auf 100 gestellt"                         # ...zum testen
            sh(VS50)
            write_zustand(Vzustand, 100)
    elif diff_ps >= max_diff_ps:
        print diff_ps , ">=" , max_diff_ps                                      # ...zum testen
        if inhalt == "0":
            print "Ventil wird von 0 auf 100 gestellt"                          # ...zum testen
            sh(VS100)
            write_zustand(Vzustand, 100)
        elif inhalt == '50':
            print "Ventil wird von 50 auf 100 gestellt"                         # ...zum testen
            sh(VS50)
            write_zustand(Vzustand, 100)
    elif diff_ps > f:
        print diff_ps , ">=" , max_diff_ps                                      # ...zum testen
        if inhalt == "0":
            print "Ventil wird von 0 auf 100 gestellt"                          # ...zum testen
            sh(VS100)
            write_zustand(Vzustand, 100)
        elif inhalt == '50':
            print "Ventil wird von 50 auf 100 gestellt"                         # ...zum testen
            sh(VS50)
            write_zustand(Vzustand, 100)

  elif inhalt == '100':
    print "Ventil steht (oder stand) schon auf ST100"                           # ...zum testen
    if diff_ps >= max_err_diff:
        print diff_ps , ">=" , max_err_diff                                     # ...zum testen
        print "ii - Es muss einen Fehler an Ventil oder Pumpe geben."           # ...zum testen
        print "ii - Ventil wird nochmals auf 100 gestellt"                      # ...zum testen
        sh(VS100)
        print "ii - Pumpe wird nochmals eingeschaltet. (%s mal)" % (PumpErr)    # ...zum testen
        Pumpe(PumpErr)

def ST50(e):
  inhalt = e
  f = max_diff_ps / 2
  if inhalt == '50':
    print "Ventil steht (oder stand) schon auf ST50"                            # ...zum testen
  elif inhalt != '50':
    print "...teste ST50:"                                                      # ...zum testen
    if diff_ps <= f:
      if diff_ps >= max_diff_sp:
        print diff_ps , "<=" , f ,inhalt                                        # ...zum testen
        print diff_ps , ">=" , max_diff_sp                                      # ...zum testen
        if inhalt == "0":
            print "Ventil wird von 0 auf 50 gestellt"                           # ...zum testen
            sh(VS50)
            write_zustand(Vzustand, 50)
        elif inhalt == '100':
            print "Ventil wird von 100 auf 50 gestellt"                         # ...zum testen
            sh(VZ50)
            write_zustand(Vzustand, 50)

def ST0(e):
  inhalt = e
  if inhalt == '0':
    print "Ventil steht (oder stand) schon auf ST0"                             # ...zum testen
  elif inhalt != '0':
    print "...teste ST0:"                                                       # ...zum testen
    if diff_ps <= max_diff_sp:
        print diff_ps , "<=" , max_diff_sp                                      # ...zum testen
        if inhalt == '100':
            print "Ventil wird von 100 auf 0 gestellt"                          # ...zum testen
            sh(VZ100)
            write_zustand(Vzustand, 0)
        elif inhalt == '50':
            print "Ventil wird von 50 auf 0 gestellt"                           # ...zum testen
            sh(VZ50)
            write_zustand(Vzustand, 0)
    elif stemp1 >= maxPool:
        print "ii - Die maximale Pooltemperatur wurde erreicht."
        print stemp1 , ">=" , maxPool
        if inhalt == '100':
            print "Ventil wird von 100 auf 0 gestellt"                          # ...zum testen
            sh(VZ100)
            write_zustand(Vzustand, 0)
        elif inhalt == '50':
            print "Ventil wird von 50 auf 0 gestellt"                           # ...zum testen
            sh(VZ50)
            write_zustand(Vzustand, 0)

def Control(d):
    inhalt = d
    y = 0
    if PZon <= Zeit:                                          ### Anlage ist im Zeitrahmen
      if PZoff >= Zeit:                                       ###
        while y != 3:
            if y == 0:
                print "...teste Ventiloptionen"                         # ...zum testen
                print "exec ST100"
       	        ST100(inhalt)
                y = 1
            elif y == 1:
                print "exec ST50"                                       # ...zum testen
                ST50(inhalt)
                y = 2
            elif y == 2:
                print "exec ST0"                                        # ...zum testen
                ST0(inhalt)
                y = 3
    if PZon >= Zeit:                                       ### ...Zeit vor Beginn.
        if inhalt != 0:                                    # Ventilzustand steht nicht auf 0
            if inhalt == 100:
                sh(VZ100)
                print "Ruhezeit- -> VZ100"
            elif inhalt == 50:
                sh(VZ50)
                print "Ruhezeit- -> VZ50"
    elif PZoff <= Zeit:                                    ### ...Zeit nach Ende.
        if inhalt != 0:                                    # Ventilzustand steht nicht auf 0
            if inhalt == 100:
                sh(VZ100)
                print "Ruhezeit+ -> VZ100"
            elif inhalt == 50:
                sh(VZ50)
                print "Ruhezeit+ -> VZ50"

    print "---------------------------------"
    print "- Ventil_Control durchgelaufen. -"      
    print "---------------------------------"

def Countdown(boom):
    min = 1
    while boom > 0:
        sleep(1*min);
        print(boom)
        boom -=1

def file_check():
    a = 0
    while a == 0:
        if os.path.isfile(Vzustand) is False:
            print "Logfile nicht vorhanden..."
            print "Ventil wird auf zirkulieren gestellt & Datei neuerstellt."
            print "Wait %s Sekunden" %Ventil_Voll
            sh(VZ100)
            write_zustand(Vzustand, 0)
            a = 1
        elif os.path.isfile(Vzustand) is True:
            a = 1

##########################################################################################################################################
def error_prevent():
    print "ii - Untersuchung auf Unstimmigkeiten !!"
    if errSmL > SerrTemp:
        print "EE - Es gab einen Fehler bei der Ventilumstellung !"          # ...zum testen
        print "ii - Ventil wird auf 100 gestellt !"                          # ...zum testen
        print "Wait %s Sekunden" %Ventil_Voll
        sh(VS100)
        write_zustand(Vzustand, 100)
    elif errSmL < -SerrTemp:
        print "EE - Es gab einen Fehler bei der Ventilumstellung !"          # ...zum testen
        print "ii - Ventil wird auf 0 gestellt !"                          # ...zum testen
        print "Wait %s Sekunden" %Ventil_Voll
        sh(VZ100)
        write_zustand(Vzustand, 0)
    else:
        print "ii - Alles OK."

##########################################################################################################################################
def main():
    write_Control__Zustand("3")
    file_check()
    inhalt = read_file(Vzustand)
    print '--------------------------------'
    print ' Sensor          | Temperatur   '      ### Zum Testen...
    print '--------------------------------'      ### Ausgabe
    print ' Pool  Sensor_1 -> ' , stemp1          ### in
    print ' Solar Sensor_2 -> ' , stemp2          ### Terminal
    print ' Luft  Sensor_3 -> ' , stemp3          ### ...Ende.
    print '--------------------------------'
    print 'ps ' , diff_ps , ' --> max_ps' , max_diff_ps
    print 'sp ' , diff_sp , ' --> max_sp' , max_diff_sp
    print 'last_temp2', last_temp2
    #print 'ls ' , diff_ls , ' --> max_ls' , max_diff_ls
    #print 'toll1 ' , toll1 , ' --> max_sp' , max_diff_sp
    print 'read_Vzustand ' , inhalt
    print '--------------------------------'
    #error_prevent()
    Control(inhalt)
    return 0                        

if __name__=="__main__":
    main()

