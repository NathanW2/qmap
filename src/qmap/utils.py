import time
import logging
import os
import json
import inspect

from PyQt4 import uic

LOG_FILENAME = 'main.log'
uic.uiparser.logger.setLevel(logging.INFO)
uic.properties.logger.setLevel(logging.INFO)
logging.basicConfig(filename=LOG_FILENAME,level=logging.NOTSET)

def _getCallerLogger():
    caller = inspect.currentframe().f_back
    logger = logging.getLogger(caller.f_globals['__name__'])
    return logger

log = lambda msg : _getCallerLogger().debug(msg)
info = lambda msg: _getCallerLogger().info(msg)
warning = lambda msg: _getCallerLogger().warning(msg)
error = lambda msg: _getCallerLogger().error(msg)
critical = lambda msg: _getCallerLogger().critical(msg)

curdir = os.path.dirname(__file__)
settingspath = os.path.join(curdir,'settings.config')
with open(settingspath,'r') as f:
    settings = json.load(f)

appdata = os.path.join(os.environ['APPDATA'], "QMap")

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

def _pluralstring(text='', num=0):
    return "%d %s%s" % (num, text, "s"[num==1:])