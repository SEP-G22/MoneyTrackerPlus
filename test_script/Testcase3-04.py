from pathlib import Path
import json
from datetime import datetime

current_time = datetime.now().isoformat(timespec='seconds')
print(current_time)
account_books_data = [
    {
        "name": "Testcase3-04",
        "type": 0,
        "transactions": [
            {
                "id": 58085545537370935411690696787300281898,
                "amount": 99.0,
                "date": f"{current_time}",
                "description": "lagend fight eat gold",
                "category": {
                    "category": "Entertainment",
                    "type": "Expense"
                }
            }
        ]
    }
]

config_data = {
    "cred_path": "",
    "db_url": "",
    "default_account_book": "Testcase3-04"
}

dist_path = Path("src/dist")
#dist_path.mkdir(parents=True, exist_ok=True)

account_books_file = dist_path / "local_account_books.json"
with account_books_file.open("w", encoding="utf-8") as f:
    json.dump(account_books_data, f, indent=4, ensure_ascii=False)

config_file = dist_path / "config.json"
with config_file.open("w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=4, ensure_ascii=False)
