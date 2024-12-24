from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox

from .money_tracker_widget import MoneyTrackerWidget
from .transaction_edit_view import TransactionEditView
from services import *


class TransactionListView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 0
        self.transactions_per_page = 50
        self.config_service = ConfigService()
        self.data_service = DataService('local_account_books.json')
        self.initSearchData()

    def initSearchData(self):
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

        # 2. 顯示交易紀錄
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(3)
        self.transaction_table.setHorizontalHeaderLabels(["日期", "金額", "備註"])
        self.transaction_table.cellDoubleClicked.connect(self.edit_transaction)
        layout.addWidget(self.transaction_table)

        # 3. 分頁按鈕
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一頁")
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addStretch()
        self.next_button = QPushButton("下一頁")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        layout.addLayout(pagination_layout)

        self.setLayout(layout)
        self.load_transactions()

    def load_transactions(self):
        # 取得當前選擇/預設的帳本名稱
        account_book_name = self.config_service.get_default_account_book()
        if not account_book_name:
            return

        # 讀取交易紀錄
        account_books = self.data_service.read_account_books()
        account_book = next((ab for ab in account_books if ab.name == account_book_name), None)
        if not account_book:
            return
        transactions = account_book.transactions
        transactions.sort(key=lambda x: x.date, reverse=True)
        start = self.current_page * self.transactions_per_page
        end = start + self.transactions_per_page
        self.display_transactions(transactions[start:end])

    def display_transactions(self, transactions):
        self.transaction_table.setRowCount(len(transactions))
        for row, transaction in enumerate(transactions):
            self.transaction_table.setItem(row, 0, QTableWidgetItem(transaction.date))
            self.transaction_table.setItem(row, 1, QTableWidgetItem(str(transaction.amount)))
            self.transaction_table.setItem(row, 2, QTableWidgetItem(transaction.description))

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_transactions()

    def next_page(self):
        self.current_page += 1
        self.load_transactions()

    def edit_transaction(self, row, column):
        transaction = self.transactions[row]
        self.parent().setCurrentWidget(TransactionEditView(transaction=transaction))

    @classmethod
    def getIconPath(cls):
        return "./images/bar-chart.png"

    @classmethod
    def getName(cls):
        return "瀏覽與查詢"
