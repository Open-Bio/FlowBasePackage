from uflow.UI.Canvas.UICommon import DEFAULT_IN_EXEC_NAME
from uflow.UI import RESOURCES_DIR
from uflow.UI.Canvas.UINodeBase import UINodeBase
from uflow.UI.Canvas.UICommon import NodeActionButtonInfo


class UISwitch(UINodeBase):
    def __init__(self, raw_node):
        super(UISwitch, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add out pin")
        actionAddOut.setToolTip("Adds an option")
        actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
        actionAddOut.triggered.connect(self.onAddOutPin)

    def postCreate(self, jsonTemplate=None):
        super(UISwitch, self).postCreate(jsonTemplate=jsonTemplate)
        inExecPin = self.getPinSG(DEFAULT_IN_EXEC_NAME)
        inExecPin.bLabelHidden = True

    def onAddOutPin(self):
        name = self._rawNode.getUniqPinName("0")
        rawPin = self._rawNode.addOutPin(name)
        uiPin = self._createUIPinWrapper(rawPin)
        return uiPin
