import pytest
from PyQt5.QtWidgets import QComboBox
from unittest.mock import MagicMock
from views.chart_view import ChartView


@pytest.fixture
def setup_chart_view(qtbot):
    def _setup(default_value, items):
        view = ChartView()
        view.accountbook_combo = QComboBox()
        view.accountbook_combo.addItems(items)
        view.accountbook_combo.setCurrentIndex(0)
        mock_config = MagicMock()
        mock_config.get_default_account_book.return_value = default_value
        view.config_service = mock_config
        return view
    return _setup


def test_valid_default_book_found(setup_chart_view):
    # GIVEN 預設帳本是 "帳本 A"，且 comboBox 有該項目
    view = setup_chart_view("帳本 A", ["帳本 A", "帳本 B"])

    # WHEN 執行設定預設帳本的函式
    view.set_default_account_book()

    # THEN comboBox 應選中 "帳本 A"
    assert view.accountbook_combo.currentText() == "帳本 A"
    assert view.accountbook_combo.currentIndex() == 0


def test_book_not_found(setup_chart_view):
    view = setup_chart_view("帳本 X", ["帳本 B", "帳本 C"])
    view.set_default_account_book()
    assert view.accountbook_combo.currentText() == "帳本 B"
    assert view.accountbook_combo.currentIndex() == 0


def test_empty_default(setup_chart_view):
    view = setup_chart_view("", ["帳本 B", "帳本 C"])
    view.set_default_account_book()
    assert view.accountbook_combo.currentText() == "帳本 B"
    assert view.accountbook_combo.currentIndex() == 0


def test_default_none(setup_chart_view):
    view = setup_chart_view(None, ["帳本 B", "帳本 C"])
    view.set_default_account_book()
    assert view.accountbook_combo.currentText() == "帳本 B"
    assert view.accountbook_combo.currentIndex() == 0
