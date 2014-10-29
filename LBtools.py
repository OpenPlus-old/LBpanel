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
# Swap code based on original alibabu

from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Components.Sources.StaticText import StaticText
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo,  config, configfile
from Components.ConfigList import ConfigListScreen
from Components.Harddisk import harddiskmanager
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.Input import Input
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Components.ScrollLabel import ScrollLabel
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigSelection, ConfigSubsection, ConfigYesNo
from Components.ConfigList import ConfigListScreen
from ServiceReference import ServiceReference
from time import *
from enigma import eEPGCache
from types import *
from enigma import *
import sys, traceback
import re
import new
import _enigma
import time
import datetime
from os import environ
import os
import gettext
import MountManager
import RestartNetwork

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("messages", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/LBpanel/locale/"))

def mountp():
	pathmp = []
	if fileExists("/proc/mounts"):
		for line in open("/proc/mounts"):
			if line.find("/dev/sd") > -1:
				pathmp.append(line.split()[1].replace('\\040', ' ') + "/")
	pathmp.append("/usr/share/enigma2/")
	return pathmp

def _(txt):
	t = gettext.dgettext("messages", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
######################################################################################
config.plugins.lbpanel = ConfigSubsection()
config.plugins.lbpanel.scriptpath = ConfigSelection(default = "/usr/CamEmu/script/", choices = [
		("/usr/CamEmu/script/", _("/usr/CamEmu/script/")),
		("/media/hdd/script/", _("/media/hdd/script/")),
		("/media/usb/script/", _("/media/usb/script/")),
])
config.plugins.lbpanel.scriptpath1 = ConfigSelection(default = "/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/script/libmem/", choices = [
		("/usr/script/", _("/usr/script/")),
		("/media/hdd/script/", _("/media/hdd/script/")),
		("/media/usb/script/", _("/media/usb/script/")),
])
config.plugins.lbpanel.direct = ConfigSelection(default = "/media/hdd/", choices = [
		("/media/hdd/", _("/media/hdd/")),
		("/media/usb/", _("/media/usb/")),
		("/usr/share/enigma2/", _("/usr/share/enigma2/")),
		("/media/cf/", _("/media/cf/")),
])
config.plugins.lbpanel.auto = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.lbpanel.auto2 = ConfigSelection(default = "no", choices = [
                ("no", _("no")),
		("yes", _("yes")),
		])
                                                
config.plugins.lbpanel.lang = ConfigSelection(default = "es", choices = [
		("es", _("spain d+")),
		])
config.plugins.lbpanel.epgtime = ConfigClock(default = ((16*60) + 15) * 60) # 18:15
config.plugins.lbpanel.epgtime2 = ConfigClock(default = ((16*60) + 15) * 60)
#config.plugins.lbpanel.weekday = ConfigSelection(default = "01", choices = [
#		("00", _("Mo")),
#		("01", _("Tu")),
#		("02", _("We")),
#		("03", _("Th")),
#		("04", _("Fr")),
#		("05", _("Sa")),
#		("06", _("Su")),
#		])
######################################################################
config.plugins.lbpanel.min = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("5", "5"),
		("10", "10"),
		("15", "15"),
		("20", "20"),
		("25", "25"),
		("30", "30"),
		("35", "35"),
		("40", "40"),
		("45", "45"),
		("50", "50"),
		("55", "55"),
		])
config.plugins.lbpanel.hour = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("0", "0"),
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
		("9", "9"),
		("10", "10"),
		("11", "11"),
		("12", "12"),
		("13", "13"),
		("14", "14"),
		("15", "15"),
		("16", "16"),
		("17", "17"),
		("18", "18"),
		("19", "19"),
		("20", "20"),
		("21", "21"),
		("22", "22"),
		("23", "23"),
		])
config.plugins.lbpanel.dayofmonth = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
		("9", "9"),
		("10", "10"),
		("11", "11"),
		("12", "12"),
		("13", "13"),
		("14", "14"),
		("15", "15"),
		("16", "16"),
		("17", "17"),
		("18", "18"),
		("19", "19"),
		("20", "20"),
		("21", "21"),
		("22", "22"),
		("23", "23"),
		("24", "24"),
		("25", "25"),
		("26", "26"),
		("27", "27"),
		("28", "28"),
		("29", "29"),
		("30", "30"),
		("31", "31"),
		])
config.plugins.lbpanel.month = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("1", _("Jan.")),
		("2", _("Feb.")),
		("3", _("Mar.")),
		("4", _("Apr.")),
		("5", _("May")),
		("6", _("Jun.")),
		("7", _("Jul")),
		("8", _("Aug.")),
		("9", _("Sep.")),
		("10", _("Oct.")),
		("11", _("Nov.")),
		("12", _("Dec.")),
		])
config.plugins.lbpanel.dayofweek = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("0", _("Su")),
		("1", _("Mo")),
		("2", _("Tu")),
		("3", _("We")),
		("4", _("Th")),
		("5", _("Fr")),
		("6", _("Sa")),
		])
config.plugins.lbpanel.command = ConfigText(default="/usr/bin/", visible_width = 70, fixed_size = False)
config.plugins.lbpanel.every = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Min")),
		("2", _("Hour")),
		("3", _("Day of month")),
		("4", _("Month")),
		("5", _("Day of week")),
		])
######################################################################################
config.plugins.lbpanel.manual = ConfigSelection(default = "0", choices = [
		("0", _("Auto")),
		("1", _("Manual")),
		])
