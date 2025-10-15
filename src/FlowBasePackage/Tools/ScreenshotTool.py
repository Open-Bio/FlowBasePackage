from uflow.UI.Tool.Tool import ShelfTool
from ..Tools import RESOURCES_DIR
from uflow.UI.ContextMenuDataBuilder import ContextMenuDataBuilder

from qtpy import QtGui
from qtpy.QtWidgets import QFileDialog


class ScreenshotTool(ShelfTool):
    """docstring for ScreenshotTool."""

    def __init__(self):
        super(ScreenshotTool, self).__init__()
        self.format = "PNG"

    def saveState(self, settings):
        super(ScreenshotTool, self).saveState(settings)
        settings.setValue("format", self.format)

    def restoreState(self, settings):
        super(ScreenshotTool, self).restoreState(settings)
        formatValue = settings.value("format")
        if formatValue is not None:
            self.format = formatValue
        else:
            self.format = "PNG"

    def onSetFormat(self, fmt):
        self.format = fmt

    def contextMenuBuilder(self):
        builder = ContextMenuDataBuilder()
        builder.addEntry("Save to PNG", "PNG", lambda: self.onSetFormat("PNG"))
        builder.addEntry("Save to JPG", "JPG", lambda: self.onSetFormat("JPG"))
        return builder

    @staticmethod
    def toolTip():
        return "Takes screenshot of visible area of canvas and\nsaves image to file"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "screenshot_icon.png")

    @staticmethod
    def name():
        return "ScreenshotTool"

    def do(self):
        name_filter = "Image (*.{0})".format(self.format.lower())
        fName = QFileDialog.getSaveFileName(filter=name_filter)
        if not fName[0] == "":
            print("save screen to {0}".format(fName[0]))
            img = self.uflowInstance.getCanvas().grab()
            img.save(fName[0], format=self.format, quality=100)
