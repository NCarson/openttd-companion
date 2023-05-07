import sys
import json

ID = 18

class TTDOutputParser:
    
    def __init__(self, callback):
        self.callback = callback
        self.out = sys.stderr

    def write(self, data):
        self.out.write(data)
        self.out.write("\n")
        self.out.flush()

    def onData(self, data):
        if data.startswith("dbg: [script]"): #if its a game script or ai
            self.onScript(data)
        else:
            self.write(data) # pass through

    def onScript(self, data):
        pieces = data.split()
        pieces = pieces[2:]
        if pieces[0] == "[{}]".format(ID): #if its our script
            kind = pieces[1][1]
            pieces = " ".join(pieces[1:])
            if kind == "I": # check what kind of message
                self.onInfo(pieces)
            elif kind == "W":
                self.onWarning(pieces)
            elif kind == "E":
                self.onError(pieces)
            elif kind == "S":
                self.onStackTrace(pieces)
            elif kind == "P":
                self.onPrint(pieces)
            else:
                raise ValueError("unknown message type: " + data.strip())
        else:
            self.write(data) # someone elses; pass through

    def onInfo(self, data): # can we actually get these?
        self.write(data)

    def onWarning(self, data):
        self.write(data)

    def onError(self, data):
        self.write(data)

    def onStackTrace(self, data):
        pieces = data.split('dbg: ')
        header = '[script] [{}] '.format(ID)
        for i, piece in enumerate(pieces):
            if piece.startswith(header):
                pieces[i] = pieces[i][len(header):]
        self.write("\n" + "\n".join(pieces) + "\n")

    def onPrint(self, data):
        if data.startswith("[P] [J]"): # if its our json flag
            self.onJson(data)
        else:
            self.write(data)

    def onJson(self, data):
        head, date, data = data.split("|")
        self.write("parser: recieved json data:" + date)
        j = json.loads(data)
        self.callback(j)


