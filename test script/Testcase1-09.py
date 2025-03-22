from pathlib import Path
import json

account_books_data = [
    {
        "name": "Testcase1-09",
        "type": 0,
        "transactions": [
            {
                "id": 58085545537370935411690696787300281898,
                "amount": 99.0,
                "date": "2025-03-22T22:01:07",
                "description": "lagend fight eat gold",
                "category": {
                    "category": "Personal",
                    "type": "Expense"
                }
            }
        ]
    }
]

config_data = {
    "cred_path": "",
    "db_url": "",
    "default_account_book": "Testcase1-09"
}

dist_path = Path("src/dist")
#dist_path.mkdir(parents=True, exist_ok=True)

account_books_file = dist_path / "local_account_books.json"
with account_books_file.open("w", encoding="utf-8") as f:
    json.dump(account_books_data, f, indent=4, ensure_ascii=False)

config_file = dist_path / "config.json"
with config_file.open("w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=4, ensure_ascii=False)
