DEBUGMODE = True

from PyQt4.QtGui import QButtonGroup, QWidget
from qmap import form_binder
from qgis.utils import iface

form = None

class TreeCollectionDialog(object):
    def __init__(self, dialog, layer, feature):
        pass
        
    def control(self, name):
        """ 
        Return a control from the dialog using its name 
        """
        return self.dialog.findChild(QWidget, name)
    
def open(dialog, layer, feature):
    form_binder.bindForm(dialog, layer, feature, iface.mapCanvas())
    
    global form
    form = TreeCollectionDialog(dialog, layer, feature)