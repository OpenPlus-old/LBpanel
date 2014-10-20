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
	<screen name="IPKToolsScreen" position="center,center" size="1150,600" title="LBpanel Ipk Tools">
	<ePixmap position="700,10" zPosition="1" size="450,590" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo19.png" alphatest="blend" transparent="1" />
	<ePixmap position="705,580" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="855,580" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" transparent="1" alphatest="on" />
	<ePixmap position="1005,580" zPosition="1" size="150,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source = "key_red" render="Label" position="705,530" zPosition="2" size="150,50" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source = "key_green" render="Label" position="855,530" zPosition="2" size="150,50" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source = "key_yellow" render="Label" position="1005,530" zPosition="2" size="150,50" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="660,580" >
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
		dospng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ipk.png"))
		self.list.append((_("IPK installer"),"one", _("Install ipk, bh.tgz, tar.gz, nab.tgz in /tmp"), onepng ))
		self.list.append((_("Feed installer"),"six", _("Feed installer"), sixpng ))
		self.list.append((_("Download extensions"),"five", _("Download feeds packages"), fivepng))
		self.list.append((_("IPK delete packages"),"four", _("Delete IPK packages"), treepng ))
		self.list.append((_("Sorys Channel List"),"dos", _("Download Sorys Channel List"), dospng ))
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
		elif item is "dos":
			self.session.openWithCallback(self.mList,installsorys)
			
###############################################
class DownloadFeed(Screen):
	skin = """
<screen name="DownloadFeed" position="center,110" size="850,520" title="Download extensions from feed">
<widget source="menu" render="Listbox" position="15,10" size="820,455" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap name="red" position="20,512" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap name="green" position="190,512" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" transparent="1" alphatest="on" />
	<ePixmap name="yellow" position="410,512" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget name="key_red" position="20,482" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget name="key_green" position="190,482" zPosition="2" size="220,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget name="key_yellow" position="410,482" zPosition="2" size="220,30" valign="center" halign="center" font="Regular;22" transparent="1" />
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
class installsorys(Screen):
	skin = """
<screen name="installsorys" position="center,160" size="1150,500" title="LBpanel-Download Sorys Settings">
    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo10.png" alphatest="blend" transparent="1" />
<widget source="menu" render="Listbox" position="15,10" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap name="red" position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap name="green" position="190,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" transparent="1" alphatest="on" />
	<widget name="key_red" position="20,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget name="key_green" position="190,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""
	  
	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("LBpanel-Download Sorys Settings"))
		self.session = session
		self.list = []
		self["menu"] = List(self.list)
		self.feedlist()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"green": self.setup,
				"red": self.cancel,
			},-1)
		self.list = [ ]
		self["key_red"] = Label(_("Close"))
		self["key_green"] = Label(_("Install"))
		
	def feedlist(self):
		self.list = []
		os.system("opkg update")
		camdlist = os.popen("opkg list | grep sorys")
		softpng = LoadPixmap(cached = True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/emumini.png"))
		for line in camdlist.readlines():
			try:
				self.list.append(("%s %s" % (line.split(' - ')[0], line.split(' - ')[1]), line.split(' - ')[-1], softpng))
			except:
				pass
		camdlist.close()
		self["menu"].setList(self.list)
		
	def ok(self):
		self.setup()
		
	def setup(self):
		self.session.open(Console,title = _("Installing Sorys Settings"), cmdlist = ["opkg install -force-overwrite %s" % self["menu"].getCurrent()[0]])
		
		
	def cancel(self):
		self.close()
#################################################
class InstallAll(Screen):
	skin = """
<screen name="InstallAll" position="center,160" size="750,370" title="LBpanel-Select files to install">
<widget source="menu" render="Listbox" position="15,10" size="720,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" transparent="1" alphatest="on" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="360,358" zPosition="1" size="250,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="360,328" zPosition="2" size="250,30" valign="center" halign="center" font="Regular;22" transparent="1" />
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
<screen name="RemoveIPK" position="center,100" size="750,570" title="LBpanel - Ipk remove">
<widget source="menu" position="15,10" render="Listbox" size="720,500">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" transparent="1" alphatest="on" />
	<ePixmap position="360,558" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_red" render="Label" position="20,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_green" render="Label" position="190,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_yellow" render="Label" position="360,528" zPosition="2" size="200,30" valign="center" halign="center" font="Regular;22" transparent="1" />
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
<screen name="downfeed" position="center,110" size="850,520" title="LBpanel-Install extensions from feed">
<widget source="menu" render="Listbox" position="15,10" size="820,455" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
	<ePixmap position="20,512" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="190,512" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" transparent="1" alphatest="on" />
	<widget source="key_red" render="Label" position="20,482" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_green" render="Label" position="190,482" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
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
