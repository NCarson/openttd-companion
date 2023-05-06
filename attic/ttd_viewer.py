#!/usr/bin/python3 

import os
import sys
import fcntl
import select

from event import onData

fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

epoll = select.epoll()
epoll.register(fd, select.EPOLLIN)

try:
    while True:
        events = epoll.poll(1)
        for fileno, event in events:
            data = ""
            while True:
                l = sys.stdin.read(64)
                if not l:
                    break
                data += l
            if data.strip():
                onData(data)

finally:
    epoll.unregister(fd)
    epoll.close()
