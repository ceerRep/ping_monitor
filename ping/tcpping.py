#! /usr/bin/env python3

import sys
import socket

from .tcpping4 import tcpping4
from .tcpping6 import tcpping6
from .resolv import gethostbyname


def tcpping(name: str, port: int, timeout: float, family=None):
    host = gethostbyname(name)
    if (family == socket.AF_INET6) or (family == None and host[1]):
        return tcpping6(host[1], port, timeout)
    elif (family == socket.AF_INET) or (family == None and host[0]):
        return tcpping4(host[0], port, timeout)
    else:
        return -2


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: %s <addr>" % sys.argv[0], file=sys.stderr)
        exit(-1)
    family = None
    dest = sys.argv[1]
    addr, port = None, None
    if dest[0] == '[':
        family = socket.AF_INET6
        addr = dest[1: dest.find(']')]
        port = dest[dest.find(']') + 2:]
    else:
        addr, port = dest.split(':')
    for i in range(0, 4):
        delay = tcpping(addr, int(port), 1, family)
        if delay == -1:
            print("Request timeout")
        elif delay == -2:
            print("Cannot resolve hostname")
        else:
            print("%.3lf ms" % (delay * 1000))
