from uflow.UI.Canvas.UICommon import DEFAULT_IN_EXEC_NAME
from uflow.UI import RESOURCES_DIR
from uflow.UI.Canvas.UINodeBase import UINodeBase
from uflow.UI.Canvas.UICommon import NodeActionButtonInfo
from uflow.UI.Utils.stylesheet import Colors
from qtpy import QtCore
from qtpy.QtWidgets import QInputDialog


class UIStoreArgs(UINodeBase):
    pinCreated = QtCore.Signal(object)

    def __init__(self, raw_node):
        super(UIStoreArgs, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add arg")
        actionAddOut.setToolTip("Add arg")
        actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
        actionAddOut.triggered.connect(self.onAddPin)

    def onAddPin(self):
        name, confirmed = QInputDialog.getText(None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            name = self._rawNode.getUniqPinName(name)
            rawPin = self._rawNode.addInPin(">" + name, "StringPin")
            uiPin = self._createUIPinWrapper(rawPin)
            self.pinCreated.emit(uiPin)

            rawPin = self._rawNode.addOutPin(name, "StringPin")
            uiPin = self._createUIPinWrapper(rawPin)
            self.pinCreated.emit(uiPin)
            self.updateNodeShape()
