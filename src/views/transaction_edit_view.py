# Implemented by 李崑銘 & 陳衍廷 & 蔡淵丞

import uuid
from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QComboBox, QLineEdit, QPushButton, QMessageBox

from .money_tracker_widget import MoneyTrackerWidget
from models import *
from utils import *
from services import *


class TransactionEditView(MoneyTrackerWidget):

    def __init__(self, parent=None, transaction=None):
        super().__init__(parent)
        self.data_service = DataService('local_account_books.json')
        self.config_service = ConfigService()
        self.cloud_service = CloudSyncService(self.config_service.get_cred_path(),
                                              self.config_service.get_db_url())
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
        for name, c in TransactionCategory.predefined_categories().items():
            icon = QIcon(c.getIconPath())
            self.category_combo.addItem(icon, name)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)

        # 6. 確定新增按鈕
        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel(""))
        button_layout.addStretch()
        self.submit_button = QPushButton("確定新增/修改")
        self.submit_button.setObjectName("applyButton")
        button_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.submit_data)
        layout.addLayout(button_layout)
        layout.addStretch()

        if self.transaction:
            self.load_transaction_data()

    def load_transaction_data(self):
        if self.transaction is None:
            return
        date_str = self.transaction.date.strftime("%Y-%m-%d")
        self.date_edit.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
        self.amount.setText(str(self.transaction.amount))
        self.description.setText(self.transaction.description)
        self.category_combo.setCurrentText(self.transaction.category.category)

    def submit_data(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        time = datetime.now().strftime("%H:%M:%S")
        datetime_str = f"{date} {time}"
        amount = self.amount.text()
        description = self.description.text()
        category_name = self.category_combo.currentText()
        account_book_name = self.config_service.get_default_account_book()
        account_book = get_account_book(account_book_name)

        if not amount or not description or not account_book_name:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("錯誤")
            msg_box.setText("請輸入金額、帳本和備註！")
            msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
            msg_box.exec_()
            return

        try:
            category = TransactionCategory.predefined_categories()[category_name]
            if self.transaction is None:
                # 新增操作
                new_transaction = Transaction(
                    id=self.generate_new_id(),  # 假設有一個方法來生成新的ID
                    date=datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S"),
                    amount=float(amount),
                    description=description,
                    category=category
                )
                account_book.add_transaction(new_transaction)
                if account_book.type == 0:  # 本地帳本
                    self.data_service.write_transactions(account_book_name, account_book.transactions)
                else:  # 雲端帳本
                    self.cloud_service.upload_account_book(account_book)
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("成功")
                msg_box.setText("帳目新增成功！")
                msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
                msg_box.exec_()
            else:
                # 修改操作
                self.transaction.date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                self.transaction.amount = float(amount)
                self.transaction.description = description
                self.transaction.category = category
                for i, t in enumerate(account_book.transactions):
                    if t.id == self.transaction.id:
                        account_book.transactions[i] = self.transaction
                        break
                if account_book.type == 0:  # 本地帳本
                    self.data_service.write_transactions(account_book_name, account_book.transactions)
                else:  # 雲端帳本
                    self.cloud_service.upload_account_book(account_book)
                self.transaction = None
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("成功")
                msg_box.setText("帳目修改成功！")
                msg_box.setStyleSheet("QLabel{color: black; font-size: 10pt;}")
                msg_box.exec_()

            # 清空填入的資訊
            self.date_edit.setDate(QDate.currentDate())
            self.amount.clear()
            self.description.clear()
            self.category_combo.setCurrentIndex(0)

        except ValueError:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("錯誤")
            msg_box.setText("金額格式錯誤，請重新輸入！")
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
