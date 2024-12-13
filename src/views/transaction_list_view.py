from .money_tracker_widget import MoneyTrackerWidget


class TransactionListView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def getIconPath(cls):
        return ""

    @classmethod
    def getName(cls):
        return "瀏覽與查詢"
