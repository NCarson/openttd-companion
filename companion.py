#!/usr/bin/python
import sys

import ttd_companion.options as options

if __name__ == '__main__':

    options_ = options.parse() #do this first so exit will be quicker on errors and help

    from ttd_companion.main_window import MainWindow
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = MainWindow(options_)
    sys.exit(app.exec_())

