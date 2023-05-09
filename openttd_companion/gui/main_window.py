import sys
import fcntl
import os
import json

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QAction, QToolBar,
    QFileDialog, QMessageBox,
)
from PyQt5.QtGui import(
    QKeySequence, QIcon
)
from PyQt5.QtCore import(
    Qt, 
    QTimer, QFile, QSaveFile,
)

import openttd_companion.__init__ as init
import openttd_companion.gui.qrc_resources as qrc_resources
from .main_widget import MainWidget

DEBUG=True

def tr(text): return text
class MainWindow(QMainWindow):
    
    polling_ms = 1000
    starting_map = (64, 64)
    extension = ".map"

    def __init__(self, options):

        super().__init__()

        self._options = options
        self._map_dict = None
        self._current_path = None

        self._widget = MainWidget(*self.starting_map)
        self.setCentralWidget(self._widget)

        self._toolbar = self._createToolbar()
        self._actions = self._createActions()
        self._createMenus(self._actions)
        #self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle(tr(init.__title__))
        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.onPollUdp)
        timer.start(self.polling_ms)

        if options.map:
            self.cmdOpenMap(options.map)

    def _test(self):
        self._widget.view.setScene(self._widget.view._newScene(32,32))
        self._map_dict = None
        self._actions["save as"].setDisabled(True)

    def _createMenus(self, actions):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        menubar.addMenu(FileMenu(self, actions))
        menubar.addMenu(ViewMenu(self, self._widget.actions))
        menubar.addMenu(HelpMenu(self))

    def _createActions(self):
        
        actions = {}

        open = QAction(tr("Open"), self)
        open.triggered.connect(self.cmdOpenMap)
        open.setIcon(QIcon(":open.svg"))
        open.setShortcut(QKeySequence(
            Qt.CTRL | Qt.Key(Qt.Key_O),
            ))
        actions["open"] = open

        save = QAction(tr("Save As Map"), self)
        save.triggered.connect(self.cmdSaveAsMap)
        save.setIcon(QIcon(":save-as.svg"))
        save.setShortcut(QKeySequence(
            Qt.CTRL | Qt.Key(Qt.Key_S),
            ))
        save.setDisabled(True)
        actions["save as"] = save 

        quit = QAction(tr("Quit"), self)
        quit.triggered.connect(QApplication.quit)
        quit.setShortcut(QKeySequence(
            Qt.CTRL | Qt.Key(Qt.Key_Q),
            ))
        quit.setIcon(QIcon(":exit.svg"))
        actions["quit"] = quit

        if DEBUG:
            test = QAction("test", self)
            test.setShortcut(QKeySequence(
                Qt.Key(Qt.Key_T),
                ))
            test.triggered.connect(self._test)
            actions["test"] = test

        return actions

    def _createToolbar(self):

        toolbar = QToolBar()
        #toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        for action in self._widget.actions.values():
            toolbar.addAction(action)
        return toolbar

    def onPollUdp(self):

        import socket
        UDP_IP = "127.0.0.1" #FIXME
        UDP_PORT = 6789
        BUF_SIZE=1024

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

        sock.bind((UDP_IP, UDP_PORT))
        sock.setblocking(0)

        try:
            msg = sock.recv(BUF_SIZE)
            msg = msg.decode("utf-8")
            print("received message: %s" % repr(msg))
        except BlockingIOError:
            print("blocking io error") #FIXME
            


    def onPollStdin(self):
        from .server.ttd_output_parser import TTDOutputParser #FIXME this is broken
        
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
        self._map_dict = d
        self._widget.view.resetScene(d)
        self._actions["save as"].setDisabled(False)

    def cmdOpenMap(self, path=None):

        if path:
            self._current_path = path
        else:
            ex = self.extension
            name = QFileDialog.getOpenFileName(
                self,
                tr("Open Map"), 
                #"./", 
                None,
                tr("Map Files (*{})").format(ex))[0]
            if not name:
                return False
            self._current_path = name

        with open(self._current_path) as f:
            s = f.read()
            d = json.loads(s)
            self._map_dict = d
            self.onMapUpdate(d)
        return True

    def cmdSaveAsMap(self):
        if not self._map_dict:
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
            j = json.dumps(self._map_dict)
            f.write(json.dumps(self._map_dict))
        return True

    def cmdToggleToolbarItem(self, action, toggled):
        action.setVisible(toggled)


class HelpMenu(QMenu):
    
    def __init__(self, window):

        super().__init__(tr("&Help"), window)

        self.window = window
        action = QAction("About", self)
        action.triggered.connect(self.getAbout)
        self.addAction(action)

    def getAbout(self):
        title = "{} {}".format(init.__title__, init.__version__)
        QMessageBox.about(self.window, title, "FIXME")

class ViewMenu(QMenu): #FIXME Toolbar Items reference the menu and the toolbar for visibility
    # we will probably have to recreate the toolbar
    
    def __init__(self, window, actions):

        super().__init__(tr("&View"), window)
        for key, action in actions.items():
            self.addAction(action)

        def f(a) :
            return lambda toggled : window.cmdToggleToolbarItem(a, toggled)

        #toolbar = window.toolbar()
        tools = self.addMenu(tr("Toolbar Items"))
        for key, action in actions.items():
            new = QAction(action.text(), self)
            new.setIcon(action.icon())
            new.setCheckable(True)
            new.setChecked(True)
            tools.addAction(new)
            new.triggered.connect(f(action))


class FileMenu(QMenu):
    
    def __init__(self, window, actions):

        super().__init__(tr("&File"), window)
        for key, action in actions.items():
            self.addAction(action)

