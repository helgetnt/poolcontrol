#!/usr/bin/env python
global dat
global plog
global vlog
from moduls.config import *

def show_plf(filename):
    p = []
    q = [p[:-4] for p in plog]
    err = "Fuer diesen Tag existiert kein Pumpen-Log (.plf)...."
    err2= "Fuer diesen Tag existiert kein komplettes Pumpen-Log (.plf)...."
    if filename[:-4] not in q:
        info_plf = """
        <table border="3">
  <tr>
    <td rowspan="2"><err>%s</err></td>
  </tr></table>""" % (err)
    #"""

    elif filename[:-4] in q:
      file1 = str(settings['data_dir']+filename)
      file2 = str(settings['data_dir']+filename)[:-4]+'.plf'
      with open(file1) as f1:
          line_count1 = len(f1.readlines())
      with open(file2) as f2:
          line_count2 = len(f2.readlines())
      if line_count1 != line_count2:
          info_plf = """
        <table border="3">
  <tr>
    <td rowspan="2"><err>%s</err></td>
  </tr></table>""" % (err2)
    #"""
      else:
        file1 = str(settings['data_dir']+filename)[:-4]+'.plf'
        f1 = open(file1, "rb")
        reader = csv.reader(f1, delimiter=" ")
        #Trigger und Variablen initialisieren	
        an = False
        aus = False
        man = False
        init100 = False
        init50 = False
        erg = timedelta(seconds=0)
        erg1 = timedelta(seconds=0)
        erg2 = timedelta(seconds=0)
        #Nun wird in jeder Zeile der Datei geprueft ob:
        for row in reader: 
            #Die Pumpe an ist 
            if row[1] == 'an':
                #Merken ob sie schon mal an war
                init100 = True
                #Damit ist sie nicht manuell
                man = False
                #Damit ist sie nicht aus
                aus = False
                #Wenn sie vorher nicht an war 
                if not an:
                    #Ist sie jetzt an 
                    an = True
                    #Merke den Timestamp
                    counter1 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
                    counter3 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
                    #Nur wenn es schon mal manuell war 
                    if init50:
                        #dann rechne den ersten Timestamp wann sie an ist minus den ersten Timestamp wann sie manuell war
                        counter4 = datetime.fromtimestamp(mktime(strptime(row[0],'%d.%m.%Y-%H:%M:%S'))) - datetime.fromtimestamp(mktime(counter4))
                        #addier die Zeit zum Ergebnis
                        erg1 = erg1 + counter4
                        init50 = False
                else:
                    #Merke den Timestamp fuer den Fall das sie am Ende der Datei ist
                    counter3 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')	
            #####################################################################################################################################
            #Das Ventil 50% offen ist
            elif row[1] == 'manuell':
                #Merken ob sie schon mal manuell war
                init50 = True
                #Damit ist sie nicht an
                an = False
                #Damit ist sie nicht aus
                aus = False
                #Wenn es vorher nicht 50% offen war 
                if not man:
                    #dann ist sie jetzt manuell 
                    man = True
                    #Merke den Timestamp
                    counter4 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
                    counter5 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
                    #Nur wenn es schon mal 100% offen war 
                    if init100:
                        #dann rechne den ersten Timestamp wann es 50% offen ist minus den ersten Timestamp wann es 100% offen war
                        counter1 = datetime.fromtimestamp(mktime(strptime(row[0],'%d.%m.%Y-%H:%M:%S'))) - datetime.fromtimestamp(mktime(counter1))
                        #addier die Zeit zum Ergebnis
                        erg = erg + counter1
                        init100 = False
                else:
                    #Merke den Timestamp fuer den Fall das sie am Ende der Datei ist
                    counter5 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
            #####################################################################################################################################
            #Die Pumpe  ist aus
            elif row[1] == 'aus':
                #Damit ist sie nicht an 
                an = False
                #Damit ist sie nicht manuell
                man = False
                # wenn sie nicht schon aus war
                if not aus:
                    #dann ist sie jetzt aus
                    aus = True
                    #Nur wenn Sie schon mal an war 
                    if init100: 
                        #dann rechne den ersten Timestamp wann sie aus ist minus den ersten Timestamp wann sie an war
                        counter2 = datetime.fromtimestamp(mktime(strptime(row[0],'%d.%m.%Y-%H:%M:%S'))) - datetime.fromtimestamp(mktime(counter1))
                        #addier die Zeit zum Ergebnis
                        erg = erg + counter2
                        init100 = False
                    #Nur wenn es schon mal manuell war 
                    if init50:
                        #dann rechne den ersten Timestamp wann sie an ist minus den ersten Timestamp wann sie manuell war
                        counter6 = datetime.fromtimestamp(mktime(strptime(row[0],'%d.%m.%Y-%H:%M:%S'))) - datetime.fromtimestamp(mktime(counter4))
                        #addier die Zeit zum Ergebnis
                        erg1 = erg1 + counter6
                        init50 = False
        #Wenn die Datei durchgelaufen ist und die Pumpe noch an ist
        if an:
            #Rechne den letzten An Timestamp minus den Timstamp wo sie angeschaltet wurde.
            counter2 = datetime.fromtimestamp(mktime(counter3)) - datetime.fromtimestamp(mktime(counter1))
            erg = erg + counter2
        #Wenn die Datei durchgelaufen ist und das Ventil noch manuell ist
        if man:
            #Rechne den letzten manuell Timestamp minus den ersten aus Timstamp.
            counter6 = datetime.fromtimestamp(mktime(counter5)) - datetime.fromtimestamp(mktime(counter4))
            erg1 = erg1 + counter6
        f1.close()
        erg2 = erg + erg1
        #Ergebnis ausgeben
        print '<title><u>Pumpenlaufzeit:</u></title>'
        info_plf = """
        <table border="3">
  <tr>
    <td><em>An</em></td>
    <td><em>Manuell</em></td>
    <td><em>Ges.</em></td>
  </tr>
  <tr>
    <td><em2>%s</em2></td>
    <td><em2>%s</em2></td>
    <td><em2>%s</em2></td>
  </tr></table>""" % (erg, erg1, erg2)
    #"""
    return info_plf

