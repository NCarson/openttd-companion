import sys
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

from .tiles import TilesItem

class View(QGraphicsView):
    
    def __init__(self, width, height):

        # Defining a scene rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.tiles = None
        scene = self._newScene(width, height)
        super().__init__(scene)
        circle = QGraphicsEllipseItem(10*20,10*20, self.tiles.width(1), self.tiles.height(1), self.tiles)
        self._setScrollBars()

    def _newScene(self, width, height, d=None):

        scene = QGraphicsScene(0, 0,
            TilesItem.width(width), 
            TilesItem.height(height),
        )
        self.tiles = TilesItem(width, height, d)
        scene.addItem(self.tiles)
        return scene

    def _setScrollBars(self):

        #hscale = self.transform().m11()
        #vscale = self.transform().m22()
        hscale = 1
        vscale = 1
        
        bar = self.horizontalScrollBar()
        bar.setSingleStep(self.tiles.width(1) * hscale)
        bar.setPageStep(self.tiles.width(10) * hscale)

        bar = self.verticalScrollBar()
        bar.setSingleStep(self.tiles.width(1) * vscale)
        bar.setPageStep(self.tiles.width(10) * vscale)

    def resetScene(self, d):
        w, h = d["map"]['x'], d['map']['y']
        self.setScene(self._newScene(w, h, d))
        
    def cmdZoomOut(self, *args):
        self.scale(.8, .8)
        #self._setScrollBars()

    def cmdZoomIn(self, *args):
        self.scale(1.25, 1.25)
        #self._setScrollBars()

    def cmdZoomFit(self, *args):
        self.fitInView(self.tiles, Qt.AspectRatioMode.KeepAspectRatio)
        #self._setScrollBars()

    #unused events
    def _keyPressEvent(self, event) :
        if (event.key() == Qt.Key_Left):
            print('left')
            bar = self.horizontalScrollBar()
            r = bar.maximum() - bar.minimum()
            step = self.tilesWidth(1)


            self.scrollContentsBy(self.tiles.width(-1), 0)
        elif (event.key() == Qt.Key_Right):
            print('right')
            self.scrollContentsBy(self.tiles.width(1), 0)

    def _event(self, e):
        print(11, e)
        return False

