# LBPanel -- Linux-Box Panel.
# Copyright (C) www.linux-box.es
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of   
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU gv; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
# 
# Author: lucifer
#         iqas
#
# Internet: www.linux-box.es
# Based on original source by epanel for openpli

from enigma import *
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Sources.List import List
from Tools.Directories import crawlDirectory, resolveFilename, SCOPE_CURRENT_SKIN
from Components.Button import Button
from Components.config import config, ConfigElement, ConfigSubsection, ConfigSelection, ConfigSubList, getConfigListEntry, KEY_LEFT, KEY_RIGHT, KEY_OK
import ExtraActionBox
import sys
from Screens.Screen import Screen
from Screens.PluginBrowser import PluginBrowser
from Components.PluginComponent import plugins
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Label import Label
from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Tools.Directories import fileExists
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from os import environ
import os
import gettext
import LBCamEmu
import LBipk
import LBtools
import LBDaemonsList
from enigma import eEPGCache
from types import *
from enigma import *
import sys, traceback
import re
import time
import new
import _enigma
import enigma
import smtplib
#import resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/libs/OscamInfo/oscaminfo.py")
#from Plugins.Extensions.LCDselector.plugin import *

global min
min = 0

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("messages", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/LBpanel/locale/"))

def _(txt):
	t = gettext.dgettext("LBpanel", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

##################################################################
config.plugins.epanel.showmain = ConfigYesNo(default = True)
config.plugins.epanel.showepanelmenu = ConfigYesNo(default = True)
config.plugins.epanel.showextsoft = ConfigYesNo(default = True)
config.plugins.epanel.shownclsw = ConfigYesNo(default = False)
config.plugins.epanel.showwcsw = ConfigYesNo(default = False)
config.plugins.epanel.showclviewer = ConfigYesNo(default = False)
config.plugins.epanel.showscriptex = ConfigYesNo(default = False)
config.plugins.epanel.showusbunmt = ConfigYesNo(default = False)
config.plugins.epanel.showsetupipk = ConfigYesNo(default = False)
config.plugins.epanel.showpbmain = ConfigYesNo(default = False)
config.plugins.epanel.filtername = ConfigYesNo(default = False)
##################################################################

# Generic function to send email
def sendemail(from_addr, to_addr, cc_addr,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % to_addr
    header += 'Cc: %s\n' % cc_addr
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr, message)
    server.quit()


class easyPanel2(Screen):
	skin = """
<screen name="easyPanel2" position="70,35" size="1150,650">
#<ePixmap position="705,640" zPosition="2" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
#<widget source="key_red" render="Label" position="705,610" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
#<ePixmap position="885,640" zPosition="2" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
#<widget source="key_green" render="Label" position="875,610" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
#<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo.png" alphatest="blend" transparent="1" />
<widget source="menu" render="Listbox" position="15,10" size="660,650" scrollbarMode="showOnDemand">
<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (200, 25), size = (600, 65), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (210, 75), size = (600, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (7, 7), size = (115, 115), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 30),gFont("Regular", 16)],
	"itemHeight": 125
	}
	</convert>
	</widget>
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions", "EPGSelectActions"],
		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.keyGreen,
			"yellow": self.keyYellow,
			"blue": self.keyBlue,
			
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("CamEmu"))
		self["key_yellow"] = StaticText(_("LBTools"))
		self["key_blue"] = StaticText(_("Install"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/softcams.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/cardserver.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/tools.png"))
		backuppng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/backup.png"))
		trespng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/seleck.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/install.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/epp2.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/system.png"))
		sevenpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/addon.png"))
		cuatropng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/daemons.png"))
		cincopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/infop.png"))
		self.list.append((_("PANEL EMULADORAS"),"com_one", _("CamEmu start-stop, Test Emu Control, Info Emus"), onepng))
		self.list.append((_("PANEL SERVICIOS"),"com_two", _("Epg,Ntp,script,info ..."), twopng ))
		self.list.append((_("PANEL SISTEMA"),"com_six", _("modulos Kernel,swap,ftp,samba,crond,usb"), sixpng ))
		#self.list.append((_("Skins LCD Selector"),"com_tres", _("Seleccioanar Skins LCD"), trespng ))
		self.list.append((_("INSTALADOR PAQUETES"),"com_four", _("Instalar,desistalar ipk,tar.gz en /tmp"), treepng))
		self.list.append((_("COMPLEMENTOS"),"com_seven", _("Interfaz Plugin"), sevenpng))
		#self.list.append((_("LB Daemons"),"com_cuatro", _("Lista Daemons"), cuatropng))
		#self.list.append((_("Info Panel"),"com_cinco", _("Informacion Panel"), cincopng))
		self["menu"].setList(self.list)


	def exit(self):
		self.close()

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "com_one":
				self.session.open(LBCamEmu.CamEmuPanel)
			elif returnValue is "com_two":
				self.session.open(LBtools.ToolsScreen)
			elif returnValue is "com_tree":
				self.session.open(backup.BackupSuite)
			#elif returnValue is "com_tres":
				#self.session.open(LCDselectorScreen)
			elif returnValue is "com_four":
				self.session.open(LBipk.IPKToolsScreen)
			elif returnValue is "com_five":
				self.session.open(ConfigExtentions)
			elif returnValue is "com_six":
				self.session.open(LBtools.SystemScreen)
			elif returnValue is "com_seven":
				self.session.open(PluginBrowser)
			#elif returnValue is "com_cuatro":
				#self.session.open(LBDaemonsList.LBDaemonsList)
			#elif returnValue is "com_cinco":
				#self.session.open(info)
			else:
				print "\n[LBpanel] cancel\n"
				self.close(None)

	def keyBlue (self):
		self.session.open(LBipk.IPKToolsScreen)
				
	def keyYellow (self):
		self.session.open(LBtools.ToolsScreen)
		
	def keyGreen (self):
		self.session.open(LBCamEmu.emuSel2)
	
	def infoKey (self):
		self.session.openWithCallback(self.mList,info)
		
##########################################################################################
class info(Screen):
	skin = """
<screen name="info" position="center,105" size="600,570" title="LBpanel">
	<ePixmap position="20,562" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,532" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="MemoryLabel" render="Label" position="20,375" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="SwapLabel" render="Label" position="20,400" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="FlashLabel" render="Label" position="20,425" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="memTotal" render="Label" position="180,375" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="swapTotal" render="Label" position="180,400" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="flashTotal" render="Label" position="180,425" zPosition="2" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="deviceLabel" render="Label" position="20,250" size="200,22" font="Regular; 20" halign="left" foregroundColor="#aaaaaa" />
	<widget source="device" render="Label" position="20,275" zPosition="2" size="560,88" font="Regular;20" halign="left" valign="top" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Hardware" render="Label" position="230,10" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Image" render="Label" position="230,35" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Kernel" render="Label" position="230,60" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="EnigmaVersion" render="Label" position="230,110" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="HardwareLabel" render="Label" position="20,10" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="ImageLabel" render="Label" position="20,35" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="KernelLabel" render="Label" position="20,59" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="EnigmaVersionLabel" render="Label" position="20,110" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="nimLabel" render="Label" position="20,145" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="nim" render="Label" position="20,170" zPosition="2" size="500,66" font="Regular;20" halign="left" valign="top" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="driver" render="Label" position="230,85" zPosition="2" size="200,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="driverLabel" render="Label" position="20,85" zPosition="2" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<eLabel position="30,140" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,242" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,367" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="30,454" size="540,2" backgroundColor="#aaaaaa" />
	<eLabel position="230,494" size="320,2" backgroundColor="#aaaaaa" />
	<ePixmap position="20,463" size="180,47" zPosition="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/2boom.png" alphatest="blend" />
	<widget source="panelver" render="Label" position="470,463" zPosition="2" size="100,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="LBpanel" render="Label" position="215,463" zPosition="2" size="250,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="cardserver" render="Label" position="350,528" zPosition="2" size="225,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="cardserverLabel" render="Label" position="215,528" zPosition="2" size="130,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
	<widget source="softcam" render="Label" position="350,503" zPosition="2" size="225,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="softcamLabel" render="Label" position="215,503" zPosition="2" size="130,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#aaaaaa" transparent="1" />
 </screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.cancel,
			"ok": self.cancel,
			})
		self["key_red"] = StaticText(_("Close"))
		self["MemoryLabel"] = StaticText(_("Memory:"))
		self["SwapLabel"] = StaticText(_("Swap:"))
		self["FlashLabel"] = StaticText(_("Flash:"))
		self["memTotal"] = StaticText()
		self["swapTotal"] = StaticText()
		self["flashTotal"] = StaticText()
		self["device"] = StaticText()
		self["deviceLabel"] = StaticText(_("Devices:"))
		self["Hardware"] = StaticText()
		self["Image"] = StaticText()
		self["Kernel"] = StaticText()
		self["nim"] = StaticText()
		self["nimLabel"] = StaticText(_("Detected NIMs:"))
		self["EnigmaVersion"] = StaticText()
		self["HardwareLabel"] = StaticText(_("Hardware:"))
		self["ImageLabel"] = StaticText(_("Image:"))
		self["KernelLabel"] = StaticText(_("Kernel Version:"))
		self["EnigmaVersionLabel"] = StaticText(_("Last Upgrade:"))
		self["driver"] = StaticText()
		self["driverLabel"] = StaticText(_("Driver Version:"))
		self["LBpanel"] = StaticText(_("LBpanel Ver: 1.1"))
		self["panelver"] = StaticText()
		self["softcamLabel"] = StaticText(_("Softcam:"))
		self["softcam"] = StaticText()
		self["cardserverLabel"] = StaticText(_("Cardserver:"))
		self["cardserver"] = StaticText()
		self.memInfo()
		self.FlashMem()
		self.devices()
		self.mainInfo()
		self.verinfo()
		self.emuname()
		
	def status(self):
		path = ' '
		if fileExists("/usr/lib/opkg/status"):
			path = "/usr/lib/opkg/status"
		elif fileExists("/var/lib/opkg/status"):
			path = "/var/lib/opkg/status"
		return path
		
	def emuname(self):
		nameemu = []
		namecard = []
		if fileExists("/etc/init.d/softcam"):
			try:
				for line in open("/etc/init.d/softcam"):
					if line.find("echo") > -1:
						nameemu.append(line)
				self["softcam"].text = "%s" % nameemu[1].split('"')[1]
			except:
				self["softcam"].text = _("Not Active")
		else:
			self["softcam"].text = _("Not Installed")
		if fileExists("/etc/init.d/cardserver"):
			try:
				for line in open("/etc/init.d/cardserver"):
					if line.find("echo") > -1:
						namecard.append(line)
				self["cardserver"].text = "%s" % namecard[1].split('"')[1]
			except:
				self["cardserver"].text = _("Not Active")
		else:
			self["cardserver"].text = _("Not Installed")
		
	def devices(self):
		list = ""
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				hdd = hddlist[count][1]
				if int(hdd.free()) > 1024:
					list += ((_("%s  %s  (%d.%03d GB free)\n") % (hdd.model(), hdd.capacity(), hdd.free()/1024 , hdd.free()%1024)))
				else:
					list += ((_("%s  %s  (%03d MB free)\n") % (hdd.model(), hdd.capacity(),hdd.free())))
		else:
			hddinfo = _("none")
		self["device"].text = list
		
	def mainInfo(self):
		listnims = ""
		package = 0
		self["Hardware"].text = about.getHardwareTypeString()
		self["Image"].text = about.getImageTypeString()
		self["Kernel"].text = about.getKernelVersionString()
		self["EnigmaVersion"].text = about.getImageVersionString()
		nims = nimmanager.nimList()
		for count in range(len(nims)):
			if count < 4:
				listnims += "%s\n" % nims[count]
			else:
				listnims += "\n"
		self["nim"].text = listnims
		for line in open(self.status()):
			if line.find("-dvb-modules") > -1 and line.find("Package:") > -1:
				package = 1
			if line.find("Version:") > -1 and package == 1:
				package = 0
				try:
					self["driver"].text = line.split()[1]
				except:
					self["driver"].text = " "
				break

	def memInfo(self):
		mem = open("/proc/meminfo", "r")
		for line in mem:
			if line.find("MemTotal:") > -1:
				memtotal = line.split()[1]
			elif line.find("MemFree:") > -1:
				memfree = line.split()[1]
			elif line.find("SwapTotal:") > -1:
				swaptotal =  line.split()[1]
			elif line.find("SwapFree:") > -1:
				swapfree = line.split()[1]
		self["memTotal"].text = _("Total: %s Kb  Free: %s Kb") % (memtotal, memfree)
		self["swapTotal"].text = _("Total: %s Kb  Free: %s Kb") % (swaptotal, swapfree)
		mem.close()
		
	def FlashMem(self):
		flash = os.popen("df | grep root")
		try:
			for line in flash:
				if line.find("root") > -1:
					self["flashTotal"].text = _("Total: %s Kb  Free: %s Kb") % (line.split()[1], line.split()[3])
		except:
			pass
		
	def verinfo(self):
		package = 0
		self["panelver"].text = " "
		for line in open(self.status()):
			if line.find("easyLBpanel") > -1:
				package = 1
			if line.find("Version:") > -1 and package == 1:
				package = 0
				try:
					self["panelver"].text = line.split()[1]
				except:
					self["panelver"].text = " "
				break

		
	def cancel(self):
		self.close()
