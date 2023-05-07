from PyQt5.QtWidgets import (QGraphicsRectItem)
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt


class TileItem(QGraphicsRectItem):

    pen_width = 2
    size = 20
    color = Qt.gray

    def __init__(self, x, y, parent):
        size = self.size
        super().__init__(0, 0, size, size, parent)

        # Set the origin (position) of the rectangle in the scene.
        self.setPos(x*size, y*size)
        # Define the brush (fill).
        brush = QBrush(self.color)
        self.setBrush(brush)
        # Define the pen (line)
        pen = QPen(Qt.gray)
        pen.setWidth(self.pen_width)
        self.setPen(pen)

class LandTileItem(TileItem):
    color = Qt.green

class WaterTileItem(TileItem):
    color = Qt.blue
