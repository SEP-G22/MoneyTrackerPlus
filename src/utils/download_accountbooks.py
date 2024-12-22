from datetime import datetime
from models import *
from services import *
import os

class downloadAccountBooks:

    def setUp(self):
        self.cred_path = './Firebase_credit/test-f6464-firebase-adminsdk-7picu-ff49354980.json'
        self.db_url = 'https://test-f6464-default-rtdb.firebaseio.com/'
        self.cloud_service = CloudSyncService(self.cred_path, self.db_url)
        self.file_path = 'test_account_books.json'
        self.data_service = DataService(self.file_path)

        account_books = self.cloud_service.download_account_books()
        return account_books