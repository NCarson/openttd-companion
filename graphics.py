
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QApplication
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QPen


class BaseItem: pass
class Tile(BaseItem):
    size = 20

    def __init__(self, x, y):
        size = self.size
        self.item = QGraphicsRectItem(0, 0, size, size)
        # Set the origin (position) of the rectangle in the scene.
        self.item.setPos(x*size, y*size)
        # Define the brush (fill).
        brush = QBrush(Qt.green)
        self.item.setBrush(brush)
        # Define the pen (line)
        pen = QPen(Qt.black)
        pen.setWidth(1)
        self.item.setPen(pen)

app = QApplication(sys.argv)
scene = QGraphicsScene(0, 0, 800, 400)
# Defining a scene rect of 400x200, with it's origin at 0,0.
# If we don't set this on creation, we can set it later with .setSceneRect

for y in range(64):
    for x in range(64):
        tile = Tile(x, y)
        scene.addItem(tile.item)

view = QGraphicsView(scene)
view.show()
app.exec_()
