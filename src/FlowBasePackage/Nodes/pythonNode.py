from types import MethodType

from uflow import getPinDefaultValueByType
from uflow.Core.Common import getUniqNameFromList
from uflow.Core.NodeBase import NodeBase
from uflow.Core.PyCodeCompiler import Py3CodeCompiler


class pythonNode(NodeBase):
    def __init__(self, name):
        super(pythonNode, self).__init__(name)
        self._nodeData = ""
        self.bCacheEnabled = False

    @property
    def nodeData(self):
        return self._nodeData

    def ensureNameUnique(self):
        existingNames = [n.name for n in self.graph().graphManager.getAllNodes()]
        nodeName = self.getName()
        if nodeName in existingNames:
            existingNames.remove(nodeName)
        self.setName(getUniqNameFromList(existingNames, nodeName))

    @nodeData.setter
    def nodeData(self, codeString):
        if codeString == "":
            return
        try:
            self._nodeData = codeString
            # compile and get symbols
            mem = Py3CodeCompiler().compile(codeString, self.getName(), {})

            # clear node pins
            for i in list(self.pins):
                i.kill()
            self.pins.clear()

            # define pins, name etc
            prepareNodeFunction = mem["prepareNode"]
            prepareNodeFunction(self)
            self.autoAffectPins()

            self.ensureNameUnique()

            # assign compute code
            computeFunction = mem["compute"]

            def nodeCompute(*args, **kwargs):
                computeFunction(self)

            self.compute = MethodType(nodeCompute, self)
            self.bCallable = self.isCallable()
            self.clearError()
        except Exception as e:
            self.setError(str(e))

    def serialize(self):
        default = super(pythonNode, self).serialize()
        default["nodeData"] = self.nodeData
        return default

    def postCreate(self, jsonTemplate=None):
        super(pythonNode, self).postCreate(jsonTemplate)

        if jsonTemplate is None:
            return

        if "nodeData" in jsonTemplate:
            self.nodeData = jsonTemplate["nodeData"]

        for inpJson in jsonTemplate["inputs"]:
            pin = self.getPinByName(inpJson["name"])
            if not pin:
                pin = self.createInputPin(
                    pinName=inpJson["name"],
                    dataType=inpJson["dataType"],
                    defaultValue=getPinDefaultValueByType(inpJson["dataType"]),
                    callback=self.compute,
                )
            pin.deserialize(inpJson)

        for outJson in jsonTemplate["outputs"]:
            pin = self.getPinByName(outJson["name"])
            if not pin:
                pin = self.createOutputPin(
                    pinName=inpJson["name"],
                    dataType=inpJson["dataType"],
                    defaultValue=getPinDefaultValueByType(inpJson["dataType"]),
                )
            pin.deserialize(outJson)

        self.autoAffectPins()

    @staticmethod
    def category():
        return "Common"

    @staticmethod
    def keywords():
        return ["Code", "Expression", "py"]

    @staticmethod
    def description():
        return "Python script node"