config.plugins.lbpanel.manualserver = ConfigText(default="ntp.ubuntu.com", visible_width = 70, fixed_size = False)
config.plugins.lbpanel.server = ConfigSelection(default = "es.pool.ntp.org", choices = [
		("ao.pool.ntp.org",_("Angola")),
		("mg.pool.ntp.org",_("Madagascar")),
		("za.pool.ntp.org",_("South Africa")),
		("tz.pool.ntp.org",_("Tanzania")),
		("bd.pool.ntp.org",_("Bangladesh")),
		("cn.pool.ntp.org",_("China")),
		("hk.pool.ntp.org",_("Hong Kong")),
		("in.pool.ntp.org",_("India")),
		("id.pool.ntp.org",_("Indonesia")),
		("ir.pool.ntp.org",_("Iran")),
		("jp.pool.ntp.org",_("Japan")),
		("kz.pool.ntp.org",_("Kazakhstan")),
		("kr.pool.ntp.org",_("Korea")),
		("my.pool.ntp.org",_("Malaysia")),
		("pk.pool.ntp.org",_("Pakistan")),
		("ph.pool.ntp.org",_("Philippines")),
		("sg.pool.ntp.org",_("Singapore")),
		("tw.pool.ntp.org",_("Taiwan")),
		("th.pool.ntp.org",_("Thailand")),
		("tr.pool.ntp.org",_("Turkey")),
		("ae.pool.ntp.org",_("United Arab Emirates")),
		("uz.pool.ntp.org",_("Uzbekistan")),
		("vn.pool.ntp.org",_("Vietnam")),
		("at.pool.ntp.org",_("Austria")),
		("by.pool.ntp.org",_("Belarus")),
		("be.pool.ntp.org",_("Belgium")),
		("bg.pool.ntp.org",_("Bulgaria")),
		("cz.pool.ntp.org",_("Czech Republic")),
		("dk.pool.ntp.org",_("Denmark")),
		("ee.pool.ntp.org",_("Estonia")),
		("fi.pool.ntp.org",_("Finland")),
		("fr.pool.ntp.org",_("France")),
		("de.pool.ntp.org",_("Germany")),
		("gr.pool.ntp.org",_("Greece")),
		("hu.pool.ntp.org",_("Hungary")),
		("ie.pool.ntp.org",_("Ireland")),
		("it.pool.ntp.org",_("Italy")),
		("lv.pool.ntp.org",_("Latvia")),
		("lt.pool.ntp.org",_("Lithuania")),
		("lu.pool.ntp.org",_("Luxembourg")),
		("mk.pool.ntp.org",_("Macedonia")),
		("md.pool.ntp.org",_("Moldova")),
		("nl.pool.ntp.org",_("Netherlands")),
		("no.pool.ntp.org",_("Norway")),
		("pl.pool.ntp.org",_("Poland")),
		("pt.pool.ntp.org",_("Portugal")),
		("ro.pool.ntp.org",_("Romania")),
		("ru.pool.ntp.org",_("Russian Federation")),
		("sk.pool.ntp.org",_("Slovakia")),
		("si.pool.ntp.org",_("Slovenia")),
		("es.pool.ntp.org",_("Spain")),
		("se.pool.ntp.org",_("Sweden")),
		("ch.pool.ntp.org",_("Switzerland")),
		("ua.pool.ntp.org",_("Ukraine")),
		("uk.pool.ntp.org",_("United Kingdom")),
		("bs.pool.ntp.org",_("Bahamas")),
		("ca.pool.ntp.org",_("Canada")),
		("gt.pool.ntp.org",_("Guatemala")),
		("mx.pool.ntp.org",_("Mexico")),
		("pa.pool.ntp.org",_("Panama")),
		("us.pool.ntp.org",_("United States")),
		("au.pool.ntp.org",_("Australia")),
		("nz.pool.ntp.org",_("New Zealand")),
		("ar.pool.ntp.org",_("Argentina")),
		("br.pool.ntp.org",_("Brazil")),
		("cl.pool.ntp.org",_("Chile")),
		])
config.plugins.lbpanel.onoff = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
config.plugins.lbpanel.time = ConfigSelection(default = "30", choices = [
		("30", _("30 min")),
		("1", _("60 min")),
		("2", _("120 min")),
		("3", _("180 min")),
		("4", _("240 min")),
		])
config.plugins.lbpanel.TransponderTime = ConfigSelection(default = "0", choices = [
		("0", _("Off")),
		("1", _("On")),
		])
config.plugins.lbpanel.cold = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
config.plugins.lbpanel.autosave = ConfigSelection(default = '0', choices = [
		('0', _("Off")),
		('29', _("30 min")),
		('59', _("60 min")),
		('119', _("120 min")),
		('179', _("180 min")),
		('239', _("240 min")),
		])
config.plugins.lbpanel.autobackup = ConfigYesNo(default = False)
######################################################################################
## lbscan section
config.plugins.lbpanel.checkauto = ConfigSelection(default = "no", choices = [
               ("yes", _("Yes")),
               ("no", _("No")), 
])
config.plugins.lbpanel.autocheck = ConfigSelection(default = "yes", choices = [
               ("yes", _("Yes")),   
               ("no", _("No")),    
 ])

config.plugins.lbpanel.checktype = ConfigSelection(default = "fast", choices = [
               ("fast", _("Fast")),   
               ("full", _("Full")),    
               ])
                              
config.plugins.lbpanel.checkhour = ConfigClock(default = ((18*60) + 30) * 60) # 20:30

config.plugins.lbpanel.checkoff = ConfigSelection(default = "yes", choices = [
               ("yes", _("Yes")),
               ("no", _("No")), 
])
config.plugins.lbpanel.lbemail = ConfigYesNo(default = False)
config.plugins.lbpanel.warnonlyemail = ConfigSelection(default = "yes", choices = [
               ("yes", _("Yes")),   
               ("no", _("No")), 
])                              
config.plugins.lbpanel.lbemailto = ConfigText(default = "mail@gmail.com",fixed_size = False, visible_width=30) 
config.plugins.lbpanel.smtpserver = ConfigText(default = "smtp.gmail.com:587",fixed_size = False, visible_width=30)
config.plugins.lbpanel.smtpuser = ConfigText(default = "I@gmail.com",fixed_size = False, visible_width=30)
config.plugins.lbpanel.smtppass = ConfigPassword(default = "mailpass",fixed_size = False, visible_width=15)

#####################################################################################

class ToolsScreen(Screen):
	skin = """
		<screen name="ToolsScreen" position="center,center" size="1150,600" title="LBpanel - Services">
		<ePixmap position="700,10" zPosition="1" size="450,590" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo7.png" alphatest="blend" transparent="1" />
	<ePixmap position="705, 580" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="705, 550" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="875, 550" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="885, 580" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />

	<widget source="menu" render="Listbox" position="15,10" size="660,580" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (200, 25), size = (600, 65), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (210, 75), size = (600, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (7, 7), size = (105, 105), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 30),gFont("Regular", 16)],
	"itemHeight": 105
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Services"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("HDD sleep"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/crash.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/info2.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/epg.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/script.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ntp.png"))
		sevenpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/libmemoria.png"))
		dospng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/net1.png"))
		eightpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/scan.png"))
		self.list.append((_("Tools Crashlog"),"com_one", _("Manage crashlog files"), onepng ))
		self.list.append((_("System Info"),"com_two", _("System info (free, dh -f)"), twopng ))
		self.list.append((_("Download D+ EPG"),"com_tree", _("Download D+ EPG"), treepng ))
		self.list.append((_("SAT Down D+ EPG"),"com_four", _("Download D+ EPG"), treepng ))
		self.list.append((_("Scan Peer Security"),"com_scan", _("Check host security"), eightpng ))
		self.list.append((_("NTP Sync"),"com_six", _("Ntp sync: 30 min,60 min,120 min, 240"), sixpng ))
		self.list.append((_("User Scripts"),"com_five", _("User Scripts"), fivepng ))
		self.list.append((_("Free Memory"),"com_seven", _("Launcher free memory"), sevenpng ))
		self.list.append((_("Network"),"com_dos", _("Restart network"), dospng ))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()
		
	def GreenKey(self):
		ishdd = open("/proc/mounts", "r")
		for line in ishdd:
			if line.find("/media/hdd") > -1:
				mountpointname = line.split()
				os.system("hdparm -y %s" % (mountpointname[0]))
				self.mbox = self.session.open(MessageBox,_("HDD go sleep"), MessageBox.TYPE_INFO, timeout = 4 )

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "com_one":
				self.session.openWithCallback(self.mList,CrashLogScreen)
			elif returnValue is "com_two":
				self.session.openWithCallback(self.mList,Info2Screen)
			elif returnValue is "com_tree":
				self.session.open(epgdn)
			elif returnValue is "com_four":
				self.session.open(epgscript)
			elif returnValue is "com_five":
				self.session.openWithCallback(self.mList, ScriptScreen)
			elif returnValue is "com_six":
				self.session.openWithCallback(self.mList, NTPScreen)
			elif returnValue is "com_seven":
				self.session.openWithCallback(self.mList,Libermen)
			elif returnValue is "com_dos":
				self.session.open(RestartNetwork.RestartNetwork)
			elif returnValue is "com_scan":
                                self.session.open(scanhost)
			else:
				print "\n[BackupSuite] cancel\n"
				self.close(None)
###############################################################################
class SwapScreen2(Screen):
	skin = """
		<screen name="SwapScreen2" position="center,160" size="1150,500" title="LBpanel - Swap Manager">
				  #<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo17.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Swap Manager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Menu,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.Menu()
		
	def Menu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swapminion.png"))
		for line in mountp():
			if line not in "/usr/share/enigma2/":
				try:
					if self.swapiswork() in line:
						self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minisonpng, line))
					else:
						self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
				except:
					self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.MenuDo, "cancel": self.close}, -1)
		
	def swapiswork(self):
		if fileExists("/proc/swaps"):
			for line in open("/proc/swaps"):
				if line.find("media") > -1:
					return line.split()[0][:-9]
		else:
			return " "
		
	def MenuDo(self):
		swppath = self["menu"].getCurrent()[3] + "swapfile"
		self.session.openWithCallback(self.Menu,SwapScreen, swppath)
	
	def exit(self):
		self.close()
