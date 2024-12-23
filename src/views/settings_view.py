from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox, QFormLayout

from .money_tracker_widget import MoneyTrackerWidget
from models import *
from utils import *
from services.config_service import ConfigService
from services.data_service import DataService
from services.cloud_sync_service import CloudSyncService


class SettingsView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_service = ConfigService()
        self.data_service = DataService('local_account_books.json')
        self.cloud_service = CloudSyncService(self.config_service.get_cred_path(), self.config_service.get_db_url())
        self.initAccountBookSettings()

    def initAccountBookSettings(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 1. 顯示並修改雲端帳本設定
        cloud_settings_layout = QFormLayout()
        self.cred_path_input = QLineEdit(self.config_service.get_cred_path())
        self.db_url_input = QLineEdit(self.config_service.get_db_url())
        save_cloud_settings_button = QPushButton("保存雲端設定")
        save_cloud_settings_button.setObjectName("cancelButton")
        save_cloud_settings_button.clicked.connect(self.save_cloud_settings)
        cloud_settings_layout.addRow("Cred Path:", self.cred_path_input)
        cloud_settings_layout.addRow("DB URL:", self.db_url_input)
        cloud_settings_layout.addRow(save_cloud_settings_button)
        layout.addLayout(cloud_settings_layout)

        # 2. 帳本選擇 ComboBox
        self.accountbook_combo = QComboBox()
        self.load_account_books()
        layout.addWidget(self.accountbook_combo)

        # 3. 新增帳本
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("新增帳本："))
        name_layout.addStretch()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("請輸入帳本名稱")
        local_add_button = QPushButton("新增本地帳本")
        local_add_button.setObjectName("cancelButton")
        local_add_button.clicked.connect(self.add_local_account_book)
        cloud_add_button = QPushButton("新增雲端帳本")
        cloud_add_button.setObjectName("cancelButton")
        cloud_add_button.clicked.connect(self.add_cloud_account_book)
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(local_add_button)
        name_layout.addWidget(cloud_add_button)
        layout.addLayout(name_layout)

        # 4. 顯示並修改帳本設定
        self.accountbook_settings_layout = QFormLayout()
        self.accountbook_name_input = QLineEdit()
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

    def save_cloud_settings(self):
        cred_path = self.cred_path_input.text().strip()
        db_url = self.db_url_input.text().strip()
        self.config_service.set_cred_path(cred_path)
        self.config_service.set_db_url(db_url)
        QMessageBox.information(self, "成功", "雲端設定已保存！")

    def load_account_books(self):
        local_books = self.data_service.read_account_books()
        cloud_books = self.cloud_service.download_account_books()
        all_books = local_books + cloud_books
        self.accountbook_combo.clear()
        self.accountbook_combo.addItems([b.name for b in all_books])
        self.accountbook_combo.currentIndexChanged.connect(self.display_account_book_settings)

    def add_local_account_book(self):
        accountbook_name = self.name_input.text().strip()
        if accountbook_name:
            self.set_up = addNewAccountBook()
            success = self.set_up.setUp(accountbook_name)
            if success:
                QMessageBox.information(self, "成功", f"本地帳本 '{accountbook_name}' 新增成功！")
                self.load_account_books()
            else:
                QMessageBox.warning(self, "失敗", "本地帳本新增失敗，請重試！")
        else:
            QMessageBox.warning(self, "錯誤", "請輸入帳本名稱！")

    def add_cloud_account_book(self):
        accountbook_name = self.name_input.text().strip()
        if accountbook_name:
            new_book = AccountBook(name=accountbook_name)
            self.cloud_service.upload_account_book(new_book)
            QMessageBox.information(self, "成功", f"雲端帳本 '{accountbook_name}' 新增成功！")
            self.load_account_books()
        else:
            QMessageBox.warning(self, "錯誤", "請輸入帳本名稱！")

    def display_account_book_settings(self):
        selected_book = self.accountbook_combo.currentText()
        self.accountbook_name_input.setText(selected_book)

    def rename_account_book(self):
        current_name = self.accountbook_combo.currentText()
        new_name = self.accountbook_name_input.text().strip()
        if new_name and current_name != new_name:
            # Implement renaming logic here
            QMessageBox.information(self, "成功", f"帳本名稱已更改為 '{new_name}'")
            self.load_account_books()
        else:
            QMessageBox.warning(self, "錯誤", "請輸入新的帳本名稱！")

    def delete_account_book(self):
        current_name = self.accountbook_combo.currentText()
        # Implement deletion logic here
        QMessageBox.information(self, "成功", f"帳本 '{current_name}' 已刪除")
        self.load_account_books()

    @classmethod
    def getIconPath(cls):
        return "./images/book-keeping.png"

    @classmethod
    def getName(cls):
        return "帳本設定"