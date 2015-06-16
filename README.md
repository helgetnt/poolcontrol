# PoolControl
Always Run as **ROOT** !!!

Automatic Pool Controller for Raspberry Pi, 
with 3 Temp.-Sensors; 1 Engine Valve, Logging and (online) Webchart

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
...functional, but not yet completed !!!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**--- The use of the provided material, EXPRESS at your own risk. ---**

... so, from here in German !!!

benutzte Software: Raspbian, Python, Pilight/Pimatic (anfangs rcswitch-pi), Lirc (nur fuer Beleuchtung),
^^^^^^^^^�^^^^^^^^^ F�lask(fuer Webapp, aber dazu später!),

--> Empfehlung(,aber kein muss,) meinerseits Pumpe + Sandfilter > egal wie gro�^� oder klein dein Pool  <--
**Für Verkabelung nur CAT5 Netzwerkkabel verwenden!!! 
Sonst kann ich nur sagen "learning by doing", auf die Schn... fallen faellt nicht schwer.**

Etwas elektrotechnisches Wissen wird vorausgesetzt !

Für die Anlage wurden nur ELRO-Funksteckdosn (433 Mhz, einstellbarer System/Unit Code) verwendet.
Fuer die Pumpe im Orginalzustand & fuer das Ventil zerlegt, um den Schaltkreis besser bauen zu koennen.
Als Temperatursensoren kam der "DS18S20" (wasserdicht) zum Einsatz.
Als Ventil benuttze ich ein"Honywell VMM 3-Wege-Ventil".
Gebaut wurde die Anlage mit einem Zwischenverteiler nach ca. 10 Meter
(in diesem befinden sich zusätzliche Komponenten zur Steuerung der Poolbeleuchtung &ein zusätzlicher Funksende).
Die laengste Kabellaenge zu einem der Temperatursensoren betraegt ca 20-22 Meter.
**Die Sensorik wird komplett aus dem 3.3V Pool des Raspi gespeist.**


**<Beschreibung der Schaltkreise folgt.>**


