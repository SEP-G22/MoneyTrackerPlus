from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox, QFormLayout

from .money_tracker_widget import MoneyTrackerWidget
from models import *
from utils import *
from services import *


class SettingsView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_service = ConfigService()
        self.data_service = DataService('local_account_books.json')
        self.initAccountBookSettings()

    def initAccountBookSettings(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 2. 帳本選擇
        combo_layout = QHBoxLayout()
        accountbook_combo_label = QLabel("選擇帳本：")
        self.accountbook_combo = QComboBox()
        self.accountbook_name_input = QLineEdit()
        self.load_account_books()
        combo_layout.addWidget(accountbook_combo_label)
        combo_layout.addWidget(self.accountbook_combo)
        layout.addLayout(combo_layout)

        # 3. 新增帳本
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("新增帳本："))
        name_layout.addStretch()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("請輸入帳本名稱")
        local_add_button = QPushButton("新增本地帳本")
        local_add_button.setObjectName("cancelButton")
        local_add_button.clicked.connect(self.add_local_account_book)
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(local_add_button)
        layout.addLayout(name_layout)

        # 4. 顯示並修改帳本設定
        self.accountbook_settings_layout = QFormLayout()
        rename_button = QPushButton("更改名稱")
        rename_button.setObjectName("cancelButton")
        rename_button.clicked.connect(self.rename_account_book)
        delete_button = QPushButton("刪除帳本")
        delete_button.setObjectName("applyButton")
        delete_button.clicked.connect(self.delete_account_book)
        self.accountbook_settings_layout.addRow("帳本名稱:", self.accountbook_name_input)
        self.accountbook_settings_layout.addRow(rename_button)
        self.accountbook_settings_layout.addRow(delete_button)
        layout.addLayout(self.accountbook_settings_layout)

        self.setLayout(layout)
        self.set_default_account_book()

    def set_default_account_book(self):
        default_book = self.config_service.get_default_account_book()
        if default_book:
            index = self.accountbook_combo.findText(default_book)
            if index != -1:
                self.accountbook_combo.setCurrentIndex(index)

    def load_account_books(self):
        try:
            self.accountbook_combo.currentIndexChanged.disconnect(self.display_account_book_settings)
        except TypeError:
            pass  # Ignore if the signal is not connected
        local_books = get_local_books()
        all_books = local_books
        self.accountbook_combo.clear()
        self.accountbook_combo.addItems([b.name for b in all_books])
        self.accountbook_combo.currentIndexChanged.connect(self.display_account_book_settings)
        self.set_default_account_book()

    def add_local_account_book(self):
        accountbook_name = self.name_input.text().strip()
        if not accountbook_name:
            QMessageBox.warning(self, "錯誤", "請輸入帳本名稱！")
            return
        try:
            if any(b.name == accountbook_name for b in get_local_books()):
                QMessageBox.warning(self, "錯誤", f"本地帳本 '{accountbook_name}' 已存在！")
            else:
                new_book = AccountBook(accountbook_name, 0)
                self.data_service.write_account_books(get_local_books() + [new_book])
                QMessageBox.information(self, "成功", f"本地帳本 '{accountbook_name}' 新增成功！")
                self.config_service.set_default_account_book(accountbook_name)
                self.load_account_books()
                self.accountbook_combo.setCurrentText(accountbook_name)
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"新增本地帳本 '{accountbook_name}' 失敗！")
            print(e)

    def display_account_book_settings(self):
        selected_book = self.accountbook_combo.currentText()
        self.accountbook_name_input.setText(selected_book)
        self.config_service.set_default_account_book(selected_book)

    def rename_account_book(self):
        current_name = self.accountbook_combo.currentText()
        new_name = self.accountbook_name_input.text().strip()
        if not new_name or current_name == new_name:
            QMessageBox.warning(self, "錯誤", "請輸入新的帳本名稱！")
            return
        try:
            account_book = get_account_book(current_name)

            if any(b.name == new_name for b in get_local_books()):
                QMessageBox.warning(self, "錯誤", f"本地帳本 '{new_name}' 已存在！")
                return
            local_books = get_local_books()
            for b in local_books:
                if b.name == current_name: b.name = new_name
            self.data_service.write_account_books(local_books)

            QMessageBox.information(self, "成功", f"帳本 '{current_name}' 已更名為 '{new_name}'")
            self.config_service.set_default_account_book(new_name)
            self.load_account_books()
            self.accountbook_combo.setCurrentText(new_name)
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"更名帳本 '{current_name}' 失敗！")
            print(e)

    def delete_account_book(self):
        current_name = self.accountbook_combo.currentText()
        account_book = get_account_book(current_name)
        if not account_book:
            QMessageBox.warning(self, "錯誤", f"找不到帳本 '{current_name}'！")
            return
        try:

            local_books = get_local_books()
            local_books = [b for b in local_books if b.name != current_name]
            self.data_service.write_account_books(local_books)

            QMessageBox.information(self, "成功", f"帳本 '{current_name}' 已刪除！")
            self.load_account_books()
            self.set_default_account_book()
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"刪除帳本 '{current_name}' 失敗！")
            print(e)

    @classmethod
    def getIconPath(cls):
        return "./images/book-keeping.png"

    @classmethod
    def getName(cls):
        return "帳本設定"
