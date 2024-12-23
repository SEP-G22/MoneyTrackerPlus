# src/services/cloud_sync_service.py

import firebase_admin
from firebase_admin import credentials, db, _apps
from typing import List, Dict, Any

from models import *


class CloudSyncService:
    """
    This is a Service class that is responsible for syncing account books with Firebase Realtime Database.
    """
    def __init__(self, cred_path: str, db_url: str) -> None:
        """
        Initialize Firebase app with credentials and database URL.

        :param cred_path: Path to the Firebase credentials JSON file.
        :type cred_path: str
        :param db_url: URL of the Firebase Realtime Database.
        :type db_url: str
        """
        if not _apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {'databaseURL': db_url})
        self.db_ref = db.reference()

    def upload_account_book(self, account_book: AccountBook) -> None:
        """
        Upload an account book to Firebase Realtime Database.

        :param account_book: The account book to upload.
        :type account_book: AccountBook
        """
        account_book_ref = self.db_ref.child('account_books').child(account_book.name)
        account_book_ref.set(account_book.to_dict())

    def download_account_books(self) -> List[AccountBook]:
        """
        Download all account books from Firebase Realtime Database.

        :return: List of account books.
        :rtype: List[AccountBook]
        """
        account_books_data = self.db_ref.child('account_books').get()
        if not account_books_data:
            return []
        return [self._dict_to_account_book(data) for data in account_books_data.values()]

    def _dict_to_account_book(self, data: Dict[str, Any]) -> AccountBook:
        """
        Convert a dictionary to an AccountBook instance.

        :param data: Dictionary representation of an account book.
        :type data: Dict[str, Any]
        :return: AccountBook instance.
        :rtype: AccountBook
        """
        return AccountBook.from_json(data)

