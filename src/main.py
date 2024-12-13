import sys

from PyQt5.QtWidgets import QApplication

from views import *

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MoneyTrackerPlusView()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        raise
