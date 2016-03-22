from kml.library import Library
from kml.ui import main_window, settings_popup
from kml import bg_file_io
from PyQt4 import QtGui, QtCore
import sys
import os
import threading
import time


class ThreadedWindow(threading.Thread):
    def __init__(self, window):
        super(ThreadedWindow, self).__init__()
        self.window = window
        self._abort = False

    def run(self):
        self.window.show()
        while not self._abort or not self.window.completed:
            time.sleep(0.2)

    def finish(self):
        self._abort = True


def main():
    app = QtGui.QApplication(sys.argv)
    
    if not os.path.isfile('settings.ini'):
        # settings_window = settings_popup.SettingsPopup()
        # t = ThreadedWindow(settings_window)
        # t.start()
        # t.join()
        folder = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Library Directory"))
        if not folder:
            exit()
        with open('settings.ini', 'w') as file:
            file.write('[Library]\nlibrary_directory={}'.format(folder))

    Library.init_site_list()
    Library.load()
    bg_file_io.initialize()

    window = main_window.Window()
    window.show()
    sys.exit(app.exec_())
    pass

if __name__ == '__main__':
    main()

"""
Something similar to what i am trying to do on osx https://github.com/DrabWeb/Komikan
MyAnimeList package documentation http://python-mal.readthedocs.org/en/latest/getting_started.html
"""
