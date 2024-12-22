# src/models/transaction.py

from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass


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
            'type': self.type
        }


@dataclass
class TransactionCategory:
    """
    Class representing a transaction category.
    """

    name: str
    type: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction category to a dictionary format.

        :return: Dictionary representation of the transaction category.
        :rtype: Dict[str, Any]
        """
        return {
            'name': self.name,
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
        # TODO: Implement this method
