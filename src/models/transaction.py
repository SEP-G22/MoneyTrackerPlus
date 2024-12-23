# src/models/transaction.py

from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass


class Transaction:
    """
    Class representing a single transaction record.
    """

    def __init__(self, id: int, amount: float, date: datetime, description: str, type: str, category: 'TransactionCategory'):

        """
        Initialize a Transaction instance.

        :param id: The unique identifier of the transaction.
        :type id: int
        :param amount: The amount of the transaction.
        :type amount: float
        :param date: The date of the transaction.
        :type date: datetime
        :param description: The description of the transaction.
        :type description: str
        :param type: The type of the transaction(Income/Expense).
        :type type: str
        :param category: The category of the transaction.
        :type category: TransactionCategory
        """
        self.id = id
        self.amount = amount
        self.date = date
        self.description = description
        self.type = type
        self.category = category

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary format.

        :return: Dictionary representation of the transaction.
        :rtype: Dict[str, Any]
        """
        return {
            'id': self.id,
            'amount': self.amount,
            'date': self.date.isoformat(),
            'description': self.description,
            'type': self.type,
            'category': self.category.category
        }


class TransactionCategory:
    """
    Class representing a transaction category.
    """
    
    def __init__(self, category="", type=""):
        """ default_categories = {
            "Allowance": "Income",
            "Bonus": "Income",
            "Clothes": "Expense",
            "Education": "Expense",
            "Entertainment": "Expense",
            "Food & Drinks": "Expense",
            "Housing & Utilities": "Expense",
            "Personal": "Expense",
            "Salary": "Income",
            "Transportation": "Expense"
        } """
        self.category = category
        self.type = type

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction category to a dictionary format.

        :return: Dictionary representation of the transaction category.
        :rtype: Dict[str, Any]
        """
        return {
            'category': self.category,
            'type': self.type
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'TransactionCategory':
        """
        Create a TransactionCategory instance from a JSON dictionary.

        :param data: JSON dictionary representing a transaction category.
        :type data: Dict[str, Any]
        :return: TransactionCategory instance.
        :rtype: TransactionCategory
        """
        return cls(category=data['category'], type=data['type'])
    
    @staticmethod
    def predefined_categories() -> Dict[str, 'TransactionCategory']:
        """
        Return a dictionary of predefined categories.

        :return: Dictionary of predefined transaction categories.
        :rtype: Dict[str, TransactionCategory]
        """
        return {
            "Allowance": TransactionCategory(category="Allowance", type="Income"),
            "Bonus": TransactionCategory(category="Bonus", type="Income"),
            "Clothes": TransactionCategory(category="Clothes", type="Expense"),
            "Education": TransactionCategory(category="Education", type="Expense"),
            "Entertainment": TransactionCategory(category="Entertainment", type="Expense"),
            "Food & Drinks": TransactionCategory(category="Food & Drinks", type="Expense"),
            "Housing & Utilities": TransactionCategory(category="Housing & Utilities", type="Expense"),
            "Personal": TransactionCategory(category="Personal", type="Expense"),
            "Salary": TransactionCategory(category="Salary", type="Income"),
            "Transportation": TransactionCategory(category="Transportation", type="Expense"),
        }
        
    def getIconPath(self) -> str:
        """
        Return the path to the icon image file for the transaction category.

        :return: Path to the icon image file.
        :rtype: str
        """
        return f"./images/{self.category}.png"


if __name__ == "__main__":
    # Example usage
    category = TransactionCategory(category="Food & Drinks", type="Expense")
    transaction = Transaction(
        id=1,
        amount=50.0,
        date=datetime.now(),
        description="Dinner at a restaurant",
        type = "Expense",
        category=category
    )

    print(transaction.to_dict())
