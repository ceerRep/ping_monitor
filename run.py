#! /usr/bin/env python3

import threading

from monitor import Monitor
from webserver import WebServer

import config

if __name__ == "__main__":
    mon = Monitor(config.serverList, config.database_name)
    server = WebServer('', 8080, 'time.db', config.serverList)

    thread_mon = threading.Thread(target=mon.loop)
    thread_srv = threading.Thread(target=server.run)

    thread_mon.start()
    thread_srv.start()

    thread_mon.join()
    thread_srv.join()
