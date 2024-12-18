from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton

from .money_tracker_widget import MoneyTrackerWidget


class TransactionListView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initSearchData()

    def initSearchData(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 1. 選擇日期
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("選擇日期："))
        date_layout.addStretch()  # 添加空間，將輸入框推到右側
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())  # 預設為當前日期
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        # 4. 確定新增按鈕
        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel(""))
        button_layout.addStretch()
        self.submit_button = QPushButton("確定")
        self.submit_button.setObjectName("applyButton")
        button_layout.addWidget(self.submit_button)
        # self.submit_button.clicked.connect(self.submit_data)  # 綁定事件
        layout.addLayout(button_layout)

    @classmethod
    def getIconPath(cls):
        return "./images/bar-chart.png"

    @classmethod
    def getName(cls):
        return "瀏覽與查詢"
