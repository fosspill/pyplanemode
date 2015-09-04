#! /usr/bin/python2

import sys
import os
import os.path
import gtk
from subprocess import CalledProcessError, check_output, call

pygtklibdir = os.path.join("/usr/lib", "pygtk", "2.0")
sys.path.insert(0, pygtklibdir)

class SystrayIconApp:
	def __init__(self):
		self.tray = gtk.StatusIcon()
		self.tray.set_from_stock(gtk.STOCK_PREFERENCES) 
		self.tray.connect('popup-menu', self.on_right_click)
		self.tray.set_tooltip(('Pyplanemode'))
		

	def on_right_click(self, icon, event_button, event_time):
		self.make_menu(event_button, event_time)

	def make_menu(self, event_button, event_time):
		menu = gtk.Menu()

		try:
			output = check_output(["rfkill", "list"])
		except CalledProcessError as e:
			output=(e.returncode)
			
		#dirty way to check if airplane mode is on or not... only works with english operating systems :D
		if "yes" not in output:
			# Add ON button
			on = gtk.MenuItem("Turn on airplane mode")
			on.show()
			menu.append(on)
			on.connect('activate', self.airplanemode_on)
		else:
			# Add OFF button
			off = gtk.MenuItem("Turn off airplane mode")
			off.show()
			menu.append(off)
			off.connect('activate', self.airplanemode_off)
		
		# show about dialog
		about = gtk.MenuItem("About")
		about.show()
		menu.append(about)
		about.connect('activate', self.show_about_dialog)

		# add quit item
		quit = gtk.MenuItem("Quit")
		quit.show()
		menu.append(quit)
		quit.connect('activate', gtk.main_quit)

		menu.popup(None, None, gtk.status_icon_position_menu,
				   event_button, event_time, self.tray)

	def airplanemode_on(self, widget):
		call(["gksudo", "rfkill block all"])

	def airplanemode_off(self, widget):
		call(["gksudo", "rfkill unblock all"])


	def  show_about_dialog(self, widget):
		about_dialog = gtk.AboutDialog()
		about_dialog.set_destroy_with_parent (True)
		about_dialog.set_icon_name ("Pyplanemode")
		about_dialog.set_name('Pyplanemode')
		about_dialog.set_version('0.4')
		about_dialog.set_copyright("Copyleft 2015 Ole Erik Brennhagen")
		about_dialog.set_comments(("Fancy airplane mode applet"))
		about_dialog.set_authors(['Ole Erik Brennhagen <oleerik@startmail.com>', 'Ivanka Heins'])
		about_dialog.run()
		about_dialog.destroy()

if __name__ == "__main__":
	SystrayIconApp()
	gtk.main()