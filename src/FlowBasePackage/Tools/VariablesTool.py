from qtpy import QtCore
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QVBoxLayout

from uflow.UI.Tool.Tool import DockTool
from uflow.UI.Views.VariablesWidget import VariablesWidget


class VariablesTool(DockTool):
    """docstring for Variables tool."""

    def __init__(self):
        super(VariablesTool, self).__init__()
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.varsWidget = None

    @staticmethod
    def isSingleton():
        return True

    def onShow(self):
        super(VariablesTool, self).onShow()
        self.varsWidget = VariablesWidget(self.uflowInstance)
        self.uflowInstance.fileBeenLoaded.connect(self.varsWidget.actualize)
        self.varsWidget.setObjectName("VariablesWidget")
        self.setWidget(self.varsWidget)
        self.varsWidget.actualize()

    def showEvent(self, event):
        super(VariablesTool, self).showEvent(event)
        if self.varsWidget is not None:
            self.varsWidget.actualize()

    @staticmethod
    def toolTip():
        return "Variables editing/creation"

    @staticmethod
    def name():
        return "Variables"
