#!/usr/bin/env python 

import sys, os, time, shutil, threading
import ConfigParser
from config import *
from time import sleep
from Pump_control import read_Pzustand, sh, Zeit, PZon, PZoff, Pumpe

Datum_Zeit = time.strftime("%d.%m.%Y-%H:%M:%S")
tmp = RAM_DIR+"Sensoren.tmp"

####################################################################################################################################
def sensorcheck():
        a = 0
        if os.path.isfile(SensorFile1) is False:
            a = 1
            print "EE - Sensor 1 ist nicht vorhanden !!!  -> ", SensorFile1, " <-"
        if os.path.isfile(SensorFile2) is False:
            a = 1
            print "EE - Sensor 2 ist nicht vorhanden !!!  -> ", SensorFile2, " <-"
        if os.path.isfile(SensorFile3) is False:
            a = 1
            print "EE - Sensor 3 ist nicht vorhanden !!!  -> ", SensorFile3, " <-"
        if a == 0:
            print "ii - Sensoren wurden initialisiert."
        if a == 1:
            print "ii - ", Datum_Zeit
            print "WW - Programm wird beendet...."
            print "ii - Anschluss der Sensoren pruefen !!!"
            exit()

####################################################################################################################################
def stemp1(faktor):                                                 ### Def: Sensor_1 ##################################################
        f = 0                                                           # f auf Null setzen
        while f == 0:                                                   # dauerhaftes auslesen (solange f = 0 ist)
                tempstr = [0] * faktor
                for t in range(faktor):                                 # faktor* Messungen durchfuehren
                        tfile = open(SensorFile1)                       # Sensor-Datei oeffnen 
                        text = tfile.read()                             # Sensor-Datei lesen
                        tfile.close()                                   # Sensor-Datei schliessen
                        tempdata = text.split("\n")[1].split(" ")[9]          # eingelesene...
                        tempstr[t] = float(tempdata[2:]) / 1000               # ...Daten...
                tempe = sum(tempstr) / faktor                                 # ...verarbeiten.
                temp = round(tempe,2)                                   # Wert auf eine Nachkommastelle runden
                if temp <= minTemp:                                     # neueinlesen wenn Temperatur unter minTemp...
                        f = 0           			        # ... erfuellt f = 0
                elif temp >= maxTemp:                                   # neueinlesen wenn Temperatur ueber maxTemp...
                        f = 0           			        # ... erfuellt f = 0
                elif temp > minTemp and temp < maxTemp:                # Wert ausgeben & Schleife beenden, wenn in def. Bereich...
                        f = 1           			        # erfuellt f = 1
			return temp                             ####################################################################

def stemp2(faktor):                                                   ### Def: Sensor_2 ##################################################
        f = 0                                                           # siehe Sensor_1
        while f == 0:
                tempstr = [0] * faktor               
                for t in range(faktor):
                        tfile = open(SensorFile2)
                        text = tfile.read()
                        tfile.close()
                        tempdata = text.split("\n")[1].split(" ")[9]
                        tempstr[t] = float(tempdata[2:]) / 1000
                tempe = sum(tempstr) / faktor
                temp = round(tempe,2)
                if temp <= minTemp:
                        f = 0
                elif temp >= maxTemp:
                        f = 0
                elif temp > minTemp and temp < maxTemp:
                        f = 1
                        return temp                             ###################################################################

def stemp3(faktor):                                                   ### Def: Sensor_3 #################################################
        f = 0                                                           # siehe Sensor_1
        while f == 0:
                tempstr = [0] * faktor
                for t in range(faktor):
                        tfile = open(SensorFile3)
                        text = tfile.read()
                        tfile.close()
                        tempdata = text.split("\n")[1].split(" ")[9]
                        tempstr[t] = float(tempdata[2:]) / 1000
                tempe = sum(tempstr) / faktor
                temp = round(tempe,2)
                if temp <= minTemp:
                        f = 0
                elif temp >= maxTemp:
                        f = 0
                elif temp > minTemp and temp < maxTemp:
                        f = 1
                        return temp                             ####################################################################
####################################################################################################################################
    ### ...Zeit bis hier (faktor=3)  rund 10 Sekunden !!! ###
    ### ...Zeit bis hier (faktor=10) rund 26 Sekunden !!! ###
####################################################################################################################################
def get_temp(num):
        k = RAM_DIR+"Sensoren.tmp"
        conf = ConfigParser.ConfigParser()
        conf.read(k)
        if num == 1:
            data = conf.get("sensors", "temp1")
        if num == 2:
            data = conf.get("sensors", "temp2")
        if num == 3:
            data = conf.get("sensors", "temp3")
        return float(data)

def get_lastTemp(num):
        k = RAM_DIR+"Sensoren_last.tmp"
        conf = ConfigParser.ConfigParser()
        conf.read(k)
        if num == 1:
            data = conf.get("sensors", "temp1")
        if num == 2:
            data = conf.get("sensors", "temp2")
        if num == 3:
            data = conf.get("sensors", "temp3")
        return float(data)

