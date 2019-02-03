#! /usr/bin/env python3

import socket


def gethostbyname(name: str):
    ret = [None, None]

    info_list = socket.getaddrinfo(name, None)

    for info in info_list:
        if info[0] == socket.AF_INET6:
            if not ret[1]:
                ret[1] = info[4][0]
        elif info[0] == socket.AF_INET:
            if not ret[0]:
                ret[0] = info[4][0]

    return ret


if __name__ == '__main__':
    print(gethostbyname('example.com'))