def show_vlf(filename):
    p = []
    q = [p[:-4] for p in vlog]
    err = "Fuer diesen Tag existiert kein Ventil-Log (.vlf)...."
    err2= "Fuer diesen Tag existiert kein komplettes Ventil-Log (.vlf)...."
    if filename[:-4] not in q:
        info_vlf = """
        <table border="3">
  <tr>
    <td rowspan="2"><err>%s</err></td>
  </tr></table>""" % (err)
    #"""
    elif filename[:-4] in q:
      file1 = str(settings['data_dir']+filename)
      file2 = str(settings['data_dir']+filename)[:-4]+'.vlf'
      with open(file1) as f1:
          line_count1 = len(f1.readlines())
      with open(file2) as f2:
          line_count2 = len(f2.readlines())
      if line_count1 != line_count2:
          info_vlf = """
        <table border="3">
  <tr>
    <td rowspan="2"><err>%s</err></td>
  </tr></table>""" % (err2)
      #"""
      else:
        f2 = open(file2, "rb")
        reader = csv.reader(f2, delimiter=" ")
        #Trigger und Variablen initialisieren   
        van = False
        vaus = False
        halb = False
        init100 = False
        init50 = False
        erg = timedelta(seconds=0)
        erg1 = timedelta(seconds=0)
        erg2 = timedelta(seconds=0)
        #Nun wird in jeder Zeile der Datei geprueft ob:
        for row in reader: 
            #Das Ventil 100% offen ist 
            if row[1] == '100':
                #Merken ob es schon mal 100% offen war
                init100 = True
                #Damit ist es nicht 50% offen
                halb = False
                #Damit ist es nicht 0% offen
                vaus = False
                #Wenn es vorher nicht 100% offen war 
                if not van:
                    #dann ist es jetzt 100% offen 
                    van = True
                    #Merke den Timestamp
                    count1 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
                    count3 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
                    #Nur wenn es schon mal 50% offen war 
                    if init50:
                        #dann rechne den ersten Timestamp wann es 100% offen ist minus den ersten Timestamp wann es 50% offen war
                        count4 = datetime.fromtimestamp(mktime(strptime(row[0],'%d.%m.%Y-%H:%M:%S'))) - datetime.fromtimestamp(mktime(count4))
                        #addier die Zeit zum Ergebnis
                        erg1 = erg1 + count4
                        init50 = False
                else:
                    #Merke den Timestamp fuer den Fall das sie am Ende der Datei ist
                    count3 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
            #####################################################################################################################################
            #Das Ventil 50% offen ist
            elif row[1] == '50':
                #Merken ob es schon mal 50% offen war
                init50 = True
                #Damit ist es nicht 100% offen
                van = False
                #Damit ist es nicht 0% offen
                vaus = False
                #Wenn es vorher nicht 50% offen war 
                if not halb:
                    #dann ist es jetzt 50% offen 
                    halb = True
                    #Merke den Timestamp
                    count4 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
                    count5 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
                    #Nur wenn es schon mal 100% offen war 
                    if init100:
                        #dann rechne den ersten Timestamp wann es 50% offen ist minus den ersten Timestamp wann es 100% offen war
                        count1 = datetime.fromtimestamp(mktime(strptime(row[0],'%d.%m.%Y-%H:%M:%S'))) - datetime.fromtimestamp(mktime(count1))
                        #addier die Zeit zum Ergebnis
                        erg = erg + count1
                        init100 = False
                else:
                    #Merke den Timestamp fuer den Fall das sie am Ende der Datei ist
                    count5 = strptime(row[0],'%d.%m.%Y-%H:%M:%S')
            #####################################################################################################################################
            #Das Ventil 0% offen  ist
            elif row[1] == '0':
                #Damit ist es nicht 100% offen 
                van = False
                #Damit ist es nicht 50% offen
                halb = False
                # wenn es nicht schon 0% offen war
                if not vaus:
                    #dann ist es jetzt 0% offen
                    vaus = True
                    #Nur wenn es schon mal 100% offen war 
                    if init100: 
                        #dann rechne den ersten Timestamp wann es 0% offen ist minus den ersten Timestamp wann es 100% offen war
                        count2 = datetime.fromtimestamp(mktime(strptime(row[0],'%d.%m.%Y-%H:%M:%S'))) - datetime.fromtimestamp(mktime(count1))
                        #addier die Zeit zum Ergebnis
                        erg = erg + count2
                        init100 = False
                    #Nur wenn es schon mal 50% offen war 
                    if init50:
                        #dann rechne den ersten Timestamp wann es 100% offen ist minus den ersten Timestamp wann es 500% offen war
                        count6 = datetime.fromtimestamp(mktime(strptime(row[0],'%d.%m.%Y-%H:%M:%S'))) - datetime.fromtimestamp(mktime(count4))
                        #addier die Zeit zum Ergebnis
                        erg1 = erg1 + count6
                        init50 = False
        #########################################################################################################################################
        #Wenn die Datei durchgelaufen ist und das Ventil noch 100% offen ist
        if van:
            #Rechne den letzten 100% Timestamp minus den ersten 0% Timstamp.
            count2 = datetime.fromtimestamp(mktime(count3)) - datetime.fromtimestamp(mktime(count1))
            erg = erg + count2
        #Wenn die Datei durchgelaufen ist und das Ventil noch 50% offen ist
        if halb:
            #Rechne den letzten 100% Timestamp minus den ersten 0% Timstamp.
            count6 = datetime.fromtimestamp(mktime(count5)) - datetime.fromtimestamp(mktime(count4))
            erg1 = erg1 + count6
        f2.close()
        erg2 = erg + erg1
        #Ergebnis ausgeben
        print '<title><u>Pumpenlaufzeit:</u></title>'
        info_vlf = """
        <table border="3">
  <tr>
    <td><em>%s</em></td>
    <td><em>%s</em></td>
    <td><em>Ges.</em></td>
  </tr>
  <tr>
    <td><em2>%s</em2></td>
    <td><em2>%s</em2></td>
    <td><em2>%s</em2></td>
  </tr></table>""" % (str("100%"), str("50%"), erg, erg1, erg2)
    #"""
    return info_vlf

