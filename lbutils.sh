#!/bin/bash
# Utils for LBPanel 
# GNU GPL2+

case $1 in
# Test updates for LBpanel and LBpanel Settings
testupdate)
	opkg update
	if (opkg list-upgradable | grep enigma2-plugin-extensions-lbpanel); then
        	echo "LBpanel Update";
                opkg install enigma2-plugin-extensions-lbpanel
                echo "." > /tmp/.lbpanel.update
        fi
                       
        if (opkg list-upgradable | grep enigma2-plugin-settings-sorys); then    
        	echo "LBsettings Update";
                echo "." > /tmp/.lbsettings.update
                for arg in `opkg list-installed | grep enigma2-plugin-settings-sorys | awk '{print $1}'` ; do
                	opkg install  $arg ;
                done;
        fi
                                                                
                                                                
	exit 0
	;;
	
#Download epg
epgdown)
	wget -q http://www.linux-box.es/epg/epg.dat.gz -O $2epg.dat.gz
	cp $2epg.dat.gz $2epg.dat.gz.copia
	rm -f $2epg.dat
	gzip -df $2epg.dat.gz $2	
	exit 0
	;;
	
*)
	echo "Usage: lbutils.sh <util> [<option1>] [<option2>]" ;
	exit 1
	;;	
esac