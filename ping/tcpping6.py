#! /usr/bin/env python3

import sys
import os
import select
import socket
import struct
import time
import fcntl
import random
import errno

from .resolv import gethostbyname


def tcpping6(addr: str, port: int, timeout: float):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    start_time = time.time()
    status = sock.connect_ex((addr, port))
    end_time = time.time()

    return end_time - start_time if status != errno.EAGAIN else -1


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s <addr> <port>" % sys.argv[0], file=sys.stderr)
        exit(-1)
    for i in range(0, 4):
        delay = tcpping6(sys.argv[1], int(sys.argv[2]), 1)
        if delay < 0:
            print("Request timeout")
        else:
            print("%.3lf ms" % (delay * 1000))
