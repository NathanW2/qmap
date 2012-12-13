from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_sync import Ui_syncForm
import os
import sys
from subprocess import Popen, PIPE

#This feels a bit hacky
pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(pardir)

from utils import log, settings

class Syncer(QObject):
    syncingtable = pyqtSignal(str, int)
    syncingfinished = pyqtSignal(int, int)
    syncingerror = pyqtSignal(str)

    def syncMSSQL(self):
        """
        Run the sync for MS SQL.

        """
        curdir = os.path.abspath(os.path.dirname(__file__))
        cmdpath = os.path.join(curdir,'syncer.exe')
        server = settings.value("syncing/server").toPyObject()
        client = settings.value("syncing/client").toPyObject()
        print server
        print client
        args = [cmdpath, '--server={0}'.format(server), '--client={0}'.format(client), '--porcelain']
        # We have to PIPE stdin even if we don't use it because of Windows  
        p = Popen(args, stdout=PIPE, stderr=PIPE,stdin=PIPE, shell=True)
        while p.poll() is None:
            # error = p.stderr.readline()
            # print "ERROR:" + error 
            out = p.stdout.readline()
            try:
                # Can't seem to get p.stderr to work correctly. Will use this hack for now.
                if out[:5] == "Error":
                    log(out)
                    self.syncingerror.emit(out)
                    continue
                values = dict(item.split(":") for item in out.split("|"))
                if 'td' in values and 'tu' in values:
                    downloads = int(values.get('td'))
                    uploads = int(values.get('tu'))
                    self.syncingfinished.emit(downloads, uploads)

                elif 't' in values:
                    table = values.get('t')
                    inserts = int(values.get('i'))
                    deletes = int(values.get('d'))
                    updates = int(values.get('u'))
                    changes = inserts + deletes + updates
                    self.syncingtable.emit(table, changes)
                else:
                    message = out 
                
            except ValueError:
                # We should really log errors but don't show them to the user
                pass

    def syncImages(self):
        """
        Run the sync over the images

        returns -- Returns a tuple of (state, message). state can be 'Pass' or
                   'Fail'
        """
        images = os.path.join(pardir, "data")
        server = settings.value("syncing/server_image_location").toString()
        if server.isEmpty():
            return ('Fail', "No server image location found in settings.ini")

        if not os.path.exists(images):
            # Don't return a fail if there is no data directory
            return ('Pass', 'Images uploaded: %s' % str(0))

        cmd = 'xcopy "%s" "%s" /Q /D /S /E /K /C /H /R /Y' % (images, server)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell = True)
        stdout, stderr = p.communicate()
        if not stderr == "":
            return ('Fail', stderr)
        else:
            return ('Pass', stdout)
       

class SyncDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_syncForm()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        scr = QApplication.desktop().screenGeometry(0)
        self.move( scr.center() - self.rect().center() )
        self.failed = False
        self.ui.buttonBox.setEnabled(False)

    def updateFailedStatus(self, text):
        self.ui.statusLabel.setStyleSheet("color: rgba(222, 13, 6);")
        self.ui.statusLabel.setText("We couldn't sync for some reason. \n "\
                                    "Dont' worry you might just not have an " \
                                    "internet connection at this time" \
                                    "\n\n We have logged it "
                                    "so we can take a look. Just in case.")
                                    
        self.ui.label.setPixmap(QPixmap(":/syncing/sad"))
        log("SYNC ERROR:" + text)
        self.ui.buttonBox.show()
        self.failed = True

    def runSync(self):
        """
        Shows the sync dialog and runs the sync commands.
        """
        sync = Syncer()
        sync.syncingtable.connect(self.tableupdate)
        sync.syncingfinished.connect(self.syncfinsihed)
        sync.syncMSSQL()

        # if state == 'Fail':
        #     self.updateFailedStatus(sqlmsg)
        #     return

        # log(sqlmsg)

        # self.ui.statusLabel.setText(message + "\n\n Syncing images...")
        # QCoreApplication.processEvents()
        
        # state, msg = syncImages()

        # if state == 'Fail':
        #     self.updateFailedStatus(msg)
        #     return

        # self.updateStatus("%s \n %s" % (sqlmsg, msg))

    def syncfinsihed(self, down, up):
        message = "Total Downloaded: {0}\nTotal Uploaded: {1}".format(down,up)
        self.ui.statusLabel.setText(message)
        self.ui.header.setText("Sync complete")
        self.ui.buttonBox.setEnabled(True)
        QCoreApplication.processEvents()

    def tableupdate(self, table, changes):
        # ewww
        if changes == 0:
            return
        message = self.ui.updatestatus.toPlainText()
        message += "\nUpdated layer {0} with {1} changes".format(table, changes)
        self.ui.updatestatus.setPlainText(message)
        QCoreApplication.processEvents()