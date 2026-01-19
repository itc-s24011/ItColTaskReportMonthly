<div align="center">

# ItCol 月次作業報告システム

### エンタープライズグレードの時間追跡・レポートシステム

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-Educational-FFA500?style=for-the-badge)]()

</div>

---

## 目次

- [概要](#概要)
- [主要機能](#主要機能)
- [システムアーキテクチャ](#システムアーキテクチャ)
- [インストール](#インストール)
- [使用方法](#使用方法)
- [データベーススキーマ](#データベーススキーマ)
- [技術スタック](#技術スタック)
- [開発情報](#開発情報)

---

## 概要

> プロジェクトの作業時間を精密なタイミングとインテリジェントな分類で追跡、集計、レポートする包括的な Web アプリケーション

正確な時間追跡と楽な月次レポート作成を求める IT プロフェッショナルのために構築されました。このシステムは、リアルタイムのタスク監視、プロジェクトおよびカテゴリ別の自動集計、ステークホルダー向けのプロフェッショナルな A4 フォーマットレポートを提供します。

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

---

## 主要機能

### モジュール 1: タスク登録システム

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

**Key Specifications:**

- **Project Name**: Required field, max 100 characters
- **Category Selection**: Dropdown (Development, Meeting, Email, Research, Other)
- **Memo Field**: Optional, max 500 characters
- **Validation**: Real-time input validation with user feedback

### MODULE 2: Precision Timer System

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

**Key Specifications:**

- **START/STOP Controls**: Initiate and terminate time tracking with single-click precision
- **Live Display**: Real-time elapsed time in hh:mm:ss format with 1-second refresh
- **Data Persistence**: Automatic storage of start time, end time, and duration (in seconds)
- **State Management**: Maintains timer state across sessions

### MODULE 3: Monthly Aggregation Engine

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

**Key Specifications:**

- **Period Selection**: Year and month dropdown selectors with dynamic filtering
- **Total Hours Display**: Aggregate work hours (decimal format, 1 decimal place)
- **Working Days Count**: Total active working days in selected period
- **SQL Optimization**: Efficient GROUP BY and SUM queries for fast aggregation

### MODULE 4/5: Project & Category Analytics

| Feature             | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| **Display Metrics** | Project/Category name, work hours, percentage distribution |
| **Sorting**         | Descending order by work hours (highest priority first)    |
| **Layout**          | A4 portrait-optimized table with responsive design         |
| **Visualization**   | Horizontal bar charts for percentage representation        |

### MODULE 6: Print-Optimized CSS System

**Key Specifications:**

- `@media print` dedicated stylesheet for professional output
- A4 portrait layout with optimized margins and spacing
- Automatic removal of interactive elements (buttons, navigation)
- High-contrast color scheme for clear printed output

---

## システムアーキテクチャ

### アーキテクチャ概要

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

---

## インストール

### 前提条件

```bash
# 必須
Python 3.8+
pip (最新版)

# オプション（本番環境用）
PostgreSQL 12+
Docker (コンテナ化デプロイ用)
```

### インストールワークフロー

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

#### ステップ 1: リポジトリのクローン

```bash
git clone https://github.com/itc-s24011/ItColTaskReportMonthly.git
cd ItColTaskReportMonthly/ItColTaskReportMonthly/ItColTaskReportMonthly
```

#### ステップ 2: 仮想環境のセットアップ

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### ステップ 3: 依存関係のインストール

```bash
pip install -r requirements.txt
```

#### ステップ 4: アプリケーションの起動

```bash
# SQLiteを使用した開発モード（デフォルト）
python3 app.py

# PostgreSQLを使用した本番モード
export USE_POSTGRESQL=1  # Linux/Mac
set USE_POSTGRESQL=1     # Windows
python3 app.py
```

#### ステップ 5: アプリケーションへのアクセス

```
http://127.0.0.1:5000
```

---

## 使用方法

### 日次ワークフロー

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

### TASK REGISTRATION & EXECUTION

**1. Create New Task**

- Enter project name (required)
- Select category from dropdown (Development, Meeting, Email, Research, Other)
- Add optional memo (max 500 characters)
- Click "Add Task" button

**2. Timer Operations**

- **START**: Begin time tracking for selected task
- **STOP**: End time tracking and save duration
- **Live Updates**: Elapsed time refreshes every second

**3. Task Management**

- **Edit**: Modify task information in-place
- **Delete**: Remove task with confirmation dialog

### MONTHLY REPORT GENERATION

**1. Period Selection**

- Choose year and month from dropdowns
- Results update automatically on selection

**2. View Toggle**

- **Project View**: Aggregated hours by project
- **Category View**: Aggregated hours by category
- Switch between views with single click

**3. Report Export**

- Click "Print" button for print preview
- A4 portrait layout with professional formatting
- Save as PDF or print directly

---

## データベーススキーマ

### エンティティ関連図

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

### カテゴリ分布

```mermaid
pie title カテゴリ分類
    "開発" : 40
    "会議" : 25
    "メール" : 15
    "調査" : 15
    "その他" : 5
```

### TASK テーブル仕様

| カラム名         | 型           | NULL 許可 | 説明                       |
| ---------------- | ------------ | --------- | -------------------------- |
| id               | INTEGER      | NO        | 主キー（自動採番）         |
| task_name        | VARCHAR(100) | NO        | プロジェクト識別子         |
| category         | VARCHAR(50)  | NO        | タスクカテゴリ             |
| memo             | VARCHAR(500) | YES       | オプションメモ             |
| created_date     | DATE         | NO        | 作成タイムスタンプ         |
| start_time       | DATETIME     | YES       | タイマー開始タイムスタンプ |
| end_time         | DATETIME     | YES       | タイマー終了タイムスタンプ |
| duration_seconds | INTEGER      | YES       | 総継続時間（秒）           |
| is_running       | BOOLEAN      | NO        | タイマー稼働フラグ         |

---

## 技術スタック

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

### スタックコンポーネント

| レイヤー                 | 技術                         | バージョン |
| ------------------------ | ---------------------------- | ---------- |
| **言語**                 | Python                       | 3.8+       |
| **Web フレームワーク**   | Flask                        | 3.1.2      |
| **ORM**                  | SQLAlchemy                   | 2.0+       |
| **データベース**         | SQLite / PostgreSQL          | 12+        |
| **フロントエンド**       | HTML5, CSS3, JavaScript ES6+ | -          |
| **データベースドライバ** | psycopg2-binary              | 2.9+       |
| **セッション管理**       | Flask-SQLAlchemy             | 3.1+       |

---

## デザインシステム

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

**Design Principles:**

- **Modern Gradient System**: Purple-based gradient backgrounds for visual hierarchy
- **Fully Responsive**: Optimized layouts for mobile, tablet, and desktop viewports
- **Category Color Coding**: Distinct color scheme for instant category recognition
- **Print Optimization**: Professional A4 portrait layout with high-contrast printing

---

## トラブルシューティング

### よくある問題と解決策

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

**問題: Flask が起動しない**

```bash
# 仮想環境を再構築
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**問題: データベースの破損またはリセットが必要**

```bash
# 既存のデータベースを削除
rm -f instance/db.sqlite
python3 app.py  # 起動時に自動的に再作成
```

**問題: ポート 5000 が既に使用中**

```python
# app.pyを編集 - ポート番号を変更
app.run(debug=True, port=5001)
```

---

## 開発情報

### プロジェクトメトリクス

```
チームサイズ:   6名の開発者
期間:          9時間（1日スプリント）
総工数:        54人時
方法論:        ラピッドプロトタイピングを伴うアジャイル開発
```

### 開発タイムライン

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

---

## ライセンス

このプロジェクトは教育目的で作成されています。

## コントリビューション

バグ報告や機能リクエストは、GitHub Issues で歓迎します。

## サポート

サポートが必要な場合は、以下を参照してください:

1. [トラブルシューティングガイド](#トラブルシューティング)
2. [GitHub Issues](https://github.com/itc-s24011/ItColTaskReportMonthly/issues)
3. 開発チームへの連絡

---

<div align="center">

### プロジェクト情報

**作成日:** 2025 年 12 月 15 日  
**最終更新:** 2026 年 1 月 19 日  
**バージョン:** 1.1.0

**開発チーム:** IT 専門学生（6 名）

---

_精密に構築。プロフェッショナルのために設計。_

</div>
