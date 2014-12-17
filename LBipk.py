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

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from enigma import eConsoleAppContainer, eDVBDB
from Components.Sources.StaticText import StaticText
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Label import Label
from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Tools.Directories import fileExists
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ
import os
import gettext
import time

global status 
if fileExists("/usr/lib/opkg/status"):
	status = "/usr/lib/opkg/status"
elif fileExists("/var/lib/opkg/status"):
	status = "/var/lib/opkg/status"

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("messages", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/LBpanel/locale/"))



def _(txt):
	t = gettext.dgettext("messages", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
	
class IPKToolsScreen(Screen):
	skin = """
	<screen name="IPKToolsScreen" position="0,0" size="1280,720" title="LBpanel Ipk Tools">
	<eLabel text="LBpanel - Red Bee" position="460,30" size="400,65" font="Regular;45" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="background"/>
<widget source="Title" transparent="1" render="Label" zPosition="2" valign="center" halign="left" position="92,110" size="700,65" font="Regular; 30" foregroundColor="#ffffff" noWrap="1" />
<widget source="session.VideoPicture" render="Pig" position="53,133" size="420,236" backgroundColor="transparent" zPosition="-10" />
<ePixmap position="60,410" zPosition="2" size="391,201" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/logo_ajustes.png" alphatest="blend" />
<widget source="session.CurrentService" render="Label" position="100,650" size="410,25" font="Regular; 22" transparent="1" valign="center" zPosition="2" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" halign="left">
			  <convert type="ServiceName">Name</convert>
			</widget>
<ePixmap position="710,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="750,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f"  foregroundColor="#000000" transparent="1" />
	<ePixmap position="830,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="870,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />
	<ePixmap position="1020,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="1060,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />
<ePixmap position="0,0" zPosition="-4" size="1281,721" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo_1_test3.png" alphatest="blend" />
<eLabel text="Panel Ipk" position="45,490" size="400,65" font="Regular;30" zPosition="2" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="background"/>
<widget source="menu" render="Listbox" position="592,191" scrollbarMode="showNever" backgroundColorSelected="#fd6502" transparent="1"
size="628,350">
<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (10, 10), size = (600, 65), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		
			],
	"fonts": [gFont("Regular", 40),gFont("Regular", 16)],
	"itemHeight": 70
	}
	</convert>
	</widget>
	</screen>"""
	 
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel Ipk Tools"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.OK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"yellow": self.clear,
			"green": self.restartGUI,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Restart GUI"))
		self["key_yellow"] = StaticText(_("Clear /tmp"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipk.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipk.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipk.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipk.png"))
		#dospng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipk.png"))
		#cuatropng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipk.png"))
		#cincopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipk.png"))
		self.list.append((_("IPK installer"),"one", _("Install ipk, bh.tgz, tar.gz, nab.tgz in /tmp"), onepng ))
		self.list.append((_("Feed installer"),"six", _("Feed installer"), sixpng ))
		self.list.append((_("Download extensions"),"five", _("Download feeds packages"), fivepng))
		self.list.append((_("IPK delete packages"),"four", _("Delete IPK packages"), treepng ))
		#self.list.append((_("Sorys Channel List"),"dos", _("Download Sorys Channel List"), dospng ))
		#self.list.append((_("Download config emus"),"cuatro", _("Download Config Emus"), cuatropng ))
		#self.list.append((_("Download Picon"),"cinco", _("Download Picon"), cincopng ))
		self["menu"].setList(self.list)
		
	def exit(self):
		self.close()
		
	def clear(self):
		os.system("rm /tmp/*.tar.gz /tmp/*.bh.tgz /tmp/*.ipk /tmp/*.nab.tgz")
		self.mbox = self.session.open(MessageBox,_("*.tar.gz & *.bh.tgz & *.ipk removed"), MessageBox.TYPE_INFO, timeout = 4 )
		
	def restartGUI(self):
		self.session.open(TryQuitMainloop, 3)

	def OK(self):
		item = self["menu"].getCurrent()[1]
		if item is "one":
			self.session.openWithCallback(self.mList,InstallAll)
		elif item is "four":
			self.session.openWithCallback(self.mList,RemoveIPK)
		elif item is "five":
			self.session.openWithCallback(self.mList,DownloadFeed)
		elif item is "six":
			self.session.openWithCallback(self.mList,downfeed)
		#elif item is "dos":
			#self.session.openWithCallback(self.mList,installsorys)
		#elif item is "cuatro":
			#self.session.openWithCallback(self.mList,installconfigemus)
		#elif item is "cinco":
			#self.session.openWithCallback(self.mList,installpicon)
			
###############################################
class DownloadFeed(Screen):
	skin = """
<screen name="DownloadFeed" position="0,0" size="1280,720" title="Download extensions from feed">
<ePixmap position="0,0" zPosition="-4" size="1281,721" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo_1_test3.png" alphatest="blend" />

<eLabel text="LBpanel Ipk Tools" position="460,30" size="400,65" font="Regular;45" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="#0140b1"/>

<widget source="Title" transparent="1" render="Label" zPosition="2" valign="center" halign="left" position="92,110" size="730,65" font="Regular; 30" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" />

<widget source="session.VideoPicture" render="Pig" position="53,133" size="420,236" backgroundColor="transparent" zPosition="-10" />
<ePixmap position="60,410" zPosition="2" size="391,201" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/logo_ajustes.png" alphatest="blend" />

<widget source="session.CurrentService" render="Label" position="100,650" size="410,25" font="Regular; 22" transparent="1" valign="center" zPosition="2" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" halign="left">
			  <convert type="ServiceName">Name</convert>

			</widget>
<eLabel text="Feed Download" position="45,490" size="400,65" font="Regular;30" zPosition="2" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="#000000"/>

<widget source="global.CurrentTime" render="Label" position="949,30" size="251,55" backgroundColor="#0140b1" foregroundColor="#00ffffff" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2"> 
		<convert type="ClockToText">Format:%-H:%M</convert> 
		</widget> 

		<widget source="global.CurrentTime" render="Label" position="900,50" size="300,55" backgroundColor="#0140b1" foregroundColor="#00ffffff" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2"> 
		<convert type="ClockToText">Date</convert>  
		</widget>
<widget source="menu" render="Listbox" position="592,191" size="628,350" scrollbarMode="showNever" foregroundColor="#ffffff" backgroundColor="#6e6e6e" backgroundColorSelected="#fd6502" transparent="1">
	<convert type="TemplatedMultiContent">

		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description

			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 21),gFont("Regular", 16)],

	"itemHeight": 50
	}
	</convert>

	</widget>
	<ePixmap position="740,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />

	<widget source="key_red" render="Label" position="780,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f"  foregroundColor="#000000" transparent="1" />
	<ePixmap position="860,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="900,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />

	<ePixmap position="980,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="1020,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />

</screen>"""
	  
	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("Download extensions from feed"))
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.feedlist()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"green": self.down,
				"yellow": self.wdown,
				"red": self.cancel,
			},-1)
		self.list = [ ]
		self["key_red"] = Label(_("Close"))
		self["key_green"] = Label(_("Download -nodeps"))
		self["key_yellow"] = Label(_("Download -deps"))
		
	def feedlist(self):
		self.list = []
		if fileExists("/usr/lib/opkg/status"):
			os.system("mv /usr/lib/opkg/status /usr/lib/opkg/status.tmp")
		elif fileExists("/var/lib/opkg/status"):
			os.system("mv /var/lib/opkg/status /var/lib/opkg/status.tmp")
		os.system("opkg update")
		camdlist = os.popen("opkg list")
		softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipkmini.png"))
		if camdlist:
			for line in camdlist:
				if config.plugins.lbpanel.filtername.value:
					if line.find("enigma2-plugin-") > -1:
						try:
							self.list.append(("%s %s" % (line.split(' - ')[0], line.split(' - ')[1]), line.split(' - ')[-1], softpng))
						except:
							pass
				else:
					try:
						self.list.append(("%s %s" % (line.split(' - ')[0], line.split(' - ')[1]), line.split(' - ')[-1], softpng))
					except:
						pass
		self["menu"].setList(self.list)
		
	def ok(self):
		self.down()
		
	def down(self):
		os.system("cd /tmp && opkg install -nodeps -download-only %s" % self["menu"].getCurrent()[0])
		self.mbox = self.session.open(MessageBox, _("%s is downloaded" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		
	def wdown(self):
		os.system("cd /tmp && opkg install -download-only %s" % self["menu"].getCurrent()[0])
		self.mbox = self.session.open(MessageBox, _("%s is downloaded" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )

	def cancel(self):
		if fileExists("/usr/lib/opkg/status.tmp"):
			os.system("mv /usr/lib/opkg/status.tmp /usr/lib/opkg/status")
			os.chmod("/usr/lib/opkg/status", 0644)
		elif fileExists("/var/lib/opkg/status.tmp"):
			os.system("mv /var/lib/opkg/status.tmp /var/lib/opkg/status")
			os.chmod("/var/lib/opkg/status", 0644)
		self.close()
#####################################################################################################
class InstallAll(Screen):
	skin = """
<screen name="InstallAll" position="0,0" size="1280,720" title="LBpanel-Select files to install">
<ePixmap position="0,0" zPosition="-4" size="1281,721" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo_1_test3.png" alphatest="blend" />
<eLabel text="LBpanel Ipk Tools" position="460,30" size="400,65" font="Regular;45" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="#0140b1"/>
<widget source="Title" transparent="1" render="Label" zPosition="2" valign="center" halign="left" position="92,110" size="730,65" font="Regular; 30" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" />
<widget source="session.VideoPicture" render="Pig" position="53,133" size="420,236" backgroundColor="transparent" zPosition="-10" />
<ePixmap position="60,410" zPosition="2" size="391,201" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/logo_ajustes.png" alphatest="blend" />
<widget source="session.CurrentService" render="Label" position="100,650" size="410,25" font="Regular; 22" transparent="1" valign="center" zPosition="2" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" halign="left">
			  <convert type="ServiceName">Name</convert>
			</widget>
<eLabel text="Ipk Install" position="45,490" size="400,65" font="Regular;30" zPosition="2" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="#000000"/>
<widget source="global.CurrentTime" render="Label" position="949,30" size="251,55" backgroundColor="#0140b1" foregroundColor="#00ffffff" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2"> 
		<convert type="ClockToText">Format:%-H:%M</convert> 
		</widget> 
		<widget source="global.CurrentTime" render="Label" position="900,50" size="300,55" backgroundColor="#0140b1" foregroundColor="#00ffffff" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2"> 
		<convert type="ClockToText">Date</convert>  
		</widget>
<widget source="menu" render="Listbox" position="592,191" size="628,350" scrollbarMode="showNever" foregroundColor="#ffffff" backgroundColor="#6e6e6e" backgroundColorSelected="#fd6502" transparent="1">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 21),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap position="740,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="780,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f"  foregroundColor="#000000" transparent="1" />
	<ePixmap position="860,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="900,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />
	<ePixmap position="980,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="1020,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />
</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Select files to install from /tmp"))
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.okInst,
				"green": self.okInst,
				"red": self.cancel,
				"yellow": self.AdvInst,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_yellow"] = StaticText(_("Forced Install"))
		
	def nList(self):
		self.list = []
		workdir = "/tmp/" 
		ipklist = os.listdir(workdir)
		ipkminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipkmini.png"))
		tarminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/tarmini.png"))
		for line in ipklist:
			if line.find(".tar.gz") > -1 or line.find(".bh.tgz") > -1 or line.find(".nab.tgz") > -1:
				try:
					self.list.append((line.strip("\n"), "%s Kb,  %s" % ((os.path.getsize(workdir + line.strip("\n")) / 1024),time.ctime(os.path.getctime(workdir + line.strip("\n")))), tarminipng))
				except:
					pass
			elif line.find(".ipk") > -1:
				try:
					self.list.append((line.strip("\n"), "%s Kb,  %s" % ((os.path.getsize(workdir + line.strip("\n")) / 1024),time.ctime(os.path.getctime(workdir + line.strip("\n")))), ipkminipng))
				except:
					pass
		self.list.sort()
		self["menu"].setList(self.list)
		
	def okInst(self):
		if self["menu"].getCurrent()[0][-4:] == '.ipk':
			try:
				self.session.open(Console,title = _("Install packets"), cmdlist = ["opkg install /tmp/%s" % self["menu"].getCurrent()[0]])
			except:
				pass
		else:
			try:
				self.session.open(Console,title = _("Install tar.gz, bh.tgz, nab.tgz"), cmdlist = ["tar -C/ -xzpvf /tmp/%s" % self["menu"].getCurrent()[0]])
			except:
				pass
			
	def AdvInst(self):
		if self["menu"].getCurrent()[0][-4:] == '.ipk':
			try:
				self.session.open(Console,title = _("Install packets"), cmdlist = ["opkg install -force-overwrite -force-downgrade /tmp/%s" % self["menu"].getCurrent()[0]])
			except:
				pass
		else:
			try:
				self.session.open(Console,title = _("Install tar.gz, bh.tgz, nab.tgz"), cmdlist = ["tar -C/ -xzpvf /tmp/%s" % self["menu"].getCurrent()[0]])
			except:
				pass
	
	def cancel(self):
		self.close()
########################################################################################################
class RemoveIPK(Screen):
	skin = """
<screen name="RemoveIPK" position="0,0" size="1280,720" title="LBpanel - Ipk remove">
<ePixmap position="0,0" zPosition="-4" size="1281,721" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo_1_test3.png" alphatest="blend" />

<eLabel text="LBpanel Ipk Tools" position="460,30" size="400,65" font="Regular;45" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="#0140b1"/>

<widget source="Title" transparent="1" render="Label" zPosition="2" valign="center" halign="left" position="92,110" size="730,65" font="Regular; 30" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" />

<widget source="session.VideoPicture" render="Pig" position="53,133" size="420,236" backgroundColor="transparent" zPosition="-10" />
<ePixmap position="60,410" zPosition="2" size="391,201" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/logo_ajustes.png" alphatest="blend" />

<widget source="session.CurrentService" render="Label" position="100,650" size="410,25" font="Regular; 22" transparent="1" valign="center" zPosition="2" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" halign="left">
			  <convert type="ServiceName">Name</convert>

			</widget>
<eLabel text="Ipk Remove" position="45,490" size="400,65" font="Regular;30" zPosition="2" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="#000000"/>

<widget source="global.CurrentTime" render="Label" position="949,30" size="251,55" backgroundColor="#0140b1" foregroundColor="#00ffffff" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2"> 
		<convert type="ClockToText">Format:%-H:%M</convert> 
		</widget> 

		<widget source="global.CurrentTime" render="Label" position="900,50" size="300,55" backgroundColor="#0140b1" foregroundColor="#00ffffff" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2"> 
		<convert type="ClockToText">Date</convert>  
		</widget>
<widget source="menu" render="Listbox" position="592,191" size="628,350" scrollbarMode="showNever" foregroundColor="#ffffff" backgroundColor="#6e6e6e" backgroundColorSelected="#fd6502" transparent="1">
	<convert type="TemplatedMultiContent">

		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description

			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 21),gFont("Regular", 16)],

	"itemHeight": 50
	}
	</convert>

	</widget>
	<ePixmap position="690,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />

	<widget source="key_red" render="Label" position="730,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f"  foregroundColor="#000000" transparent="1" />
	<ePixmap position="810,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="850,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />

	<ePixmap position="980,652" zPosition="1" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="1020,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />

</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel - Ipk Remove"))
		self.session = session
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnInstall"))
		self["key_yellow"] = StaticText(_("Adv. UnInstall"))
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.Remove,
				"green": self.Remove,
				"red": self.cancel,
				"yellow": self.ARemove,
			},-1)
		
	def nList(self):
		self.list = []
		ipkminipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipkmini.png"))
		for line in open(status):
			try:
				if line.find("Package:") > -1:
					name1 = line.replace("\n","").split()[-1]
				elif line.find("Version:") > -1:
					name2 = line.split()[-1] + "\n"
					self.list.append((name1, name2, ipkminipng))
			except:
				pass
		self.list.sort()
		self["menu"].setList(self.list)
		
	def cancel(self):
		self.close()
		
	def Remove(self):
		try:
			os.system("opkg remove %s" % self["menu"].getCurrent()[0])
			self.mbox = self.session.open(MessageBox, _("%s is UnInstalled" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox, _("%s is Error UnInstalled" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()

	def ARemove(self):
		try:
			os.system("opkg remove -force-remove %s" % self["menu"].getCurrent()[0])
			self.mbox = self.session.open(MessageBox, _("%s is UnInstalled" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox, _("%s is Error UnInstalled" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
		self.nList()
#####################################################################################
class downfeed(Screen):
	skin = """
<screen name="downfeed" position="0,0" size="1280,720" title="LBpanel-Install extensions from feed">
<ePixmap position="0,0" zPosition="-4" size="1281,721" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo_1_test3.png" alphatest="blend" />

<eLabel text="LBpanel Ipk Tools" position="460,30" size="400,65" font="Regular;45" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="#0140b1"/>

<widget source="Title" transparent="1" render="Label" zPosition="2" valign="center" halign="left" position="92,110" size="730,65" font="Regular; 30" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" />

<widget source="session.VideoPicture" render="Pig" position="53,133" size="420,236" backgroundColor="transparent" zPosition="-10" />
<ePixmap position="60,410" zPosition="2" size="391,201" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/logo_ajustes.png" alphatest="blend" />

<widget source="session.CurrentService" render="Label" position="100,650" size="410,25" font="Regular; 22" transparent="1" valign="center" zPosition="2" backgroundColor="#000000" foregroundColor="#ffffff" noWrap="1" halign="left">
			  <convert type="ServiceName">Name</convert>

			</widget>
<eLabel text="Feed Install" position="45,490" size="400,65" font="Regular;30" zPosition="2" halign="center" noWrap="1" transparent="1" foregroundColor="#ffffff" backgroundColor="#000000"/>

<widget source="global.CurrentTime" render="Label" position="949,30" size="251,55" backgroundColor="#0140b1" foregroundColor="#00ffffff" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2"> 
		<convert type="ClockToText">Format:%-H:%M</convert> 
		</widget> 

		<widget source="global.CurrentTime" render="Label" position="900,50" size="300,55" backgroundColor="#0140b1" foregroundColor="#00ffffff" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2"> 
		<convert type="ClockToText">Date</convert>  
		</widget>
<widget source="menu" render="Listbox" position="592,191" size="628,350" scrollbarMode="showNever" foregroundColor="#ffffff" backgroundColor="#6e6e6e" backgroundColorSelected="#fd6502" transparent="1">
	<convert type="TemplatedMultiContent">

		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description

			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 21),gFont("Regular", 16)],

	"itemHeight": 50
	}
	</convert>

	</widget>
	<ePixmap position="940,652" zPosition="2" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<ePixmap position="1060,652" zPosition="2" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="980,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f"  foregroundColor="#000000" transparent="1" />
	<widget source="key_green" render="Label" position="1100,650" zPosition="2" size="200,30" font="Regular;20" backgroundColor="#8f8f8f" foregroundColor="#000000" transparent="1" />

</screen>"""
	  
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel-Install extensions from feed"))
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.nList()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.setup,
				"green": self.setup,
				"red": self.cancel,
			},-1)
		self.list = [ ]
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		
	def nList(self):
		self.list = []
		os.system("opkg update")
		try:
			ipklist = os.popen("opkg list")
		except:
			pass
		png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipkmini.png"))
		if ipklist:
			for line in ipklist.readlines():
				try:
					self.list.append(("%s %s" % (line.split(' - ')[0], line.split(' - ')[1]), line.split(' - ')[-1], png))
				except:
					pass
		self["menu"].setList(self.list)
		
	def cancel(self):
		self.close()
		
	def setup(self):
		os.system("opkg install -force-reinstall %s" % self["menu"].getCurrent()[0])
		self.mbox = self.session.open(MessageBox, _("%s is installed" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )
##############################################################################
