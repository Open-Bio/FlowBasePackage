import asyncio
import time

from uflow.Core import NodeBase, PinBase
from uflow.Core.Common import *
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from ..Nodes import FLOW_CONTROL_COLOR
import json


class combineArgs(NodeBase):
    def __init__(self, name):
        super(combineArgs, self).__init__(name)
        self.bCacheEnabled = False
        self.combine_result = self.createOutputPin("combine_result", "StringPin", "")

    def addInPin(self, name, dataType):
        p = self.createInputPin(name, dataType)
        p.enableOptions(
            PinOptions.RenamingEnabled
            | PinOptions.Dynamic
            | PinOptions.AllowMultipleConnections
            | PinOptions.Storable
        )
        return p

    def postCreate(self, jsonTemplate=None):
        super(combineArgs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        existingPins = self.namePinInputsMap
        if jsonTemplate is not None:
            sortedInputs = sorted(jsonTemplate["inputs"], key=lambda x: x["pinIndex"])
            for inPinJson in sortedInputs:
                if inPinJson["name"] not in existingPins:
                    inDyn = self.addInPin(inPinJson["name"], inPinJson["dataType"])
                    inDyn.uid = uuid.UUID(inPinJson["uuid"])
                    try:
                        val = json.loads(
                            inPinJson["value"], cls=inDyn.jsonDecoderClass()
                        )
                        inDyn.setData(val)
                    except:
                        inDyn.setData(inDyn.defaultValue())

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType("StringPin")
        return helper

    @staticmethod
    def category():
        return "Cmd"

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "combine opts to one cmd line"

    def compute(self, *args, **kwargs):
        cmd_line = ""
        for elem in self.orderedInputs.values():
            name = elem.name.lstrip(" ")
            if 0 == len(name) or name.isdigit():
                cmd_line += " {0} ".format(elem.getData())
                continue
            if 1 == len(name) and name.isalpha():
                cmd_line += " -{0} {1} ".format(name, elem.getData())
                continue
            if name[:1] == "-":
                cmd_line += " {0} {1} ".format(name, elem.getData())
                continue
            cmd_line += " --{0} {1} ".format(name, elem.getData())
        self.combine_result.setData(cmd_line)
