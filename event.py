import grid

ID = 18

def onData(data):
    if data.startswith("dbg: [script]"): #if its a game script or ai
        onScript(data)
    else:
        print(data.strip()) # pass through

def onScript(data):
    pieces = data.split()
    pieces = pieces[2:]
    if pieces[0] == "[{}]".format(ID): #if its our script
        kind = pieces[1][1]
        pieces = " ".join(pieces[1:])
        if kind == "I":
            onInfo(pieces)
        elif kind == "W":
            onWarning(pieces)
        elif kind == "E":
            onError(pieces)
        elif kind == "S":
            onStackTrace(pieces)
        elif kind == "P":
            onPrint(pieces)
        else:
            raise ValueError("unknown message type: " + data.strip())
    else:
        print(data.strip()) # someone elses; pass through

def onInfo(data):
    print(data)

def onWarning(data):
    print(data)

def onError(data):
    print(data)

def onStackTrace(data):
    pieces = data.split('dbg: ')
    header = '[script] [{}] '.format(ID)
    for i, piece in enumerate(pieces):
        if piece.startswith(header):
            pieces[i] = pieces[i][len(header):]
    print()
    print("\n".join(pieces))
    print()

def onPrint(data):
    if data.startswith("[P] [J]"):
        onJson(data)
    else:
        print(data)

def onJson(data):
    head, date, json = data.split("|")
    grid.parse(json)

