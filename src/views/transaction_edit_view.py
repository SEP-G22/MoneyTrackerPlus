import uuid
from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QComboBox, QLineEdit, QPushButton, QMessageBox

from .money_tracker_widget import MoneyTrackerWidget
from models import *
from utils import *


class TransactionEditView(MoneyTrackerWidget):

    def __init__(self, parent=None, transaction=None, account_book=None):
        super().__init__(parent)
        self.transaction = transaction
        if account_book is not None:
            self.account_book = account_book
        else:
            self.account_book = get_account_book(self.config_service.get_default_account_book())
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
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = self.amount.text()
        description = self.description.text()
        category_name = self.category_combo.currentText()
        account_book_name = self.config_service.get_default_account_book()
        account_book = get_account_book(account_book_name)

        if not date or not amount or not description or not account_book_name:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("錯誤")
            msg_box.setText("請輸入日期、金額、帳本和備註！")
            msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
            msg_box.exec_()
            return

        try:
            category = TransactionCategory.predefined_categories()[category_name]
            if self.transaction is None:
                # 新增操作
                new_transaction = Transaction(
                    id=self.generate_new_id(),  # 假設有一個方法來生成新的ID
                    date=datetime.strptime(date, "%Y-%m-%d"),
                    amount=float(amount),
                    description=description,
                    category=category
                )
                if account_book.type == 0:  # 本地帳本
                    local_transactions = get_local_transactions(account_book_name)
                    local_transactions.append(new_transaction)
                    self.data_service.write_transactions(account_book_name, local_transactions)
                else:  # 雲端帳本
                    self.cloud_service.upload_transaction(account_book_name, new_transaction)
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("成功")
                msg_box.setText("帳目新增成功！")
                msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
                msg_box.exec_()
            else:
                # 修改操作
                self.transaction.date = datetime.strptime(date, "%Y-%m-%d")
                self.transaction.amount = float(amount)
                self.transaction.description = description
                self.transaction.category = category
                if account_book.type == 0:  # 本地帳本
                    local_transactions = get_local_transactions(account_book_name)
                    for i, t in enumerate(local_transactions):
                        if t.id == self.transaction.id:
                            local_transactions[i] = self.transaction
                            break
                    self.data_service.write_transactions(account_book_name, local_transactions)
                else:  # 雲端帳本
                    self.cloud_service.update_transaction(account_book_name, self.transaction)
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("成功")
                msg_box.setText("帳目修改成功！")
                msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
                msg_box.exec_()
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("失敗")
            msg_box.setText("帳目操作失敗，請重試！")
            msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
            msg_box.exec_()
            print(e)

    def generate_new_id(self):
        """
        Generate a new unique identifier for a transaction.

        :return: A new unique identifier.
        :rtype: int
        """
        return uuid.uuid4().int

    @classmethod
    def getIconPath(cls):
        return "./images/add.png"

    @classmethod
    def getName(cls):
        return "新增/編輯"
