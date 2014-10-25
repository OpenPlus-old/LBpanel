#!/bin/sh

#-------------------------------------------------------------------
# EPG
# Pigital+
# Astra 19.2
#
#-------------------------------------------------------------------

cd /usr/lib/enigma2/python/Plugins/Extensions/LBpanel/libs/mhw2epgdownloader.e2
# Cambiar al canal guia pigital
DELAY=3
#BAR
#CHANNEL=1:0:1:75B1:422:1:C00000:0:0:0:
CHANNEL=1:0:1:759C:422:1:C00000:0:0:0:
#BASEDIR=$(dirname $0)
#echo $BASEDIR
#cd $BASEDIR

echo "Cambio al canal guia pigital"
killall -9 wget
#wget -Y off -O- -q http://localhost/web/zap?sRef=$CHANNEL > /dev/null

sleep 2
echo "espera de $DELAY segundos"
sleep $DELAY


echo "elimina los ejecutables que no se correspondan con la arguitectura de tu maquina"
echo "si no lo haces... da igual ;-) "
echo "solo se va ejecutar el que se corresponda con la arquitectura de tu maquina " 

#./mhw2epgdownloader.sh4
./mhw2epgdownloader.mips
#./mhw2epgdownloader.ppc
#./mhw2epgdownloader.x86

