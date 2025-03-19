# MoneyTrackerPlus
Final project for course: Software Engineering Practice

### Project Structure
```text
MoneyTrackerPlus/
├── src/
│   ├── models/
│   │   ├── transaction.py
│   │   └── account_book.py
│   │
│   ├── views/
│   │   ├── main_window.py
│   │   ├── transaction_edit_view.py
│   │   ├── transaction_list_view.py
│   │   ├── chart_view.py
│   │   ├── settings_view.py
│   │   └── money_tracker_widget.py
│   │
│   ├── services/
│   │   ├── data_service.py
│   │   ├── config_service.py
│   │   └── cloud_sync_service.py
│   │
│   ├── utils/
│   │   ├── chart_generator.py
│   │   ├── get_categories.py
│   │   └── account_book_utils.py
│   │
│   ├── test.py
│   └── main.py
│
├── requirements.txt
└── README.md
```

### 主要功能/頁面
- 新增/編輯：右側顯示新增介面，包含選取日期、類別、金額、備註
- 瀏覽與查詢：右側顯示所有紀錄或篩選過的紀錄，點擊紀錄會跳至新增/編輯
- 分析：右側顯示分析結果
- 帳本設定：右側顯示帳本的設定，包含顯示目前帳本、刪除帳本、共享設定
