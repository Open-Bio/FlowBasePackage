from uflow.Core import PinBase
from uflow.Core.Common import *


class StringPin(PinBase):
    """doc string for StringPin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(StringPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue("")

    @staticmethod
    def IsValuePin():
        return True

    def getInputWidgetVariant(self):
        if self.annotationDescriptionDict is not None:
            if PinSpecifiers.VALUE_LIST in self.annotationDescriptionDict:
                return "EnumWidget"
            if PinSpecifiers.INPUT_WIDGET_VARIANT in self.annotationDescriptionDict:
                return self.annotationDescriptionDict[
                    PinSpecifiers.INPUT_WIDGET_VARIANT
                ]
        return self._inputWidgetVariant

    @staticmethod
    def supportedDataTypes():
        return ("StringPin",)

    @staticmethod
    def color():
        return 255, 8, 127, 255

    @staticmethod
    def pinDataTypeHint():
        return "StringPin", ""

    @staticmethod
    def internalDataStructure():
        return str

    @staticmethod
    def processData(data):
        return StringPin.internalDataStructure()(data)
