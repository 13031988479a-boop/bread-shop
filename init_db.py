import sqlite3

conn = sqlite3.connect('bread_shop.db')
cursor = conn.cursor()

# 创建产品表
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT,
    is_hot INTEGER DEFAULT 0,
    is_new INTEGER DEFAULT 0,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 插入一些示例数据
sample_products = [
    ("招牌可颂", "外酥内软，黄油香气浓郁，每日现烤", 18.0, "面包", 1, 0, None),
    ("生吐司", "绵密柔软，奶香十足，切片即食", 28.0, "面包", 1, 1, None),
    ("红丝绒蛋糕", "经典红丝绒，奶油芝士霜，口感细腻", 38.0, "蛋糕", 0, 1, None),
    ("肉桂卷", "美式经典，肉桂香气，淋上乳酪糖霜", 22.0, "面包", 0, 0, None),
    ("冰拿铁", "现萃咖啡+鲜奶，冰爽顺滑", 25.0, "饮品", 0, 0, None),
]

cursor.executemany('''
INSERT OR IGNORE INTO products (name, description, price, category, is_hot, is_new, image_url)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', sample_products)

conn.commit()
conn.close()

print("数据库初始化完成！")
print("示例数据已添加。")