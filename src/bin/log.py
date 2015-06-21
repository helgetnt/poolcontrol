#!/usr/bin/env python

import sys, os, time, shutil, threading, unittest

sys.path.append(os.getcwd())
from config import *

Datum = time.strftime("%d.%m.%Y")                      # Datumsstempel 
Zeit = time.strftime("%H:%M:%S")                       # Zeitstempel
pclog = time.strftime("%Y-%m-%d.log")                  # PoolControl Log-Backup-Datei
logfile = time.strftime("%Y-%m-%d.dat")                # Name der Logdatei
plogfile = time.strftime("%Y-%m-%d.plf")               # Pumpen-Logdatei
vlogfile = time.strftime("%Y-%m-%d.vlf")               # Ventil-Logdatei
refillfile = time.strftime("%Y-%m-%d.rf")               # Refill-Logdatei
global log
global log2
global ftp
global ftp2
log = LOG_DIR
log2 = LOG_DIR2
sh = os.system

from time import *
from timestring import *
from datetime import datetime
from datetime import timedelta
dZeit = datetime.now()
Zeitformat = "%Y-%m-%d %H:%M:%S"
LCon  = datetime.strptime(str(Date(LCon)), Zeitformat)
LCoff = datetime.strptime(str(Date(LCoff)), Zeitformat)

##########################################################################################################################################
def log_clean():
    if LCon <= dZeit:
        if LCoff >= dZeit:
            sh("sudo "+workdir+"bin/log_cleaner.sh LogClean")
            sh("sudo "+workdir+"bin/log_cleaner.sh PC-LogBackup")

def last_temp(n):
    dat  = sorted([fn for fn in os.listdir(LOG_DIR) if any([fn.endswith('.dat')])])
    last_dat = str(LOG_DIR+max(dat))

    last_temps = read_file(last_dat)[:-2].split(' ')
    last_temp = float(last_temps[n])
    return last_temp

######################################################################
def write_refill(stat):       ###
    k = log+refillfile
    v = abgleich()
    q = v + " " + stat + "\n"
    control = open(k,"a")
    control.write(q)
    control.close()

def refill_log():          ### 
    if read_file(Pool_refill) == "0":
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

def prepare_first(log, file4):
    global ftp
    x = log+file4
    ftp = FTP_DIR+log[7:]
    ftp2 = FTP_DIR2+log[7:]
    init = False
    a = 0
    if not os.path.isdir(log):
        os.mkdir(log)
        b = open(log+file4,"a")
        b.close()
        print "ii - LOG_DIR & %s wurden erstellt !!!" % (file4)      # ...zum testen   

    if not os.path.isfile(log+file4):
        b = open(log+file4,"a")
        b.close()
        print "ii - %s wurde erstellt !!!" % (file4)                 # ...zum testen  

    if FTP_DIR == "":
        print "ii - Kein FTP_DIR in Config angegeben."
        print "ii - Backup wird ausgesetzt."
    elif FTP_DIR != "":
        if os.path.isdir(FTP_DIR):
            if os.path.isdir(ftp):
                ftp = ftp
            elif not os.path.isdir(ftp):
                os.mkdir(ftp)
                print "ii - %s wurde erstellt !!!" % (ftp)                 # ...zum testen
                ftp = ftp

        elif not os.path.isdir(FTP_DIR):
          print "EE - FTP_DIR [%s] ist nicht erreichbar." % (FTP_DIR)
          print "ii - Notfall-FTP wird eingerichtet."
          if FTP_DIR2 == "":
            print "EE - Kein FTP_DIR2 in Config angegeben."
          elif FTP_DIR2 != "":
            if os.path.isdir(FTP_DIR2):
                print "ii - FTP_DIR2 [%s] wird benutzt." % (FTP_DIR2)
                if os.path.isdir(ftp2):
                    ftp = ftp2
                elif not os.path.isdir(ftp2):
                    os.mkdir(ftp2)
                    print "ii - %s wurde erstellt !!!" % (ftp2)                 # ...zum testen  
                    ftp = ftp2
            elif not os.path.isdir(FTP_DIR2):
                print "EE - FTP_DIR2 [%s] ist nicht erreichbar." % (FTP_DIR2)
                ftp = "/home/pi"+log
                os.mkdir(ftp)
                print "ii - %s wird benutzt." % (ftp)

        y = ftp+file4
        if not os.path.isfile(ftp+file4):
            shutil.copyfile(x, y)
        a = 0
        with open(str(x)) as x1:
            lc_x = len(x1.readlines())
        with open(str(y)) as y1:
            lc_y = len(y1.readlines())
        while a == 0:
            if not os.path.isdir(ftp):
                a = 0
            elif os.path.isdir(ftp):
                a = 1
                if os.path.isfile(y):
                    if not os.path.isfile(x):
                        shutil.copyfile(y, x)
                        print "ftp -cp-> %s" % (file4)                # ...zum testen
                        time.sleep(4)                        
                    while a == 1:
                        with open(str(x)) as x1:
                            lc_x = len(x1.readlines())
                        with open(str(y)) as y1:
                            lc_y = len(y1.readlines())
                        if lc_y == lc_x:
                            init = False 
                            a = 2
                        if lc_y > lc_x:
                            shutil.copyfile(y, x)
                            print "ftp -cp-> %s" % (file4)                # ...zum testen
                            time.sleep(3)
                            init = True
                            if init == True:
                                time.sleep(3)
                        else:
                            a = 2






def prepare_last(log, file5):
    ftp = FTP_DIR+log[7:]
    ftp2 = FTP_DIR2+log[7:]
    a = 0
    while a != 2:
        if not os.path.isfile(ftp+file5):
            shutil.copyfile(log+file5, ftp+file5)
            print "ii - %s -cp-> ftp" % (file5)                              # ...zum testen
            a = 2
        elif os.path.isfile(ftp+file5):
            a = 1
            while a == 1:
              if FTP_DIR != "":
                  if ftp:
                      y = ftp+file5
                  if not ftp:
                      if ftp2:
                          y = ftp2+file5
                      if not ftp2:
                          y = "/home/pi"+log+logfile
                  if os.path.getsize(log+file5) > os.path.getsize(y):
                      shutil.copyfile(log+file5, y)
                      print "ii - %s -cp-> ftp" % (file5)                              # ...zum testen
              if os.path.getsize(log+file5) == os.path.getsize(ftp+file5):
                  a = 2
