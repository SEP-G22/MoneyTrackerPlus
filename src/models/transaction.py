# src/models/transaction.py

from typing import Dict, Any
from datetime import datetime


class Transaction:
    """
    Class representing a single transaction record.
    """

    def __init__(self, id: int, amount: float, date: datetime, description: str, category: 'TransactionCategory'):

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
        :param category: The category of the transaction.
        :type category: TransactionCategory
        """
        self.id = id
        self.amount = amount
        self.date = date
        self.description = description
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
            'category': self.category.to_dict()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Transaction':
        """
        Create a Transaction instance from a JSON dictionary.

        :param data: JSON dictionary representing a transaction.
        :type data: Dict[str, Any]
        :return: Transaction instance.
        :rtype: Transaction
        """
        return cls(
            id=data['id'],
            amount=data['amount'],
            date=datetime.fromisoformat(data['date']),
            description=data['description'],
            category=TransactionCategory.from_json(data['category'])
        )


class TransactionCategory:
    """
    Class representing a transaction category.
    """
    
    def __init__(self, category: str, type: str):
        self.category = category
        self.type = type

    def to_dict(self) -> Dict[str, str]:
        """
        Convert the transaction category to a dictionary format.

        :return: Dictionary representation of the transaction category.
        :rtype: Dict[str, str]
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
