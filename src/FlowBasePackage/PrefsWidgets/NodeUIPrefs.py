from qtpy.QtWidgets import *
from qtpy import QtCore

from uflow.UI.Widgets.PreferencesWindow import CategoryWidgetBase
from uflow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget


class NodeUIPreferences(CategoryWidgetBase):
    def __init__(self, parent=None):
        super(NodeUIPreferences, self).__init__(parent)
        self.content = QWidget()
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)
        self.setWidget(self.content)

        uiCategory = CollapsibleFormWidget(headName="Node UI")
        self.cbShowComputingTime = QCheckBox(self)
        uiCategory.addWidget("Show computing time on nodes", self.cbShowComputingTime)
        self.layout.addWidget(uiCategory)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

    def initDefaults(self, settings):
        settings.setValue("ShowComputingTime", True)

    def serialize(self, settings):
        settings.setValue(
            "ShowComputingTime",
            self.cbShowComputingTime.checkState() == QtCore.Qt.Checked,
        )

    def onShow(self, settings):
        try:
            self.cbShowComputingTime.setChecked(
                settings.value("ShowComputingTime") == "true"
            )
        except Exception:
            pass
