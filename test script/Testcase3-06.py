from pathlib import Path
import json

account_books_data = [
    {
        "name": "Testcase3-06",
        "type": 0,
        "transactions": [
            {
                "id": 220842473330780031395227172212478238739,
                "amount": 2999.0,
                "date": "2025-03-21T22:54:44",
                "description": "2999",
                "category": {
                    "category": "Clothes",
                    "type": "Expense"
                }
            },
            {
                "id": 333452111199274643746322684664798568347,
                "amount": 100.0,
                "date": "2025-04-21T22:55:14",
                "description": "w",
                "category": {
                    "category": "Entertainment",
                    "type": "Expense"
                }
            },
            {
                "id": 105798294001254808021989000130325256973,
                "amount": 200.0,
                "date": "2025-05-21T22:55:31",
                "description": "200",
                "category": {
                    "category": "Food & Drinks",
                    "type": "Expense"
                }
            }
        ]
    }
]

config_data = {
    "cred_path": "",
    "db_url": "",
    "default_account_book": "Testcase3-06"
}

dist_path = Path("src/dist")
#dist_path.mkdir(parents=True, exist_ok=True)

account_books_file = dist_path / "local_account_books.json"
with account_books_file.open("w", encoding="utf-8") as f:
    json.dump(account_books_data, f, indent=4, ensure_ascii=False)

config_file = dist_path / "config.json"
with config_file.open("w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=4, ensure_ascii=False)