def write_tmp():
        k = RAM_DIR+"Sensoren.tmp"
        control = open(k,"w")
        control.write("[sensors]\n" + "temp1=" + str(temp1) + "\n" + "temp2=" + str(temp2) + "\n" + "temp3=" + str(temp3) + "\n")
        control.close()

def tmp_check():
        a = 0
        while a == 0:
            if os.path.isfile(tmp) is False:
                robj_out = open(tmp,"w")
                robj_out.write("[sensors]\n" + "temp1=" + temp1 + "\n" + "temp2=" + temp2 + "\n" + "temp3=" + temp3 + "\n")
                robj_out.close()
                a = 1
            elif os.path.isfile(tmp) is True:
                write_tmp()
                a = 1
        return man

def error_prevent():
    rPump = int(read_Pzustand())
    if PZon >= Zeit:                              ### ...Zeit vor Beginn.
        if rPump != 0:                            # Pumpzustand steht nicht auf 0
            Pumpe("0")
    elif PZoff <= Zeit:                           ### ...Zeit nach Ende.
        if rPump != 0:                            # Pumpzustand steht nicht  auf 0
            Pumpe("0")
    elif PZon <= Zeit:                            ### Pumpe ist im Zeitrahmen an
      if PZoff >= Zeit:                           ###
        if rPump == 0:
            print "ii - Pumpe wird 20sec. angeschaltet, um Messfehler zu vermeiden."
            Pumpe("1")
            sleep(20)
            Pumpe("0")

##########################################################################################################################################

def main():
    last_temp1 = get_temp(1)
    last_temp2 = get_temp(2)
    last_temp3 = get_temp(3)
#    print '--------------------------'
#    print ' Sensor    | Temperatur   '      ### Zum Testen...
#    print '--------------------------'      ### Ausgabe
#    print ' Sensor_1 -> ' , stemp1           ### in
#    print ' Sensor_2 -> ' , stemp2           ### Terminal
#    print ' Sensor_3 -> ' , stemp3           ### ...Ende.
#    print '--------------------------'
    print "ii - Sensorcheck !!!"
    error_prevent()
    a = 0
    b = 0
    while b != 3:
        if os.path.isfile(SensorFile1) is False:
            print "EE - Sensor 1 ist nicht vorhanden !!!  -> ", SensorFile1, " <-"
            sleep(5)
            b += 1
            if b == 3:
                a = 1
        if os.path.isfile(SensorFile1) is True:
            temp1 = stemp1(Faktor)
            print "ii - Sensor 1 wurde eingelesen !!!  -> ", SensorFile1, " <-"
            b = 3
############################################
    b = 0
    while b != 3:
        if os.path.isfile(SensorFile2) is False:
            print "EE - Sensor 2 ist nicht vorhanden !!!  -> ", SensorFile2, " <-"
            sleep(5)
            b += 1
            if b == 3:
                a = 1
        if os.path.isfile(SensorFile2) is True:
            temp2 = stemp2(Faktor)
            print "ii - Sensor 2 wurde eingelesen !!!  -> ", SensorFile2, " <-"
            b = 3
############################################
    b = 0
    while b != 3: 
        if os.path.isfile(SensorFile3) is False:
            print "EE - Sensor 3 ist nicht vorhanden !!!  -> ", SensorFile3, " <-"
            sleep(5)
            b += 1
            if b == 3:
                a = 1
        if os.path.isfile(SensorFile3) is True:
            temp3 = stemp3(Faktor)
            print "ii - Sensor 3 wurde eingelesen !!!  -> ", SensorFile3, " <-"
            b = 3
############################################
    b = 0
    while b != 3:
        terr = last_temp1 - temp1
        if terr <= errorTemp:
            b = 3
        if terr >= -errorTemp:
            b = 3
        if terr >= errorTemp:
            print "EE - Pooltemperatur muss falsch sein !!!  -> ", temp1, " <-"
            print "ii - Messung wird wiederholt.", Datum_Zeit
            temp1 = stemp1(Faktor)
            sleep(3)
            b += 1
            if b == 3:
                a = 1
        if terr <= -errorTemp:
            print "EE - Pooltemperatur muss falsch sein !!!  -> ", temp1, " <-"
            print "ii - Messung wird wiederholt.", Datum_Zeit
            temp1 = stemp1(Faktor)
            sleep(3)
            b += 1
            if b == 3:
                a = 1

############################################
    if a == 0:
        k = RAM_DIR+"Sensoren.tmp"
        control = open(k,"w")
        control.write("[sensors]\n" + "temp1=" + str(temp1) + "\n" + "temp2=" + str(temp2) + "\n" + "temp3=" + str(temp3) + "\n")
        control.close()
        print "ii - Sensoren wurden initialisiert."
    if a == 1:
        print "ii - ", Datum_Zeit
        print "WW - Programm wird beendet...."
        print "ii - Anschluss der Sensoren pruefen !!!"
        exit()
    return 0

if __name__=="__main__":
    main()
