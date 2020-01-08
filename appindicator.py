import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

from pasw import PastWindow, key_listen
ctrl , alt, f = False, False, False

APPINDICATOR_ID = 'Snipaste'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, 'whatever', appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    # item_cap = gtk.MenuItem("截图")
    # item_cap.connect("activate", capture)
    # menu.append(item_cap)
    item_quit = gtk.MenuItem('退出')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu
def capture(source):
    PastWindow()

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    key_listen()
    main()