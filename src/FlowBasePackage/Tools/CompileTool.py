from uflow.UI.Tool.Tool import ShelfTool
from ..Tools import RESOURCES_DIR

from qtpy import QtGui
from qtpy.QtWidgets import *


class CompileTool(ShelfTool):
    """docstring for CompileTool."""

    def __init__(self):
        super(CompileTool, self).__init__()
        self.format = None

    def onSetFormat(self, fmt):
        self.format = fmt

    @staticmethod
    def toolTip():
        return "Ensures everything is ok!"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "compile.png")

    @staticmethod
    def name():
        return "CompileTool"

    def do(self):
        for node in self.uflowInstance.graphManager.get().getAllNodes():
            node.checkForErrors()
