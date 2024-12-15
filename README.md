# MoneyTrackerPlus
Final project for course: Programming and its Applications

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
│   │   └── settings_view.py
│   │
│   ├── services/
│   │   ├── data_service.py
│   │   └── cloud_sync_service.py
│   │
│   ├── utils/
│   │   ├── chart_generator.py
│   │   └── validators.py
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

### 使用說明
- Firebase 設定
  - 到 Google Firebase 註冊帳號並建立專案
  - 請在 Firebase 中設定建立 RealTime Database
  - 在 Firebase > 專案設定 > 服務帳戶 > Python > 產生私密金鑰 獲取金鑰檔案
  - 將金鑰檔案放置於專案`src/Firebase_credit/`中，並在需要使用的地方引入該金鑰檔案的路徑
  - 其他內容可以參考
    - [Python 串接 Firebase RealTime Database 存取資料](https://ithelp.ithome.com.tw/articles/10335735)
    - [如何透過 Firebase Realtime Database](https://vocus.cc/article/63df0b17fd897800013e8019)
