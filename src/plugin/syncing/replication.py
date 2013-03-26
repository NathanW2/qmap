from PyQt4.QtCore import pyqtSignal, QProcess, QObject
from qmap.utils import log


class SyncProvider(QObject):
    syncComplete = pyqtSignal()
    syncStarted = pyqtSignal()
    syncMessage = pyqtSignal()
    syncError = pyqtSignal()
    
    def startSync(self):
        pass
    
    def getReport(self):
        return "<p>No report for sync provider generated<p>"
    

class ReplicationSync(SyncProvider):
    def __init__(self, name, cmd):
        super(SyncProvider, self).__init__()
        self.name = name
        self.cmd = cmd
        self.process = QProcess()
        self.process.finished.connect(self.syncComplete)
        self.process.started.connect(self.syncStarted)
        self.process.readyReadStandardError.connect(self.readOutput)
        self.output = None
        
    def startSync(self):
        self.data = None
        self.process.start(self.cmd, [])
        
    def getReport(self):
        if not self.output:
            self.output = self.process.readAllStandardOutput()
        
        html = """<h2> {0} sync report </h2><br><br>
                  {1}""".format(self.name, self.output)
        log(self.output)
        log(html)
        return html
    
    def readOutput(self):
        line = self.process.readLine() 
        log("SYNC LINE " + line)