from uflow.Core import NodeBase
from uflow.Core.Common import *
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from ..Nodes import FLOW_CONTROL_COLOR


class delay(NodeBase):
    def __init__(self, name):
        super(delay, self).__init__(name)
        self.inp0 = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.delay = self.createInputPin("Delay(s)", "FloatPin")
        self.delay.setDefaultValue(0.2)
        self.out0 = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, "ExecPin")
        self.process = False
        self._total = 0.0
        self._currentDelay = 0.0
        self.headerColor = FLOW_CONTROL_COLOR

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("FloatPin")
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
        return "Delayed call"

    def callAndReset(self):
        self.process = False
        self._total = 0.0
        self.out0.call()

    def Tick(self, delta):
        if self.process:
            self._total += delta
            if self._total >= self._currentDelay:
                self.callAndReset()

    def compute(self, *args, **kwargs):
        self._currentDelay = self.delay.getData()
        if not self.process:
            self.process = True
