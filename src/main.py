import sys
import logging
import traceback

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from views import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    """Handles uncaught exceptions by logging them."""
    logging.critical(''.join(traceback.format_exception(ex_cls, ex, tb)))
    sys.exit(1)


if __name__ == '__main__':
    logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s",
                        level=logging.INFO,
                        )
    logging.info("Process started.")

    try:
        app = QApplication(sys.argv)
        font = QFont("微軟正黑體", 10)  # 字體名稱和字號
        app.setFont(font)
        window = MoneyTrackerPlusView()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(traceback.format_exc())
