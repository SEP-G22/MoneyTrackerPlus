from .money_tracker_widget import MoneyTrackerWidget


class TransactionEditView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def getIconPath(cls):
        return ""

    @classmethod
    def getName(cls):
        return "新增/編輯"
