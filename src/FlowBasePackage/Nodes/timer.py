from uflow.Core import NodeBase
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from uflow.Core.Common import *
from ..Nodes import FLOW_CONTROL_COLOR


## Timer node
class timer(NodeBase):
    def __init__(self, name):
        super(timer, self).__init__(name)
        self.out = self.createOutputPin("OUT", "ExecPin")
        self.beginPin = self.createInputPin("Begin", "ExecPin", None, self.start)
        self.stopPin = self.createInputPin("Stop", "ExecPin", None, self.stop)
        self.interval = self.createInputPin("Delta(s)", "FloatPin")
        self.interval.setDefaultValue(0.2)
        self.accum = 0.0
        self.bWorking = False
        self.headerColor = FLOW_CONTROL_COLOR

    def Tick(self, delta):
        super(timer, self).Tick(delta)
        if self.bWorking:
            interval = self.interval.getData()
            if interval < 0.02:
                interval = 0.02
            self.accum += delta
            if self.accum >= interval:
                self.out.call()
                self.accum = 0.0

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("FloatPin")
        helper.addOutputDataType("ExecPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    def stop(self, *args, **kwargs):
        self.bWorking = False
        self.accum = 0.0

    def start(self, *args, **kwargs):
        self.accum = 0.0
        self.bWorking = True

    @staticmethod
    def category():
        return "FlowControl"
