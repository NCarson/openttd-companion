from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QFont
from PyQt5.QtCore import Qt

class FeatureItem(QGraphicsEllipseItem):

    pen_width = 1
    tile_size = 20 #FIXME make this a param for init
    size = 20
    color = Qt.gray

    def __init__(self, x, y, name, parent):

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

        name = QGraphicsTextItem(name, parent)
        font = QFont()
        font.setPointSize(28)
        name.setFont(font)
        name.setPos((x-3)*size, (y-4)*size)

class TownItem(FeatureItem):
    color = Qt.yellow

class IndustryItem(FeatureItem):
    color = Qt.black
