import socket
from time import sleep
import logging

class UdpHandler(logging.Handler):
    
    def emit(self, record):

        def split_msg(msg, size):
            return ([msg[i:i+size] for i in range(0, len(msg), size)])

        address = ("127.0.0.1", 6789)
        bufsize = 5

        msg = bytes(record.getMessage() + "\n", 'utf-8')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

        i = 0
        print('server_logging:', sock, address)
        while (i < 5):
            for piece in split_msg(msg, bufsize):
                sock.sendto(piece, address)
                print(i, piece)
            sleep(1)
            i += 1

logger = logging.getLogger('test')
handler = UdpHandler()
logger.addHandler(handler)
logger.error("HI")


def server_plain():
    def split_msg(msg, size):
        return ([msg[i:i+size] for i in range(0, len(msg), size)])

    address = ("127.0.0.1", 6789)
    bufsize = 5
    msg = b"Hello, World!\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    i = 0
    print('server_plain:', sock, address)
    while (i < 5):
        for piece in split_msg(msg, bufsize):
            sock.sendto(piece, address)
            print(i, piece)
        sleep(1)
        i += 1
