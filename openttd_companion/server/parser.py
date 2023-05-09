import sys
import json
import copy
import logging

import openttd_companion.app_logging as mylogger

logger = mylogger.setup_logger()

def setup_loggers(ids, udp_address, udp_bufsize):
    
    kwargs = {
        "udp_address" : udp_address,
        "udp_bufsize" : udp_bufsize,
        "level": logging.JSON
    }

    #script logger
    class ScriptDebugAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            game_date = kwargs.pop('game_date', self.extra['game_date']).strip()
            method = kwargs.pop('method', self.extra['method']).strip()
            id = kwargs.pop('id', self.extra['id'])
            reset = "\x1b[0m"
            return ':%s %s %s]%s %s' % (id, game_date, method, reset, msg), kwargs

    fmt = "%(color)s[%(levelname)1.1s script%(message)s"
    formatter = mylogger.LogFormatter(fmt=fmt) # we need logzero for color
    script_logger = mylogger.setup_logger(
        name="script_logger", 
        formatter=formatter,
        **kwargs
        )

    script_logger = ScriptDebugAdapter(
        script_logger, 
        {"game_date": None, "method": None, "id":id}
        )

    #game debug
    class GameDebugAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            module = kwargs.pop('module', self.extra['module']).strip()
            reset = "\x1b[0m"
            return ' %s]%s %s' % (module, reset, msg), kwargs

    fmt = "%(color)s[%(levelname)1.1s openttd%(message)s"
    formatter = mylogger.LogFormatter(fmt=fmt) # we need logzero for color
    game_debug_logger = mylogger.setup_logger(
        name="game_debug_logger", 
        formatter=formatter,
        **kwargs
        )
    game_debug_logger = GameDebugAdapter(
        game_debug_logger, 
        {"module": None}
        )

    #json logger
    formatter = mylogger.LogFormatter(fmt="%(color)s%(message)s%(end_color)s")
    json_logger = mylogger.setup_logger(
        name="script_json", 
        formatter=formatter,
        **kwargs
        )

    logger.info(f"setup UDP service on {udp_address[0]}:{udp_address[1]}")
    return script_logger, json_logger, game_debug_logger


class Parser:
    
    def __init__(self, args):
        self.ids = args.ids or [None]
        self.out = sys.stderr

        udp_address = (args.host, args.port)
        self.script_logger, self.json_logger, self.game_debug_logger =\
            setup_loggers(args.ids, udp_address, args.bufsize)

    def write(self, data):
        self.out.write(data)
        self.out.write("\n")
        self.out.flush()

    def onData(self, data):
        if data.startswith("dbg: [script]"): #if its a game script or ai
            self.onScript(data)
        elif data.startswith("dbg: "): # if its stderr
            module, msg = data[5:].split("] ")
            module = module[1:]
            self.game_debug_logger.debug(msg , module=module)

        else: # else its stdout
            self.game_debug_logger.info(data, module='stdout')

    def onScript(self, data):
        pieces = data.split()
        pieces = pieces[2:]
        handled = False
        for id in self.ids:
            if (id is None # pass through all scripts
                or pieces[0] == "[{}]".format(id) #if its our script
                ):
                id = pieces[0][1:-1]
                kind = pieces[1][1]
                pieces = " ".join(pieces[1:])

                if kind == "I": # check what kind of message
                    self.onInfo(id, pieces)
                    handled = True
                elif kind == "W":
                    self.onWarning(id, pieces)
                    handled = True
                elif kind == "E":
                    self.onError(id, pieces)
                    handled = True
                elif kind == "S":
                    self.onStackTrace(id, pieces)
                    handled = True
                elif kind == "P":
                    self.onPrint(id, pieces)
                    handled = True
                else:
                    raise ValueError("unknown message type: " + data.strip())

        if not handled: #FIXME script we are not listening to
            self.write(data) # someone elses; pass through

    def _onLog(self, func, id, data):
        try:
            stamp, game_date, method, msg = data.split(":")
        except ValueError:
            logger.warning("could not parse data")
            msg, game_date, method = data, "", ""
        func(msg, game_date=game_date, method=method, id=id)

    def onInfo(self, id, data):
        self._onLog(self.script_logger.info, id, data)

    def onWarning(self, id, data):
        self._onLog(self.script_logger.warning, id, data)

    def onError(self, id, data):
        self._onLog(self.script_logger.error, id, data)

    def onStackTrace(self, id, data):
        pieces = data.split('dbg: ')
        for id in self.ids: #FIXME this wont work with ids unset
            header = '[script] [{}] '.format(id)
            for i, piece in enumerate(pieces):
                if piece.startswith(header):
                    pieces[i] = pieces[i][len(header):]

            data = ("\n" + "\n".join(pieces) + "\n")
            self.script_logger.critical(data, game_date=None, method=None, id=id)

    def onPrint(self, id, data):
        if data.startswith("[P] [J]"): # if its our json flag
            self.onJson(id, data)
        else:
            self.script_logger.info(data, game_date="", method="", id=id)

    def onJson(self, id, data):
        head, date, data = data.split("|")
        self.json_logger.json("[J script:%s] %s" % (id, data))
        j = json.loads(data)

if __name__ == '__main__':
    pass
    #script_logger, json_logger, game_debug_logger = setup_loggers([1,2])
    #script_logger.warning("HI", game_date=1, method=2, id=3)
    #game_debug_logger.debug("HI", module='m')

