from qtpy.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QCheckBox,
    QSpacerItem,
    QSizePolicy,
    QWidget,
)
from uflow.UI.Widgets.PreferencesWindow import CategoryWidgetBase
from uflow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget


class AIPreferences(CategoryWidgetBase):
    """DeepSeek 接入配置页"""

    def __init__(self, parent=None):
        super(AIPreferences, self).__init__(parent)
        self.content = QWidget()
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)
        self.setWidget(self.content)

        section = CollapsibleFormWidget(headName="DeepSeek")

        self.apiKey = QLineEdit()
        self.apiKey.setPlaceholderText("支持环境变量 DEEPSEEK_API_KEY（仅本地保存）")
        section.addWidget("api_key", self.apiKey)

        self.baseUrl = QLineEdit()
        self.baseUrl.setPlaceholderText("https://api.deepseek.com")
        section.addWidget("base_url", self.baseUrl)

        self.model = QLineEdit()
        self.model.setPlaceholderText("deepseek-chat / deepseek-coder / 其他兼容模型名")
        section.addWidget("model", self.model)

        self.layout.addWidget(section)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

    def initDefaults(self, settings):
        settings.setValue("OpenAI/api_key", "")
        settings.setValue("OpenAI/base_url", "https://api.deepseek.com")
        settings.setValue("OpenAI/model", "deepseek-chat")

    def serialize(self, settings):
        settings.setValue("OpenAI/api_key", self.apiKey.text())
        settings.setValue("OpenAI/base_url", self.baseUrl.text())
        settings.setValue("OpenAI/model", self.model.text())

    def onShow(self, settings):
        self.apiKey.setText(settings.value("OpenAI/api_key"))
        base = settings.value("OpenAI/base_url")
        self.baseUrl.setText(base if base else "https://api.deepseek.com")
        mdl = settings.value("OpenAI/model")
        self.model.setText(mdl if mdl else "deepseek-chat")
