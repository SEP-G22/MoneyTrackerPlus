from .money_tracker_widget import MoneyTrackerWidget


class ChartView(MoneyTrackerWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def getIconPath(cls):
        return "./images/requirements.png"

    @classmethod
    def getName(cls):
        return "圖表分析"
