import logzero
import logging
from colored import fg#, bg, attr

DEFAULT_FMT = "[%(levelname)1.1s "\
    + "%(asctime)s %(module)s:%(lineno)d] "\
    + "%(message)s"

COLOR_DEFAULT_FMT = "%(color)s[%(levelname)1.1s "\
    "%(asctime)s %(module)s:%(lineno)d]%(end_color)"\
    "%(message)s"

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

logzero.DEFAULT_COLORS = {
    logging.TRACE: fg(117),
    logging.DEBUG: fg(31),
    logging.INFO: fg('aquamarine_3'),
    logging.WARNING: fg(186),
    logging.ERROR: fg(168),
    logging.CRITICAL: fg(200)
}


def setup_logger(
    name='mylogger',
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
        formatter = logging.Formatter(DEFAULT_FMT) #remove color
        fhandler.setFormatter(formatter)

    return logger


if __name__ == '__main__':

    logger = setup_logger("app", level=logging.TRACE, logfile='test.log')

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