####################################################################
class ConfigExtentions(ConfigListScreen, Screen):
	skin = """
<screen name="ConfigExtentions" position="center,160" size="750,370" title="LBpanel Menu/Extensionmenu config">
		<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="340,358" zPosition="1" size="230,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
		<widget source="key_yellow" render="Label" position="340,328" zPosition="2" size="230,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel Menu/Extensionmenu config"))
		self.list = []
		self.list.append(getConfigListEntry(_("Show E-Panel in MainMenu"), config.plugins.epanel.showmain))
		self.list.append(getConfigListEntry(_("Show E-Panel in ExtensionMenu"), config.plugins.epanel.showepanelmenu))
		self.list.append(getConfigListEntry(_("Show CamEmu Manager in ExtensionMenu"), config.plugins.epanel.showextsoft))
		self.list.append(getConfigListEntry(_("Show E-NewCamd.list switcher in ExtensionMenu"), config.plugins.epanel.shownclsw))
		self.list.append(getConfigListEntry(_("Show E-Wicardd.conf switcher in ExtensionMenu"), config.plugins.epanel.showwcsw))
		self.list.append(getConfigListEntry(_("Show E-CrashLog viewr in ExtensionMenu"), config.plugins.epanel.showclviewer))
		self.list.append(getConfigListEntry(_("Show E-Script Executter in ExtensionMenu"), config.plugins.epanel.showscriptex))
		self.list.append(getConfigListEntry(_("Show E-Usb Unmount in ExtensionMenu"), config.plugins.epanel.showusbunmt))
		self.list.append(getConfigListEntry(_("Show E-Installer in ExtensionMenu"), config.plugins.epanel.showsetupipk))
		self.list.append(getConfigListEntry(_("Show PluginBrowser in E-Panel MainMenu"), config.plugins.epanel.showpbmain))
		self.list.append(getConfigListEntry(_("Filter by Name in download extentions"), config.plugins.epanel.filtername))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Restart GUI"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.restart_einigma,
			"ok": self.save
		}, -2)
		
	def cancel(self):
		self.close(False)
		
	def restart_einigma(self):
		self.session.open(TryQuitMainloop, 3)
	
	def save(self):
		config.plugins.epanel.showmain.save()
		config.plugins.epanel.showepanelmenu.save()
		config.plugins.epanel.showextsoft.save()
		config.plugins.epanel.shownclsw.save()
		config.plugins.epanel.showwcsw.save()
		config.plugins.epanel.showclviewer.save()
		config.plugins.epanel.showscriptex.save()
		config.plugins.epanel.showusbunmt.save()
		config.plugins.epanel.showsetupipk.save()
		config.plugins.epanel.showpbmain.save()
		config.plugins.epanel.filtername.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
####################################################################
## Cron especific function for lbpanel
class lbCron():
	def __init__(self):
		self.dialog = None

	def gotSession(self, session):
		self.session = session
		self.timer = enigma.eTimer() 
		self.timer.callback.append(self.update)
		self.timer.start(60000, True)

	def update(self):
		self.timer.stop()
		now = time.localtime(time.time())
		# cron control epg
		if (config.plugins.epanel.auto.value == "yes" and config.plugins.epanel.epgtime.value[0] == now.tm_hour and config.plugins.epanel.epgtime.value[1] == now.tm_min):
			self.dload()
		# cron control scan peer
		if (config.plugins.epanel.checkauto.value == "yes" and config.plugins.epanel.checkhour.value[0] == now.tm_hour and config.plugins.epanel.checkhour.value[1] == now.tm_min):
			self.scanpeer()
                #cron for send email
                if (config.plugins.epanel.lbemail.value and os.path.isfile("/tmp/.lbscan.end")):
                	os.remove("/tmp/.lbscan.end")
                	msg = ""
                        scaninfo = open("/tmp/.lbscan.log", "r")
                        for line in scaninfo:
                               msg += line  
			
			scaninfo.close()
                	sendemail(config.plugins.epanel.smtpuser.value, config.plugins.epanel.lbemailto.value,"", "Scan report from LBpanel",msg,config.plugins.epanel.smtpuser.value,config.plugins.epanel.smtppass.value)
                                                               			
		if config.plugins.epanel.autosave.value != '0':
			if min > int(config.plugins.epanel.autosave.value) and config.plugins.epanel.epgtime.value[1] != now.tm_min:
				global min
				min = 0
				self.save_load_epg()
				if config.plugins.epanel.autobackup.value:
					self.autobackup()
			else:
				global min
				min = min + 1
		self.timer.start(60000, True)
		
	def autobackup(self):
		os.system("gzip -c %sepg.dat > %sepgtmp/epg.dat.gz" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value))
		
	def save_load_epg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
		epgcache = eEPGCache.getInstance().load()

	def scanpeer(self):
		os.system("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/lbscan.py %s %s %s %s &" % (config.plugins.epanel.checktype.value, config.plugins.epanel.autocheck.value, config.plugins.epanel.checkoff.value, config.plugins.epanel.warnonlyemail.value))
	
	def dload(self):
		try:
                        os.system("wget -q http://www.linux-box.es/epg/epg.dat.gz -O %sepg.dat.gz" % (config.plugins.epanel.direct.value))
                        if fileExists("%sepg.dat" % config.plugins.epanel.direct.value):
                                os.unlink("%sepg.dat" % config.plugins.epanel.direct.value)
                                os.system("rm -f %sepg.dat" % config.plugins.epanel.direct.value)
                        if not os.path.exists("%sepgtmp" % config.plugins.epanel.direct.value):  
                                os.system("mkdir -p %sepgtmp" % config.plugins.epanel.direct.value)
                        os.system("cp -f %sepg.dat.gz %sepgtmp" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value))
                        os.system("gzip -df %sepg.dat.gz" % config.plugins.epanel.direct.value)
                        os.chmod("%sepg.dat" % config.plugins.epanel.direct.value, 0644)
                        self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
                        epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
                        epgcache = eEPGCache.getInstance().load()

#			os.system("wget -q http://www.xmltvepg.be/dplus/epg.dat.gz -O %sepg.dat.gz" % (config.plugins.epanel.lang.value, config.plugins.epanel.direct.value))
#			if fileExists("%sepg.dat" % config.plugins.epanel.direct.value):
#				os.unlink("%sepg.dat" % config.plugins.epanel.direct.value)
#				os.system("rm -f %sepg.dat" % config.plugins.epanel.direct.value)
#			if not os.path.exists("%sepgtmp" % config.plugins.epanel.direct.value):
#				os.system("mkdir -p %sepgtmp" % config.plugins.epanel.direct.value)
#			os.system("cp -f %sepg.dat.gz %sepgtmp" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value))
#			os.system("gzip -df %sepg.dat.gz" % config.plugins.epanel.direct.value)
#			if fileExists("%sepg.dat" % config.plugins.epanel.direct.value):
#				os.chmod("%sepg.dat" % config.plugins.epanel.direct.value, 0644)
#			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
#			epgcache = eEPGCache.getInstance().load()
#			self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )
#####################################################
def main(session, **kwargs):
	session.open(epgdn2)
##############################################################################
pEmu = lbCron()
##############################################################################
def sessionstart(reason,session=None, **kwargs):
	if reason == 0:
		pEmu.gotSession(session)
##############################################################################
def main(session, **kwargs):
	session.open(easyPanel2)

def menu(menuid, **kwargs):
	if menuid == "mainmenu":
		return [(_("LBpanel"), main, _("e-panel_for_pli"), 48)]
	return []

def extsoft(session, **kwargs):
	session.open(LBCamEmu.emuSel2)
	
def nclsw(session, **kwargs):
	session.open(LBCamEmu.NCLSwp2)
	
def wcsw(session, **kwargs):
	session.open(LBCamEmu.wicconfsw)
	
def clviewer(session, **kwargs):
	session.open(LBtools.CrashLogScreen)
	
def scriptex(session, **kwargs):
	session.open(LBtools.ScriptScreen)
	
def usbunmt(session, **kwargs):
	session.open(LBtools.UsbScreen)
	
def setupipk(session, **kwargs):
	session.open(LBipk.InstallAll)
	
def Plugins(**kwargs):
	list = [PluginDescriptor(name=_("LBpanel"), description=_("simple tools para LBTEAM"), where = [PluginDescriptor.WHERE_PLUGINMENU], icon="LBpanel.png", fnc=main)]
	if config.plugins.epanel.showepanelmenu.value:
		list.append(PluginDescriptor(name=_("LBpanel"), description=_("simple tools for Pli image"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=main))
	if config.plugins.epanel.showextsoft.value:
		list.append(PluginDescriptor(name=_("CamEmu Manager"), description=_("Start, Stop, Restart Sofcam/Cardserver"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=extsoft))
	if config.plugins.epanel.shownclsw.value:
		list.append(PluginDescriptor(name=_("E-Newcamd.list switcher"), description=_("Switch newcamd.list with remote conrol"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=nclsw))
	if config.plugins.epanel.showwcsw.value:
		list.append(PluginDescriptor(name=_("E-Wicardd.conf switcher"), description=_("Switch wicardd.conf with remote conrol"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=wcsw))
	if config.plugins.epanel.showclviewer.value:
		list.append(PluginDescriptor(name=_("E-Crashlog viewer"), description=_("Switch newcamd.list with remote conrol"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=clviewer))
	if config.plugins.epanel.showscriptex.value:
		list.append(PluginDescriptor(name=_("E-Script Executer"), description=_("Start scripts from /usr/script"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=scriptex))
	if config.plugins.epanel.showusbunmt.value:
		list.append(PluginDescriptor(name=_("E-Unmount USB"), description=_("Unmount usb devices"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=usbunmt))
	if config.plugins.epanel.showsetupipk.value:
		list.append(PluginDescriptor(name=_("E-Installer"), description=_("install & forced install ipk, bh.tgz, tar.gz, nab.tgz from /tmp"), where = [PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=setupipk))
	if config.plugins.epanel.showmain.value:
		list.append(PluginDescriptor(name=_("LBPanel"), description=_("LBTEAM EXTENSION 2.0"), where = [PluginDescriptor.WHERE_MENU], fnc=menu))
	list.append(PluginDescriptor(name=_("LBPanel"), description=_("LBTEAM EXTENSION 2.0"), where = [PluginDescriptor.WHERE_AUTOSTART, PluginDescriptor.WHERE_SESSIONSTART], fnc = sessionstart))
	return list


