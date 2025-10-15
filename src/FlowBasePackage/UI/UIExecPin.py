from qtpy import QtGui, QtCore

from uflow.UI.Canvas.UIPinBase import UIPinBase
from uflow.UI.Canvas.Painters import PinPainter


class UIExecPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIExecPin, self).__init__(owningNode, raw_pin)

    def paint(self, painter, option, widget):
        # PinPainter.asValuePin(self, painter, option, widget)
        PinPainter.asExecPin(self, painter, option, widget)

    def hoverEnterEvent(self, event):
        super(UIPinBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        event.accept()
