#! /usr/bin/python3


import time
import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, wait


import config
from pingtest import pingtest
from database import database
from log import logging


def doPingTestFor(lst_id: int, server_lst: list, dbname: str):
    try:
        begin_time = time.time()
        name, _, proto, addr, family = config.serverList[lst_id]
        logging.debug('Started ping test for ID#%d, name: %s' % (lst_id, name))
        min_time, avg_time, max_time, std_dev = pingtest(
            config.ping_interval, config.ping_batchnum, config.ping_timeout, proto, addr, family)
        db = database(dbname)
        db.insert_record(name, begin_time, min_time,
                         avg_time, max_time, std_dev)
        logging.debug('Ping test ended ID#%d, name: %s' % (lst_id, name))
    except BaseException as e:
        logging.error(e)


class Monitor(object):
    def __init__(self, server_lst: list, dbname: str):
        self.server_lst = server_lst
        self.dbname = dbname

    def run_test(self):
        logging.info("Ping test started")
        serverNum = len(config.serverList)
        executor = ThreadPoolExecutor(max_workers=serverNum)
        f_list = []
        for lst_id in range(0, serverNum):
            f_list.append(executor.submit(
                doPingTestFor, lst_id, self.server_lst, self.dbname))
        wait(f_list)

    def loop(self):
        prev_min = -1
        while True:
            now = datetime.datetime.now()
            if now.minute != prev_min and now.minute % 15 == 0:
                self.run_test()
                prev_min = now.minute
            time.sleep(60)
            """
            if now.second != prev_min and now.second % 15 == 0:
                self.run_test()
                prev_min = now.second
            time.sleep(0.1)"""


if __name__ == '__main__':
    mon = Monitor(config.serverList, config.database_name)
    mon.loop()
