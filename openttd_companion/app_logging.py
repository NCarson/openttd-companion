import socket
import logging

import logzero
from colored import fg#, bg, attr

DEFAULT_FMT = "[%(levelname)1.1s "\
    + "%(asctime)s %(module)s:%(lineno)d] "\
    + "%(message)s"

COLOR_DEFAULT_FMT = "%(color)s[%(levelname)1.1s "\
    "%(asctime)s %(module)s:%(lineno)d]%(end_color)"\
    "%(message)s"

LogFormatter = logzero.LogFormatter


#https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
def addLoggingLevel(levelName, levelNum, methodName=None):
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)
addLoggingLevel("TRACE", 5)
addLoggingLevel("JSON", 4)

logzero.DEFAULT_COLORS = {
    logging.JSON: fg(245),
    logging.TRACE: fg(117),
    logging.DEBUG: fg(31),
    logging.INFO: fg('aquamarine_3'),
    logging.WARNING: fg(186),
    logging.ERROR: fg(168),
    logging.CRITICAL: fg(200)
}

class UdpHandler(logging.Handler):
    
    def __init__(self, host, port, bufsize, level=logging.NOTSET):
        
        if not host:
            raise ValueError("host must be set")
        if not port:
            raise ValueError("port must be set")
        if not bufsize:
            raise ValueError("bufsize must be set")

        super().__init__(level=level)
        self.address = (host, port)
        self.bufsize = bufsize
        self.sock = None

    def emit(self, record):

        def split_msg(msg, size):
            return ([msg[i:i+size] for i in range(0, len(msg), size)])

        if not self.sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        msg = bytes(self.format(record) + "\n", "utf-8")

        for piece in split_msg(msg, self.bufsize):
            self.sock.sendto(piece, self.address)


def setup_logger(
    name='app',
    logfile=None,
    level=logging.DEBUG,
    formatter=None,
    maxBytes=0,
    backupCount=0,
    fileLoglevel=None,
    disableStderrLogger=False,
    isRootLogger=False,
    json=False,
    json_ensure_ascii=False,
    udp_address = None, # for UdpHandler
    udp_bufsize = None, # for UdpHandler
    ):

    logger = logzero.setup_logger(
        name=name,
        logfile=logfile,
        level=level,
        formatter=formatter,
        maxBytes=maxBytes,
        backupCount=backupCount,
        fileLoglevel=fileLoglevel,
        disableStderrLogger=disableStderrLogger,
        isRootLogger=isRootLogger,
        json=json,
        json_ensure_ascii=json_ensure_ascii,
        )

    if logfile:
        shandler, fhandler = logger.handlers
    else:
        shandler, fhandler = logger.handlers[0], None

    #stream
    # looks like formatter is cached from init
    shandler.formatter._colors = logzero.DEFAULT_COLORS

    #file
    if fhandler:
        _formatter = logging.Formatter(DEFAULT_FMT) #remove color
        fhandler.setFormatter(_formatter)

    #udp
    if udp_address:
        host, port = udp_address
        uhandler = UdpHandler(host, port, udp_bufsize)
        #formatter = LogFormatter(fmt=COLOR_DEFAULT_FMT)
        if not formatter:
            formatter = logging.Formatter(fmt=DEFAULT_FMT)
        formatter = LogFormatter(fmt=formatter._fmt, color=False) # need to get rid of colors for udp
        uhandler.setFormatter(formatter)
        logger.addHandler(uhandler)

    return logger


if __name__ == '__main__':

    logger = setup_logger(
        "app", 
        level=logging.JSON, 
        logfile='test.log',
        udp_address=("127.0.0.1", 6789),
        )

    logger.json('{"a":1}')
    logger.trace("trace")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warn")
    logger.error("error")
    logger.critical("critical")

    class CustomAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            my_context = kwargs.pop('id', self.extra['id'])
            return '[id=%s]' % (my_context), kwargs

    formatter = logging.Formatter("%(message)s")

    diff = logzero.setup_logger(name="diff", formatter=formatter)
    diff = CustomAdapter(diff, {"id": None})
    diff.debug("", id=12)


