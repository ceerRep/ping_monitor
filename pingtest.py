import time
import random

from ping import tcpping
from ping import icmpping
from log import logging


def pingtest(interval: float, batchnum: int, timeout: float, proto: str, addr: str, family=None):
    # seq 可能重复？
    try:
        if proto == 'icmp':
            def func(addr): return icmpping(
                addr, random.randint(0, 65535), timeout, family)
        elif proto == 'tcp':
            def func(addr): return tcpping(
                addr, timeout, family)

        res = []
        for _ in range(0, batchnum):
            delay = func(addr)
            if delay > 0:
                res.append(delay)
            time.sleep(interval)

        resnum = len(res)

        if resnum == 0:
            return (0, 0, 0, 0)

        ressum = sum(res)
        resavg = ressum / resnum
        resmax = max(res)
        resmin = min(res)
        res_stddev = (sum([(x - resavg) ** 2 for x in res]) / resnum)**0.5

        return (resmin, resavg, resmax, res_stddev)
    except BaseException as e:
        logging.warning(e)
        return (0, 0, 0, 0)


if __name__ == '__main__':
    print(pingtest(0.1, 10, 1, 'icmp', 'example.com'))
