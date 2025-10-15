## Copyright 2015-2025 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from ..UI.UIImageDisplayNode import UIImageDisplayNode

from ..UI.UIStoreArgsNode import UIStoreArgs
from ..UI.UICombineArgsNode import UICombineArgs
from ..UI.UISubProcessNode import UISubProcess
from ..UI.UISwitchNode import UISwitch
from ..UI.UIGetVarNode import UIGetVarNode
from ..UI.UISetVarNode import UISetVarNode
from ..UI.UISequenceNode import UISequenceNode
from ..UI.UICommentNode import UICommentNode
from ..UI.UIStickyNote import UIStickyNote
from ..UI.UIRerouteNodeSmall import UIRerouteNodeSmall
from ..UI.UIPythonNode import UIPythonNode
from ..UI.UIGraphNodes import UIGraphInputs, UIGraphOutputs
from ..UI.UIFloatRamp import UIFloatRamp
from ..UI.UIColorRamp import UIColorRamp

from ..UI.UICompoundNode import UICompoundNode
from ..UI.UIConstantNode import UIConstantNode
from ..UI.UIConvertToNode import UIConvertToNode
from ..UI.UIMakeDictNode import UIMakeDictNode
from ..UI.UIForLoopBeginNode import UIForLoopBeginNode
from ..UI.UIWhileLoopBeginNode import UIWhileLoopBeginNode

from uflow.UI.Canvas.UINodeBase import UINodeBase


def createUINode(raw_instance):
    if raw_instance.__class__.__name__ == "getVar":
        return UIGetVarNode(raw_instance)
    if raw_instance.__class__.__name__ == "setVar":
        return UISetVarNode(raw_instance)
    if raw_instance.__class__.__name__ == "subProcess":
        return UISubProcess(raw_instance)
    if raw_instance.__class__.__name__ == "storeArgs":
        return UIStoreArgs(raw_instance)
    if raw_instance.__class__.__name__ == "combineArgs":
        return UICombineArgs(raw_instance)
    if raw_instance.__class__.__name__ == "switch":
        return UISwitch(raw_instance)
    if raw_instance.__class__.__name__ == "sequence":
        return UISequenceNode(raw_instance)
    if raw_instance.__class__.__name__ == "commentNode":
        return UICommentNode(raw_instance)
    if raw_instance.__class__.__name__ == "stickyNote":
        return UIStickyNote(raw_instance)
    if (
        raw_instance.__class__.__name__ == "reroute"
        or raw_instance.__class__.__name__ == "rerouteExecs"
    ):
        return UIRerouteNodeSmall(raw_instance)
    if raw_instance.__class__.__name__ == "graphInputs":
        return UIGraphInputs(raw_instance)
    if raw_instance.__class__.__name__ == "graphOutputs":
        return UIGraphOutputs(raw_instance)
    if raw_instance.__class__.__name__ == "compound":
        return UICompoundNode(raw_instance)
    if raw_instance.__class__.__name__ == "pythonNode":
        return UIPythonNode(raw_instance)
    if raw_instance.__class__.__name__ == "constant":
        return UIConstantNode(raw_instance)
    if raw_instance.__class__.__name__ == "convertTo":
        return UIConvertToNode(raw_instance)
    if raw_instance.__class__.__name__ == "makeDict":
        return UIMakeDictNode(raw_instance)
    if raw_instance.__class__.__name__ == "makeAnyDict":
        return UIMakeDictNode(raw_instance)
    if raw_instance.__class__.__name__ == "floatRamp":
        return UIFloatRamp(raw_instance)
    if raw_instance.__class__.__name__ == "colorRamp":
        return UIColorRamp(raw_instance)
    if raw_instance.__class__.__name__ == "imageDisplay":
        return UIImageDisplayNode(raw_instance)
    if raw_instance.__class__.__name__ == "forLoopBegin":
        return UIForLoopBeginNode(raw_instance)
    if raw_instance.__class__.__name__ == "whileLoopBegin":
        return UIWhileLoopBeginNode(raw_instance)
    return UINodeBase(raw_instance)
