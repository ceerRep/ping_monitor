import time
import json

from flask import Flask
from flask import request

import config

from database import database


class WebServer(object):
    def __init__(self, bind_addr: str, bind_port: int, dbname: str, serverlst: list):
        self.__app = Flask(__name__)
        self.__bind_addr = bind_addr
        self.__bind_port = bind_port
        self.__dbname = dbname
        self.__serverList = serverlst

        @self.__app.route('/', methods=['GET', 'POST'])
        def onGetRoot():
            body = ''
            with open('chart.html') as fin:
                body = ''.join(fin.readlines())
            return body

        @self.__app.route('/rawdata.json', methods=['GET'])
        def onGetData():
            db = database(self.__dbname)
            dataset = dict()
            for server in self.__serverList:
                data = db.query_between(
                    server[0], time.time() - 2 * 24 * 60 * 60, time.time())
                dataset['%s <%s>' % (server[0], 'Private' if server[1] else server[3])] = [
                    [time.asctime(time.localtime(row[0])), row[2]-row[4], row[2]+row[4], row[1], row[3]] for row in data]
            db.close()

            #start_response('200 OK', [('Content-Type', 'application/json')])
            return (json.dumps(dataset), 201, {'Content-Type': 'application/json'})

        self.onGetRoot = onGetRoot
        self.onGetData = onGetData

    def runServer(self):
        self.__app.run(
            host=self.__bind_addr,
            port=self.__bind_port
        )


if __name__ == '__main__':
    server = WebServer(
        '0.0.0.0',
        8080,
        config.database_name,
        config.serverList
    )
    server.runServer()
