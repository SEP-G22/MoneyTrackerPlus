from pathlib import Path
import json

account_books_data = [
    {
        "name": "Testcase3-05",
        "type": 0,
        "transactions": [
            {
                "id": 285142223652219421607238170766438268629,
                "amount": 10.0,
                "date": "2025-03-21T22:19:15",
                "description": "ten",
                "category": {
                    "category": "Allowance",
                    "type": "Income"
                }
            },
            {
                "id": 21860610457676909012547688061474047727,
                "amount": 1000.0,
                "date": "2025-04-21T22:19:41",
                "description": "road",
                "category": {
                    "category": "Bonus",
                    "type": "Income"
                }
            },
            {
                "id": 262733770491834535318218666749957434201,
                "amount": 22000.0,
                "date": "2025-05-21T22:20:01",
                "description": "w",
                "category": {
                    "category": "Allowance",
                    "type": "Income"
                }
            }
        ]
    }
]

config_data = {
    "cred_path": "",
    "db_url": "",
    "default_account_book": "Testcase3-05"
}

dist_path = Path("src/dist")
#dist_path.mkdir(parents=True, exist_ok=True)

account_books_file = dist_path / "local_account_books.json"
with account_books_file.open("w", encoding="utf-8") as f:
    json.dump(account_books_data, f, indent=4, ensure_ascii=False)

config_file = dist_path / "config.json"
with config_file.open("w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=4, ensure_ascii=False)
