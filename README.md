# ItCol 月次作業報告ツール

IT 業務における作業実績を日々記録し、月次で集計・報告するための Web アプリケーションです。

## プロジェクトの目的

このツールは以下を実現します：

- タスク単位での作業時間の正確な計測
- プロジェクト・カテゴリ別の自動集計
- 月次レポートのワンクリック生成
- A4 印刷対応の報告書作成

## プロジェクトの現状

### 現在の実装状況

**完了済み**

- PostgreSQL / SQLite データベース接続
- タスク管理機能（登録・編集・削除）
- タイマー機能（START/STOP、リアルタイム更新）
- 月次集計機能（プロジェクト別・カテゴリ別）
- レスポンシブデザイン
- A4 印刷対応 CSS
- Flask + SQLAlchemy による実装

### 開発体制

- **対象者**: IT 専門学生 6 名
- **開発期間**: 9 時間（1 日）
- **合計工数**: 54 人時間
- **技術スタック**: Python 3.x, Flask, PostgreSQL/SQLite, Vanilla JS

## クイックスタート

### 前提条件

```bash
# 必須
- Python 3.8以上
- pip

# オプション（本番環境）
- PostgreSQL 12以上
```

### セットアップ

**方法 1: SQLite で開始（推奨・初心者向け）**

```bash
# 1. リポジトリをクローン
git clone <repository-url>
cd ItColTaskReportMonthly/ItColTaskReportMonthly/ItColTaskReportMonthly

# 2. 仮想環境作成
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 依存関係インストール
pip install -r requirements.txt

# 4. アプリケーション起動
python app.py

# 5. ブラウザでアクセス
# http://127.0.0.1:5000
```

**方法 2: PostgreSQL を使用**

```bash
# PostgreSQL セットアップ
# Linux/Mac
./setup.sh

# Windows
.\setup_windows.ps1

# Docker
./setup_docker.sh

# 環境変数を設定して起動
USE_POSTGRESQL=1 python app.py
```

### サンプルデータ投入（オプション）

```bash
# 過去30日分のサンプルデータを自動生成
python create_sample_data.py
```

## 使い方

### 1. タスク登録と作業時間計測

1. **新規タスク作成**

   ```
   プロジェクト名: [例] ウェブサイト改修
   カテゴリ: 開発
   メモ: フロントエンド実装
   ```

2. **作業開始**

   - 「START」ボタンをクリック
   - タイマーが自動で開始
   - リアルタイムで経過時間表示

3. **作業終了**
   - 「STOP」ボタンをクリック
   - 作業時間が自動記録

### 2. 月次レポート確認

1. 「月次レポート」タブをクリック
2. 年月を選択
3. 「プロジェクト別」または「カテゴリ別」を選択
4. 印刷する場合は「印刷」ボタン

### 3. 便利な機能

- **編集**: タスク情報の修正
- **削除**: 不要なタスクの削除（確認あり）
- **当日の作業時間**: リアルタイム集計表示

## プロジェクト構成

```
ItColTaskReportMonthly/
├── app.py                    # メインアプリケーション
├── requirements.txt          # 依存パッケージ
├── README.md                 # このファイル
├── APP_README.md            # アプリケーション詳細ドキュメント
├── create_sample_data.py    # サンプルデータ生成スクリプト
├── generate_ui_images.py    # UI画像生成スクリプト
├── .gitignore               # Git除外設定
├── venv/                     # Python仮想環境
├── instance/
│   └── db.sqlite            # SQLiteデータベース
├── templates/
│   ├── index.html           # タスク登録画面
│   └── report.html          # 月次レポート画面
├── static/
│   └── style.css            # スタイルシート
├── docs/
│   ├── external_design.html  # 外部設計書
│   └── images/              # UI参考画像
└── setup scripts/           # 各種セットアップスクリプト
```

## ドキュメント

### 外部設計書

**場所**: `docs/external_design.html`

以下の情報が含まれます：

- システム概要と目的
- UI 画面と機能仕様（MUST / OPTION）
- データベース設計
- API 設計
- 工数見積もり
- 役割分担（6 名体制）

**閲覧方法**:

