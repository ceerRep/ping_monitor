#! /usr/bin/python3

from wsgiref.simple_server import make_server, WSGIRequestHandler

from database import database
import config
from log import logging

import json
import time
import datetime


class LoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        logging.info("%s - - [%s] %s" %
                     (self.client_address[0],
                      self.log_date_time_string(),
                      format % args))


class WebServer(object):
    def __init__(self, addr: str, port: int, dbname: str, serverList: list):
        self.__addr = addr
        self.__port = port
        self.__dbname = dbname
        self.__httpd = ''
        self.__serverList = serverList

    def run(self):
        logging.info('Web Server has been started')
        self.__httpd = make_server(
            self.__addr, self.__port, self.application, handler_class=LoggingWSGIRequestHandler)
        self.__httpd.serve_forever()

    def onGetFile(self, environ: dict, start_response):
        body = ''
        with open('chart.html') as fin:
            body = ''.join(fin.readlines())
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def onGetData(self, environ: dict, start_response):
        db = database(self.__dbname)
        dataset = dict()
        for server in self.__serverList:
            data = db.query_between(
                server[0], time.time() - 2 * 24 * 60 * 60, time.time())
            dataset['%s <%s>' % (server[0], 'Private' if server[1] else server[3])] = [
                [time.asctime(time.localtime(row[0])), row[2]-row[4], row[2]+row[4], row[1], row[3]] for row in data]
        db.close()

        start_response('200 OK', [('Content-Type', 'application/json')])
        return [json.dumps(dataset).encode('utf-8')]

    def onError(self, errno: int, environ: dict, start_response, errinfo: str = ''):
        if errno == 404:
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            return [b'<b>404 Not Found</b>']

    def application(self, environ: dict, start_response):
        if environ['PATH_INFO'] == '/':
            return self.onGetFile(environ, start_response)
        elif environ['PATH_INFO'] == '/rawdata.json':
            return self.onGetData(environ, start_response)
        else:
            return self.onError(404, environ, start_response)


if __name__ == '__main__':
    server = WebServer('', 8080, 'time.db', config.serverList)
    server.run()
