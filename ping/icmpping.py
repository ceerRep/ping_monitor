#! /usr/bin/env python3

import sys
import socket

from .icmpping4 import icmpping4
from .icmpping6 import icmpping6
from .resolv import gethostbyname


def icmpping(name: str, seq: int, timeout: float, family=None):
    host = gethostbyname(name)
    if (family == socket.AF_INET6) or (family == None and host[1]):
        return icmpping6(host[1], seq, timeout)
    elif (family == socket.AF_INET) or (family == None and host[0]):
        return icmpping4(host[0], seq, timeout)
    else:
        return -2


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: %s <addr>" % sys.argv[0], file=sys.stderr)
        exit(-1)
    for i in range(0, 4):
        delay = icmpping(sys.argv[1], i, 1)
        if delay == -1:
            print("Request timeout")
        elif delay == -2:
            print("Cannot resolve hostname")
        else:
            print("%.3lf ms" % (delay * 1000))