```bash
# ブラウザで開く
open docs/external_design.html        # Mac
xdg-open docs/external_design.html    # Linux
start docs/external_design.html       # Windows
```

### アプリケーションドキュメント

詳細な使用方法は `APP_README.md` を参照してください。

## 開発の進め方

### チーム分担（6 名想定）

| 担当 | 役割                               | 工数 |
| ---- | ---------------------------------- | ---- |
| A    | プロジェクトリーダー兼 API 開発    | 9h   |
| B    | データベース担当兼集計 API         | 9h   |
| C    | フロントエンド 1（タスク登録画面） | 9h   |
| D    | フロントエンド 2（レポート画面）   | 9h   |
| E    | テスト担当兼品質保証               | 9h   |
| F    | 技術検証・調査兼発表資料           | 9h   |

### タイムライン（9 時間）

| 時間      | フェーズ     | 内容                   |
| --------- | ------------ | ---------------------- |
| 0:00-1:00 | キックオフ   | 設計レビュー、環境構築 |
| 1:00-4:00 | 実装 1       | 並行開発開始           |
| 4:00-4:30 | 中間レビュー | 進捗確認、調整         |
| 4:30-7:00 | 実装 2       | 実装継続、統合         |
| 7:00-8:30 | テスト       | 統合テスト、修正       |
| 8:30-9:00 | 成果確認     | 最終確認、発表準備     |

## 技術スタック

| レイヤー       | 技術                    | バージョン |
| -------------- | ----------------------- | ---------- |
| バックエンド   | Flask                   | 3.1.2      |
| データベース   | PostgreSQL/SQLite       | 12+ / 3    |
| ORM            | SQLAlchemy              | 2.0+       |
| フロントエンド | HTML5, CSS3, Vanilla JS | -          |
| スタイル       | CSS Grid, Flexbox       | -          |

## 開発者向け情報

### API エンドポイント

```python
# タスク管理
GET  /                      # タスク登録画面
POST /add_task              # タスク追加
POST /start_timer/<id>      # タイマー開始
POST /stop_timer/<id>       # タイマー停止
POST /edit_task/<id>        # タスク編集
POST /delete_task/<id>      # タスク削除

# レポート
GET  /report                # 月次レポート画面
GET  /api/report/monthly    # 集計データ取得(JSON)
GET  /api/timer_status      # タイマー状態取得(JSON)
```

### データベースモデル

```python
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    memo = db.Column(db.String(500))
    created_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer, default=0)
    is_running = db.Column(db.Boolean, default=False)
```

### 環境変数

```bash
USE_POSTGRESQL=1           # PostgreSQL使用（デフォルト: SQLite）
FLASK_ENV=development      # 開発モード
```

## トラブルシューティング

### よくある問題

**1. ポート 5000 が使用中**

```python
# app.py 最終行を変更
app.run(debug=True, port=5001)
```

**2. データベースエラー**

```bash
# SQLiteをリセット
rm -f instance/db.sqlite
python app.py  # 再起動で自動作成
```

**3. 依存関係エラー**

```bash
# 仮想環境を再作成
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. タイマーが更新されない**

- ブラウザのコンソールでエラー確認
- `/api/timer_status` が正常に動作しているか確認
- ページを再読み込み

## パフォーマンス

- **ページ読み込み**: < 1 秒
- **タイマー更新**: 1 秒間隔
- **月次集計**: < 0.5 秒（1000 タスク以下）

## セキュリティ

- SQL インジェクション対策: SQLAlchemy ORM 使用
- XSS 対策: Jinja2 自動エスケープ
- CSRF 対策: 実装推奨（本番環境では必須）

## サポート

問題が発生した場合：

1. `APP_README.md` を確認
2. `docs/external_design.html` を確認
3. GitHub の Issues で報告

## ライセンス

このプロジェクトは教育目的で作成されています。

## 貢献

プルリクエストを歓迎します！

1. Fork
2. Feature branch 作成
3. Commit
4. Push
5. Pull Request 作成

---

**開発**: IT 専門学生チーム  
**作成日**: 2025 年 12 月 15 日  
**バージョン**: 1.0.0

**Good luck with your development! 🚀**
