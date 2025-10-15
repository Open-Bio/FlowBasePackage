import uuid
from qtpy import QtGui
from qtpy import QtCore
from qtpy.QtWidgets import *
from uflow.UI.Utils.stylesheet import Colors
from uflow.UI.Canvas.Painters import NodePainter
from uflow.UI.Canvas.UINodeBase import UINodeBase
from uflow.UI.Canvas.IConvexHullBackDrop import IConvexHullBackDrop
from uflow.Core.Common import *
from uflow.Core.NodeBase import NodeBase


class UIWhileLoopBeginNode(UINodeBase, IConvexHullBackDrop):
    def __init__(self, raw_node):
        super(UIWhileLoopBeginNode, self).__init__(raw_node)
        IConvexHullBackDrop.__init__(self)

    def postCreate(self, jsonTemplate=None):
        super(UIWhileLoopBeginNode, self).postCreate(jsonTemplate)
        self.scene().addItem(self.backDrop)
        self.computeHull()
        self.backDrop.update()

    def eventDropOnCanvas(self):
        # TODO: try to simplify this with Canvas.spawnNode
        nodeTemplate = NodeBase.jsonTemplate()
        nodeTemplate["package"] = "FlowBasePackage"
        nodeTemplate["lib"] = ""
        nodeTemplate["type"] = "loopEnd"
        nodeTemplate["name"] = self.canvasRef().graphManager.getUniqNodeName("loopEnd")
        nodeTemplate["x"] = self.scenePos().x() + self.geometry().width() + 30
        nodeTemplate["y"] = self.scenePos().y()
        nodeTemplate["uuid"] = str(uuid.uuid4())
        endNode = self.canvasRef()._createNode(nodeTemplate)
        self.getPinSG("Paired block").setData(str(endNode.path()))
        endNode.getPinSG("Paired block").setData(self.path())
        self.canvasRef().connectPins(
            self.getPinSG("LoopBody"), endNode.getPinSG(DEFAULT_IN_EXEC_NAME)
        )

    def paint(self, painter, option, widget):
        self.computeHull()
        self.backDrop.update()
        NodePainter.default(self, painter, option, widget)
