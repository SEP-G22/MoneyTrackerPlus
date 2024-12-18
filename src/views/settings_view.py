from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit

from .money_tracker_widget import MoneyTrackerWidget


class SettingsView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initAccountBookSettings()

    def initAccountBookSettings(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 2. 選擇當前帳本
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("選擇當前帳本："))
        type_layout.addStretch()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Book1", "Book2", "Book3"])
        account_select_button = QPushButton("確定")
        account_select_button.setObjectName("applyButton")
        type_layout.addWidget(self.type_combo)
        type_layout.addWidget(account_select_button)
        layout.addLayout(type_layout)

        # 3. 新增帳本
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("新增帳本："))
        name_layout.addStretch()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("請輸入帳本名稱")  # 輸入提示
        account_add_button = QPushButton("確定")
        account_add_button.setObjectName("applyButton")
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(account_add_button)
        layout.addLayout(name_layout)

    @classmethod
    def getIconPath(cls):
        return "./images/book-keeping.png"

    @classmethod
    def getName(cls):
        return "帳本設定"