####################################################################
class SwapScreen(Screen):
	skin = """
		<screen name="SwapScreen" position="center,160" size="1150,500" title="LBpanel - Swap Manager">
		  #<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo17.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session, swapdirect):
		self.swapfile = swapdirect
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Swap Manager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.CfgMenuDo,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()

	def isSwapPossible(self):
		for line in open("/proc/mounts"):
			fields= line.rstrip('\n').split()
			if fields[1] == "%s" % self.swapfile[:-9]:
				if fields[2] == 'ext2' or fields[2] == 'ext3' or fields[2] == 'ext4' or fields[2] == 'vfat':
					return 1
				else:
					return 0
		return 0
		
	def isSwapRun(self):
		try:
			for line in open('/proc/swaps'):
				if line.find(self.swapfile) > -1:
					return 1
			return 0
		except:
			pass
			
	def isSwapSize(self):
		try:
			swapsize = os.path.getsize(self.swapfile) / 1048576
			return ("%sMb" % swapsize)
		except:
			pass
			
	def makeSwapFile(self, size):
		try:
			os.system("dd if=/dev/zero of=%s bs=1024 count=%s" % (self.swapfile, size))
			os.system("mkswap %s" % (self.swapfile))
			self.mbox = self.session.open(MessageBox,_("Swap file created"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		except:
			pass
	
	def CfgMenu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swapminion.png"))
		if self.isSwapPossible():
			if os.path.exists(self.swapfile):
				if self.isSwapRun() == 1:
					self.list.append((_("Swap off"),"5", (_("Swap on %s off (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minisonpng))
				else:
					self.list.append((_("Swap on"),"4", (_("Swap on %s on (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
					self.list.append((_("Remove swap"),"7",( _("Remove swap on %s (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
			else:
				self.list.append((_("Make swap"),"11", _("Make swap on %s (128MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"12", _("Make swap on %s (256MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"13", _("Make swap on %s (512MB)") % self.swapfile[7:10].upper(), minispng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.CfgMenuDo, "cancel": self.close}, -1)
			
	def CfgMenuDo(self):
		m_choice = self["menu"].getCurrent()[1]
		if m_choice is "4":
			try:
				for line in open("/proc/swaps"):
					if  line.find("swapfile") > -1:
						os.system("swapoff %s" % (line.split()[0]))
			except:
				pass
			os.system("swapon %s" % (self.swapfile))
			os.system("sed -i '/swap/d' /etc/fstab")
			os.system("echo -e '%s/swapfile swap swap defaults 0 0' >> /etc/fstab" % self.swapfile[:10])
			self.mbox = self.session.open(MessageBox,_("Swap file started"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		elif m_choice is "5":
			os.system("swapoff %s" % (self.swapfile))
			os.system("sed -i '/swap/d' /etc/fstab")
			self.mbox = self.session.open(MessageBox,_("Swap file stoped"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		elif m_choice is "11":
			self.makeSwapFile("131072")

		elif m_choice is "12":
			self.makeSwapFile("262144")

		elif m_choice is "13":
			self.makeSwapFile("524288")

		elif m_choice is "7":
			os.system("rm %s" % (self.swapfile))
			self.mbox = self.session.open(MessageBox,_("Swap file removed"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
			
	def exit(self):
		self.close()
####################################################################
class UsbScreen(Screen):
	skin = """
