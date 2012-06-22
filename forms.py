import os.path
from PyQt4.QtCore import QSettings,QString
from PyQt4.QtGui import QIcon
from PyQt4.uic import loadUi
import os
import imp

def getForms():
    """ Get all the custom user forms that have been created.
    Checks for "form" at the start to detect module as custom form

    @Returns A list of modules that contain user forms.
    """
    modules = []
    curdir = os.path.abspath(os.path.dirname(__file__))
    formspath = os.path.join(curdir,'entry_forms')
    for module in os.listdir(formspath):
        if module[:4] == 'form':
            instance = loadFormModule(module)
            modules.append(Form(instance))

    return modules

def loadFormModule(module):
    """ Load the forms module """
    formmodule = __import__("entry_forms.%s" % module, locals(), globals(),["*"], 1)
    return formmodule

class Form(object):
    """
    Represents a data collection form.  Contains links to the python module for the form.
    """

    def __init__(self, module):
        self._module = module
        self._settings = None
        
    @property
    def module(self):
        return self._module

    def formInstance(self):
        path = os.path.dirname(self.module.__file__)
        uiFile = os.path.join(path, "form.ui")
        return loadUi(uiFile)

    def settings(self):
        if self._settings is None:
            path = os.path.dirname(self.module.__file__)
            self._settings = QSettings(os.path.join(path, "settings.ini"), QSettings.IniFormat )

        return self._settings

    def layerName(self):
        return str(self.settings().value("layer_name").toString())

    def formName(self):
        return str(self.settings().value("form_name").toString())

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(self.module.__file__),'icon.png'))