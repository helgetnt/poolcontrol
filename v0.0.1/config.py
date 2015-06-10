#####################################
###                               ###
###   KEINE Umlaute verwenden!!!  ###
### 	Syntax beibehalten,       ###
###   da die Konfiguration von    ###
###  Bash & Python benutzt wird.  ###
###                               ###
#####################################
###  Vorsicht bei Aenderungen!!!  ###
###     Change carefully !!!      ###
#####################################

### Log-Files ###
RAM_DIR="/ramfs/"

### Ziel der erstellten Temperatur-DATEN
LOG_DIR=RAM_DIR+"tp/"                           # Zwischenspeicher
FTP_DIR="/hoster_ssh/home/helgetnt/Rpi/tp/"     # Endspeicher
FTP_DIR2="/ftp/tp/"
BAK_DIR="/ftp/tp_bak/"                          # Backup-Endspeicher
Web_DIR="/usr/lib/cgi-bin/"                     # Pfad zum Webscript


#LOG_DIR=home
#FTP_DIR=LOG_DIR
#FTP_DIR2=LOG_DIR
#BAK_DIR=LOG_DIR
#Web_DIR="/usr/lib/cgi-bin/"

### Poolcontrol
LOG=RAM_DIR+"Poolcontrol.log"                   # Logdatei
Controlzustand=RAM_DIR+"Controlzustand.TNT"     # aktiv -> 0=AUS / 1=PoolControl / 2=TempProtokoll / 3=VentilControl

### Pumpenzustand
Pzeit=RAM_DIR+"Pumpenlaufzeit.TNT"              # Pumpenlaufzeit in sec. (...wird erst nach ausschalten der Pumpe geloggt!)
Pzustand=RAM_DIR+"Pumpenzustand.TNT"            # Pumpenzustand -> 0=AUS / 1=AN
Pool_manuell=RAM_DIR+"manuell.TNT"              # Manuell-Schalter -> 0=Automatik / 1=Manuell
Pool_refill=RAM_DIR+"refill.TNT"                # Nachfuell-Schalter -> 0=Normal / 1=Nachfuellen
# Script-Zeit-Interval in sec.
#Script_Interval=360
Croninterval=300
CrontabZeile="*/5 * * * *   pi  /opt/start.py"  ### Standart ->  muss in der "/etc/crontab"geaendert werden !!!


# Sensor-Dateien (sind bei jedem anders -> anpassen !!! )
SensorFile1="/sys/bus/w1/devices/w1_bus_master1/28-00000521b227/w1_slave"	### S1 = POOL
SensorFile2="/sys/bus/w1/devices/w1_bus_master1/28-0000052210cf/w1_slave"	### S2 = SOLAR
SensorFile3="/sys/bus/w1/devices/w1_bus_master1/28-0000052688ab/w1_slave"	### S3 = LUFT

# Temperaturbereich der Fehlerkorrektur
minTemp=0.5	            # in Grad Celsius
maxTemp=81.0            # in Grad Celsius
errorTemp=10.0          # in Grad Celsius
Faktor=5                # Temp-protokoll: Temp. wird hier x mal gelesen & Durchschnitt errechnet

# Zeit in der die Pumpe aktiv sein kann...
Pumpzeit_an="7:00:00"
Pumpzeit_aus="20:00:00"
Pumpe_minTime=3              ### minimale Pumpenlaufzeit in Stunden (Minuten  -> Pmulti='Minuten'
Pmulti='Stunden'             ###                                     Sekunden -> Pmulti='Sekunden')
##########################################################################################################

Ventilzustand=RAM_DIR+"Ventilzustand.TNT"       # Ventilzustand -> 0 = Zirkulieren / 50 = halboffen / 100 = ganz offen

# Temperaturen fuer Solarsteuerung (in Grad Celsius)
maxPool=42.0        # wenn waermer als... auf Zirkulation umschalten
maxSolar=38.0       # wenn waermer als... auf Solar umschalten
max_diff_ps=0.5		# Differenz zwischen Pool  -> Solar
max_diff_sp=0.1     # Differenz zwischen Solar -> Pool 
max_diff_ls=5.0		# Differenz zwischen Luft und Solar

# auszufuehrende Befehle
#Pumpe_An="sudo /home/pi/tools/rcswitch-pi/send 10100 2 1"                   # TEST -> Venti AN
#Pumpe_Aus="sudo /home/pi/tools/rcswitch-pi/send 10100 2 0"                  # TEST -> Venti AUS
Pumpe_An="pilight-send --protocol=elro_he --systemcode=10 --unitcode=1 --on "                          # 
Pumpe_Aus="pilight-send --protocol=elro_he --systemcode=10 --unitcode=1 --off "                        # 

Ventil_Solar_an="pilight-send --protocol=elro_he --systemcode=10 --unitcode=16 --on "                  # 
Ventil_Solar_aus="pilight-send --protocol=elro_he --systemcode=10 --unitcode=16 --off "                # 
Ventil_Zirkulieren_an="pilight-send --protocol=elro_he --systemcode=21 --unitcode=16 --on "            # 
Ventil_Zirkulieren_aus="pilight-send --protocol=elro_he --systemcode=21 --unitcode=16 --off "          # 

#Ventil_Solar_an="sudo /home/pi/tools/rcswitch-pi/send 10101 5 1 "              # ok
#Ventil_Solar_aus="sudo /home/pi/tools/rcswitch-pi/send 10101 5 0 "             # ok
#Ventil_Zirkulieren_an="sudo /home/pi/tools/rcswitch-pi/send 01010 5 1 "        # ok
#Ventil_Zirkulieren_aus="sudo /home/pi/tools/rcswitch-pi/send 01010 5 0 "       # ok

VS50="sudo /home/pi/tools/TempController/Ventil_control.sh VS50"         # Kommando: Ventil  50% Solar
VS100="sudo /home/pi/tools/TempController/Ventil_control.sh VS100"       # Kommando: Ventil 100% Solar
VZ50="sudo /home/pi/tools/TempController/Ventil_control.sh VZ50"         # Kommando: Ventil  50% Zirkulieren
VZ100="sudo /home/pi/tools/TempController/Ventil_control.sh VZ100"       # Kommando: Ventil 100% Zirkulieren

#############################################################################################
### TIP: Am besten mit Stopuhr messen. Die Herstellerangaben muessen nicht immer stimmen. ###
#############################################################################################
Ventil_Voll=100    # Zeit die das Ventil zum totalen umschalten braucht (+6sec)
Ventil_Halb=49     # Zeit die das Ventil zum halben  umschalten braucht (+2sec)
#Ventil_Voll=10     ### Test
#Ventil_Halb=5     ### Test
Latenz=9           # Ausfuehrung des Gegenbefehls -> Dauer ca 5-6 Sekunde

###################################
###     SYSTEMBEREICH           ###
###   Nicht veraendern !!!      ###
###################################

Pon=Pumpe_An
Poff=Pumpe_Aus
PZon=Pumpzeit_an
PZoff=Pumpzeit_aus
Pmin=Pumpe_minTime

###################################
