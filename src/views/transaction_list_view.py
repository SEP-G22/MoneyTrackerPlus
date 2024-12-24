from PyQt5.QtCore import QDate, Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QMessageBox, QLineEdit, QHeaderView, QComboBox
from PyQt5.QtGui import QIcon
import re

from .money_tracker_widget import MoneyTrackerWidget
from .transaction_edit_view import TransactionEditView
from services import *
from utils import *


class TransactionListView(MoneyTrackerWidget):
    switch_view = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 0
        self.transactions_per_page = 50
        self.config_service = ConfigService()
        self.data_service = DataService('local_account_books.json')
        self.cloud_service = CloudSyncService(self.config_service.get_cred_path(), self.config_service.get_db_url())
        self.transactions = []
        self.initSearchData()
        self.setStyleSheet("""
        QPushButton {
            border: none;
            background-color: #E0E0E0;
            color: #333333;
        }
        QPushButton:hover {
            background-color: #C9C9C9;
        }
        """)

    def initSearchData(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 1. 選擇日期範圍
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("選擇日期範圍："))
        date_layout.addStretch()
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        date_layout.addWidget(self.start_date_edit)
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(self.end_date_edit)
        layout.addLayout(date_layout)

        # 2. 查詢描述
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("查詢描述："))
        search_layout.addStretch()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("請輸入描述查詢")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # 3. 顯示交易紀錄
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(4)
        self.transaction_table.setHorizontalHeaderLabels(["日期", "金額", "備註", "分類"])
        self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.transaction_table.cellDoubleClicked.connect(self.edit_transaction)
        layout.addWidget(self.transaction_table)

        # 4. 分頁按鈕
        pagination_layout = QHBoxLayout()
        self.first_button = QPushButton("第一頁")
        self.first_button.clicked.connect(self.first_page)
        pagination_layout.addWidget(self.first_button)

        self.prev_button = QPushButton("上一頁")
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)

        pagination_layout.addStretch()

        self.page_input = QLineEdit()
        self.page_input.setFixedWidth(30)
        self.page_input.setText(str(self.current_page + 1))
        self.page_input.returnPressed.connect(self.go_to_page)
        pagination_layout.addWidget(self.page_input)

        self.page_label = QLabel()
        pagination_layout.addWidget(self.page_label)

        pagination_layout.addStretch()

        self.next_button = QPushButton("下一頁")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)

        self.last_button = QPushButton("最後頁")
        self.last_button.clicked.connect(self.last_page)
        pagination_layout.addWidget(self.last_button)

        layout.addLayout(pagination_layout)

        # 5. 查詢和重設按鈕
        action_layout = QHBoxLayout()
        self.search_button = QPushButton("查詢")
        self.search_button.clicked.connect(self.load_transactions)
        action_layout.addWidget(self.search_button)

        self.reset_button = QPushButton("重設")
        self.reset_button.clicked.connect(self.reset_filters)
        action_layout.addWidget(self.reset_button)

        layout.addLayout(action_layout)

        self.setLayout(layout)
        self.load_transactions()

    def load_transactions(self):
        account_book_name = self.config_service.get_default_account_book()
        if not account_book_name:
            return

        account_book = get_account_book(account_book_name)
        if not account_book:
            return
        self.transactions = account_book.transactions  # Populate the transactions attribute

        # Filter by date range
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()
        self.transactions = [t for t in self.transactions if start_date <= t.date.date() <= end_date]

        # Filter by description regex
        search_text = self.search_input.text()
        if search_text:
            self.transactions = [t for t in self.transactions if re.search(search_text, t.description)]

        self.transactions.sort(key=lambda x: x.date, reverse=True)
        start = self.current_page * self.transactions_per_page
        end = start + self.transactions_per_page
        self.display_transactions(self.transactions[start:end])

        self.page_label.setText(
            f"/ {max(1, (len(self.transactions) + self.transactions_per_page - 1) // self.transactions_per_page)}")
        self.page_input.setText(str(self.current_page + 1))

        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(end < len(self.transactions))
        self.first_button.setEnabled(self.current_page > 0)
        self.last_button.setEnabled(end < len(self.transactions))

    def display_transactions(self, transactions):
        self.transaction_table.setRowCount(len(transactions))
        for row, transaction in enumerate(transactions):
            self.transaction_table.setItem(row, 0, QTableWidgetItem(transaction.date.strftime("%Y-%m-%d %H:%M:%S")))
            self.transaction_table.setItem(row, 1, QTableWidgetItem(str(transaction.amount)))
            self.transaction_table.setItem(row, 2, QTableWidgetItem(transaction.description))
            category_item = QTableWidgetItem(transaction.category.category)
            category_item.setIcon(QIcon(transaction.category.getIconPath()))
            self.transaction_table.setItem(row, 3, category_item)

    def first_page(self):
        self.current_page = 0
        self.load_transactions()

    def last_page(self):
        account_book_name = self.config_service.get_default_account_book()
        account_book = get_account_book(account_book_name)
        transactions = account_book.transactions
        self.current_page = (len(transactions) - 1) // self.transactions_per_page
        self.load_transactions()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_transactions()

    def next_page(self):
        account_book_name = self.config_service.get_default_account_book()
        account_book = get_account_book(account_book_name)
        transactions = account_book.transactions
        if (self.current_page + 1) * self.transactions_per_page < len(transactions):
            self.current_page += 1
            self.load_transactions()

    def go_to_page(self):
        try:
            account_book_name = self.config_service.get_default_account_book()
            account_book = get_account_book(account_book_name)
            page = int(self.page_input.text()) - 1
            max_page = (len(account_book.transactions) - 1) // self.transactions_per_page
            if 0 <= page <= max_page:
                self.current_page = page
                self.load_transactions()
        except ValueError:
            pass
        finally:
            self.page_input.setText(str(self.current_page + 1))

    def edit_transaction(self, row, column):
        transaction = self.transactions[row]
        edit_view = self.parent().findChild(TransactionEditView)
        edit_view.transaction = transaction
        edit_view.load_transaction_data()
        self.switch_view.emit(0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected_row = self.transaction_table.currentRow()
            if selected_row >= 0:
                transaction = self.transactions[selected_row]
                self.delete_transaction(transaction)
                self.load_transactions()
        else:
            super().keyPressEvent(event)

    def delete_transaction(self, transaction):
        account_book_name = self.config_service.get_default_account_book()
        account_book = get_account_book(account_book_name)
        if account_book:
            account_book.transactions = [t for t in account_book.transactions if t.id != transaction.id]
            if account_book.type == 0:  # 本地帳本
                self.data_service.write_transactions(account_book_name, account_book.transactions)
            else:  # 雲端帳本
                self.cloud_service.upload_account_book(account_book)

    def reset_filters(self):
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.end_date_edit.setDate(QDate.currentDate())
        self.search_input.clear()
        self.load_transactions()

    @classmethod
    def getIconPath(cls):
        return "./images/bar-chart.png"

    @classmethod
    def getName(cls):
        return "瀏覽與查詢"
