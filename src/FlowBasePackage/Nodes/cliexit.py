from uflow.Core import NodeBase
from uflow.Core.Common import *
from uflow.Core.GraphManager import GraphManagerSingleton
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from ..Nodes import FLOW_CONTROL_COLOR


class cliexit(NodeBase):
    def __init__(self, name):
        super(cliexit, self).__init__(name)
        self.inp0 = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CLI"

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Stops cli program loop"

    def compute(self, *args, **kwargs):
        man = GraphManagerSingleton().get()
        man.terminationRequested = True
