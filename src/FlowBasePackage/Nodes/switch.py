from uflow.Core import NodeBase
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from uflow.Core import PinBase
from uflow.Core.Common import *
from ..Nodes import FLOW_CONTROL_COLOR
import uuid


class switch(NodeBase):
    def __init__(self, name):
        super(switch, self).__init__(name)
        self.inExecPin = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.inVal = self.createInputPin(
            "in", "AnyPin", supportedPinDataTypes=["StringPin", "IntPin", "BoolPin"]
        )
        self.defaultPin = self.createOutputPin("default", "ExecPin")
        self.headerColor = FLOW_CONTROL_COLOR

    def postCreate(self, jsonTemplate=None):
        super(switch, self).postCreate(jsonTemplate=jsonTemplate)
        existingPins = self.namePinOutputsMap
        if jsonTemplate is not None:
            sortedOutputs = sorted(
                jsonTemplate["outputs"], key=lambda pinDict: pinDict["pinIndex"]
            )
            for pinJson in sortedOutputs:
                if pinJson["name"] not in existingPins:
                    inDyn = self.addOutPin(pinJson["name"])
                    inDyn.uid = uuid.UUID(pinJson["uuid"])

    def addOutPin(self, name):
        p = self.createOutputPin(name, "ExecPin")
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        pinAffects(self.inExecPin, p)
        return p

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("StringPin")
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
        return "Execute output depending on input string"

    def compute(self, *args, **kwargs):
        string = str(self.inVal.getData())
        namePinOutputsMap = self.namePinOutputsMap
        if string in namePinOutputsMap:
            namePinOutputsMap[string].call(*args, **kwargs)
        else:
            self.defaultPin.call(*args, **kwargs)
