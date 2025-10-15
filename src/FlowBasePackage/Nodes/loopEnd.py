from uflow.Core.Common import *
from uflow.Core.PathsRegistry import PathsRegistry
from uflow.Core.NodeBase import NodePinsSuggestionsHelper
from uflow.Core import NodeBase
from ..Nodes import FLOW_CONTROL_ORANGE


class loopEnd(NodeBase):
    def __init__(self, name):
        super(loopEnd, self).__init__(name)
        self.inExec = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.loopBeginNode = self.createInputPin("Paired block", "StringPin")
        self.loopBeginNode.setInputWidgetVariant("ObjectPathWidget")
        self.completed = self.createOutputPin("Completed", "ExecPin")
        self.headerColor = FLOW_CONTROL_ORANGE
        self.setExperimental()

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("StringPin")
        helper.addInputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "FlowControl"

    @staticmethod
    def keywords():
        return ["iter", "end"]

    @staticmethod
    def description():
        return "For loop end block"

    def compute(self, *args, **kwargs):
        node = PathsRegistry().getEntity(self.loopBeginNode.getData())
        if node is not None:
            if node.graph() == self.graph():
                if node.loopEndNode.getData() != self.path():
                    self.setError("Invalid pair")
                    return
                if node.__class__.__name__ == "forLoopBegin":
                    node.prevIndex = node.currentIndex
                    node.currentIndex += 1
                    if node.currentIndex >= node.lastIndex.getData():
                        self.completed.call()
                else:
                    node.onNext()
            else:
                err = "block ends in different graphs"
                node.setError(err)
                self.setError(err)
        else:
            self.setError("Pair {} not found".format(self.loopBeginNode.getData()))
