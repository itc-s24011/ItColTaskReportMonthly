from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func, extract
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False     

# 環境変数でデータベースを切り替え可能
# デフォルトはSQLite、USE_POSTGRESQL=1でPostgreSQLを使用
USE_POSTGRESQL = os.environ.get('USE_POSTGRESQL') == '1'

if USE_POSTGRESQL:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todo_user:todo_password@localhost/todo_db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

# タスクモデル
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)  # プロジェクト名
    category = db.Column(db.String(50), nullable=False)  # カテゴリ（開発、会議、メール、調査、その他）
    memo = db.Column(db.String(500))  # メモ
    created_date = db.Column(db.Date, nullable=False, default=datetime.now().date)  # 作成日
    start_time = db.Column(db.DateTime)  # 開始時刻
    end_time = db.Column(db.DateTime)  # 終了時刻
    duration_seconds = db.Column(db.Integer, default=0)  # 作業時間（秒）
    is_running = db.Column(db.Boolean, default=False)  # タイマー実行中フラグ


# ホーム画面（タスク登録・実行画面）
@app.route("/")
def home():
    today = datetime.now().date()
    
    # 今日のタスク一覧を取得
    tasks = Task.query.filter_by(created_date=today).order_by(Task.id.desc()).all()
    
    # 今日の総作業時間を計算（時間単位）
    total_seconds = db.session.query(func.sum(Task.duration_seconds)).filter_by(created_date=today).scalar() or 0
    total_hours = round(total_seconds / 3600, 1)
    
    # 実行中のタスクがあるか確認
    running_task = Task.query.filter_by(is_running=True).first()
    
    # データベース情報
    db_info = None
    if USE_POSTGRESQL:
        db_info = {
            'type': 'PostgreSQL',
            'database': 'todo_db',
            'user': 'todo_user',
            'host': 'localhost'
        }
    
    return render_template("index.html", 
                         tasks=tasks, 
                         today=today,
                         total_hours=total_hours,
                         running_task=running_task,
                         db_info=db_info)


# タスク追加
@app.route("/add_task", methods=["POST"])
def add_task():
    task_name = request.form.get("task_name")
    category = request.form.get("category")
    memo = request.form.get("memo", "")
    
    if task_name and category:
        new_task = Task(
            task_name=task_name,
            category=category,
            memo=memo,
            created_date=datetime.now().date()
        )
        db.session.add(new_task)
        db.session.commit()
    
    return redirect(url_for("home"))


# タイマー開始
@app.route("/start_timer/<int:task_id>", methods=["POST"])
def start_timer(task_id):
    # 既に実行中のタスクがあれば停止
    running_task = Task.query.filter_by(is_running=True).first()
    if running_task:
        running_task.is_running = False
        if running_task.start_time and not running_task.end_time:
            running_task.end_time = datetime.now()
            duration = (running_task.end_time - running_task.start_time).total_seconds()
            running_task.duration_seconds += int(duration)
    
    # 新しいタスクを開始
    task = Task.query.get(task_id)
    if task:
        task.start_time = datetime.now()
        task.end_time = None
        task.is_running = True
        db.session.commit()
    
    return redirect(url_for("home"))


# タイマー停止
@app.route("/stop_timer/<int:task_id>", methods=["POST"])
def stop_timer(task_id):
    task = Task.query.get(task_id)
    if task and task.is_running:
        task.end_time = datetime.now()
        task.is_running = False
        if task.start_time:
            duration = (task.end_time - task.start_time).total_seconds()
            task.duration_seconds += int(duration)
        db.session.commit()
    
    return redirect(url_for("home"))


# タスク削除
@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    
    return redirect(url_for("home"))


# タスク編集
@app.route("/edit_task/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.task_name = request.form.get("task_name", task.task_name)
        task.category = request.form.get("category", task.category)
        task.memo = request.form.get("memo", task.memo)
        db.session.commit()
    
    return redirect(url_for("home"))


# 月次レポート画面
@app.route("/report")
def report():
    # クエリパラメータから年月を取得（デフォルトは今月）
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    view_type = request.args.get('view', 'project')  # project または category
    
    # 指定月の開始日と終了日
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date()
    else:
        end_date = datetime(year, month + 1, 1).date()
    
    # 月次集計
    tasks = Task.query.filter(
        Task.created_date >= start_date,
        Task.created_date < end_date
    ).all()
    
    # 総作業時間（時間単位）
    total_seconds = sum(task.duration_seconds for task in tasks)
    total_hours = round(total_seconds / 3600, 1)
    
    # 総作業日数（ユニークな日付の数）
    unique_dates = set(task.created_date for task in tasks)
    total_days = len(unique_dates)
    
    # プロジェクト別またはカテゴリ別集計
    if view_type == 'category':
        # カテゴリ別集計
        aggregation = db.session.query(
            Task.category.label('name'),
            func.sum(Task.duration_seconds).label('total_seconds')
        ).filter(
            Task.created_date >= start_date,
            Task.created_date < end_date
        ).group_by(Task.category).all()
    else:
        # プロジェクト別集計
        aggregation = db.session.query(
            Task.task_name.label('name'),
            func.sum(Task.duration_seconds).label('total_seconds')
        ).filter(
            Task.created_date >= start_date,
            Task.created_date < end_date
        ).group_by(Task.task_name).all()
    
    # 集計結果を整形（作業時間の降順）
    summary_list = []
    for item in aggregation:
        hours = round(item.total_seconds / 3600, 1)
        percentage = round((item.total_seconds / total_seconds * 100), 1) if total_seconds > 0 else 0
        summary_list.append({
            'name': item.name,
            'hours': hours,
            'percentage': percentage
        })
    
    # 作業時間で降順ソート
    summary_list.sort(key=lambda x: x['hours'], reverse=True)
    
    # 年月の選択肢を生成（過去12ヶ月）
    month_options = []
    for i in range(12):
        date = datetime.now() - timedelta(days=30 * i)
        month_options.append({
            'year': date.year,
            'month': date.month,
            'label': f"{date.year}年{date.month}月"
        })
    
    return render_template("report.html",
                         year=year,
                         month=month,
                         view_type=view_type,
                         total_hours=total_hours,
                         total_days=total_days,
                         summary_list=summary_list,
                         month_options=month_options)


# API: 実行中のタスクの経過時間を取得
@app.route("/api/timer_status")
def timer_status():
    running_task = Task.query.filter_by(is_running=True).first()
    if running_task and running_task.start_time:
        elapsed_seconds = int((datetime.now() - running_task.start_time).total_seconds())
        return jsonify({
            'task_id': running_task.id,
            'elapsed_seconds': elapsed_seconds,
            'is_running': True
        })
    return jsonify({'is_running': False})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
