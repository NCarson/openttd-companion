
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 6789
BUF_SIZE=5

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    msg = b""
    while True:
        data = sock.recv(BUF_SIZE)
        if not data:
            break
        msg += data
        if data[-1] == ord("\n"):
            break

    msg = msg.decode("utf-8")
    print("received message: %s" % repr(msg))