def show_log(filename):
    plf = show_plf(filename)
    vlf = show_vlf(filename)
    temp = show_temp(filename)
    info = """
    <table border="5">
  <tr>
    <th><em1>Temperaturen</em1></th>
    <th><em1>Pumpenlaufzeit</em1></th>
    <th><em1>Ventil-Zeiten</em1></th>
  </tr>
  <tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
  </tr>
    </table>
  <br>
  </br> """ % (temp, plf, vlf)
    #"""
    print info

def show_temp(filename):
    akt="Letzter Wert"
    if datecheck == option:
        akt="Aktuell"
    else:
        akt="Letzter Wert"
    pool=[]
    solar=[]
    luft=[]
    p = 0
    s = 0
    l = 0
    file_name = str(settings['data_dir']+filename)
    f1 = open(file_name, "rb")
    reader = csv.reader(f1, delimiter=" ")
    for row in reader:
        p += float(row[1])
        s += float(row[2])
        l += float(row[3])
        pool.append(float(row[1]))
        solar.append(float(row[2]))
        luft.append(float(row[3]))
    max_pool  = str(round(max(pool), 2))
    max_solar = str(round(max(solar), 2))
    max_luft  =  str(round(max(luft), 2))
    mid_pool  = str(round(p / len(pool), 2))
    mid_solar = str(round(s / len(solar), 2))
    mid_luft  = str(round(l / len(luft), 2))
    min_pool  = str(round(min(pool), 2))
    min_solar = str(round(min(solar), 2))
    min_luft  =  str(round(min(luft), 2))
    f1.close()
    a = str(chr(176)+"C")
    info_temp = """
    <div id="t_div">
    <table id="temp" border-collapse="collapse">
  <TR><TH>
      <TH><em1>Pool</em1>
      <TH><em1>Solar</em1>
      <TH><em1>Luft</em1>
  <TR><th><em2>%s</em2><TD><em2>%s</em2><TD><em2>%s</em2><TD><em2>%s</em2>
  <TR><th><em1>Maximal</em1><TD><em>%s</em><TD><em1>%s</em1><TD><em1>%s</em1>
  <TR><th><em1>Mittel</em1><TD><em1>%s</em1><TD><em1>%s</em1><TD><em1>%s</em1>
  <TR><th><em1>Minimal</em1><TD><em1>%s</em1><TD><em1>%s</em1><TD><em1>%s</em1>
  </table></div>""" % (akt, row[1]+a, row[2]+a, row[3]+a, max_pool+a, max_solar+a, max_luft+a, mid_pool+a, mid_solar+a, mid_luft+a, min_pool+a, min_solar+a, min_luft+a)
    #"""
    return info_temp

def plf_check(wert):
    a = '0'
    if wert == 'an':
        a = settings['Pumpe_an']
    elif wert == 'aus':
        a = settings['Pumpe_aus']
    elif wert == 'manuell':
        a = settings['Pumpe_auto']
    return a

def vlf_check(wert):
    a = '0'
    if wert == '100':
        a = settings['V100']
    elif wert == '0':
        a = settings['V0']
    elif wert == '50':
        a = settings['V50']
    return a
