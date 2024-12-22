from datetime import datetime
from models import *
from services import *
import os

class addNewTransaction:
    def setUp(self, accountbook: AccountBook, date, amount, description):
        self.cred_path = './Firebase_credit/moneytrackerplus-firebase-adminsdk-aqbar-de7e7069eb.json'
        self.db_url = 'https://moneytrackerplus-default-rtdb.firebaseio.com/'
        self.cloud_service = CloudSyncService(self.cred_path, self.db_url)
        self.file_path = 'test_account_books.json'
        self.data_service = DataService(self.file_path)

        transaction = Transaction(
            id=1,
            amount=amount,
            date=date,
            description=description
        )
        accountbook.add_transaction(transaction)
        return accountbook