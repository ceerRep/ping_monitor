#! /usr/bin/env python3

import threading

from monitor import Monitor
from webserver import runServer

import config

if __name__ == "__main__":
    mon = Monitor(config.serverList, config.database_name)

    def server(): return runServer('0.0.0.0', 8080)

    thread_mon = threading.Thread(target=mon.loop)
    thread_srv = threading.Thread(target=server)

    thread_mon.start()
    thread_srv.start()

    thread_mon.join()
    thread_srv.join()
