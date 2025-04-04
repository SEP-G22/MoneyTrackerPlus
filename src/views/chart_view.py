# This file is for the chart analysis view

from datetime import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDateEdit, QHBoxLayout, QPushButton, QApplication, QComboBox, QLineEdit
from models import AccountBook
from .money_tracker_widget import MoneyTrackerWidget
from services import *
from utils import *


class ChartView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_service = ConfigService()
        self.data_service = DataService('local_account_books.json')
        self.initPlotAnalysis()

    def initPlotAnalysis(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 2. 選擇起始日期
        date_start_layout = QHBoxLayout()
        date_start_layout.addWidget(QLabel("選擇起始日期："))
        date_start_layout.addStretch()  # 添加空間，將輸入框推到右側
        self.date_start_edit = QDateEdit()
        self.date_start_edit.setCalendarPopup(True)
        self.date_start_edit.setDate(QDate.currentDate())  # 預設為當前日期
        date_start_layout.addWidget(self.date_start_edit)
        layout.addLayout(date_start_layout)

        # 3. 選擇結束日期
        date_end_layout = QHBoxLayout()
        date_end_layout.addWidget(QLabel("選擇結束日期："))
        date_end_layout.addStretch()  # 添加空間，將輸入框推到右側
        self.date_end_edit = QDateEdit()
        self.date_end_edit.setCalendarPopup(True)
        self.date_end_edit.setDate(QDate.currentDate())  # 預設為當前日期
        date_end_layout.addWidget(self.date_end_edit)
        layout.addLayout(date_end_layout)

        # 4. 選擇圖表
        select_chart_layout = QHBoxLayout()
        select_chart_layout.addWidget(QLabel("選擇圖表："))
        select_chart_layout.addStretch()
        self.chart_combo = QComboBox()
        self.chart_combo.addItems(["圓餅圖", "折線圖", "柱狀圖"])
        select_chart_layout.addWidget(self.chart_combo)
        layout.addLayout(select_chart_layout)

        # 5. 確定新增按鈕
        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel(""))
        button_layout.addStretch()
        self.submit_button = QPushButton("確定")
        self.submit_button.setObjectName("applyButton")
        button_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.display_plot)  # 綁定事件
        layout.addLayout(button_layout)

        self.chart_label = QLabel()
        layout.addWidget(self.chart_label)
        self.submit_button.click()

    def load_account_books(self):
        local_books = get_local_books()
        cloud_books = get_cloud_books()
        all_books = local_books + cloud_books
        self.accountbook_combo.clear()
        self.accountbook_combo.addItems([b.name for b in all_books])
        self.set_default_account_book()
    
    def set_default_account_book(self):
        """
        Set the default account book in the dropdown (QComboBox).

        Retrieves the default account book name from `config_service`,
        finds it in the `accountbook_combo`, and sets it as the selected item
        if it exists in the dropdown list.

        If the default book is not found or is not set, the current selection remains unchanged.
        """
        default_book: str = self.config_service.get_default_account_book()
        if default_book:
            # Attempt to find the index of the default book in the dropdown list
            index: int = self.accountbook_combo.findText(default_book)
            if index != -1:
                # If found(index != -1), set the current selection to the matched index
                self.accountbook_combo.setCurrentIndex(index)

    def get_transactions(self, accountbook: AccountBook, start_date: datetime, end_date: datetime) -> list:
        """
        Retrieve transactions from an account book within a specified date range.

        If the start date is after the end date, the two will be swapped to ensure
        a valid chronological range.

        Args:
            accountbook (AccountBook): The account book containing transaction records.
            start_date (datetime): The beginning of the date range.
            end_date (datetime): The end of the date range.

        Returns:
            list: A list of transactions occurring within the specified date range.
        """
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        transactions: list = []
        for transaction in accountbook.transactions:
            transaction_date = transaction.date.date() if isinstance(transaction.date, datetime) else transaction.date
            if start_date <= transaction_date <= end_date:
                transactions.append(transaction)
        return transactions

    def display_plot(self):
        accountbook_name = self.config_service.get_default_account_book()
        accountbook = get_account_book(accountbook_name)
        if not accountbook:
            return
        transactions = self.get_transactions(accountbook, self.date_start_edit.date().toPyDate(),
                                             self.date_end_edit.date().toPyDate())
        chart_type = self.chart_combo.currentText()

        if chart_type == "圓餅圖":
            chart_image_path = generate_pie_chart(transactions)
        elif chart_type == "折線圖":
            chart_image_path = generate_line_chart(transactions)
        elif chart_type == "柱狀圖":
            chart_image_path = generate_bar_chart(transactions)
        self.chart_label.setPixmap(QPixmap(chart_image_path))

    @classmethod
    def getIconPath(cls):
        return "./images/requirements.png"

    @classmethod
    def getName(cls):
        return "圖表分析"
