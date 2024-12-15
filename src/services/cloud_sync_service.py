# src/services/cloud_sync_service.py

import firebase_admin
from firebase_admin import credentials, firestore
from typing import List, Dict, Any
from datetime import datetime
from src.models.account_book import AccountBook
from src.models.transaction import Transaction


class CloudSyncService:
    def __init__(self, cred_path: str) -> None:
        """
        Initialize Firebase app with credentials.

        :param cred_path: Path to the Firebase credentials JSON file.
        :type cred_path: str
        """
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def upload_account_book(self, account_book: AccountBook) -> None:
        """
        Upload an account book to Firestore.

        :param account_book: The account book to upload.
        :type account_book: AccountBook
        """
        collection_ref = self.db.collection('account_books')
        doc_ref = collection_ref.document(account_book.name)
        doc_ref.set(account_book.to_dict())

    def download_account_books(self) -> List[AccountBook]:
        """
        Download all account books from Firestore.

        :return: List of account books.
        :rtype: List[AccountBook]
        """
        collection_ref = self.db.collection('account_books')
        docs = collection_ref.stream()
        return [self._dict_to_account_book(doc.to_dict()) for doc in docs]

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
