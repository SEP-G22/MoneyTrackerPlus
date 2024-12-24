from PyQt5.QtCore import QDate, Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QMessageBox, QLineEdit

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
        self.transactions = []
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
        self.first_button = QPushButton("第一頁")
        self.first_button.setObjectName("cancelButton")
        self.first_button.clicked.connect(self.first_page)
        pagination_layout.addWidget(self.first_button)

        self.prev_button = QPushButton("上一頁")
        self.prev_button.setObjectName("cancelButton")
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
        self.next_button.setObjectName("cancelButton")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)

        self.last_button = QPushButton("最後頁")
        self.last_button.setObjectName("cancelButton")
        self.last_button.clicked.connect(self.last_page)
        pagination_layout.addWidget(self.last_button)

        layout.addLayout(pagination_layout)

        self.setLayout(layout)
        self.load_transactions()

    def load_transactions(self):
        account_book_name = self.config_service.get_default_account_book()
        if not account_book_name:
            return

        account_books = self.data_service.read_account_books()
        account_book = next((ab for ab in account_books if ab.name == account_book_name), None)
        if not account_book:
            return
        self.transactions = account_book.transactions  # Populate the transactions attribute
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

    def first_page(self):
        self.current_page = 0
        self.load_transactions()

    def last_page(self):
        account_book_name = self.config_service.get_default_account_book()
        account_books = self.data_service.read_account_books()
        account_book = next((ab for ab in account_books if ab.name == account_book_name), None)
        transactions = account_book.transactions
        self.current_page = (len(transactions) - 1) // self.transactions_per_page
        self.load_transactions()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_transactions()

    def next_page(self):
        account_book_name = self.config_service.get_default_account_book()
        account_books = self.data_service.read_account_books()
        account_book = next((ab for ab in account_books if ab.name == account_book_name), None)
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
        account_books = self.data_service.read_account_books()
        account_book = next((ab for ab in account_books if ab.name == account_book_name), None)
        if account_book:
            account_book.transactions = [t for t in account_book.transactions if t.id != transaction.id]
            if account_book.type == 0:  # 本地帳本
                self.data_service.write_transactions(account_book_name, account_book.transactions)
            else:  # 雲端帳本
                self.cloud_service.upload_account_book(account_book)

    @classmethod
    def getIconPath(cls):
        return "./images/bar-chart.png"

    @classmethod
    def getName(cls):
        return "瀏覽與查詢"
