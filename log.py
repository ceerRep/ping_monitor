#! /use/bin/python3

import logging

console = logging.StreamHandler()
console.setLevel(logging.INFO)

filehandler = logging.FileHandler("logger.log")
filehandler.setLevel(logging.DEBUG)

formatter = logging.Formatter(logging.BASIC_FORMAT)
filehandler.setFormatter(formatter)
console.setFormatter(formatter)

logging.getLogger('').addHandler(console)
logging.getLogger('').addHandler(filehandler)

logging.getLogger('').setLevel(logging.DEBUG)
