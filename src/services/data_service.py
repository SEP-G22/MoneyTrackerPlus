# src/services/data_service.py

import json
import os
from typing import List, Dict, Any
from datetime import datetime
from models import *


class DataService:
    """
    This is a Service class that is responsible for reading and writing account books to a local JSON file.
    """
    def __init__(self, file_path: str) -> None:
        """
        Initialize the DataService with the path to the JSON file.

        :param file_path: Path to the JSON file where data is stored.
        :type file_path: str
        """
        self.file_path = file_path

    def read_account_books(self) -> List[AccountBook]:
        """
        Read account books from the JSON file.

        :return: List of account books.
        :rtype: List[AccountBook]
        """
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [self._dict_to_account_book(item) for item in data]

    def write_account_books(self, account_books: List[AccountBook]) -> None:
        """
        Write account books to the JSON file.

        :param account_books: List of account books to write.
        :type account_books: List[AccountBook]
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump([account_book.to_dict() for account_book in account_books], file, ensure_ascii=False, indent=4)

    def _dict_to_account_book(self, data: Dict[str, Any]) -> AccountBook:
        """
        Convert a dictionary to an AccountBook instance.

        :param data: Dictionary representation of an account book.
        :type data: Dict[str, Any]
        :return: AccountBook instance.
        :rtype: AccountBook
        """
        account_book = AccountBook(data['name'])
        for transaction_data in data['transactions']:
            transaction = Transaction(
                id=transaction_data['id'],
                amount=transaction_data['amount'],
                date=datetime.fromisoformat(transaction_data['date']),
                description=transaction_data['description']
            )
            account_book.add_transaction(transaction)
        return account_book
