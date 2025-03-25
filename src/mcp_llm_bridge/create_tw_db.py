import sqlite3
import os
from datetime import datetime

def create_test_database(db_path: str = "test.db"):
    """建立包含測試商品的資料庫"""
    
    # 如果資料庫已存在，則刪除重新建立
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # 建立並連接資料庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 建立 products 商品資料表
    cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT,
        stock INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 測試商品資料（繁體中文＋新台幣）
    products = [
        ("專業筆電 Pro X", "高效能筆記型電腦，搭載 16GB 記憶體", 41599, "電子產品", 50),
        ("無線滑鼠", "人體工學設計無線滑鼠", 959, "電子產品", 200),
        ("咖啡機", "12杯裝可程式咖啡機", 2559, "家電", 30),
        ("跑鞋", "輕量化跑步鞋", 2879, "運動用品", 100),
        ("瑜珈墊", "防滑運動瑜珈墊", 799, "運動用品", 150),
        ("智慧手錶", "健身追蹤智慧手錶", 6399, "電子產品", 75),
        ("登山背包", "防潑水登山用背包", 1599, "戶外用品", 120),
        ("水壺", "保溫不鏽鋼水壺", 639, "戶外用品", 200),
        ("檯燈", "可調亮度 LED 檯燈", 1279, "居家用品", 80),
        ("藍牙喇叭", "可攜式無線藍牙喇叭", 2239, "電子產品", 60),
        ("花盆", "室內陶瓷花盆", 511, "居家用品", 100),
        ("辦公椅", "人體工學辦公椅", 6399, "家具", 25),
        ("筆記本", "硬殼橫線筆記本", 319, "文具", 300),
        ("畫具組", "壓克力顏料畫具組附刷具", 1119, "藝術用品", 45),
        ("耳機", "降噪耳罩式耳機", 5119, "電子產品", 40)
    ]
    
    # 插入商品資料
    cursor.executemany(
        "INSERT INTO products (title, description, price, category, stock) VALUES (?, ?, ?, ?, ?)",
        products
    )
    
    # 建立分類資料表
    cursor.execute("""
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    """)
    
    # 分類資料（繁體中文）
    categories = [
        ("電子產品", "電子設備與配件"),
        ("家電", "家庭電器用品"),
        ("運動用品", "運動與健身器材"),
        ("戶外用品", "戶外活動與登山裝備"),
        ("居家用品", "家居裝飾與配件"),
        ("家具", "家庭與辦公室家具"),
        ("文具", "書寫與辦公文具用品"),
        ("藝術用品", "藝術創作工具與材料")
    ]
    
    # 插入分類資料
    cursor.executemany(
        "INSERT INTO categories (name, description) VALUES (?, ?)",
        categories
    )
    
    # 提交並關閉連線
    conn.commit()
    conn.close()
    
    print(f"資料庫已成功建立於 {db_path}")
    print("已建立資料表：products, categories")
    print(f"已插入 {len(products)} 筆商品資料與 {len(categories)} 筆分類資料")

if __name__ == "__main__":
    create_test_database()