<screen name="UsbScreen" position="center,160" size="1150,500" title="LBpanel - Unmount manager">
  #<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo18.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="190,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_yellow" render="Label" position="360,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="20,20" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 60), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 70
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Unmount manager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.CfgMenu,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnMount"))
		self["key_yellow"] = StaticText(_("reFresh"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/usbico.png"))
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				hdd = hddlist[count][1]
				devpnt = self.devpoint(hdd.mountDevice())
				if hdd.mountDevice() != '/media/hdd':
					if devpnt != None:
						if int(hdd.free()) > 1024:
							self.list.append(("%s" % hdd.model(),"%s  %s  %s (%d.%03d GB free)" % (devpnt, self.filesystem(hdd.mountDevice()),hdd.capacity(), hdd.free()/1024 , hdd.free()%1024 ), minipng, devpnt))
						else:
							self.list.append(("%s" % hdd.model(),"%s  %s  %s (%03d MB free)" % (devpnt, self.filesystem(hdd.mountDevice()), hdd.capacity(),hdd.free()), minipng, devpnt))
		else:
			hddinfo = _("none")
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		try:
			item = self["menu"].getCurrent()[3]
			os.system("umount -f %s" % item)
			self.mbox = self.session.open(MessageBox,_("Unmounted %s" % item), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			pass
		self.CfgMenu()
		
	def filesystem(self, mountpoint):
		try:
			for line in open("/proc/mounts"):
				if line.find(mountpoint)  > -1:
					return "%s  %s" % (line.split()[2], line.split()[3].split(',')[0])
		except:
			pass
			
	def devpoint(self, mountpoint):
		try:
			for line in open("/proc/mounts"):
				if line.find(mountpoint)  > -1:
					return line.split()[0]
		except:
			pass
			
	def exit(self):
		self.close()
		
####################################################################
class ScriptScreen(Screen):
	skin = """
	<screen name="ScriptScreen" position="center,160" size="1150,500" title="LBpanel - User Script" >
	    <ePixmap position="710,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo11.png" alphatest="blend" transparent="1" />
		<widget name="list" position="20,10" size="660,450" scrollbarMode="showOnDemand" />
		<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="190,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="190,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("LBpanel - User Script"))
		self.scrpit_menu()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Config"))
		self["actions"] = ActionMap(["OkCancelActions","ColorActions"], {"ok": self.run, "red": self.exit, "green": self.config_path, "cancel": self.close}, -1)
		
	def scrpit_menu(self):
		list = []
		try:
			list = os.listdir("%s" % config.plugins.lbpanel.scriptpath.value[:-1])
			list = [x[:-3] for x in list if x.endswith('.sh')]
		except:
			list = []
		list.sort()
		self["list"] = MenuList(list)
		
	def run(self):
		script = self["list"].getCurrent()
		if script is not None:
			name = ("%s%s.sh" % (config.plugins.lbpanel.scriptpath.value, script))
			os.chmod(name, 0755)
			self.session.open(Console, script.replace("_", " "), cmdlist=[name])
			
	def config_path(self):
		self.session.open(ConfigScript)

	def exit(self):
		self.close()
########################################################################
class ConfigScript(ConfigListScreen, Screen):
	skin = """
<screen name="ConfigScript" position="center,160" size="750,370" title="LBpanel - Config script Executer">
		<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Config script Executer"))
		self.list = []
		self.list.append(getConfigListEntry(_("Set script path"), config.plugins.lbpanel.scriptpath))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"ok": self.save
		}, -2)
		
	def cancel(self):
		self.close()
		
	def save(self):
		if not os.path.exists(config.plugins.lbpanel.scriptpath.value):
			try:
				os.system("mkdir %s" % config.plugins.lbpanel.scriptpath.value)
			except:
				pass
		config.plugins.lbpanel.scriptpath.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
########################################################################
class NTPScreen(ConfigListScreen, Screen):
	skin = """
<screen name="NTPScreen" position="center,160" size="1150,500" title="LBpanel - NTP Sync">
    #<ePixmap position="720,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo14.png" alphatest="blend" transparent="1" />
		<widget position="15,10" size="690,450" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="10,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="175,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="340,488" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
		<widget source="key_yellow" render="Label" position="340,458" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="535,488" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
		<widget source="key_blue" render="Label" position="535,458" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - NTP Sync"))
		self.cfgMenu()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Update Now"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.UpdateNow,
			"blue": self.Manual,
			"ok": self.save
		}, -2)
		
	def cfgMenu(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Sync NTP"), config.plugins.lbpanel.onoff))
		self.list.append(getConfigListEntry(_("Set time of upgrade"), config.plugins.lbpanel.time))
		self.list.append(getConfigListEntry(_("Set time of transponder"), config.plugins.lbpanel.TransponderTime))
		self.list.append(getConfigListEntry(_("Sync on boot"), config.plugins.lbpanel.cold))
		self.list.append(getConfigListEntry(_("Server mode"), config.plugins.lbpanel.manual))
		self.list.append(getConfigListEntry(_("Select time zone"), config.plugins.lbpanel.server))
		self.list.append(getConfigListEntry(_("Select ntp server"), config.plugins.lbpanel.manualserver))
		ConfigListScreen.__init__(self, self.list)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	def Manual(self):
		ManualSetTime(self.session)
	
	def save(self):
		path = "/etc/cron/crontabs/root"
		if config.plugins.lbpanel.onoff.value == "0":
			if fileExists(path):
				os.system("sed -i '/ntp./d' %s" % path)
		if config.plugins.lbpanel.onoff.value == "1":
			if fileExists(path):
				os.system("sed -i '/ntp./d' %s" % path)
			if config.plugins.lbpanel.manual.value == "0":
				if config.plugins.lbpanel.time.value == "30":
					os.system("echo -e '/%s * * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.lbpanel.time.value, config.plugins.lbpanel.server.value, path))
				else:
					os.system("echo -e '* /%s * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.lbpanel.time.value, config.plugins.lbpanel.server.value, path))
			else:
				if config.plugins.lbpanel.time.value == "30":
					os.system("echo -e '/%s * * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.lbpanel.time.value, config.plugins.lbpanel.manualserver.value, path))
				else:
					os.system("echo -e '* /%s * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.lbpanel.time.value, config.plugins.lbpanel.manualserver.value, path))
		os.system("echo -e 'root' >> /etc/cron/crontabs/cron.update")
		if fileExists(path):
			os.chmod("%s" % path, 0644)
		if config.plugins.lbpanel.TransponderTime.value == "0": 
			config.misc.useTransponderTime.value = False
			config.misc.useTransponderTime.save()
		else:
			config.misc.useTransponderTime.value = True
			config.misc.useTransponderTime.save()
		if config.plugins.lbpanel.cold.value == "0":
			if fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.unlink("/etc/rcS.d/S42ntpdate.sh")
		else:
			os.system("tar -C/ -xzpvf /usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.tar.gz")
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.sh"):
				if config.plugins.lbpanel.manual.value == "0":
					os.system("sed -i 's/ntp_server/%s/g' /usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.sh" % config.plugins.lbpanel.server.value)
				else:
					os.system("sed -i 's/ntp_server/%s/g' /usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.sh" % config.plugins.lbpanel.manualserver.value)
			if not fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.symlink("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.sh", "/etc/rcS.d/S42ntpdate.sh")
				os.chmod("/etc/rcS.d/S42ntpdate.sh", 0777)
		for i in self["config"].list:
			i[1].save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("Configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
			
	def UpdateNow(self):
		list =""
		synkinfo = os.popen("/usr/bin/ntpdate -v -u pool.ntp.org")
		for line in synkinfo:
			list += line
		self.mbox = self.session.open(MessageBox,list, MessageBox.TYPE_INFO, timeout = 6 )
####################################################################
class ManualSetTime(Screen):
	def __init__(self, session):
		self.session = session
		self.currentime = strftime("%d:%m:%Y %H:%M",localtime())
		self.session.openWithCallback(self.newTime,InputBox, text="%s" % (self.currentime), maxSize=16, type=Input.NUMBER)

	def newTime(self,what):
		try:
			lenstr=len(what)
		except:
			lengstr = 0
		if what is None:
			self.breakSetTime(_("new time not available"))
		elif ((what.count(" ") < 1) or (what.count(":") < 3) or (lenstr != 16)):
			self.breakSetTime(_("bad format"))
		else:
			newdate = what.split(" ",1)[0]
			newtime = what.split(" ",1)[1]
			newday = newdate.split(":",2)[0]
			newmonth = newdate.split(":",2)[1]
			newyear = newdate.split(":",2)[2]
			newhour = newtime.split(":",1)[0]
			newmin = newtime.split(":",1)[1]
			maxmonth = 31
			if (int(newmonth) == 4) or (int(newmonth) == 6) or (int(newmonth) == 9) or (int(newmonth) == 11):
				maxmonth=30
			elif (int(newmonth) == 2):
				if ((4*int(int(newyear)/4)) == int(newyear)):
					maxmonth=28
				else:
					maxmonth=27
			if (int(newyear) < 2007) or (int(newyear) > 2027)  or (len(newyear) < 4):
				self.breakSetTime(_("bad year %s") %newyear)
			elif (int(newmonth) < 0) or (int(newmonth) >12) or (len(newmonth) < 2):
				self.breakSetTime(_("bad month %s") %newmonth)
			elif (int(newday) < 1) or (int(newday) > maxmonth) or (len(newday) < 2):
				self.breakSetTime(_("bad day %s") %newday)
			elif (int(newhour) < 0) or (int(newhour) > 23) or (len(newhour) < 2):
				self.breakSetTime(_("bad hour %s") %newhour)
			elif (int(newmin) < 0) or (int(newmin) > 59) or (len(newmin) < 2):
				self.breakSetTime(_("bad minute %s") %newmin)
			else:
				self.newtime = "%s%s%s%s%s" %(newmonth,newday,newhour,newmin,newyear)
				self.session.openWithCallback(self.ChangeTime,MessageBox,_("Apply the new System time?"), MessageBox.TYPE_YESNO)

	def ChangeTime(self,what):
		if what is True:
			os.system("date %s" % (self.newtime))
		else:
			self.breakSetTime(_("not confirmed"))

	def breakSetTime(self,reason):
		self.session.open(MessageBox,(_("Change system time was canceled, because %s") % reason), MessageBox.TYPE_WARNING)

####################################################################
class SystemScreen(Screen):
	skin = """
		<screen name="SystemScreen" position="center,center" size="1150,600" title="LBpanel - System utils">
	<ePixmap position="700,10" zPosition="1" size="450,590" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo13.png" alphatest="blend" transparent="1" />
	<ePixmap position="705, 640" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="705, 610" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="660,630" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (200, 25), size = (600, 65), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (210, 75), size = (600, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (7, 7), size = (105, 105), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 30),gFont("Regular", 16)],
	"itemHeight": 105
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - System Utils"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernel.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swap.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/cron.png"))
		seispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/disco.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/unusb.png"))
		self.list.append((_("Manager Kernel Modules"),"1", _("Load & unload Kernel Modules"), onepng))
		self.list.append((_("Cron Manager"),"5", _("Cron Manager"), fivepng))
		self.list.append((_("Mount Manager"),"6", _("HArd Disc Manager"), seispng))
		self.list.append((_("Swap Manager"),"4", _("Start, Stop, Create, Remove Swap Files"), fourpng ))
		self.list.append((_("UnMount USB"),"3", _("Unmount usb devices"), treepng ))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "1":
				self.session.openWithCallback(self.mList,KernelScreen)
			elif returnValue is "3":
				self.session.openWithCallback(self.mList,UsbScreen)
			elif returnValue is "4":
				self.session.openWithCallback(self.mList,SwapScreen2)
			elif returnValue is "5":
				self.session.openWithCallback(self.mList,CrontabMan)
			elif returnValue is "6":
				self.session.open(MountManager.HddMount)
			else:
				print "\n[BackupSuite] cancel\n"
				self.close(None)
