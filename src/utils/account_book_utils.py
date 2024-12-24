from models import *
from services import *


def get_local_books():
    try:
        service = DataService('local_account_books.json')
        return service.read_account_books()
    except Exception as e:
        print(e)
        return []


def get_cloud_books():
    try:
        service = CloudSyncService(ConfigService().get_cred_path(), ConfigService().get_db_url())
        return service.download_account_books()
    except Exception as e:
        print(e)
        return []


def get_account_book(name: str) -> AccountBook:
    try:
        local_books = get_local_books()
        cloud_books = get_cloud_books()
        for book in local_books + cloud_books:
            if book.name == name:
                return book
        return None
    except Exception as e:
        print(e)
        return None
