#!/usr/bin/python

import sys
import fcntl
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QAction, QToolBar,
    QFileDialog,
)
from PyQt5.QtGui import(
    QKeySequence, QIcon
)
from PyQt5.QtCore import(
    Qt, 
    QTimer, QFile, QSaveFile,
)

import qrc_resources
from debug_parser import DebugParser

def tr(text): return text

from view import View

class ViewMenu(QMenu):
    
    def __init__(self, window, actions):

        super().__init__(tr("&View"), window)
        for key, action in actions.items():
            self.addAction(action)


class FileMenu(QMenu):
    
    def __init__(self, window, actions):

        super().__init__(tr("&File"), window)
        for key, action in actions.items():
            self.addAction(action)


class MainWindow(QMainWindow):
    
    polling_ms = 1000
    starting_map = (64, 64)
    extension = ".map"

    def __init__(self):

        super().__init__()

        self.widget = MainWidget(*self.starting_map)
        self.setCentralWidget(self.widget)

        self._createToolbars()

        actions = self._createActions()
        self._createMenus(actions)
        #self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle(tr('OpenTTD Observer'))
        self.show()

        self.parser = DebugParser(self.onMapUpdate)
        self.map_dict = None

        # XXX we HAVE to set the file to non-blocking or it will just hang
        # unfortunately this is not portable to windows
        self.stdin = open(sys.stdin.fileno())
        flags = fcntl.fcntl(self.stdin, fcntl.F_GETFL)
        fcntl.fcntl(self.stdin, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        # https://doc.qt.io/qt-6/qiodevicebase.html:
        # ... for example, QTcpSocket does not support Unbuffered mode, 
        # and limitations in the native API prevent QFile from supporting 
        # Unbuffered on Windows.
        # I cant even get the below to non-block in linux!

        #self.stdin = QFile()
        #self.stdin.open(
        #    sys.stdin.fileno(),
        #    QFile.ReadOnly | QFile.Unbuffered | QFile.Text
        #    )

        # other workarounds:
        # - start it as a sub-process in qt.

        timer = QTimer(self)
        timer.timeout.connect(self.onPollStdin)
        timer.start(self.polling_ms)
        
    def onPollStdin(self):
        
        n = 0
        data = ""
        while True:
            l = sys.stdin.read(64)
            if not l:
                break
            data += l

        if not data:
            return
        for line in data.split("\n"):
            self.parser.onData(line)

    def onMapUpdate(self, d):
        self.map_dict = d
        self.widget.view.resetScene(d)

    def _createMenus(self, actions):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        menubar.addMenu(FileMenu(self, actions))
        menubar.addMenu(ViewMenu(self, self.widget.actions))

    def saveMap(self):
        if not self.map_dict:
            return False
        ex = self.extension
        name = QFileDialog.getSaveFileName(
            self,
            tr("Save Map"), 
            "./", 
            tr("Map Files (*{})").format(ex))[0]
        if not name.endswith(ex):
            name += ex
        with open(name, "w") as f:
            f.write(str(self.map_dict))
            f.flush()
        return True

    def _createActions(self):
        
        actions = {}

        save = QAction(tr("Save"), self)
        save.triggered.connect(self.saveMap)
        save.setShortcut(QKeySequence(
            Qt.CTRL | Qt.Key(Qt.Key_S),
            ))
        #save.setIcon(QIcon(":exit.svg"))
        actions["save"] = save 

        quit = QAction(tr("Quit"), self)
        quit.triggered.connect(QApplication.quit)
        quit.setShortcut(QKeySequence(
            Qt.CTRL | Qt.Key(Qt.Key_Q),
            ))
        quit.setIcon(QIcon(":exit.svg"))
        actions["quit"] = quit

        test = QAction("test", self)
        test.triggered.connect(self._test)
        actions["test"] = test

        return actions

    def _test(self):
        self.widget.view.resetScene(32,32)
        print("test")

    def _createToolbars(self):

        toolbar = QToolBar()
        #toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        for action in self.widget.actions.values():
            toolbar.addAction(action)


class MainWidget(QWidget):

    def __init__(self, width, height):
        super().__init__()

        self.view = View(width, height)
        self.actions = self._initActions(self.view)

        outer = QHBoxLayout()
        #outer.addStretch(1)
        outer.addWidget(self.view)
        self.setLayout(outer)

        self.show()
        self.view.cmdZoomFit()

    def _initActions(self, view):

        actions = {}

        zoomin = QAction(tr("Zoom In"), self)
        zoomin.triggered.connect(view.cmdZoomIn)
        zoomin.setShortcut(QKeySequence(Qt.Key(Qt.Key_Equal)))
        zoomin.setIcon(QIcon(":zoom-in.svg"))
        actions["zoomin"] = zoomin

        zoomout = QAction(tr("Zoom Out"), self)
        zoomout.triggered.connect(view.cmdZoomOut)
        zoomout.setShortcut(QKeySequence(Qt.Key(Qt.Key_Minus)))
        zoomout.setIcon(QIcon(":zoom-out.svg"))
        actions["zoomout"] = zoomout

        zoomfit = QAction(tr("Zoom Fit"), self)
        zoomfit.triggered.connect(view.cmdZoomFit)
        zoomfit.setShortcut(QKeySequence(Qt.Key(Qt.Key_0)))
        zoomfit.setIcon(QIcon(":zoom-best.svg"))
        actions["zoomfit"] = zoomfit

        return actions


if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = MainWindow()
     sys.exit(app.exec_())

