from uflow.Core import NodeBase
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from uflow.Core.Common import *
from ..Nodes import FLOW_CONTROL_COLOR


class doOnce(NodeBase):
    def __init__(self, name):
        super(doOnce, self).__init__(name)
        self.inExec = self.createInputPin("inExec", "ExecPin", None, self.compute)
        self.reset = self.createInputPin("Reset", "ExecPin", None, self.OnReset)
        self.bStartClosed = self.createInputPin("Start closed", "BoolPin")
        self.completed = self.createOutputPin("Completed", "ExecPin")
        self.bClosed = False
        self.headerColor = FLOW_CONTROL_COLOR

    def OnReset(self):
        self.bClosed = False
        self.bStartClosed.setData(False)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("BoolPin")
        helper.addOutputDataType("ExecPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "FlowControl"

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Will fire off an execution pin just once. But can reset."

    def compute(self, *args, **kwargs):
        bStartClosed = self.bStartClosed.getData()

        if not self.bClosed and not bStartClosed:
            self.completed.call(*args, **kwargs)
            self.bClosed = True
            self.bStartClosed.setData(False)
