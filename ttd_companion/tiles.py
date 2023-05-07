from PyQt5.QtWidgets import QGraphicsItemGroup
#from PyQt5.QtCore import Qt

from .tile import TileItem, WaterTileItem, LandTileItem
from .feature import FeatureItem, TownItem, IndustryItem
from .grid import Grid

class TilesItem(QGraphicsItemGroup):

    @classmethod
    def width(cls, num_x):
        return (TileItem.size) * num_x

    @classmethod
    def height(cls, num_y):
        return TileItem.size * num_y

    def __init__(self, width, height, d={}):

        super().__init__()

        if d:
            s = d['map']['is_water']
        else: 
            s = "0" * (width * height // 4) # dummy string

        grid = Grid(width, height, s)
            

        self._tiles = {}
        for x, y in grid.iterIndexes():
            try: #FIXME
                kind = WaterTileItem if grid[(x,y)] else LandTileItem
            except IndexError:
                kind = TileItem
            tile = kind(x, y, self)
            self.addToGroup(tile)
            self._tiles[x,y] = tile

        if d:
            for town in d['towns']:
                x, y = width - town['x'] -1, town['y'] - 1
                name = town['name']
                feature = TownItem(x, y, name, self)
                #self.addToGroup(tile) XXX do we need this?

            for industry in d['industries']:
                x, y = width - industry['x'] -1, industry['y'] - 1
                name = industry['name']
                feature = IndustryItem(x, y, name, self)
                #self.addToGroup(tile) XXX do we need this?

    def __getitem__(self, key):
        return self._tiles[key]
    

