# src/models/transaction.py

from typing import Dict, Any
from datetime import datetime


class Transaction:
    """
    Class representing a single transaction record.
    """

    def __init__(self, id: int, amount: float, date: datetime, description: str) -> None:
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
            'description': self.description
        }
