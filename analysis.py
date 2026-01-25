import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# DB接続
conn = sqlite3.connect("homes.db")

# データ取得
df = pd.read_sql("""
SELECT rent, station_walk
FROM properties
WHERE station_walk IS NOT NULL
""", conn)

conn.close()

print(df.head())

# 可視化
plt.scatter(df["station_walk"], df["rent"])
plt.xlabel("駅徒歩分数（分）")
plt.ylabel("家賃（円）")
plt.title("駅徒歩分数と家賃の関係")
plt.show()
