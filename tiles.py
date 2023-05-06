from PyQt5.QtWidgets import QGraphicsItemGroup
#from PyQt5.QtCore import Qt

from tile import TileItem

class TilesItem(QGraphicsItemGroup):

    @classmethod
    def width(cls, num_x):
        return (TileItem.size) * num_x

    @classmethod
    def height(cls, num_y):
        return TileItem.size * num_y

    def __init__(self, width, height, d=None):

        super().__init__()

        self._tiles = {}
        for y in range(height):
            for x in range(width):
                tile = TileItem(x, y, self)
                self.addToGroup(tile)
                self._tiles[x,y] = tile

    def __getitem__(self, key):
        return self._tiles[key]
    

