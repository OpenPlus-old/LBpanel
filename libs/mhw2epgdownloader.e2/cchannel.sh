#!/bin/sh

#-------------------------------------------------------------------
# EPG
# Pigital+
# Astra 19.2
#
#-------------------------------------------------------------------

cd /usr/lib/enigma2/python/Plugins/Extensions/LBpanel/libs/mhw2epgdownloader.e2
# Cambiar al canal guia pigital
DELAY=1
#BAR
#CHANNEL=1:0:1:75B1:422:1:C00000:0:0:0:
CHANNEL=1:0:1:759C:422:1:C00000:0:0:0:
#BASEDIR=$(dirname $0)
#echo $BASEDIR
#cd $BASEDIR

echo "Cambio al canal guia pigital"
wget -q http://localhost/web/zap?sRef=$CHANNEL > /dev/null

echo "espera de $DELAY segundos"
sleep $DELAY


