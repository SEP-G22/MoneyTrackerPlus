from .money_tracker_widget import MoneyTrackerWidget


class SettingsView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def getIconPath(cls):
        return "./images/book-keeping.png"

    @classmethod
    def getName(cls):
        return "帳本設定"