###############################################################################
class KernelScreen(Screen):
	skin = """
<screen name="KernelScreen" position="center,100" size="1150,500" title="LBpanel - Kernel Modules Manager">
  #<ePixmap position="710,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo15.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="185,458" zPosition="2" size="210,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<ePixmap position="390,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="390,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_blue" render="Label" position="560,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="560,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" transparent="1" alphatest="on" />
	<widget source="menu" render="Listbox" position="20,10" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Kernel Modules Manager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Load/UnLoad"))
		self["key_yellow"] = StaticText(_("LsMod"))
		self["key_blue"] = StaticText(_("Reboot"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def BlueKey(self):
		os.system("reboot")
		
	def YellowKey(self):
		self.session.openWithCallback(self.CfgMenu,lsmodScreen)
		
	def IsRunnigModDig(self, what):
		modrun = os.popen ("lsmod | grep %s" % (what[:-4]))
		for line in modrun:
			if line.find(what[:-4]) > -1:
				return 1
				break
		return 0
		
	def CfgMenu(self):
		self.list = []
		DvrName = os.popen("modprobe -l -t drivers")
		for line in DvrName:
			kernDrv = line.split("/")
			if self.IsRunnigModDig(kernDrv[-1]) == 1:
				minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernelminimem.png"))
				self.list.append((kernDrv[-1],line,minipng, "1"))
			else:
				minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernelmini.png"))
				self.list.append((kernDrv[-1],line,minipng, "0"))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.Ok, "cancel": self.close}, -1)

	def Ok(self):
		item = self["menu"].getCurrent()
		isrunning = item[3]
		nlist = item[0]
		if item[3] == "0":
			os.system(("modprobe %s" % (nlist[:-4])))
			os.system(("echo %s>/etc/modutils/%s" % (nlist[:-4],nlist[:-4])))
			os.chmod(("/etc/modutils/%s" % (nlist[:-4])), 0644)
			os.system("update-modules")
			self.mbox = self.session.open(MessageBox,(_("Loaded %s") % (nlist)), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			os.system(("rmmod%s" % (" " + nlist[:-4])))
			os.system(("rm /etc/modutils/%s" % (nlist[:-4])))
			os.system("update-modules")
			self.mbox = self.session.open(MessageBox,(_("UnLoaded %s") % (nlist)), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def exit(self):
		self.close()
####################################################################
class lsmodScreen(Screen):
	skin = """
