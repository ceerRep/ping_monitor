#! /usr/bin/env python3

import sys
import os
import select
import socket
import struct
import time
import fcntl
import random

from .resolv import gethostbyname


def calc_checksum(packet: bytes):
    sum = 0
    prev = -1

    for now in packet:
        if prev == -1:
            prev = now
        else:
            sum += (now << 8) | prev
            sum = sum & 0xFFFFFFFF
            prev = -1

    if prev != -1:
        sum += prev
        sum = sum & 0xFFFFFFFF

    while sum & 0xFFFF0000:
        sum = (sum >> 16) + (sum & 0xFFFF)

    return socket.htons((~sum) & 0xFFFF)


def gen_packet(icmp_id: int, icmp_sq: int, pattern: bytes = b'MenciAKIOIsroMenciorz'):
    checksum = 0
    packet = struct.pack('!BBHHH%ds' % len(pattern), 8,
                         0, checksum, icmp_id, icmp_sq, pattern)
    checksum = calc_checksum(packet)
    packet = struct.pack('!BBHHH%ds' % len(pattern), 8,
                         0, checksum, icmp_id, icmp_sq, pattern)
    return packet


def send_one_ping(rawsocket: socket.socket, dst_addr: str, icmp_id: int, icmp_sq: int):
    packet = gen_packet(icmp_id, icmp_sq)
    send_time = time.time()
    rawsocket.sendto(packet, (dst_addr, 1))
    return send_time, dst_addr


def recv_one_ping(rawsocket: socket.socket, icmp_id: int, icmp_sq: int, time_out: float):
    start_time = time.time()
    while True:
        try:
            now_time = time.time()
            received_packet, _ = rawsocket.recvfrom(1024)
            recv_time = time.time()
        except BlockingIOError as e:
            time.sleep(0.00001)
        except socket.error as e:
            if e == socket.errno.EAGAIN or e == socket.errno.EWOULDBLOCK:
                time.sleep(0.00001)
                pass
            else:
                raise e
        else:
            if received_packet[20] == 0:
                icmpHeader = received_packet[20:28]
                ptype, _, _, packet_id, sequence = struct.unpack(
                    "!BBHHH", icmpHeader
                )
                if ptype == 0 and packet_id == icmp_id and sequence == icmp_sq:
                    return (recv_time + now_time) / 2 - start_time
        if now_time - start_time > time_out:
            return -1


def icmpping4(addr: str, seq: int, timeout: float):
    rawsocket = socket.socket(
        socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    fcntl.fcntl(rawsocket, fcntl.F_SETFL, os.O_NONBLOCK)
    send_one_ping(rawsocket, addr, os.getpid() & 0xFFFF, seq)
    delay = recv_one_ping(rawsocket, os.getpid() & 0xFFFF, seq, timeout)
    rawsocket.close()
    return delay


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: %s <addr>" % sys.argv[0], file=sys.stderr)
        exit(-1)
    for i in range(0, 4):
        delay = icmpping4(sys.argv[1], i, 1)
        if delay < 0:
            print("Request timeout")
        else:
            print("%.3lf ms" % (delay * 1000))
