
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import re

from colored import fg, bg, attr


class StreamFormatter(logging.Formatter):

    fmt = "" \
        + "{clvl}{levelname}{cend}"\
        + " | {filename}"\
        + " | {funcName}"\
        + " | {message}"


    def __init__(self, fmt=None, ):
        super().__init__(fmt=fmt or self.fmt, style="{", datefmt=None)

    def colorPalette(self, levelno):
        
        c  = [
            fg('white'),
            fg('slate_blue_3a'),
            fg('aquamarine_3'),
            fg('gold_3b'),
            fg('red'),
            fg('hot_pink_1a'),
        ]
        if levelno < 10:
            color = c[0]
        elif levelno < 20:
            color = c[1]
        elif levelno < 30:
            color = c[2]
        elif levelno < 40:
            color = c[3]
        elif levelno < 50:
            color = c[4]
        else:
            color = c[5]

        bcolor = color + attr("bold")
            
        return {
            'clvl': color,
            'cblvl': bcolor,
            'cend': attr("reset"),
        }

    def format(self, record):
        palette = self.colorPalette(record.levelno)
        d = record.__dict__
        d["message"] = d["msg"]
        return self._fmt.format(**{**d, **palette})


class SimpleStreamFormatter(StreamFormatter):
    fmt = "" \
        + "{cblvl}{levelname}{cend}"\
        + " | {clvl}{message}{cend}"


class FileFormatter(logging.Formatter):
    fmt = "{asctime} | {levelname} | {filename} | {funcName} | {message}"

    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt=fmt or self.fmt, style="{", datefmt=datefmt)


class StreamHandler(logging.StreamHandler):
    
    def __init__(self, handler=sys.stderr, formatter=None):
        super().__init__(handler)
        if not formatter:
            formatter = StreamFormatter()
        self.setFormatter(formatter)


class FileHandler(logging.FileHandler):
    def __init__(self, fdescr, formatter=None):
        super().__init__(fdescr)
        if not formatter:
            formatter = FileFormatter()
        self.setFormatter(formatter)


class Logging:
    @staticmethod
    def getLogger(
            path, 
            level=logging.DEBUG,

            file_handler=True,
            stream_handler=True,
            stream_formatter=None,
            ):
        logger = logging.getLogger(path)
        logger.setLevel(level)

        if file_handler:
            logger.addHandler(FileHandler(path))

        if stream_handler:
            if stream_formatter:
                handler = StreamHandler(formatter=stream_formatter)
            else:
                handler = StreamHandler()
            logger.addHandler(handler)

        logger.propagate = False
        return logger
        

if __name__ == '__main__':

    logger = Logging.getLogger(
        "test.log", 
        stream_formatter=SimpleStreamFormatter()
        )
    logger.log(9, "HII") # suppressed
    logger.log(11, "HII")
    logger.debug("HII")
    logger.info("HII")
    logger.warning("HII")
    logger.error("HII")
    logger.critical("HII")

