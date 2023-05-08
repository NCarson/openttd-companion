import sys
import json
import copy

from mylogger import Logging, SimpleStreamFormatter
game_logger = Logging.getLogger(
    "test.log",
    stream_formatter=SimpleStreamFormatter(),
    )

class TTDOutputParser:
    
    def __init__(self, callback, ids=[]):
        self.ids = ids or [None]
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
            self.write("out: " + data) # pass through

    def onScript(self, data):
        pieces = data.split()
        pieces = pieces[2:]
        handled = False
        for id in self.ids:
            if (id is None # pass through all scripts
                or pieces[0] == "[{}]".format(id) #if its our script
                ):
                kind = pieces[1][1]
                pieces = " ".join(pieces[1:])

                if kind == "I": # check what kind of message
                    self.onInfo(pieces)
                    handled = True
                elif kind == "W":
                    self.onWarning(pieces)
                    handled = True
                elif kind == "E":
                    self.onError(pieces)
                    handled = True
                elif kind == "S":
                    self.onStackTrace(pieces)
                    handled = True
                elif kind == "P":
                    self.onPrint(pieces)
                    handled = True
                else:
                    raise ValueError("unknown message type: " + data.strip())

        if not handled:
            self.write(data) # someone elses; pass through

    def onInfo(self, data): # can we actually get these?
        stamp, game_date, method, msg = data.split(":")
        game_logger.info(msg, game_date=game_date, method=method)

    def onWarning(self, data):
        stamp, game_date, method, msg = data.split(":")
        game_logger.warning(msg, game_date=game_date, method=method)

    def onError(self, data):
        stamp, game_date, method, msg = data.split(":")
        game_logger.error(msg, game_date=game_date, method=method)

    def onStackTrace(self, data):
        pieces = data.split('dbg: ')
        for id in self.ids:
            header = '[script] [{}] '.format(id)
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
        game_logger.debug("JSON ...", game_date=date, method='')
        j = json.loads(data)
        self.callback(j)


