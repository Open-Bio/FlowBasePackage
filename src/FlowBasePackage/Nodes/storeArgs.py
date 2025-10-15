import asyncio
import time

from uflow.Core import NodeBase, PinBase
from uflow.Core.Common import *
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from ..Nodes import FLOW_CONTROL_COLOR
import json


class storeArgs(NodeBase):
    def __init__(self, name):
        super(storeArgs, self).__init__(name)
        self.bCacheEnabled = False
        self.hold_pos = self.createInputPin("0", "StringPin", "")
        self.combine_result = self.createOutputPin("combine_result", "StringPin", "")

    def addInPin(self, name, dataType):
        p_in = self.createInputPin(name, dataType)
        p_in.enableOptions(
            PinOptions.RenamingEnabled | PinOptions.Dynamic | PinOptions.Storable
        )
        return p_in

    def addOutPin(self, name, dataType):
        p_out = self.createOutputPin(name, dataType)
        return p_out

    def postCreate(self, jsonTemplate=None):
        super(storeArgs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        existingPins = self.namePinInputsMap
        if jsonTemplate is not None:
            sortedInputs = sorted(jsonTemplate["inputs"], key=lambda x: x["pinIndex"])
            for pinJson in sortedInputs:
                if pinJson["name"] not in existingPins:
                    pinDyn = self.addInPin(pinJson["name"], pinJson["dataType"])
                    pinDyn.uid = uuid.UUID(pinJson["uuid"])
                    try:
                        val = json.loads(
                            pinJson["value"], cls=pinDyn.jsonDecoderClass()
                        )
                        pinDyn.setData(val)
                    except:
                        pinDyn.setData(pinDyn.defaultValue())
            sortedOutputs = sorted(jsonTemplate["outputs"], key=lambda x: x["pinIndex"])
            for pinJson in sortedOutputs:
                if pinJson["name"] not in existingPins:
                    pinDyn = self.addOutPin(pinJson["name"], pinJson["dataType"])
                    pinDyn.uid = uuid.UUID(pinJson["uuid"])
                    try:
                        val = json.loads(
                            pinJson["value"], cls=pinDyn.jsonDecoderClass()
                        )
                        pinDyn.setData(val)
                    except:
                        pinDyn.setData(pinDyn.defaultValue())

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        return helper

    @staticmethod
    def category():
        return "Cmd"

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "store args"

    def compute(self, *args, **kwargs):
        cmd_line = ""
        output_map = self.namePinOutputsMap
        for elem in self.orderedInputs.values():
            name = elem.name.lstrip("> ")
            if name in output_map:
                output_map[name].setData(elem.getData())
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
