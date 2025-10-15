from uflow.UI.Canvas.UIPinBase import UIPinBase

from ..UI.UIAnyPin import UIAnyPin
from ..UI.UIExecPin import UIExecPin


def createUIPin(owningNode, raw_instance):
    if raw_instance.__class__.__name__ == "AnyPin":
        return UIAnyPin(owningNode, raw_instance)
    elif raw_instance.__class__.__name__ == "ExecPin":
        return UIExecPin(owningNode, raw_instance)
    else:
        return UIPinBase(owningNode, raw_instance)
