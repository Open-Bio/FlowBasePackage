from uflow.Core import NodeBase
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from uflow.Core.Common import *


class rerouteExecs(NodeBase):
    def __init__(self, name):
        super(rerouteExecs, self).__init__(name)
        self.input = self.createInputPin("in", "ExecPin")
        self.output = self.createOutputPin("out", "ExecPin")
        pinAffects(self.input, self.output)
        self.input.call = self.output.call

    def postCreate(self, jsonTemplate=None):
        super(rerouteExecs, self).postCreate(jsonTemplate=jsonTemplate)
        self.setName("reroute")

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addOutputDataType("ExecPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "Common"

    def compute(self, *args, **kwargs):
        pass
