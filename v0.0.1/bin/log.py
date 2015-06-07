#!/usr/bin/env python

import sys, os, time, shutil, threading, unittest

sys.path.append(os.getcwd())
from config import *

Datum = time.strftime("%d.%m.%Y")                      # Datumsstempel 
Zeit = time.strftime("%H:%M:%S")                       # Zeitstempel
logfile = time.strftime("%Y-%m-%d.dat")                # Name der Logdatei
plogfile = time.strftime("%Y-%m-%d.plf")               # Pumpen-Logdatei
vlogfile = time.strftime("%Y-%m-%d.vlf")               # Ventil-Logdatei
refillfile = time.strftime("%Y-%m-%d.rf")               # Refill-Logdatei
global log
global ftp
global ftp2
log = LOG_DIR
ftp = FTP_DIR
ftp2 = FTP_DIR2

##########################################################################################################################################

def write_refill(stat):       ###
    k = log+refillfile
    v = abgleich()
    q = v + " " + stat + "\n"
    control = open(k,"a")
    control.write(q)
    control.close()

def refill_log():          ### 
    if read_file(Pool_refill) == "0":
        #write_refill("0")
        print "ii - Pool ist im Normalbetrieb."
    elif read_file(Pool_refill) == "1":
        write_refill("refill")
        print "ii- Pool wird derzeit nachgefuellt."


#####################################################################
def write_Control__Zustand(on_off):         ###
    k = Controlzustand
    control = open(k,"w")
    control.write(on_off)
    control.close()

def abgleich():             ###
    data_lines=[]
    file_name = LOG_DIR+logfile
    with open(file_name, "r") as data_file:
        data_lines=data_file.readlines()
        w = data_lines[-1].strip('\n').split(' ')
    return w[0]

def write_Plog(stat):       ###
    k = log+plogfile
    v = abgleich()
    q = v + " " + stat + "\n"
    control = open(k,"a")
    control.write(q)
    control.close()

def read_file(file):           ###
    x = file
    pfobj_in = open(x,"r")
    for line in pfobj_in:
        inhalt = line
    pfobj_in.close()
    return inhalt

def pumplog():          ###
    if read_file(Pool_manuell) == "1":
        write_Plog("manuell")
        print "PumpLog -> manuell"
    elif read_file(Pool_manuell) == "0":
        if read_file(Pzustand) == "0":
            write_Plog("aus")
            print "PumpLog -> aus"
        elif read_file(Pzustand) == "1":
            write_Plog("an")
            print "PumpLog -> an"

def write_Vlog(stat):       ###
    k = log+vlogfile
    v = abgleich()
    q = v + " " + stat + "\n"
    control = open(k,"a")
    control.write(q)
    control.close()

def ventillog():          ### 
    if read_file(Ventilzustand) == "0":
        write_Vlog("0")
        print "VentilLog -> 0%"
    elif read_file(Ventilzustand) == "50":
        write_Vlog("50")
        print "VentilLog -> 50%"
    elif read_file(Ventilzustand) == "100":
        write_Vlog("100")
        print "VentilLog -> 100%"


def prepare_first(file4):
    global ftp
    x = log+file4
    #y = ftp+file4
    init = False
    #z = ftp2+file4
    a = 0
    if os.path.isdir(log) is False:
        os.mkdir(log)
        b = open(log+file4,"a")
        b.close()
        print "LOG_DIR & %s wurden erstellt !!!" % (file4)      # ...zum testen   

    if os.path.isfile(log+file4) is False:
        b = open(log+file4,"a")
        b.close()
        print "%s wurde erstellt !!!" % (file4)                 # ...zum testen  

    if FTP_DIR != "":
        if not ftp:
            if ftp2:
               ftp = ftp2
            if not ftp2:
               ftp = "/home/pi"+log
        y = ftp+file4
        if os.path.isfile(ftp+file4) == False:
            shutil.copyfile(x, y)
        a = 0
        with open(str(x)) as x1:
            lc_x = len(x1.readlines())
        with open(str(y)) as y1:
            lc_y = len(y1.readlines())
        while a == 0:
            if os.path.isdir(ftp) == False:
                a = 0
            elif os.path.isdir(ftp) == True:
                a = 1
                if os.path.isfile(y) is True:
                    while a == 1:
                        with open(str(x)) as x1:
                            lc_x = len(x1.readlines())
                        with open(str(y)) as y1:
                            lc_y = len(y1.readlines())
                        if lc_y == lc_x:
                            init = False 
                            a = 2
                        if lc_y > lc_x:
                        #if os.path.getsize(y) > os.path.getsize(x):
                            shutil.copyfile(y, x)
                            print "ftp -cp-> %s" % (file4)                # ...zum testen
                            time.sleep(3)
                            init = True
                        #elif lc_y == lc_x:
                        #elif os.path.getsize(y) == os.path.getsize(x):
                            if init == True:
                                time.sleep(3)
                        else:
                            a = 2

def prepare_last(file5):
    x = log+file5
    y = ftp+file5
    z = ftp2+file5
    a = 0
    while a != 2:
        if os.path.isfile(y) is False:
            shutil.copyfile(x, y)
            print "%s -cp-> ftp" % (file5)                              # ...zum testen
            a = 2
        elif os.path.isfile(y) is True:
            a = 1
            while a == 1:
              if FTP_DIR != "":
                  if not ftp:
                      if ftp2:
                          y = z
                      if not ftp2:
                          y = "/home/pi"+log+logfile
                  if os.path.getsize(x) > os.path.getsize(y):
                      shutil.copyfile(x, y)
                      print "%s -cp-> ftp" % (file5)                              # ...zum testen
#                if ftp2 != "":
#                  if os.path.getsize(x) > os.path.getsize(z):
#                      shutil.copyfile(x, z)
#                      print "log -cp-> ftp2"
                #if os.path.getsize(x) > os.path.getsize(z):
                  #shutil.copyfile(x, z)
                  #print "log -cp-> ftp2"
              if os.path.getsize(x) == os.path.getsize(y): #and os.path.getsize(x) == os.path.getsize(z):
                  a = 2
