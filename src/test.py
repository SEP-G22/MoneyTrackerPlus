# test.py

import unittest
from datetime import datetime
from models import *
from services import *
import os


class TestServices(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment. Initialize the services and create test data.
        """
        self.cred_path = './Firebase_credit/moneytrackerplus-firebase-adminsdk-aqbar-5c9acd5080.json'
        self.db_url = 'https://moneytrackerplus-default-rtdb.firebaseio.com/:1000'
        self.cloud_service = CloudSyncService(self.cred_path, self.db_url)
        self.file_path = 'test_account_books.json'
        self.data_service = DataService(self.file_path)

        self.transaction = Transaction(
            id=1,
            amount=100.0,
            date=datetime.now(),
            description='Test transaction'
        )
        self.account_book = AccountBook(name='Test Account Book')
        self.account_book.add_transaction(self.transaction)

    def tearDown(self):
        """
        Clean up the test environment. Remove the test file if it exists.
        """
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_upload_and_download_account_book(self):
        """
        Test uploading and downloading account books with CloudSyncService.
        """
        self.cloud_service.upload_account_book(self.account_book)
        account_books = self.cloud_service.download_account_books()
        self.assertTrue(any(ab.name == self.account_book.name for ab in account_books))

    def test_write_and_read_account_books(self):
        """
        Test writing and reading account books with DataService.
        """
        self.data_service.write_account_books([self.account_book])
        account_books = self.data_service.read_account_books()
        self.assertTrue(any(ab.name == self.account_book.name for ab in account_books))


if __name__ == '__main__':
    # To run the unit tests, use the following command:
    # python -m unittest test.py
    unittest.main()
