from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QComboBox, QLineEdit, QPushButton, QMessageBox

from .money_tracker_widget import MoneyTrackerWidget
from models import *
from utils import *

class TransactionEditView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initAddData()

    def initAddData(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        download = downloadAccountBooks()
        self.accountbooks = download.setUp()
        self.current_accountbook_name = self.accountbooks[0].name

        # 選擇當前帳本
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("選擇當前帳本："))
        type_layout.addStretch()
        self.type_combo = QComboBox()
        self.type_combo.addItems([self.accountbooks[i].name for i in range(len(self.accountbooks))])
        account_select_button = QPushButton("確定")
        account_select_button.setObjectName("applyButton")
        account_select_button.clicked.connect(self.select_account_book)
        type_layout.addWidget(self.type_combo)
        type_layout.addWidget(account_select_button)
        layout.addLayout(type_layout)

        # 1. 選擇日期
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("選擇日期："))
        date_layout.addStretch()  # 添加空間，將輸入框推到右側
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())  # 預設為當前日期
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        # 2. 選擇收入或支出
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("選擇收入或支出："))
        type_layout.addStretch()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["支出", "收入"])
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)

        # 3. 輸入金額
        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("輸入金額："))
        amount_layout.addStretch()
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("請輸入金額")  # 輸入提示
        amount_layout.addWidget(self.amount)
        layout.addLayout(amount_layout)

        # 3. 輸入備註
        description_layout = QHBoxLayout()
        description_layout.addWidget(QLabel("輸入備註："))
        description_layout.addStretch()
        self.description = QLineEdit()
        self.description.setPlaceholderText("請輸入備註")  # 輸入提示
        description_layout.addWidget(self.description)
        layout.addLayout(description_layout)

        # 4. 確定新增按鈕
        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel(""))
        button_layout.addStretch()
        self.submit_button = QPushButton("確定新增")
        self.submit_button.setObjectName("applyButton")
        button_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.submit_data)  # 綁定事件
        layout.addLayout(button_layout)
    
    def select_account_book(self):
        self.current_accountbook_name = self.type_combo.currentText()
    
    def submit_data(self):
        add_new_transaction = addNewTransaction()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = self.amount.text()
        description = self.description.text()
        self.current_accountbook = self.accountbooks[0]
        for i in range(len(self.accountbooks)):
            if self.accountbooks[i].name == str(self.current_accountbook_name):
                self.current_accountbook = self.accountbooks[i]
        if date and amount and description and self.current_accountbook:
            self.current_accountbook = add_new_transaction.setUp(self.current_accountbook, date, float(amount), description)
            if self.current_accountbook is not None:
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setWindowTitle("成功")
                    msg_box.setText(f"帳目新增成功！")
                    msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")  # 设置文字颜色为黑色
                    msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("失敗")
                msg_box.setText("帳目新增失敗，請重試！")
                msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")  # 设置文字颜色为黑色
                msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("錯誤")
            msg_box.setText("請輸入日期、金額、帳本和備註！")
            msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")  # 设置文字颜色为黑色
            msg_box.exec_()

    @classmethod
    def getIconPath(cls):
        return "./images/add.png"

    @classmethod
    def getName(cls):
        return "新增/編輯"