<screen name="lsmodScreen" position="center,100" size="750,570" title="LBpanel - List Kernel Drivers in Memory">
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,528" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,10" size="710,500" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - List Kernel Drivers in Memory"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		DvrName = os.popen("lsmod")
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernelminimem.png"))
		for line in DvrName:
			item = line.split(" ")
			size = line[:28].split(" ")
			minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernelminimem.png"))
			if line.find("Module") != 0:
				self.list.append((item[0],( _("size: %s  %s") % (size[-1], item[-1])), minipng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)

	def exit(self):
		self.close()
####################################################################
class CrashLogScreen(Screen):
	skin = """
<screen name="CrashLogScreen" position="center,160" size="1150,500" title="LBpanel - Crashlog files">
    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo8.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<widget source="key_green" render="Label" position="190,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="360,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_blue" render="Label" position="530,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="530,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" transparent="1" alphatest="on" />
	<widget source="menu" render="Listbox" position="20,10" size="690,347" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Crashlog files"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("View"))
		self["key_yellow"] = StaticText(_("Remove"))
		self["key_blue"] = StaticText(_("Remove All"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/crashmini.png"))
		try:
			crashfiles = os.listdir("/media/hdd")
			for line in crashfiles:
				if line.find("enigma2_crash") > -1:
					self.list.append((line,"%s" % time.ctime(os.path.getctime("/media/hdd/" + line)), minipng))
		except:
			pass
		self.list.sort()
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		try:
			item = "/media/hdd/" + self["menu"].getCurrent()[0]
			self.session.openWithCallback(self.CfgMenu,LogScreen, item)
		except:
			pass
	
	def YellowKey(self):
		item = "/media/hdd/" +  self["menu"].getCurrent()[0]
		try:
			os.system("rm %s"%(item))
			self.mbox = self.session.open(MessageBox,(_("Removed %s") % (item)), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Failed remove")), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def BlueKey(self):
		try:
			os.system("rm /media/hdd/enigma2_crash*.log")
			self.mbox = self.session.open(MessageBox,(_("Removed All Crashlog Files") ), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Failed remove")), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def exit(self):
		self.close()
####################################################################
class LogScreen(Screen):
	skin = """
<screen name="LogScreen" position="center,80" size="1170,600" title="LBpanel - View Crashlog file">
	<ePixmap position="20,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,590" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="190,560" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="390,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="390,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="10,10" size="1150,542" font="Console;22" />
</screen>"""

	def __init__(self, session, what):
		self.session = session
		Screen.__init__(self, session)
		self.crashfile = what
		self.setTitle(_("LBpanel - View Crashlog file"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Restart GUI"))
		self["key_yellow"] = StaticText(_("Save"))
		self["text"] = ScrollLabel("")
		self.listcrah()
		
	def exit(self):
		self.close()
	
	def GreenKey(self):
		self.session.open(TryQuitMainloop, 3)
		
	def YellowKey(self):
		os.system("gzip %s" % (self.crashfile))
		os.system("mv %s.gz /tmp" % (self.crashfile))
		self.mbox = self.session.open(MessageBox,_("%s.gz created in /tmp") % self.crashfile, MessageBox.TYPE_INFO, timeout = 4)
		
	def listcrah(self):
		list = " "
		files = open(self.crashfile, "r")
		for line in files:
			if line.find("Traceback (most recent call last):") != -1:
				for line in files:
					list += line
					if line.find("]]>") != -1:
						break
		self["text"].setText(list)
		files.close()
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
######################################################################################
class epgdn(ConfigListScreen, Screen):
	skin = """
<screen name="epgdn" position="center,160" size="1150,500" title="LBpanel - EPG D+">
    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo9.png" alphatest="blend" transparent="1" />
  <widget position="15,10" size="690,450" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="540,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="540,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - D+ EPG"))
		self.list = []
		self.list.append(getConfigListEntry(_("Select where to save epg.dat"), config.plugins.lbpanel.direct))
		self.list.append(getConfigListEntry(_("Select D+ epg"), config.plugins.lbpanel.lang))
		self.list.append(getConfigListEntry(_("Auto download epg.dat"), config.plugins.lbpanel.auto))
		self.list.append(getConfigListEntry(_("Auto download hour"), config.plugins.lbpanel.epgtime))
		self.list.append(getConfigListEntry(_("Auto load and save EPG"), config.plugins.lbpanel.autosave))
		self.list.append(getConfigListEntry(_("Save copy in ../epgtmp.gz"), config.plugins.lbpanel.autobackup))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("EPG Download"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.downepg,
			"blue": self.manual,
			"ok": self.save
		}, -2)
		
	def downepg(self):
		try:
			os.system("wget -q http://appstore.linux-box.es/epg/epg.dat.gz -O %sepg.dat.gz" % (config.plugins.lbpanel.direct.value))
			if fileExists("%sepg.dat" % config.plugins.lbpanel.direct.value):
				os.unlink("%sepg.dat" % config.plugins.lbpanel.direct.value)
				os.system("rm -f %sepg.dat" % config.plugins.lbpanel.direct.value)
			if not os.path.exists("%sepgtmp" % config.plugins.lbpanel.direct.value):
				os.system("mkdir -p %sepgtmp" % config.plugins.lbpanel.direct.value)
			os.system("cp -f %sepg.dat.gz %sepgtmp" % (config.plugins.lbpanel.direct.value, config.plugins.lbpanel.direct.value))
			os.system("gzip -df %sepg.dat.gz" % config.plugins.lbpanel.direct.value)
			os.chmod("%sepg.dat" % config.plugins.lbpanel.direct.value, 0644)
			self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
		except:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)
	
	def save(self):
		config.misc.epgcache_filename.value = ("%sepg.dat" % config.plugins.lbpanel.direct.value)
		config.misc.epgcache_filename.save()
		config.plugins.lbpanel.epgtime.save()
		config.plugins.lbpanel.lang.save()
		config.plugins.lbpanel.direct.save()
		config.plugins.lbpanel.auto.save()
		config.plugins.lbpanel.autosave.save()
		config.plugins.lbpanel.autobackup.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
################################################################################################################
	def manual(self):
		self.session.open(epgdmanual)
################################################################################################################
	def restart(self):
		self.session.open(TryQuitMainloop, 3)
#####################################################
################################################################################################################

class epgscript(ConfigListScreen, Screen):
	skin = """
<screen name="epgdn" position="center,160" size="1150,500" title="LBpanel - EPG D+">
    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo9.png" alphatest="blend" transparent="1" />
  <widget position="15,10" size="690,450" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="540,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="540,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - D+ SAT EPG"))
		self.list = []
		self.list.append(getConfigListEntry(_("Select where to save epg.dat"), config.plugins.lbpanel.direct))
		self.list.append(getConfigListEntry(_("Select D+ epg"), config.plugins.lbpanel.lang))
		self.list.append(getConfigListEntry(_("Auto download epg.dat"), config.plugins.lbpanel.auto2))
		self.list.append(getConfigListEntry(_("Auto download hour"), config.plugins.lbpanel.epgtime2))
		self.list.append(getConfigListEntry(_("Auto load and save EPG"), config.plugins.lbpanel.autosave))
		self.list.append(getConfigListEntry(_("Save copy in ../epgtmp.gz"), config.plugins.lbpanel.autobackup))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("EPG Download"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.downepg,
			"blue": self.manual,
			"ok": self.save
		}, -2)
		
	def downepg(self):
		try:
			epgservice='1:0:1:75c6:422:1:c00000:0:0:0'
			#epgservice='1:0:1:759C:422:1:C00000:0:0:0:' 
			self.oldService = self.session.nav.getCurrentlyPlayingServiceReference().toString()
			self.session.nav.playService(eServiceReference(epgservice))
			os.system("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/libs/mhw2epgdownloader.e2/cchannel.sh &")
			os.system("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/libs/mhw2epgdownloader.e2/run.e2.sh")
			self.session.nav.playService(self.oldService)
			#if fileExists("%sepg.dat" % config.plugins.lbpanel.direct.value):
			#	os.unlink("%sepg.dat" % config.plugins.lbpanel.direct.value)
			#	os.system("rm -f %sepg.dat" % config.plugins.lbpanel.direct.value)
			#if not os.path.exists("%sepgtmp" % config.plugins.lbpanel.direct.value):
			#	os.system("mkdir -p %sepgtmp" % config.plugins.lbpanel.direct.value)
			#os.system("cp -f %sepg.dat.gz %sepgtmp" % (config.plugins.lbpanel.direct.value, config.plugins.lbpanel.direct.value))
			#os.system("gzip -df %sepg.dat.gz" % config.plugins.lbpanel.direct.value)
			#os.chmod("%sepg.dat" % config.plugins.lbpanel.direct.value, 0644)
			#self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
			#epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			#epgcache = eEPGCache.getInstance().load()
		except:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)
	
	def save(self):
		config.misc.epgcache_filename.value = ("%sepg.dat" % config.plugins.lbpanel.direct.value)
		config.misc.epgcache_filename.save()
		config.plugins.lbpanel.epgtime2.save()
		config.plugins.lbpanel.lang.save()
		config.plugins.lbpanel.direct.save()
		config.plugins.lbpanel.auto2.save()
		config.plugins.lbpanel.autosave.save()
		config.plugins.lbpanel.autobackup.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
################################################################################################################
	def manual(self):
		self.session.open(epgdmanual)
################################################################################################################
	def restart(self):
		self.session.open(TryQuitMainloop, 3)
#####################################################
################################################################################################################

class epgdmanual(Screen):
	skin = """
