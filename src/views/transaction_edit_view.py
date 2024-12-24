from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QComboBox, QLineEdit, QPushButton, QMessageBox

from .money_tracker_widget import MoneyTrackerWidget
from models import *
from utils import *


class TransactionEditView(MoneyTrackerWidget):

    def __init__(self, parent=None, transaction=None):
        super().__init__(parent)
        self.transaction = transaction
        self.initAddData()

    def initAddData(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 1. 選擇日期
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("選擇日期："))
        date_layout.addStretch()
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
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
        self.amount.setPlaceholderText("請輸入金額")
        amount_layout.addWidget(self.amount)
        layout.addLayout(amount_layout)

        # 4. 輸入備註
        description_layout = QHBoxLayout()
        description_layout.addWidget(QLabel("輸入備註："))
        description_layout.addStretch()
        self.description = QLineEdit()
        self.description.setPlaceholderText("請輸入備註")
        description_layout.addWidget(self.description)
        layout.addLayout(description_layout)

        # 5. 選擇分類
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("選擇分類："))
        category_layout.addStretch()
        self.category_combo = QComboBox()
        self.category_combo.addItems([name for name, _ in TransactionCategory.predefined_categories().items()])
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)

        # 6. 確定新增按鈕
        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel(""))
        button_layout.addStretch()
        self.submit_button = QPushButton("確定新增")
        self.submit_button.setObjectName("applyButton")
        button_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.submit_data)
        layout.addLayout(button_layout)

        if self.transaction:
            self.load_transaction_data()

    def load_transaction_data(self):
        self.date_edit.setDate(QDate.fromString(self.transaction.date, "yyyy-MM-dd"))
        self.amount.setText(str(self.transaction.amount))
        self.description.setText(self.transaction.description)
        self.category_combo.setCurrentText(self.transaction.category.name)

    def submit_data(self):
        add_new_transaction = addNewTransaction()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = self.amount.text()
        description = self.description.text()
        category = self.category_combo.currentText()
        account_book_name = self.config_service.get_default_account_book()
        if date and amount and description and account_book_name:
            self.current_accountbook = add_new_transaction.setUp(account_book_name, date, float(amount), description, category)
            if self.current_accountbook is not None:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("成功")
                msg_box.setText(f"帳目新增成功！")
                msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("失敗")
                msg_box.setText("帳目新增失敗，請重試！")
                msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
                msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("錯誤")
            msg_box.setText("請輸入日期、金額、帳本和備註！")
            msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
            msg_box.exec_()

    @classmethod
    def getIconPath(cls):
        return "./images/add.png"

    @classmethod
    def getName(cls):
        return "新增/編輯"
