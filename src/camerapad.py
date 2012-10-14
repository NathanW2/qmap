from camera import VideoWidget
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import Qt
from ui_camera import Ui_CameraWindow
import uuid
import functools

class CameraPad(QDialog):
    def __init__(self, startimage=None):
        QDialog.__init__(self)
        self.saveAsActs = []
        
        self.ui = Ui_CameraWindow()
        self.ui.setupUi(self)

        self.videowidget = VideoWidget()

        self.ui.frame.layout().addWidget(self.videowidget)
        self.createActions()

        self.setWindowTitle("Camera")
        self.resize(500, 500)

    def saveImage(self, filename):
        filename = filename + ".png"
        log(filename)
        return self.scribbleArea.saveImage(filename, "png")

    def setPen(self, color, size=3):
        self.scribbleArea.setPenWidth(size)
        self.scribbleArea.setPenColor(color)

    def createActions(self):
        self.ui.actionCaptureImage.triggered.connect(self.captureImage)
        self.ui.actionRecaptureImage.triggered.connect(self.reloadCamera)
        self.ui.toolCapture.setDefaultAction(self.ui.actionCaptureImage)

        self.videowidget.mousePressed.connect(self.captureImage)

        # self.ui.toolMapSnapshot.setDefaultAction(self.ui.actionMapSnapshot)

        self.ui.toolSave.setDefaultAction(self.ui.actionSave)
        self.ui.toolCancel.setDefaultAction(self.ui.actionCancel)

    def captureImage(self):
        self.videowidget.captureImage()
        self.ui.toolCapture.setDefaultAction(self.ui.actionRecaptureImage)

    def reloadCamera(self):
        self.videowidget.restartCamera()
        self.ui.toolCapture.setDefaultAction(self.ui.actionCaptureImage)

    def saveImage(self):
         id = str(uuid.uuid1())
         image = self.videowidget.saveImage('/home/woo/apps/QMap/images/%s.png' % id, 'png')

    def show(self):
        super(CameraPad,self).show()
        self.videowidget.startCamera(1000,1000)

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication

    app = QApplication(sys.argv)
    window = CameraPad()
    window.show()
    sys.exit(app.exec_())
