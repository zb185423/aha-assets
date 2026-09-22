# AHA

## ディレクトリ構成

 assets
│   ├── free
│   │   ├── 001
│   │   │   ├── aft.jpg
│   │   │   ├── ans.jpg
│   │   │   └── bef.jpg
│   │   ├── 002
│   │   │   ├── aft.jpg
│   │   │   ├── ans.jpg
│   │   │   └── bef.jpg
│   │   └── 003
│   │       ├── aft.jpg
│   │       ├── ans.jpg
│   │       └── bef.jpg
│   └── premium
│       ├── 001
│       │   ├── 001
│       │   │   ├── aft.jpg
│       │   │   ├── ans.jpg
│       │   │   └── bef.jpg
│       │   ├── 002
│       │   │   ├── aft.jpg
│       │   │   ├── ans.jpg
│       │   │   └── bef.jpg
│       │   ├── 003
│       │   │   ├── aft.jpg
│       │   │   ├── ans.jpg
│       │   │   └── bef.jpg
│       │   ├── 004
│       │   │   ├── aft.jpg
│       │   │   ├── ans.jpg
│       │   │   └── bef.jpg
│       │   └── 005
│       │   │   ├── aft.jpg
│       │   │   ├── ans.jpg
│       │   │   └── bef.jpg
│       └── 002
│           ├── 001
│           │   ├── aft.jpg
│           │   ├── ans.jpg
│           │   └── bef.jpg
│           ├── 002
│           │   ├── aft.jpg
│           │   ├── ans.jpg
│           │   └── bef.jpg
│           ├── 003
│           │   ├── aft.jpg
│           │   ├── ans.jpg
│           │   └── bef.jpg
│           ├── 004
│           │   ├── aft.jpg
│           │   ├── ans.jpg
│           │   └── bef.jpg
│           └── 005
│               ├── aft.jpg
│               ├── ans.jpg
│               └── bef.jpg
└── questions.json

- premium直下はアプリ内課金アイテム単位でディレクトリを切っています（5問ずつ）


## questions.json の仕様

ベースURLは、`https://zb185423.github.io/aha-assets/`

```json
[
  {
    "id": "free_001",
    "title": {"ja": "", "en": "", "zh-Hans": ""},
    "base_url": "https://zb185423.github.io/aha-assets/assets/free/001/bef.jpg",
    "changed_url": "https://zb185423.github.io/aha-assets/assets/free/001/aft.jpg",
    "answer_url": "https://zb185423.github.io/aha-assets/assets/free/001/ans.jpg",
    "difficulty": 1,
    "change_points_number": 1,
    "is_premium": false,
    "size": [
      1254,
      1254
    ],
    "regions": [
      {
        "x0": 328,
        "y0": 160,
        "x1": 1056,
        "y1": 488
      }
    ],
    "updated_at": "2026-09-15T20:54:59+09:00"
  },
  {
    "id": "premium_001_001",
    "title": {"ja": "", "en": "", "zh-Hans": ""},
    "base_url": "https://zb185423.github.io/aha-assets/assets/premium/001/001/q001_bef.jpg",
    "changed_url": "https://zb185423.github.io/aha-assets/assets/premium/001/001/q001_aft.jpg",
    "answer_url": "https://zb185423.github.io/aha-assets/assets/premium/001/001/q001_ans.jpg",
    "difficulty": 1,
    "change_points_number": 1,
    "is_premium": true,
    "size": [
      1254,
      1254
    ],
    "regions": [
      {
        "x0": 328,
        "y0": 160,
        "x1": 1056,
        "y1": 488
      }
    ],
    "updated_at": "2026-09-15T20:54:59+09:00",
    "premium_id": "001"
  }
]
```

### フィールド説明

- id (String): 問題を一意に識別するためのID。階層構造のディレクトリ名をアンダースコアで連結して生成（例: free_001, premium_001_001）。

- title (Object): 一覧画面に出す問題のタイトル。言語コードをキーにした文字列（ja / en / zh-Hans）。例: `{"ja": "気球びより", "en": "Balloon Weather", "zh-Hans": "热气球的天空"}`

- base_url (String): 変更前の画像（bef）の配信URL。

- changed_url (String): 変化後の画像（aft）の配信URL。

- answer_url (String): 正解表示用の画像（ans）の配信URL。

- difficulty (Int): 問題の難易度(1~5)。

- change_points_number (Int): 画像内で変化する箇所の総数。

- is_premium (Bool): 課金コンテンツ（プレミアム問題）かどうかを示すフラグ（true / false）。

- size (List): 画像の解像度（ピクセル単位）。[横幅 (width), 縦幅 (height)] の形式。

- regions (List): 画像内で変化する領域（正解判定エリア）の座標オブジェクト配列。

    - x0: 変化領域の左端座標（ピクセル）

    - y0: 変化領域の上端座標（ピクセル）

    - x1: 変化領域の右端座標（ピクセル）

    - y1: 変化領域の下端座標（ピクセル）

- updated_at (String): 問題データの最終更新日時（ISO 8601形式・JST +09:00）。アプリ側のキャッシュ同期・差分取得用。

- premium_id (String ※オプショナル): is_premium が true の場合のみ付与される、所属する課金パックの識別ID（premium/ 直下のディレクトリ名）。