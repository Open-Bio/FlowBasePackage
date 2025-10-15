from uflow.Core import NodeBase
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from uflow.Core.Common import *
from uflow import findPinClassByType, getAllPinClasses
from uflow import CreateRawPin
from copy import copy


class convertTo(NodeBase):
    def __init__(self, name):
        super(convertTo, self).__init__(name)
        self.input = self.createInputPin("in", "AnyPin", defaultValue=None)
        self.output = self.createOutputPin("result", "AnyPin", defaultValue=None)
        pinAffects(self.input, self.output)
        self.input.enableOptions(PinOptions.AllowAny)
        self.pinTypes = []
        for pinClass in getAllPinClasses():
            if pinClass.IsValuePin():
                self.pinTypes.append(pinClass.__name__)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("AnyPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "GenericTypes"

    def serialize(self):
        orig = super(convertTo, self).serialize()
        orig["currDataType"] = self.output.dataType
        return orig

    def postCreate(self, jsonTemplate=None):
        super(convertTo, self).postCreate(jsonTemplate)
        if "currDataType" in jsonTemplate:
            self.updateType(self.pinTypes.index(jsonTemplate["currDataType"]))

    def updateType(self, dataTypeIndex):
        self.output.enableOptions(PinOptions.ChangeTypeOnConnection)
        self.changeType(self.pinTypes[dataTypeIndex], True)
        self.output.disableOptions(PinOptions.ChangeTypeOnConnection)

    def changeType(self, dataType, init=False):
        b = self.output.initType(dataType, init)

    def compute(self, *args, **kwargs):
        otherClass = findPinClassByType(self.output.dataType)
        self.output.setData(otherClass.processData(self.input.getData()))
