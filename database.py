#! /usr/bin/env python3

import sqlite3

from log import logging


class database(object):
    def __init__(self, filename: str):
        self.__conn = sqlite3.connect(filename)
        self.__conn.execute("""
        CREATE TABLE IF NOT EXISTS DATA(
            ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME    VARCHAR(64) NOT NULL,
            TIME    DOUBLE NOT NULL,
            MIN     FLOAT,
            AVG     FLOAT,
            MAX     FLOAT,
            STDDEV  FLOAT,
            MID     FLOAT
        );
        """)

    def insert_record(self, name: str, time: float, min_time: float, avg_time: float, max_time: float, std_dev: float, mid_time: float):
        self.__conn.execute("INSERT INTO DATA (NAME, TIME, MIN, AVG, MAX, STDDEV, MID) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (name, time, min_time, avg_time, max_time, std_dev, mid_time))
        logging.debug("Sqlite: INSERT INTO DATA (NAME, TIME, MIN, AVG, MAX, STDDEV, MID) VALUES (%s, %f, %f, %f, %f, %f, %f)" %
                      (name, time, min_time, avg_time, max_time, std_dev, mid_time))
        self.__conn.commit()

    def query_between(self, name: str, time_begin: float, time_end: float):
        cur = self.__conn.execute(
            "SELECT TIME, MIN, AVG, MAX, STDDEV, MID FROM DATA WHERE NAME == ? AND TIME >= ? AND TIME < ?", (name, time_begin, time_end))
        logging.debug("Sqlite: SELECT TIME, MIN, AVG, MAX, STDDEV, MID FROM DATA WHERE NAME == %s AND TIME >= %f AND TIME < %f" % (
            name, time_begin, time_end))
        return [list(row) for row in cur]

    def close(self):
        self.__conn.close()


if __name__ == '__main__':
    db = database('test.db')
    for i in range(1, 10):
        j = i / 2
        db.insert_record('te st;\'', j, j+1, j+2, j+3, j+4, j+5)

    print(db.query_between('te st;\'', 1.5, 4.0))
    db.close()
