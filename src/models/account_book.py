# src/models/account_book.py

from typing import List, Dict, Any
from .transaction import Transaction


class AccountBook:
    """
    Class representing an account book which contains multiple transactions.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize an AccountBook instance.

        :param name: The name of the account book.
        :type name: str
        """
        self.name = name
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a transaction to the account book.

        :param transaction: The transaction to add.
        :type transaction: Transaction
        """
        self.transactions.append(transaction)

    def get_transactions(self) -> List[Transaction]:
        """
        Get all transactions in the account book.

        :return: List of transactions.
        :rtype: List[Transaction]
        """
        return self.transactions

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the account book to a dictionary format.

        :return: Dictionary representation of the account book.
        :rtype: Dict[str, Any]
        """
        return {
            'name': self.name,
            'transactions': [transaction.to_dict() for transaction in self.transactions]
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'AccountBook':
        """
        Create an AccountBook instance from a JSON dictionary.

        :param data: JSON dictionary representing an account book.
        :type data: Dict[str, Any]
        :return: AccountBook instance.
        :rtype: AccountBook
        """
        account_book = cls(data['name'])
        for transaction_data in data['transactions']:
            transaction = Transaction.from_json(transaction_data)
            account_book.add_transaction(transaction)
        return account_book
