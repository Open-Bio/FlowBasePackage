from qtpy import QtGui, QtCore
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
)

from uflow.UI.Tool.Tool import DockTool
from uflow.ConfigManager import ConfigManager
from uflow.AI.openai_client import OpenAIClient
from uflow.AI.service import (
    AIServiceError,
    ConfigurationError,
    ValidationError,
    NetworkError,
    APIError,
)
from uflow.UI.Widgets.BlueprintCanvas import getNodeInstance
from uflow import getRawNodeInstance
import uuid
import os
import time


class AINodeGenerator(DockTool):
    def __init__(self):
        super(AINodeGenerator, self).__init__()
        self.setWindowTitle(self.name())

        root = QWidget(self)
        lay = QVBoxLayout(root)
        self.prompt = QTextEdit()
        self.prompt.setPlaceholderText(
            "描述你要的纯函数节点：输入/输出/逻辑，例如：\n计算字符串前5个字符\n计算两个数的乘积\n字符串转大写"
        )
        lay.addWidget(self.prompt)

        btns = QHBoxLayout()
        self.btnGenerate = QPushButton("AI 生成纯函数")
        self.btnClean = QPushButton("清理代码")
        self.btnApplySelected = QPushButton("应用到选中 PythonNode")
        self.btnInsert = QPushButton("新建并插入")
        btns.addWidget(self.btnGenerate)
        btns.addWidget(self.btnClean)
        btns.addWidget(self.btnApplySelected)
        btns.addWidget(self.btnInsert)
        lay.addLayout(btns)

        lay.addWidget(QLabel("AI生成信息"))
        self.outDsl = QPlainTextEdit()
        self.outDsl.setReadOnly(True)
        lay.addWidget(self.outDsl)

        lay.addWidget(QLabel("生成的纯函数节点代码"))
        self.outCode = QPlainTextEdit()
        self.outCode.setReadOnly(True)
        lay.addWidget(self.outCode)

        self.setWidget(root)

        self.btnGenerate.clicked.connect(self.onGenerate)
        self.btnClean.clicked.connect(self.onClean)
        self.btnApplySelected.clicked.connect(self.onApplySelected)
        self.btnInsert.clicked.connect(self.onInsert)

        self.lastGoodCode = ""
        self._genThread = None
        self._genWorker = None

    def __del__(self):
        """析构函数，确保线程资源被清理"""
        self._cleanupThread()

    class _GenerateWorker(QtCore.QObject):
        finished = QtCore.Signal(str, str, str)

        def __init__(self, prompt: str):
            super().__init__()
            self._prompt = prompt

        def _clean_code_fences(self, code: str) -> str:
            """清理代码中的围栏"""
            if not code:
                return ""

            # 去掉可能的围栏
            if code.startswith("```"):
                code = code.strip("`\n")
                if code.startswith("python\n"):
                    code = code[7:]
                elif code.startswith("py\n"):
                    code = code[3:]

            return code.strip()

        @QtCore.Slot()
        def run(self):
            try:
                client = OpenAIClient()
                code = client.generate_code(self._prompt)
                if not code:
                    raise RuntimeError("AI返回空内容")

                # 清理代码中的围栏
                cleaned_code = self._clean_code_fences(code)
                if not cleaned_code:
                    raise RuntimeError("代码清理失败")

                # 额外验证生成的代码
                self._validate_generated_code(cleaned_code)

                self.finished.emit("AI生成成功", cleaned_code, "")
            except ConfigurationError as e:
                self.finished.emit("", "", f"配置错误: {e}")
            except ValidationError as e:
                self.finished.emit("", "", f"输入验证错误: {e}")
            except NetworkError as e:
                self.finished.emit("", "", f"网络错误: {e}")
            except APIError as e:
                self.finished.emit("", "", f"API错误: {e}")
            except AIServiceError as e:
                self.finished.emit("", "", f"AI服务错误: {e}")
            except Exception as e:
                self.finished.emit("", "", f"未知错误: {e}")

        def _validate_generated_code(self, code: str) -> None:
            """验证生成的代码"""
            if not code or not isinstance(code, str):
                raise ValueError("代码内容无效")

            # 检查基本结构
            if "from uflow.Core.Common import *" not in code:
                raise ValueError("生成的代码缺少必要的导入")
            if "def prepareNode" not in code:
                raise ValueError("生成的代码缺少prepareNode函数")
            if "def compute" not in code:
                raise ValueError("生成的代码缺少compute函数")

            # 检查是否包含执行流代码（违反纯函数原则）
            exec_keywords = ["ExecPin", "outExec", "inExec", ".call("]
            for keyword in exec_keywords:
                if keyword in code:
                    raise ValueError(f"生成的代码包含执行流相关代码: {keyword}")

            # 检查代码长度
            if len(code) > 10000:
                raise ValueError("生成的代码过长")

    @staticmethod
    def getIcon():
        return QtGui.QIcon(":brick.png")

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def name():
        return str("AINodeGenerator")

    def _ensurePrefs(self):
        s = ConfigManager().getSettings("PREFS")
        s.beginGroup("AI")
        ok = bool(s.value("OpenAI/api_key", "")) or bool(
            os.environ.get("DEEPSEEK_API_KEY", "")
        )
        s.endGroup()
        return ok

    def _saveTemp(self, code: str) -> str:
        """安全地保存临时文件"""
        if not code or not isinstance(code, str):
            raise ValueError("代码内容无效")

        tempDir = self.uflowInstance.getTempDirectory()
        aiDir = os.path.join(tempDir, "ai_nodes")

        # 确保目录存在且权限正确
        try:
            if not os.path.exists(aiDir):
                os.makedirs(aiDir, mode=0o700)  # 仅所有者可读写执行
        except OSError as e:
            raise RuntimeError(f"无法创建临时目录: {e}")

        # 使用UUID生成安全的文件名
        import uuid

        filename = f"ai_node_{uuid.uuid4().hex}.pynode"
        path = os.path.join(aiDir, filename)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            # 设置文件权限
            os.chmod(path, 0o600)  # 仅所有者可读写
        except OSError as e:
            raise RuntimeError(f"无法保存临时文件: {e}")

        return path

    def _setBusy(self, busy: bool):
        self.btnGenerate.setDisabled(busy)
        self.btnApplySelected.setDisabled(busy)
        self.btnInsert.setDisabled(busy)
        if busy:
            self.outDsl.setPlainText("生成中，请稍候...")

    def _onGenerateFinished(self, info_text: str, code: str, error: str):
        self._setBusy(False)
        if error:
            self.outDsl.setPlainText(f"生成失败: {error}")
            self.outCode.setPlainText("")
            return

        self.outDsl.setPlainText(info_text)
        self.outCode.setPlainText(code)
        self.lastGoodCode = code

        try:
            self._saveTemp(code)
        except Exception as e:
            self.outCode.appendPlainText(f"\n[警告] 保存临时文件失败: {e}")

        # 清理线程对象引用
        self._cleanupThread()

    def _cleanupThread(self):
        """清理线程资源"""
        if self._genThread is not None:
            self._genThread.quit()
            self._genThread.wait(3000)  # 等待3秒
            if self._genThread.isRunning():
                self._genThread.terminate()
                self._genThread.wait()
        self._genThread = None
        self._genWorker = None

    def onGenerate(self):
        if not self._ensurePrefs():
            self.outDsl.setPlainText(
                "请先在 Preferences > AI 配置 DeepSeek api_key 或设置环境变量 DEEPSEEK_API_KEY"
            )
            return

        prompt = self.prompt.toPlainText().strip()
        if not prompt:
            self.outDsl.setPlainText("请输入需求描述")
            return

        if len(prompt) < 5:
            self.outDsl.setPlainText("需求描述太短，请提供更详细的说明")
            return

        # 检查是否已有生成任务在进行
        if self._genThread is not None and self._genThread.isRunning():
            self.outDsl.setPlainText("生成任务正在进行中，请稍候...")
            return

        # 后台线程执行，避免阻塞 UI
        self._setBusy(True)
        self._genThread = QtCore.QThread(self)
        self._genWorker = self._GenerateWorker(prompt)
        self._genWorker.moveToThread(self._genThread)
        self._genThread.started.connect(self._genWorker.run)
        self._genWorker.finished.connect(self._onGenerateFinished)
        self._genThread.start()

    def onClean(self):
        """清理代码中的中文注释和无效内容"""
        # 只清理纯代码，不包含日志信息
        code = self.lastGoodCode
        if not code:
            self.outCode.appendPlainText("[提示] 没有代码需要清理")
            return

        lines = code.split("\n")
        cleaned_lines = []
        removed_count = 0

        for line in lines:
            # 跳过纯中文行（但不跳过包含中文的代码行）
            if all("\u4e00" <= char <= "\u9fff" for char in line.strip()):
                removed_count += 1
                continue
            # 跳过以 # 开头的注释行
            if line.strip().startswith("#"):
                removed_count += 1
                continue
            cleaned_lines.append(line)

        cleaned_code = "\n".join(cleaned_lines)
        # 更新纯代码
        self.lastGoodCode = cleaned_code
        # 重新设置显示内容
        self.outCode.setPlainText(cleaned_code)

        if removed_count > 0:
            self.outCode.appendPlainText(
                f"\n[已清理] 移除了 {removed_count} 行注释和无效内容"
            )
        else:
            self.outCode.appendPlainText("\n[提示] 代码无需清理")

    def onApplySelected(self):
        # 只使用lastGoodCode，避免日志信息混入
        code = self.lastGoodCode
        if not code:
            self.outCode.appendPlainText("\n[提示] 没有可应用的代码")
            return

        # 通过 canvas 属性访问 selectedNodes 方法
        canvas = self.uflowInstance.getCanvas()
        selected = canvas.selectedNodes()
        if not selected:
            self.outCode.appendPlainText("\n[提示] 请先选择一个 PythonNode")
            return

        # 仅对第一个选中节点尝试
        ui_node = selected[0]
        try:
            ui_node.tryApplyNodeData(code)
            self.outCode.appendPlainText("\n[成功] 已应用到选中节点")
        except Exception as e:
            self.outCode.appendPlainText(f"\n[失败] 应用代码时出错: {e}")

    def onInsert(self):
        # 只使用lastGoodCode，避免日志信息混入
        code = self.lastGoodCode
        if not code:
            self.outCode.appendPlainText("\n[提示] 没有可插入的代码")
            return

        # 使用 spawnNode 方法创建节点，避免图引用问题
        canvas = self.uflowInstance.getCanvas()
        try:
            # 使用 spawnNode 创建 pythonNode
            ui = canvas.spawnNode("pythonNode", 100, 100)
            if ui:
                ui.tryApplyNodeData(code)
                self.outCode.appendPlainText("\n[成功] 已插入并应用代码")
            else:
                self.outCode.appendPlainText("\n[失败] 无法创建 pythonNode")
        except Exception as e:
            self.outCode.appendPlainText(f"\n[失败] 插入节点时出错: {e}")
