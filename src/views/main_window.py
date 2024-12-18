from typing import Type, Final

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, \
    QStackedWidget, QScrollArea, QWidget, QLabel, QDateEdit, QComboBox, QLineEdit, QPushButton \
    
from PyQt5.QtCore import QDate

from .chart_view import ChartView
from .money_tracker_widget import MoneyTrackerWidget
from .settings_view import SettingsView
from .transaction_edit_view import TransactionEditView
from .transaction_list_view import TransactionListView


class MoneyTrackerPlusView(QWidget):

    items: Final[list[Type[MoneyTrackerWidget]]] = [TransactionEditView, TransactionListView, ChartView, SettingsView]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("記帳+")
        self.setStyleSheet(self.get_stylesheet())

        # 创建分类列表
        self.category_list = QListWidget()
        self.category_list.setFixedWidth(200)  # 设置固定宽度
        for it in self.items:
            self.add_category_item(it.getName(), it.getIconPath())
        self.category_list.setCurrentRow(0)  # 默认选择第一个项
        self.category_list.currentRowChanged.connect(self.display_content)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.category_list)
        scroll_area.setFixedWidth(200)  # 确保滚动区域宽度一致

        # 创建右侧的内容区域
        self.content_stack = QStackedWidget()
        for it in self.items:
            self.content_stack.addWidget(it(self))

        # 设置主布局
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(scroll_area)  # 添加到布局中
        self.layout.addWidget(self.content_stack)

    @classmethod
    def get_stylesheet(cls):
        return """
        QDialog {
            background-color: white;
        }
        QDialog * {
            font-family: "Microsoft JhengHei";
            font-size: 12pt;
        }
        QListWidget {
            border: none;
            outline: 0;
            border: 1px solid #C9C9C9;
        }
        QScrollArea {
            border: none;
        }
        QListWidget::item {
            padding: 10px;
            border-radius: 10px;
        }
        QListWidget::item:hover {
            background-color: #f0f0f0;
        }
        QListWidget::item:selected {
            background-color: #E8F0FE;
            color: #2871D5;
        }
        QLineEdit[readOnly="true"], QLineEdit:disabled {
            border: 1px solid #dcdcdc;
            background-color: #f5f5f5;
        }
        QLineEdit, QTextEdit {
            border: 1px solid #6F747A;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton {
            border-radius: 5px;
            padding: 6px 12px;
        }
        QPushButton#applyButton {
            border: none;
            background-color: #4A90E2;
            color: white;
        }
        QPushButton#applyButton:hover {
            background-color: #1767C3;
        }
        QPushButton#cancelButton {
            border: none;
            background-color: #E0E0E0;
            color: #333333;
        }
        QPushButton#cancelButton:hover {
            background-color: #C9C9C9;
        }
        """

    def add_category_item(self, text, icon_path):
        """向分类列表中添加带有图标的项目"""
        item = QListWidgetItem(QIcon(icon_path), text)
        self.category_list.addItem(item)

    def display_content(self, index):
        self.content_stack.setCurrentIndex(index)
