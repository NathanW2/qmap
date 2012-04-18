from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint
from PyQt4.QtCore import pyqtSignal, QVariant
from PyQt4.QtGui import QAction, QCursor, QPixmap

class SelectFeatureTool(QgsMapToolEmitPoint):
    foundFeature = pyqtSignal(QgsFeature, QVariant, str)
    
    def __init__(self, canvas, layername, column, bindto ):
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.layername = layername
        self.column = column
        self.bindto = bindto
        self.canvas = canvas
        self.bindto = bindto
        self.canvasClicked.connect(self.findFeature)
        self.canvas.setMapTool(self)
        self.cursor = QCursor(QPixmap(["16 16 3 1",
            "      c None",
            ".     c #32CD32",
            "+     c #32CD32",
            "                ",
            "       +.+      ",
            "      ++.++     ",
            "     +.....+    ",
            "    +.     .+   ",
            "   +.   .   .+  ",
            "  +.    .    .+ ",
            " ++.    .    .++",
            " ... ...+... ...",
            " ++.    .    .++",
            "  +.    .    .+ ",
            "   +.   .   .+  ",
            "   ++.     .+   ",
            "    ++.....+    ",
            "      ++.++     ",
            "       +.+      "]))

    def findFeature(self, point, button):
        for layer in self.canvas.layers():
            QgsMessageLog.logMessage("Looking at %s to match %s" % (layer.name(), self.column), "SDRC")
            if layer.name() == self.layername:
                QgsMessageLog.logMessage("Found layer", "SDRC")

                searchRadius = self.canvas.extent().width() * ( 0.5 / 100.0)
                rect = QgsRectangle()
                rect.setXMinimum( point.x() - searchRadius );
                rect.setXMaximum( point.x() + searchRadius );
                rect.setYMinimum( point.y() - searchRadius );
                rect.setYMaximum( point.y() + searchRadius );

                layer.select( layer.pendingAllAttributesList(), rect, True, True)
                feature = QgsFeature()
                layer.nextFeature(feature)
                try:
                    index = layer.fieldNameIndex(self.column)
                    value = feature.attributeMap()[index].toString()
                    self.foundFeature.emit(feature, value, self.bindto)
                    break
                except KeyError:
                    break

    def setActive(self):
        self.canvas.setMapTool(self)
        self.canvas.setCursor(self.cursor)