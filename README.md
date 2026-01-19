# ItCol 月次作業報告ツール

プロジェクト作業時間を計測・集計し、月次レポートを作成する Web アプリケーション

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)]()

## 📋 目次

- [概要](#概要)
- [主な機能](#主な機能)
- [システム構成](#システム構成)
- [セットアップ](#セットアップ)
- [使い方](#使い方)
- [データベース構造](#データベース構造)
- [技術スタック](#技術スタック)

## 🎯 概要

IT 業務における作業実績を日々記録し、月次で集計・報告するための Web アプリケーションです。タスク単位での作業時間の正確な計測と、プロジェクト・カテゴリ別の自動集計により、効率的な作業報告を実現します。

### アプリケーションフロー

```mermaid
graph TD
    A[ユーザー] -->|タスク登録| B[タスク登録画面]
    B -->|START| C[タイマー開始]
    C -->|作業中| D[時間計測]
    D -->|STOP| E[作業時間記録]
    E -->|データ保存| F[(データベース)]
    F -->|集計| G[月次レポート画面]
    G -->|表示| H[プロジェクト別集計]
    G -->|表示| I[カテゴリ別集計]
    H -->|印刷| J[A4レポート出力]
    I -->|印刷| J
```

### ユースケース図

```mermaid
graph LR
    User((ユーザー))

    User -->|登録| UC1[タスク登録]
    User -->|計測| UC2[作業時間計測]
    User -->|編集| UC3[タスク編集]
    User -->|削除| UC4[タスク削除]
    User -->|閲覧| UC5[月次レポート表示]
    User -->|出力| UC6[レポート印刷]

    UC1 -.->|含む| UC1A[プロジェクト名入力]
    UC1 -.->|含む| UC1B[カテゴリ選択]
    UC1 -.->|含む| UC1C[メモ入力]

    UC2 -.->|含む| UC2A[タイマーSTART]
    UC2 -.->|含む| UC2B[タイマーSTOP]
    UC2 -.->|含む| UC2C[経過時間表示]

    UC5 -.->|含む| UC5A[期間選択]
    UC5 -.->|含む| UC5B[プロジェクト別表示]
    UC5 -.->|含む| UC5C[カテゴリ別表示]
```

## ✨ 主な機能

### M-1. タスク登録フォーム ✅

```mermaid
flowchart LR
    A[入力フォーム] --> B{入力検証}
    B -->|OK| C[データベース保存]
    B -->|NG| D[エラー表示]
    C --> E[タスク一覧更新]

    style A fill:#e1f5ff
    style C fill:#c8e6c9
    style D fill:#ffcdd2
```

- **プロジェクト名**: 必須入力、最大 100 文字
- **カテゴリ選択**: プルダウン（開発、会議、メール、調査、その他）
- **メモ**: 任意入力、最大 500 文字

### M-2. タイマー機能 ✅

```mermaid
stateDiagram-v2
    [*] --> 待機中
    待機中 --> 実行中: START
    実行中 --> 待機中: STOP
    実行中 --> 実行中: 時間更新(1秒ごと)
    待機中 --> [*]: タスク削除

    note right of 実行中
        経過時間をリアルタイム表示
        hh:mm:ss形式
    end note
```

- **START/STOP ボタン**: 作業時間の計測開始・停止
- **経過時間表示**: リアルタイムで時間表示（hh:mm:ss 形式）
- **データ記録**: 開始時刻、終了時刻、作業時間（秒単位）を DB に保存

### M-3. 月次集計機能 ✅

```mermaid
graph TD
    A[期間選択] --> B[年月指定]
    B --> C{データ取得}
    C -->|SQL集計| D[総作業時間計算]
    C -->|SQL集計| E[総作業日数計算]
    C -->|GROUP BY| F[プロジェクト別集計]
    C -->|GROUP BY| G[カテゴリ別集計]

    D --> H[結果表示]
    E --> H
    F --> H
    G --> H

    style C fill:#fff9c4
    style H fill:#c8e6c9
```

- **集計期間選択**: 年月をプルダウンで選択
- **総作業時間表示**: 選択月の総作業時間（h 単位、小数点 1 桁）
- **総作業日数表示**: 選択月の実働日数

### M-4/M-5. プロジェクト別・カテゴリ別一覧 ✅

| 項目       | 説明                                           |
| ---------- | ---------------------------------------------- |
| 表示項目   | プロジェクト名/カテゴリ名、作業時間、割合（%） |
| ソート     | 作業時間の降順                                 |
| レイアウト | A4 縦印刷対応テーブル                          |

### M-6. 印刷対応（CSS） ✅

- `@media print` を使用した印刷専用 CSS
- A4 縦サイズでページ内に収まるレイアウト
- 不要要素（ボタン、ナビゲーション）を自動非表示

## 🏗️ システム構成

### システムアーキテクチャ

```mermaid
graph TB
    subgraph クライアント
        A[Webブラウザ]
        B[HTML/CSS/JavaScript]
    end

    subgraph Webサーバー
        C[Flask 3.1.2]
        D[ルーティング]
        E[テンプレートエンジン]
    end

    subgraph データ層
        F[SQLAlchemy ORM]
        G[(SQLite)]
        H[(PostgreSQL)]
    end

    A --> B
    B -->|HTTP Request| C
    C --> D
    D --> E
    E --> F
    F -->|開発環境| G
    F -->|本番環境| H
    E -->|HTTP Response| B

    style A fill:#e3f2fd
    style C fill:#fff3e0
    style G fill:#f3e5f5
    style H fill:#e8f5e9
```

### ディレクトリ構造

```mermaid
graph TD
    A[ItColTaskReportMonthly/] --> B[app.py]
    A --> C[requirements.txt]
    A --> D[venv/]
    A --> E[instance/]
    A --> F[static/]
    A --> G[templates/]
    A --> H[docs/]

    E --> E1[db.sqlite]
    F --> F1[style.css]
    G --> G1[index.html]
    G --> G2[report.html]
    H --> H1[external_design.html]
    H --> H2[images/]

    style A fill:#bbdefb
    style B fill:#c8e6c9
    style F fill:#fff9c4
    style G fill:#ffccbc
```

## 🚀 セットアップ

### 前提条件

- Python 3.8 以上
- pip
- (オプション) PostgreSQL 12 以上

### インストール手順

```mermaid
sequenceDiagram
    participant U as ユーザー
    participant T as ターミナル
    participant P as Python
    participant D as データベース

    U->>T: リポジトリクローン
    T->>T: 仮想環境作成
    U->>T: 仮想環境有効化
    T->>P: パッケージインストール
    U->>T: アプリ起動
    T->>P: Flaskサーバー起動
    P->>D: データベース初期化
    D-->>P: 接続確認
    P-->>U: http://127.0.0.1:5000
```

### 1. リポジトリのクローン

```bash
git clone https://github.com/itc-s24011/ItColTaskReportMonthly.git
cd ItColTaskReportMonthly/ItColTaskReportMonthly/ItColTaskReportMonthly
```

### 2. 仮想環境のセットアップ

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. アプリケーションの起動

```bash
# SQLiteを使用（デフォルト）
python3 app.py

# PostgreSQLを使用
export USE_POSTGRESQL=1  # Linux/Mac
# または
set USE_POSTGRESQL=1     # Windows
python3 app.py
```

### 5. ブラウザでアクセス

```
http://127.0.0.1:5000
```

## 📖 使い方

### タスク登録から報告までの流れ

```mermaid
journey
    title 作業報告の1日の流れ
    section 朝
      タスク登録: 5: ユーザー
      タイマーSTART: 5: ユーザー
    section 日中
      作業実施: 5: ユーザー
      タイマーSTOP: 5: ユーザー
      次のタスクSTART: 5: ユーザー
    section 夕方
      最後のタスクSTOP: 5: ユーザー
      当日の作業確認: 4: ユーザー
    section 月末
      月次レポート表示: 5: ユーザー
      レポート印刷: 5: ユーザー
```

### タスク登録・実行画面

1. **新規タスク登録**

   - プロジェクト名を入力
   - カテゴリを選択（開発、会議、メール、調査、その他）
   - メモを入力（任意）
   - 「タスクを追加」ボタンをクリック

2. **タイマーの操作**

   - **START**: タスクの作業時間計測を開始
   - **STOP**: 作業時間計測を停止
   - 経過時間はリアルタイムで更新されます

3. **タスクの編集・削除**
   - **編集**: タスク情報を変更
   - **削除**: タスクを削除（確認ダイアログが表示されます）

### 月次レポート画面

1. **期間選択**

   - 年と月をプルダウンから選択
   - 自動的に集計結果が更新されます

2. **表示切替**

   - **プロジェクト別**: プロジェクトごとの作業時間を表示
   - **カテゴリ別**: カテゴリごとの作業時間を表示

3. **印刷**
   - 「印刷」ボタンをクリック
   - A4 縦サイズで印刷プレビューが表示されます

## 🗄️ データベース構造

### ERD（Entity Relationship Diagram）

```mermaid
erDiagram
    TASK {
        INTEGER id PK "主キー（自動採番）"
        VARCHAR task_name "プロジェクト名（最大100文字）"
        VARCHAR category "カテゴリ（最大50文字）"
        VARCHAR memo "メモ（最大500文字）"
        DATE created_date "作成日"
        DATETIME start_time "開始時刻"
        DATETIME end_time "終了時刻"
        INTEGER duration_seconds "作業時間（秒）"
        BOOLEAN is_running "タイマー実行中フラグ"
    }
```

### カテゴリマスタ

```mermaid
pie title カテゴリ分類
    "開発" : 40
    "会議" : 25
    "メール" : 15
    "調査" : 15
    "その他" : 5
```

### Task テーブル詳細

| カラム名         | 型           | NULL | 説明                 |
| ---------------- | ------------ | ---- | -------------------- |
| id               | INTEGER      | NO   | 主キー（自動採番）   |
| task_name        | VARCHAR(100) | NO   | プロジェクト名       |
| category         | VARCHAR(50)  | NO   | カテゴリ             |
| memo             | VARCHAR(500) | YES  | メモ                 |
| created_date     | DATE         | NO   | 作成日               |
| start_time       | DATETIME     | YES  | 開始時刻             |
| end_time         | DATETIME     | YES  | 終了時刻             |
| duration_seconds | INTEGER      | YES  | 作業時間（秒単位）   |
| is_running       | BOOLEAN      | NO   | タイマー実行中フラグ |

## 🔧 技術スタック

```mermaid
graph LR
    subgraph フロントエンド
        A[HTML5]
        B[CSS3]
        C[JavaScript]
    end

    subgraph バックエンド
        D[Python 3.8+]
        E[Flask 3.1.2]
        F[SQLAlchemy]
    end

    subgraph データベース
        G[SQLite]
        H[PostgreSQL]
    end

    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    F --> H

    style E fill:#90caf9
    style F fill:#a5d6a7
    style G fill:#ce93d8
    style H fill:#81c784
```

### 使用技術一覧

| カテゴリ           | 技術                    | バージョン |
| ------------------ | ----------------------- | ---------- |
| 言語               | Python                  | 3.8+       |
| Web フレームワーク | Flask                   | 3.1.2      |
| ORM                | SQLAlchemy              | 2.0+       |
| データベース       | SQLite / PostgreSQL     | -          |
| フロントエンド     | HTML5, CSS3, JavaScript | -          |
| その他             | psycopg2-binary         | 2.9+       |

## 🎨 デザイン特徴

### カラーパレット

```mermaid
graph LR
    A[開発<br/>青系] -->|#4A90E2| B[会議<br/>オレンジ系]
    B -->|#F5A623| C[メール<br/>緑系]
    C -->|#7ED321| D[調査<br/>紫系]
    D -->|#9013FE| E[その他<br/>グレー系]
    E -->|#6C757D| A

    style A fill:#4A90E2,color:#fff
    style B fill:#F5A623,color:#fff
    style C fill:#7ED321,color:#fff
    style D fill:#9013FE,color:#fff
    style E fill:#6C757D,color:#fff
```

- **モダンなグラデーション**: 紫系のグラデーション背景
- **レスポンシブデザイン**: モバイル・タブレット・デスクトップに対応
- **カテゴリカラー**: カテゴリごとに色分け
- **印刷最適化**: A4 縦サイズで綺麗に印刷可能

## 🐛 トラブルシューティング

### よくある問題と解決方法

```mermaid
graph TD
    A[問題発生] --> B{症状は?}
    B -->|起動しない| C[仮想環境確認]
    B -->|DB接続エラー| D[DB設定確認]
    B -->|ポート使用中| E[ポート変更]

    C --> C1[仮想環境再作成]
    C1 --> F[解決]

    D --> D1[接続情報確認]
    D1 --> F

    E --> E1[app.py修正]
    E1 --> F

    style A fill:#ffcdd2
    style F fill:#c8e6c9
```

### Flask が起動しない

```bash
# 仮想環境を再作成
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### データベースをリセットしたい

```bash
rm -f instance/db.sqlite
python3 app.py  # 再起動時に自動作成
```

### ポート 5000 が使用中

```python
# app.py の最後の行を変更
app.run(debug=True, port=5001)
```

## 📊 開発情報

### 開発体制

- **対象者**: IT 専門学生 6 名
- **開発期間**: 9 時間（1 日）
- **合計工数**: 54 人時間

### 開発の流れ

```mermaid
gantt
    title 開発スケジュール
    dateFormat HH:mm
    axisFormat %H:%M

    section 設計
    要件定義        :done, 09:00, 1h
    画面設計        :done, 10:00, 1h

    section 実装
    データベース    :done, 11:00, 2h
    バックエンド    :done, 13:00, 2h
    フロントエンド  :done, 15:00, 2h

    section テスト
    動作確認        :done, 17:00, 1h
```

## 📄 ライセンス

このプロジェクトは教育目的で作成されています。

## 🤝 コントリビューション

バグ報告や機能リクエストは、GitHub の Issues でお願いします。

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. [トラブルシューティング](#トラブルシューティング)
2. GitHub Issues
3. 開発チームへの連絡

---

**作成日**: 2025 年 12 月 15 日  
**最終更新**: 2026 年 1 月 19 日  
**バージョン**: 1.1.0  
**開発**: IT 専門学生 6 名による共同開発プロジェクト
