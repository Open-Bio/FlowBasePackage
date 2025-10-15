import logging

from uflow.Core import NodeBase
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from uflow.ConfigManager import ConfigManager
from uflow.Core.Common import *


class consoleOutput(NodeBase):
    def __init__(self, name):
        super(consoleOutput, self).__init__(name)
        self.inExec = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.entity = self.createInputPin(
            "entity", "AnyPin", structure=StructureType.Multi
        )
        self.entity.enableOptions(PinOptions.AllowAny)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, "ExecPin")

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("ExecPin")
        helper.addInputStruct(StructureType.Multi)
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "Common"

    @staticmethod
    def keywords():
        return ["print"]

    @staticmethod
    def description():
        return "Python's 'print' function wrapper"

    def compute(self, *args, **kwargs):
        redirectionEnabled = ConfigManager().shouldRedirectOutput()
        if self.getWrapper() is not None and redirectionEnabled:
            data = str(self.entity.getData())
            if self.entity.dataType != "StringPin":
                data = data.encode("unicode-escape")
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            data = str(data).replace("\\n", "<br/>")

            errorLink = (
                """<a href=%s><span style=" text-decoration: underline; color:green;">%s</span></a></p>"""
                % (self.name, "<br/>%s" % data)
            )
            logging.getLogger(None).consoleoutput(errorLink)
        else:
            print(self.entity.getData())
        self.outExec.call()
