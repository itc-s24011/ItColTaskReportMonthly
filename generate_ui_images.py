#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI参考画像生成スクリプト
外部設計書で使用するUI画像を生成します。
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 画像保存先ディレクトリ
OUTPUT_DIR = "docs/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 共通設定
MOBILE_WIDTH = 375
BG_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#4A90C2"
SECONDARY_COLOR = "#2C5F8D"
TEXT_COLOR = "#333333"
LIGHT_GRAY = "#F5F5F5"
BORDER_COLOR = "#DDDDDD"
GREEN_COLOR = "#4CAF50"
RED_COLOR = "#FF5252"


def get_font(size):
    """フォントを取得（日本語対応）"""
    try:
        # Linux環境の日本語フォント候補
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ]
        for font_path in font_paths:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        return ImageFont.load_default()
    except:
        return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill):
    """角丸の長方形を描画"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def generate_task_entry_screen():
    """タスク登録・実行画面を生成"""
    height = 700
    img = Image.new('RGB', (MOBILE_WIDTH, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(24)
    font_medium = get_font(16)
    font_small = get_font(14)
    
    y_pos = 20
    
    # ヘッダー
    draw.rectangle([0, 0, MOBILE_WIDTH, 60], fill=PRIMARY_COLOR)
    draw.text((MOBILE_WIDTH // 2, 30), "Task Tracker", fill="white", 
              font=font_large, anchor="mm")
    
    y_pos = 80
    
    # 日付表示
    draw.text((20, y_pos), "2020年4月5日 (日)", fill=TEXT_COLOR, font=font_medium)
    y_pos += 30
    
    # 当日の作業時間
    draw.text((20, y_pos), "当日の作業時間: 0.0h", fill=SECONDARY_COLOR, 
              font=font_medium)
    y_pos += 50
    
    # プロジェクト名入力フィールド
    draw.text((20, y_pos), "プロジェクト名", fill=TEXT_COLOR, font=font_small)
    y_pos += 25
    draw_rounded_rect(draw, [20, y_pos, MOBILE_WIDTH - 20, y_pos + 40], 
                      radius=5, fill=LIGHT_GRAY)
    draw.text((30, y_pos + 20), "プロジェクト名を入力", fill="#999999", 
              font=font_small, anchor="lm")
    y_pos += 55
    
    # タグ（カテゴリ）選択
    draw.text((20, y_pos), "カテゴリ", fill=TEXT_COLOR, font=font_small)
    y_pos += 25
    
    # タグボタン
    tags = ["開発", "会議", "メール", "調査", "その他"]
    tag_x = 20
    for tag in tags:
        tag_width = 65
        draw_rounded_rect(draw, [tag_x, y_pos, tag_x + tag_width, y_pos + 30],
                         radius=5, fill=LIGHT_GRAY)
        draw.text((tag_x + tag_width // 2, y_pos + 15), tag, fill=TEXT_COLOR,
                 font=font_small, anchor="mm")
        tag_x += tag_width + 8
    
    y_pos += 50
    
    # メモ入力エリア
    draw.text((20, y_pos), "メモ", fill=TEXT_COLOR, font=font_small)
    y_pos += 25
    draw_rounded_rect(draw, [20, y_pos, MOBILE_WIDTH - 20, y_pos + 80],
                      radius=5, fill=LIGHT_GRAY)
    draw.text((30, y_pos + 10), "作業内容のメモを入力", fill="#999999",
              font=font_small)
    y_pos += 100
    
    # STARTボタン（大きな円形ボタン）
    button_center_x = MOBILE_WIDTH // 2
    button_center_y = y_pos + 60
    button_radius = 50
    
    # ボタンの円
    draw.ellipse([button_center_x - button_radius, button_center_y - button_radius,
                  button_center_x + button_radius, button_center_y + button_radius],
                 fill=GREEN_COLOR)
    
    # STARTテキスト
    draw.text((button_center_x, button_center_y), "START", fill="white",
              font=font_large, anchor="mm")
    
    y_pos += 140
    
    # タスク一覧（サンプル）
    draw.text((20, y_pos), "今日のタスク", fill=TEXT_COLOR, font=font_medium)
    y_pos += 30
    
    # タスク項目（サンプル1つ）
    task_height = 60
    draw_rounded_rect(draw, [20, y_pos, MOBILE_WIDTH - 20, y_pos + task_height],
                      radius=5, fill=LIGHT_GRAY)
    draw.text((30, y_pos + 15), "サンプルプロジェクト", fill=TEXT_COLOR, font=font_small)
    draw.text((30, y_pos + 35), "会議 | 1.5h", fill="#666666", font=font_small)
    
    # 編集・削除ボタン
    draw_rounded_rect(draw, [MOBILE_WIDTH - 110, y_pos + 10, MOBILE_WIDTH - 70, y_pos + 35],
                      radius=3, fill=PRIMARY_COLOR)
    draw.text((MOBILE_WIDTH - 90, y_pos + 22), "編集", fill="white", font=font_small, anchor="mm")
    
    draw_rounded_rect(draw, [MOBILE_WIDTH - 60, y_pos + 10, MOBILE_WIDTH - 30, y_pos + 35],
                      radius=3, fill=RED_COLOR)
    draw.text((MOBILE_WIDTH - 45, y_pos + 22), "削除", fill="white", font=font_small, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "ui_task_entry.png")
    img.save(output_path)
    print(f"✓ 生成完了: {output_path}")
    return output_path


def generate_monthly_report_screen():
    """月次集計・レポート画面を生成"""
    height = 700
    img = Image.new('RGB', (MOBILE_WIDTH, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(24)
    font_medium = get_font(16)
    font_small = get_font(14)
    font_tiny = get_font(12)
    
    y_pos = 20
    
    # ヘッダー
    draw.rectangle([0, 0, MOBILE_WIDTH, 60], fill=PRIMARY_COLOR)
    draw.text((MOBILE_WIDTH // 2, 30), "Monthly Report", fill="white",
              font=font_large, anchor="mm")
    
    y_pos = 80
    
    # 年月選択
    draw.text((20, y_pos), "2020年 1月", fill=TEXT_COLOR, font=font_large)
    y_pos += 40
    
    # 総日数・総時間表示
    summary_box_height = 60
    draw_rounded_rect(draw, [20, y_pos, MOBILE_WIDTH - 20, y_pos + summary_box_height],
                      radius=8, fill=PRIMARY_COLOR)
    
    draw.text((MOBILE_WIDTH // 2, y_pos + 20), "31 DAYS / 132.0 HOURS",
              fill="white", font=font_medium, anchor="mm")
    draw.text((MOBILE_WIDTH // 2, y_pos + 40), "月間総作業時間",
              fill="white", font=font_small, anchor="mm")
    
    y_pos += summary_box_height + 30
    
    # プロジェクト別一覧
    draw.text((20, y_pos), "プロジェクト別", fill=TEXT_COLOR, font=font_medium)
    y_pos += 30
    
    # プロジェクト項目データ
    projects = [
        ("Project Alpha", 21.8, 16.5),
        ("Project Beta", 18.5, 14.0),
        ("Project Gamma", 15.2, 11.5),
        ("Internal Meeting", 12.0, 9.1),
        ("Email Response", 8.5, 6.4),
        ("Other Tasks", 56.0, 42.4),
    ]
    
    item_height = 50
    for project_name, hours, percentage in projects:
        # 背景
        draw_rounded_rect(draw, [20, y_pos, MOBILE_WIDTH - 20, y_pos + item_height],
                         radius=5, fill=LIGHT_GRAY)
        
        # プロジェクト名
        draw.text((30, y_pos + 12), project_name, fill=TEXT_COLOR, font=font_small)
        
        # 時間と割合
        draw.text((30, y_pos + 32), f"{hours}h ({percentage}%)",
                 fill="#666666", font=font_tiny)
        
        # 横棒グラフ
        bar_width = int((MOBILE_WIDTH - 160) * (percentage / 100))
        bar_y = y_pos + 15
        draw_rounded_rect(draw, [MOBILE_WIDTH - 140, bar_y, MOBILE_WIDTH - 140 + bar_width, bar_y + 20],
                         radius=3, fill=GREEN_COLOR)
        
        y_pos += item_height + 10
    
    # 下部タブ（簡略版）
    tab_y = height - 60
    draw.rectangle([0, tab_y, MOBILE_WIDTH, height], fill=LIGHT_GRAY)
    
    tabs = ["Calendar", "Projects", "Tags", "Settings"]
    tab_width = MOBILE_WIDTH // len(tabs)
    
    for i, tab_name in enumerate(tabs):
        tab_x = i * tab_width
        # Projectsタブをアクティブに
        if tab_name == "Projects":
            draw.rectangle([tab_x, tab_y, tab_x + tab_width, height], fill=PRIMARY_COLOR)
            text_color = "white"
        else:
            text_color = "#666666"
        
        draw.text((tab_x + tab_width // 2, tab_y + 30), tab_name,
                 fill=text_color, font=font_tiny, anchor="mm")
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, "ui_monthly_report.png")
    img.save(output_path)
    print(f"✓ 生成完了: {output_path}")
    return output_path


def main():
    """メイン実行"""
    print("=" * 50)
    print("UI参考画像の生成を開始します")
    print("=" * 50)
    
    # タスク登録画面を生成
    print("\n1. タスク登録・実行画面を生成中...")
    task_entry_path = generate_task_entry_screen()
    
    # 月次レポート画面を生成
    print("\n2. 月次集計・レポート画面を生成中...")
    monthly_report_path = generate_monthly_report_screen()
    
    print("\n" + "=" * 50)
    print("✓ すべての画像生成が完了しました！")
    print("=" * 50)
    print(f"\n生成された画像:")
    print(f"  - {task_entry_path}")
    print(f"  - {monthly_report_path}")
    print("\n次のコマンドで外部設計書を確認できます:")
    print("  firefox docs/external_design.html")
    print("=" * 50)


if __name__ == "__main__":
    main()
