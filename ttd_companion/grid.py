import json


class Grid:

    @classmethod
    def decodeString(cls, data):
        o = []
        for piece in data.split():
            if piece.startswith('z'): # compressed 0's
                o.append("0" * int(piece[1:]))
            elif piece.startswith('f'):
                o.append("F" * int(piece[1:])) # compressed F's
            else:
                o.append(piece)

        return "".join(o)
    
    def __init__(self, max_x, max_y, data):
        self._max_x = max_x
        self._max_y = max_y
        s = self.decodeString(data)
        self._str, self._num = self._parse(s)

    def __getitem__(self, idx):
        x, y = idx
        mx = self._max_x
        x = mx - x # openttd origin is the ne corner of map
        return int(self._str[(y * mx + x)])

    def __len__(self):
        return len(self._str)

    def __iter__(self):
        return iter(self._str)

    def str(self):
        out = []
        for i in range(len(self._str)):
            out.append(self._str[i])
            if (i and not ((i+1) % 64)): # break it up so we can see on terminal
                out.append("\n")
        return "".join(out)

    def iterIndexes(self):
        for y in range(self._max_y):
            for x in range(self._max_x):
                yield (x, y)

    def _parse(self, data):

        size = len(data) * 4 # hex encodes 4 bits
        # python integer size is only limited by memory so I guess
        # we dont have to break up the numbers
        num = int(data, 16) # convert to hex
        o = []

        for i in range(size):
            if ((num & 1 << i) != 0): # check the bit
                o.append("1")
            else:
                o.append("0")
        return o, num

if __name__ == "__main__":
    test = {"map": {"y": 64, "x": 64, "is_water": "z368 C z15 C z15 C z15 C z14 1C z14 1C z14 1E z14 7F8 z13 C z13 C z13 C z13 7FE z13 7FC z13 3FC z13 3F8 z13 3 z14 3 z14 3 z14 3 z14 3 z14 3 z14 3 z14 3 z14 3 z14 3F8 z13 1F8 z13 1F8 z13 1 z65 18 z15 C z141"}, "industries": [{"name": "Little Flondbourne Iron Ore Mine", "x": 21, "y": 12}, {"name": "Lenningpool Oil Wells", "x": 34, "y": 39}, {"name": "Little Flondbourne Farm", "x": 26, "y": 53}, {"name": "Lenningpool Steel Mill", "x": 55, "y": 56}, {"name": "Little Flondbourne Factory", "x": 16, "y": 31}, {"name": "Little Flondbourne Oil Refinery", "x": 13, "y": 28}, {"name": "Little Flondbourne Forest", "x": 16, "y": 6}, {"name": "Little Flondbourne Sawmill", "x": 37, "y": 21}, {"name": "Little Flondbourne Power Plant", "x": 5, "y": 6}, {"name": "Little Flondbourne Coal Mine", "x": 31, "y": 19}], "towns": [{"y": 25, "x": 23, "name": "Little Flondbourne", "population": 229, "house_num": 12}, {"y": 43, "x": 49, "name": "Lenningpool", "population": 668, "house_num": 26}]}
    s = test["map"]["is_water"]
    g = Grid(64, 64, s)
    print(g.str())
    print(len(g))

