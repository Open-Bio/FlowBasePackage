from uflow.UI.Tool.Tool import ShelfTool
from ..Tools import RESOURCES_DIR
from uflow.Core.Common import Direction

from qtpy import QtGui


class AlignLeftTool(ShelfTool):
    """docstring for AlignLeftTool."""

    def __init__(self):
        super(AlignLeftTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Aligns selected nodes by left most node"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "alignleft.png")

    @staticmethod
    def name():
        return "AlignLeftTool"

    def do(self):
        self.uflowInstance.getCanvas().alignSelectedNodes(Direction.Left)
