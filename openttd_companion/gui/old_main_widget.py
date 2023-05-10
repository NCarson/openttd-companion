from PyQt5.QtWidgets import (
    QWidget, QAction,
    QVBoxLayout, QHBoxLayout,
)
from PyQt5.QtGui import(
    QKeySequence, QIcon
)
from PyQt5.QtCore import(
    Qt, 
)

from .view import View

def tr(text): return text

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
