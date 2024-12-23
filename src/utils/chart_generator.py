# 生成分析圖表
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc

# 設定中文字體為 Microsoft YaHei 或 STHeiti，這些字體在許多系統中都有安裝
rc("font", family="Microsoft YaHei")  # 你可以替換為 "STHeiti" 或 "Arial Unicode MS"
rc("axes", unicode_minus=False)  # 解決負號顯示問題

class PieChartWidget(QWidget):
    def __init__(self, transactions, parent=None):
        super().__init__(parent)
        self.transactions = transactions
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 圓餅圖
        self.figure = Figure(figsize=(5, 4))  # 設置更小的圖表尺寸 (寬5，高4)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # 表格顯示每個交易的收入/支出明細
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["日期", "描述", "金額"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # 設置行高
        self.table.verticalHeader().setDefaultSectionSize(30)
        # 設置列寬
        self.table.horizontalHeader().setDefaultSectionSize(150)

        # 生成圖表按鈕
        self.generate_button = QPushButton("生成圖表")
        self.generate_button.clicked.connect(self.generate_chart)
        layout.addWidget(self.generate_button, alignment=Qt.AlignRight)

    def generate_chart(self):
        # 解析傳入的交易數據
        data = {"收入": 0, "支出": 0}
        for transaction in self.transactions:
            amount = transaction["amount"]
            if amount > 0:
                data["收入"] += amount
            else:
                data["支出"] += -amount

        # 繪製圓餅圖
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(
            [data["支出"], data["收入"]],
            labels=["支出", "收入"],
            autopct="%1.1f%%",
            colors=["#FF9999", "#99CCFF"],
            textprops={"fontsize": 14}  # 調整分類標籤字體大小
        )
        ax.set_title("收入與支出比例", fontsize=16)
        self.canvas.draw()

        # 更新表格內容
        self.table.setRowCount(len(self.transactions))
        for i, transaction in enumerate(self.transactions):
            self.table.setItem(i, 0, QTableWidgetItem(transaction["date"]))
            self.table.setItem(i, 1, QTableWidgetItem(transaction["description"]))
            self.table.setItem(i, 2, QTableWidgetItem(f"{transaction['amount']}"))

if __name__ == "__main__":
    # 測試數據
    transactions = [
        {"id": 1, "amount": -500, "date": "2024-12-22", "description": "食物"},
        {"id": 2, "amount": -200, "date": "2024-12-21", "description": "交通"},
        {"id": 3, "amount": -150, "date": "2024-12-20", "description": "娛樂"},
        {"id": 4, "amount": 3000, "date": "2024-12-19", "description": "薪水"},
        {"id": 5, "amount": 500, "date": "2024-12-18", "description": "投資"},
    ]

    app = QApplication(sys.argv)
    window = PieChartWidget(transactions)
    window.resize(800,600)
    window.show()
    sys.exit(app.exec_())
