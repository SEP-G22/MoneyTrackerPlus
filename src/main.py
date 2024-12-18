import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from views import *

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        font = QFont("微軟正黑體", 10)  # 字體名稱和字號
        app.setFont(font)
        window = MoneyTrackerPlusView()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        raise
