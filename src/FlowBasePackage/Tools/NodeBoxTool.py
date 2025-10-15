from qtpy import QtCore

from uflow.UI.Tool.Tool import DockTool
from uflow.UI.Views.NodeBox import NodesBox


class NodeBoxTool(DockTool):
    """docstring for NodeBox tool."""

    def __init__(self):
        super(NodeBoxTool, self).__init__()
        self.content = None

    def onShow(self):
        super(NodeBoxTool, self).onShow()
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.content = NodesBox(
            self, self.uflowInstance.getCanvas(), False, False, bUseDragAndDrop=True
        )
        self.content.setObjectName("NodeBoxToolContent")
        self.setWidget(self.content)

    def refresh(self):
        self.content.treeWidget.refresh()

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.LeftDockWidgetArea

    @staticmethod
    def toolTip():
        return "Available nodes"

    @staticmethod
    def name():
        return "NodeBox"
