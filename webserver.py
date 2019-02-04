import time
import json

from flask import Flask
from flask import request

import config

from database import database


__app = Flask(__name__)
__dbname = config.database_name
__serverList = config.serverList


@__app.route('/', methods=['GET', 'POST'])
def onGetRoot():
    body = ''
    with open('chart.html') as fin:
        body = ''.join(fin.readlines())
    return body


@__app.route('/rawdata.json', methods=['GET'])
def onGetData():
    db = database(__dbname)
    dataset = dict()
    for server in __serverList:
        data = db.query_between(
            server[0], time.time() - 2 * 24 * 60 * 60, time.time())
        dataset['%s <%s>' % (server[0], 'Private' if server[1] else server[3])] = [
            [time.asctime(time.localtime(row[0])), row[2]-row[4], row[2]+row[4], row[1], row[3]] for row in data]
    db.close()

    #start_response('200 OK', [('Content-Type', 'application/json')])
    return (json.dumps(dataset), 201, {'Content-Type': 'application/json'})


def runServer(addr: str, port: int):
    __app.run(
        host=addr,
        port=port
    )


if __name__ == '__main__':
    runServer('0.0.0.0', 8080)
