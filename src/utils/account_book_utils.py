# This file contains utility functions for account books
# Implemented by 陳衍廷

from models import *
from services import *


def get_local_books():
    """
    Retrieve account books from the local JSON file.

    :return: List of local account books.
    :rtype: List[AccountBook]
    """
    try:
        service = DataService('local_account_books.json')
        return service.read_account_books()
    except Exception as e:
        print(e)
        return []


def get_account_book(name: str) -> AccountBook:
    """
    Retrieve an account book by name from local and cloud sources.

    :param name: The name of the account book to retrieve.
    :type name: str
    :return: The account book with the specified name, or None if not found.
    :rtype: AccountBook
    """
    try:
        local_books = get_local_books()
        for book in local_books:
            if book.name == name:
                return book
        return None
    except Exception as e:
        print(e)
        return None
