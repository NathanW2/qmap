import time
from qgis.core import QgsMessageLog
import logging

LOG_FILENAME = 'main.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.NOTSET)

log = lambda msg: logging.debug(msg)
info = lambda msg: logging.info(msg)
warning = lambda msg: logging.warning(msg)

class Timer():
    def __init__(self, message=""):
        self.message = message
    def __enter__(self):
        self.start = time.time()
    def __exit__(self, *args):
        log(self.message + " " + str(time.time() - self.start))

def timeit(method):
    def wrapper(*args, **kwargs):
        ts = time.time ()
        result = method (*args, **kwargs)
        th = time.time ()

       # log("% r (% r,% r)% 2.2f seconds " % (method.__name__, args, kw, th-ts))
        return result