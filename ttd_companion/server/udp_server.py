import socket
from time import sleep

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUF_SIZE = 5
msg = b" Hello, World!\n"

def split_msg(msg, size):
    return ([msg[i:i+size] for i in range(0, len(msg), size)])

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

i = 0
while True:
    i += 1
    data = b'#' + bytes(str(i), "utf-8") + msg
    for piece in split_msg(data, BUF_SIZE):
        print(piece)
        sock.sendto(piece, (UDP_IP, UDP_PORT))
    sleep(1)
    
