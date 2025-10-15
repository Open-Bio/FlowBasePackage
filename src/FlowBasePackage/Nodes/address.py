from uflow.Core import NodeBase
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from uflow.Core.Common import *


class address(NodeBase):
    def __init__(self, name):
        super(address, self).__init__(name)
        self.obj = self.createInputPin("obj", "AnyPin", structure=StructureType.Multi)
        self.obj.enableOptions(PinOptions.AllowAny)
        self.addr = self.createOutputPin("out", "StringPin")

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("StringPin")
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "Utils"

    @staticmethod
    def keywords():
        return ["id"]

    @staticmethod
    def description():
        return "Returns address of an object in memory"

    def compute(self, *args, **kwargs):
        self.addr.setData(hex(id(self.obj.getData())))
