#!/usr/bin/python
import sys

import openttd_companion.gui.options as options
from openttd_companion.config import Config

if __name__ == '__main__':

    args = options.parse(Config()) #do this first so exit will be quicker on errors and help

    from openttd_companion.gui.main_window import MainWindow
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setCursorFlashTime(0) # WOW! QT really put this in outer class
    app.setOrganizationName("openttd");
    app.setOrganizationDomain("org");
    app.setApplicationName("companion");
    ex = MainWindow(args)
    sys.exit(app.exec_())

