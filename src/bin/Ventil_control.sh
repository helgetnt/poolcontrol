#! /bin/bash

dir=${0::-21}
conf="config.py"

source $dir$conf

SECS=3
countdown()
(
  while [[ 0 -ne $SECS ]]; do
    echo "$SECS.."
    sleep 1
    SECS=$[$SECS-1]
  done;
);

SEC=$Latenz
Timer()
(
  befehl=$1" "$2" "$3" "$4" "$5
  while [[ 0 -ne $SEC ]]; do
  $befehl
  SEC=$[$SEC-1]
  done;
);

Zustand()
(
    for i in $(cat $RAM_DIR${Ventilzustand:8}); do
    echo $i                                  #test
    if [ $i = "0" ]; then
         echo "Ventil steht auf Zirkulieren.";
    elif [ $i = "100" ]; then
         echo "Ventil steht auf Solar.";
    elif [ $i = "50" ]; then
         echo "Ventil steht auf 50%.";
    else echo "Ventilzustand.TNT ......Datei nicht gefunden oder undefinierbarer Zustand !!! ";
    fi
    done;
);

case "$1" in
  test)
    echo ""
    echo "$dir$conf"
    echo "$dir"
    echo ""
    ;;
  VS50)
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Solar_an & sleep 0.1
    Timer $Ventil_Zirkulieren_aus
    sleep $Ventil_Halb
    $Ventil_Solar_aus & sleep 0.1
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Zirkulieren_aus & sleep 0.2
    #echo "VC.sh -> Ventil steht auf 50% Solar."
    ;;
  VS100)
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Solar_an &  sleep 0.1
    Timer $Ventil_Zirkulieren_aus
    sleep $Ventil_Voll
    $Ventil_Solar_aus & sleep 0.1
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Zirkulieren_aus & sleep 0.2
    $Ventil_Zirkulieren_aus & sleep 0.2
    #echo "VC.sh -> Ventil steht auf 100% Solar."
    ;;
  VZ50)
    #echo "VC.sh -> Ventil wird jetzt auf 50% Zirkulieren gestellt."
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Zirkulieren_an & sleep 0.1
    Timer $Ventil_Solar_aus
    sleep $Ventil_Halb
    $Ventil_Zirkulieren_aus & sleep 0.1
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Solar_aus & sleep 0.2
    #echo "VC.sh -> Ventil steht auf 50% Zirkulieren."
    ;;
  VZ100)
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Zirkulieren_an & sleep 0.1
    Timer $Ventil_Solar_aus
    sleep $Ventil_Voll
    $Ventil_Zirkulieren_aus & sleep 0.1
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Solar_aus & sleep 0.2
    $Ventil_Solar_aus & sleep 0.2
    #echo "VC.sh -> Ventil steht auf 100% Zirkulieren."
    ;;
  Zustand)
    Zustand
    ;;

 *)
    echo "-----------------------------------------------------------"
    echo "Optionen: VS50 | VS100 | VZ50 | VZ100 | Zustand | test" >&2
    echo "-----------------------------------------------------------"
    echo "VS50            |Ventil auf  50% Solar stellen"
    echo "VS100           |Ventil auf 100% Solar stellen"
    echo "VZ50            |Ventil auf  50% Zirkulieren stellen"
    echo "VZ100           |Ventil auf 100% Zirkulieren stellen"
    echo ""
    echo "Zustand         |VentilStand 0|50|100% auf Solar"
    echo "test            |echo -> Config & Config_dir"
    exit 3
    ;;
esac