<screen name="epgdmanual" position="center,260" size="850,50" title="LBpanel - EPG D+">
  <ePixmap position="10,40" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,10" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="375,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="375,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="574,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="574,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - EPG D+"))
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save epg.dat"))
		self["key_yellow"] = StaticText(_("Restore epg.dat"))
		self["key_blue"] = StaticText(_("Reload epg.dat"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.savepg,
			"yellow": self.restepg,
			"blue": self.reload,
		}, -2)
################################################################################################################
	def reload(self):
		try:
			if fileExists("%sepgtmp/epg.dat.gz" % config.plugins.lbpanel.direct.value):
				os.system("cp -f %sepgtmp/epg.dat.gz %s" % (config.plugins.lbpanel.direct.value, config.plugins.lbpanel.direct.value))
				os.system("gzip -df %sepg.dat.gz" % config.plugins.lbpanel.direct.value)
				os.chmod("%sepg.dat" % config.plugins.lbpanel.direct.value, 0644)
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
			self.mbox = self.session.open(MessageBox,(_("epg.dat reloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("reload epg.dat failed")), MessageBox.TYPE_INFO, timeout = 4 )
################################################################################################################
	def savepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		self.mbox = self.session.open(MessageBox,(_("epg.dat saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def restepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
		epgcache = eEPGCache.getInstance().load()
		self.mbox = self.session.open(MessageBox,(_("epg.dat restored")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def cancel(self):
		self.close(False)
##############################################################################
class CrontabMan(Screen):
	skin = """
<screen name="CrontabMan" position="center,160" size="1150,500" title="LBpanel - Cron Manager">
  #<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo16.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="195,458" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="195,488" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="370,458" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="370,488" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="15,15" size="660,450" scrollbarMode="showOnDemand">
		<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (10, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 29
	}
			</convert>
		</widget>
</screen>"""
	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Cron Manager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Add tabs"))
		self["key_yellow"] = StaticText(_("Remove tabs"))
		self.list = []
		self["menu"] = List(self.list)
		self.cMenu()

	def cMenu(self):
		self.list = []
		count = 0
		if fileExists("/etc/cron/crontabs/root"):
			cron = open("/etc/cron/crontabs/root", "r")
			for line in cron:
				count = count + 1
				self.list.append((line, count))
			cron.close()
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.Ok, "cancel": self.close}, -1)

	def Ok(self):
		self.close()
		
	def GreenKey(self):
		self.session.openWithCallback(self.cMenu,CrontabManAdd)

	
	def YellowKey(self):
		try:
			os.system("sed -i %sd /etc/cron/crontabs/root" % str(self["menu"].getCurrent()[1]))
			os.system("echo -e 'root' >> /etc/cron/crontabs/cron.update")
		except:
			pass
		self.cMenu()
		
	def exit(self):
		self.close()
####################################################################
class CrontabManAdd(ConfigListScreen, Screen):
	skin = """
<screen name="CrontabManAdd" position="center,160" size="750,370" title="LBpanel - Add tabs" >
		<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />

</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Add tabs"))
		self.list = []
		self.list.append(getConfigListEntry(_("Min"), config.plugins.lbpanel.min))
		self.list.append(getConfigListEntry(_("Hour"), config.plugins.lbpanel.hour))
		self.list.append(getConfigListEntry(_("Day of month"), config.plugins.lbpanel.dayofmonth))
		self.list.append(getConfigListEntry(_("Month"), config.plugins.lbpanel.month))
		self.list.append(getConfigListEntry(_("Day of week"), config.plugins.lbpanel.dayofweek))
		self.list.append(getConfigListEntry(_("Command"), config.plugins.lbpanel.command))
		self.list.append(getConfigListEntry(_("Every"), config.plugins.lbpanel.every))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Add"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.ok,
			"ok": self.ok
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	
	def ok(self):
		everymin = ""
		everyhour = ""
		everydayofmonth = ""
		everymonth = ""
		everydayofweek = ""
		if config.plugins.lbpanel.min.value != '*' and config.plugins.lbpanel.every.value == '1':
			everymin = '/'
		elif config.plugins.lbpanel.hour.value != '*' and config.plugins.lbpanel.every.value == '2':
			everyhour = '/'
		elif config.plugins.lbpanel.dayofmonth.value != '*' and config.plugins.lbpanel.every.value == '3':
			everydayofmonth = '/'
		elif config.plugins.lbpanel.month.value != '*' and config.plugins.lbpanel.every.value == '4':
			everymonth = '/'
		elif config.plugins.lbpanel.dayofweek.value != '*' and config.plugins.lbpanel.every.value == '5':
			everydayofweek = '/'
			
		if config.plugins.lbpanel.min.value == '*' and config.plugins.lbpanel.hour.value == '*' and config.plugins.lbpanel.dayofmonth.value == '*' and config.plugins.lbpanel.month.value == '*' and  config.plugins.lbpanel.dayofweek.value == '*':
			print ("error")
		else:
			os.system("echo -e '%s%s %s%s %s%s %s%s %s%s    %s' >> /etc/cron/crontabs/root" % (everymin, config.plugins.lbpanel.min.value,
																				everyhour, config.plugins.lbpanel.hour.value, 
																				everydayofmonth, config.plugins.lbpanel.dayofmonth.value,
																				everymonth, config.plugins.lbpanel.month.value,
																				everydayofweek, config.plugins.lbpanel.dayofweek.value,
																				config.plugins.lbpanel.command.value))
		os.system("echo -e 'root' >> /etc/cron/crontabs/cron.update")
		for i in self["config"].list:
			i[1].cancel()
		self.close()
###############################################################################
class Info2Screen(Screen):
	skin = """
<screen name="Info2Screen" position="center,100" size="890,560" title="LBpanel - System Info">
	<ePixmap position="20,548" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,518" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="15,10" size="860,500" font="Console;20" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - System Info"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"ok": self.exit,
			})
		self["key_red"] = StaticText(_("Close"))
		self["text"] = ScrollLabel("")
		self.meminfoall()
		
	def exit(self):
		self.close()
		
	def meminfoall(self):
		list = " "
		try:
			os.system("free>/tmp/mem && echo>>/tmp/mem && df -h>>/tmp/mem")
			meminfo = open("/tmp/mem", "r")
			for line in meminfo:
				list += line
			self["text"].setText(list)
			meminfo.close()
			os.system("rm /tmp/mem")
		except:
			list = " "
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
######################################################################################
class Libermen(Screen):
	skin = """
	<screen name="ScriptScreen" position="center,160" size="1150,500" title="LBpanel - Free Memory" >
	    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo12.png" alphatest="blend" transparent="1" />
			<widget name="list" position="20,10" size="660,450" scrollbarMode="showOnDemand" />
		<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("LBpanel - Free Memory"))
		self.scrpit_menu()
		self["key_red"] = StaticText(_("Close"))
		self["actions"] = ActionMap(["OkCancelActions","ColorActions"], {"ok": self.run, "red": self.exit, "cancel": self.close}, -1)
		
	def scrpit_menu(self):
		list = []
		try:
			list = os.listdir("%s" % config.plugins.lbpanel.scriptpath1.value[:-1])
			list = [x[:-3] for x in list if x.endswith('.sh')]
		except:
			list = []
		list.sort()
		self["list"] = MenuList(list)
		
	def run(self):
		script = self["list"].getCurrent()
		if script is not None:
			name = ("%s%s.sh" % (config.plugins.lbpanel.scriptpath1.value, script))
			os.chmod(name, 0755)
			self.session.open(Console, script.replace("_", " "), cmdlist=[name])
			
	def config_path(self):
		self.session.open(ConfigScript)

	def exit(self):
		self.close()

######################################################################################
class scanhost(ConfigListScreen, Screen):
	skin = """
<screen name="scanhost" position="center,160" size="1150,500" title="LBpanel - Check Hosts">
    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo100.png" alphatest="blend" transparent="1" />
  <widget position="15,10" size="690,450" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="540,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="540,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <widget name="LabelStatus" position="10,400" zPosition="2" size="400,40"  font="Regular;20"/>
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Check Host"))
		self.list = []
		self.list.append(getConfigListEntry(_("Auto Daily Test"), config.plugins.lbpanel.checkauto))
		self.list.append(getConfigListEntry(_("Hour"), config.plugins.lbpanel.checkhour))
		self.list.append(getConfigListEntry(_("Disable Faulty Lines?"), config.plugins.lbpanel.checkoff))
		self.list.append(getConfigListEntry(_("Scan type"), config.plugins.lbpanel.checktype))
		self.list.append(getConfigListEntry(_("Auto scan localhost"), config.plugins.lbpanel.autocheck))
		#self.list.append(getConfigListEntry(_("Send email with log?"), config.plugins.lbpanel.lbemail))
		self.list.append(getConfigListEntry(_("Send email only in danger lines?"), config.plugins.lbpanel.warnonlyemail))
		#self.list.append(getConfigListEntry(_("Send report to: (email)"), config.plugins.lbpanel.lbemailto))
		#self.list.append(getConfigListEntry(_("Smtp server"), config.plugins.lbpanel.smtpserver))
		#self.list.append(getConfigListEntry(_("Smtp user"), config.plugins.lbpanel.smtpuser))
		#self.list.append(getConfigListEntry(_("Smtp password"), config.plugins.lbpanel.smtppass))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("View"))
		self["key_blue"] = StaticText(_("Run"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.viewscanlog,
			"blue": self.checkt,
			"ok": self.save
		}, -2)
		self["LabelStatus"] = Label(_("Configure and press blue key to check"))
		
        def check(self):
	        try:   
			self["LabelStatus"].setText("Scan init")                     
        		os.system("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/lbscan.py %s %s %s %s" % (config.plugins.lbpanel.checktype.value, config.plugins.lbpanel.autocheck.value, config.plugins.lbpanel.checkoff.value, config.plugins.lbpanel.warnonlyemail.value))
        		self["LabelStatus"].setText("Scan end")
        		self.session.open(showScan)
                except IOError:
                      	self.mbox = self.session.open(MessageBox,(_("Sorry, I can not find lbscan.py")), MessageBox.TYPE_INFO, timeout = 4 )
		
        def checkt(self):
	        try:   
	        	self["LabelStatus"].setText("Scan init")
        		self.session.open(Console,_("Scan peer"),["/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/lbscan.py " + config.plugins.lbpanel.checktype.value + " " + config.plugins.lbpanel.autocheck.value + " " + config.plugins.lbpanel.checkoff.value + " " + config.plugins.lbpanel.warnonlyemail.value])
        		self["LabelStatus"].setText("Scan end")
        		# Send email with result by cron
        		
#        		self.session.open(showScan)
                except:
                      	self.mbox = self.session.open(MessageBox,(_("Sorry, I can not find lbscan.py")), MessageBox.TYPE_INFO, timeout = 4 )
	def viewscanlog(self):
		if (os.path.exists("/tmp/.lbscan.log")):
			 self.session.open(showScan)
		else:
			 self.mbox = self.session.open(MessageBox,(_("Sorry, I can not find scan data, scan first")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)
	
	def save(self):
		config.plugins.lbpanel.checkauto.save()
		config.plugins.lbpanel.checkhour.save()
		config.plugins.lbpanel.checkoff.save()
		config.plugins.lbpanel.checktype.save()
		config.plugins.lbpanel.autocheck.save()
#		config.plugins.lbpanel.lbemail.save()
		config.plugins.lbpanel.warnonlyemail.save()
#		config.plugins.lbpanel.lbemailto.save()
#		config.plugins.lbpanel.smtpserver.save()
#		config.plugins.lbpanel.smtpuser.save()
#		config.plugins.lbpanel.smtppass.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("Configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )

	def messagebox(self):
		self.mbox = self.session.open(MessageBox,(_("Scaning hosts, please wait")), MessageBox.TYPE_INFO, timeout = 4 )
	
	
################################################################################################################
class showScan(Screen):
	skin = """
<screen name="Show Scan" position="center,100" size="890,560" title="LBpanel - Scan Results">
	<ePixmap position="20,548" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,518" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="15,10" size="860,500" font="Console;20" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Scan Results"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"ok": self.exit,
			})
		self["key_red"] = StaticText(_("Close"))
		self["text"] = ScrollLabel("")
		self.meminfoall()
		
	def exit(self):
		self.close()
		
	def meminfoall(self):
		list = " "
		try:
			scaninfo = open("/tmp/.lbscan.log", "r")
			for line in scaninfo:
				list += line
			self["text"].setText(list)
			scaninfo.close()
		except:
			list = " "
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
