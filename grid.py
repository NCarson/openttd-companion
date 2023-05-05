import json
j = """{ "map": { "x":64, "y":64, "is_water":"z368 C z15 C z15 C z15 C z14 1C z14 1C z14 1E z14 7F8 z13 C z13 C z13 C z13 7FE z13 7FC z13 3FC z13 3F8 z13 3 z14 3 z14 3 z14 3 z14 3 z14 3 z14 3 z14 3 z14 3 z14 3F8 z13 1F8 z13 1F8 z13 1 z65 18 z15 C z141"}}"""

def parse(data):
    d = json.loads(data)
    encoded = d['map']['is_water']
    o = []
    for piece in encoded.split():
        if piece.startswith('z'):
            o.append("0"*int(piece[1:]))
        elif piece.startswith('f'):
            o.append("F"*int(piece[1:]))
        else:
            o.append(piece)
    i = 0
    out = []
    for piece in o:
        for char in piece:
            out.append(char)
            if i and not ((i+1) % 64):
                out.append("\n")
            i += 1

    out = "".join(out).split("\n")
    o = []
    for piece in out:
        if piece == "\n":
            continue
        piece = int(piece, 16)
        for i in range(64):
            if ((piece & 1 << i) != 0):
                o.append("1")
            else:
                o.append("0")
            if i and not ((i+1) % 64):
                o.append("\n")

    o = "".join(o)
    print(o)

