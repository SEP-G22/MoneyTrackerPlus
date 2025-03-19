# This file contains the implementation of the CloudSyncService class.
# Implemented by 李崑銘

import firebase_admin
from firebase_admin import credentials, db, _apps
from typing import List, Dict, Any

from models import AccountBook


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
        if cred_path == '' or db_url == '':
            self.db_ref = None
            return
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
        if not self.db_ref:
            return
        account_book_ref = self.db_ref.child('account_books').child(account_book.name)
        if account_book_ref.get() is None:
            # Account book does not exist, create a new one
            account_book_ref.set(account_book.to_dict())
        else:
            # Account book exists, update it with the current logic
            account_book_ref.update(account_book.to_dict())

    def upload_account_books(self, account_books: List[AccountBook]) -> None:
        """
        Upload multiple account books to Firebase Realtime Database.

        :param account_books: List of account books to upload.
        :type account_books: List[AccountBook]
        """
        if not self.db_ref:
            return
        for account_book in account_books:
            self.upload_account_book(account_book)

    def download_account_books(self) -> List[AccountBook]:
        """
        Download all account books from Firebase Realtime Database.

        :return: List of account books.
        :rtype: List[AccountBook]
        """
        if not self.db_ref:
            return []
        account_books_data = self.db_ref.child('account_books').get()
        if not account_books_data:
            return []
        return [self._dict_to_account_book(data) for data in account_books_data.values()]

    def delete_account_book(self, account_book_name: str) -> None:
        """
        Delete an account book from Firebase Realtime Database.

        :param account_book_name: The name of the account book to delete.
        :type account_book_name: str
        """
        if not self.db_ref:
            return
        account_book_ref = self.db_ref.child('account_books').child(account_book_name)
        account_book_ref.delete()

    def _dict_to_account_book(self, data: Dict[str, Any]) -> AccountBook:
        """
        Convert a dictionary to an AccountBook instance.

        :param data: Dictionary representation of an account book.
        :type data: Dict[str, Any]
        :return: AccountBook instance.
        :rtype: AccountBook
        """
        return AccountBook.from_json(data)
