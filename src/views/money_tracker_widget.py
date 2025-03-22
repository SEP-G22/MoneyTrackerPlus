# This ia a abstract class that is used to define the interface of the money tracker widget
from PyQt5.QtWidgets import QWidget


class MoneyTrackerWidget(QWidget):

    @classmethod
    def getIconPath(cls):
        pass

    @classmethod
    def getName(cls):
        pass
