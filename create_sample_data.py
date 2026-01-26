#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サンプルデータ投入スクリプト
テスト用のタスクデータを作成します
"""

from app import app, db, Task
from datetime import datetime, timedelta
import random

# カテゴリリスト
CATEGORIES = ['開発', '会議', 'メール', '調査', 'その他']

# プロジェクト名のサンプル
PROJECT_NAMES = [
    'ウェブサイト改修プロジェクト',
    'モバイルアプリ開発',
    'データベース最適化',
    '顧客対応',
    '新機能開発',
    'バグ修正',
    'ドキュメント作成',
    'コードレビュー',
    'システム保守',
    'ミーティング準備'
]

# メモのサンプル
MEMOS = [
    'フロントエンド実装を完了',
    'チームミーティングに参加',
    '顧客からの問い合わせ対応',
    '技術調査とドキュメント作成',
    'コードのリファクタリング',
    'テストケースの作成',
    'デプロイ準備',
    'パフォーマンス改善',
    'セキュリティ対策の実装',
    'API設計の見直し'
]

def create_sample_data():
    """サンプルデータを作成"""
    
    with app.app_context():
        # 既存のデータを削除
        Task.query.delete()
        db.session.commit()
        
        print("=" * 60)
        print("サンプルデータの作成を開始します")
        print("=" * 60)
        
        # 過去30日分のデータを作成
        base_date = datetime.now().date()
        
        for days_ago in range(30, -1, -1):
            current_date = base_date - timedelta(days=days_ago)
            
            # 1日あたり2〜5個のタスクをランダムに作成
            num_tasks = random.randint(2, 5)
            
            for _ in range(num_tasks):
                project_name = random.choice(PROJECT_NAMES)
                category = random.choice(CATEGORIES)
                memo = random.choice(MEMOS)
                
                # ランダムな作業時間（30分〜4時間）
                duration_seconds = random.randint(1800, 14400)
                
                # タスクを作成
                task = Task(
                    task_name=project_name,
                    category=category,
                    memo=memo,
                    created_date=current_date,
                    duration_seconds=duration_seconds,
                    is_running=False
                )
                
                db.session.add(task)
            
            # 日付ごとにコミット
            db.session.commit()
            
            total_hours = Task.query.filter_by(created_date=current_date).with_entities(
                db.func.sum(Task.duration_seconds)
            ).scalar() or 0
            total_hours = round(total_hours / 3600, 1)
            
            print(f"✓ {current_date}: {num_tasks}件のタスク（合計 {total_hours}h）")
        
        # 統計情報を表示
        print("\n" + "=" * 60)
        print("サンプルデータの作成が完了しました！")
        print("=" * 60)
        
        total_tasks = Task.query.count()
        total_seconds = db.session.query(db.func.sum(Task.duration_seconds)).scalar() or 0
        total_hours = round(total_seconds / 3600, 1)
        
        print(f"\n📊 統計情報:")
        print(f"  - 総タスク数: {total_tasks}件")
        print(f"  - 総作業時間: {total_hours}時間")
        print(f"  - 期間: 過去31日間")
        
        # カテゴリ別の集計
        print(f"\n📂 カテゴリ別集計:")
        for category in CATEGORIES:
            cat_tasks = Task.query.filter_by(category=category).count()
            cat_seconds = db.session.query(db.func.sum(Task.duration_seconds)).filter(
                Task.category == category
            ).scalar() or 0
            cat_hours = round(cat_seconds / 3600, 1)
            print(f"  - {category}: {cat_tasks}件 ({cat_hours}h)")
        
        print("\n" + "=" * 60)
        print("ブラウザで http://127.0.0.1:5000 にアクセスして確認してください")
        print("=" * 60)

if __name__ == "__main__":
    create_sample_data()
