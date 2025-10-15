from qtpy import QtGui
from uflow.UI import RESOURCES_DIR
from uflow.UI.Canvas.UINodeBase import UINodeBase
from qtpy.QtWidgets import QLabel


class UIImageDisplayNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIImageDisplayNode, self).__init__(raw_node)
        self.resizable = True
        self.Imagelabel = QLabel("test3")
        self.pixmap = QtGui.QPixmap(RESOURCES_DIR + "/wizard-cat.png")
        self.addWidget(self.Imagelabel)
        self.updateSize()
        self._rawNode.loadImage.connect(self.onLoadImage)

    def onLoadImage(self, imagePath):
        self.pixmap = QtGui.QPixmap(imagePath)
        self.updateSize()

    def paint(self, painter, option, widget):
        self.updateSize()
        super(UIImageDisplayNode, self).paint(painter, option, widget)

    def updateSize(self):
        scaledPixmap = self.pixmap.scaledToWidth(self.customLayout.geometry().width())
        self.Imagelabel.setPixmap(scaledPixmap)
