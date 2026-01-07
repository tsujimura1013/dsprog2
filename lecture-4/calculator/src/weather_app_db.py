import flet as ft
import requests
import sqlite3
from datetime import datetime

AREA_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"

DB_NAME = "weather.db"


# -------------- DB 初期化 -----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS forecasts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area_code TEXT,
        date TEXT,
        weather TEXT,
        tmin TEXT,
        tmax TEXT
    )
    """)

    conn.commit()
    conn.close()


# -------------- DB 保存 -----------------
def save_forecast(area_code, date, weather, tmin, tmax):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO forecasts(area_code, date, weather, tmin, tmax) VALUES (?, ?, ?, ?, ?)",
        (area_code, date, weather, tmin, tmax)
    )
    conn.commit()
    conn.close()


# -------------- DB 読み込み -----------------
def load_forecast(area_code):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT date, weather, tmin, tmax FROM forecasts WHERE area_code=? ORDER BY date",
        (area_code,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# -------------- API 取得 -----------------
def fetch_and_store_weather(area_code):
    url = FORECAST_URL.format(area_code)
    data = requests.get(url).json()

    time_series = data[0]["timeSeries"]

    # 日付
    dates = time_series[0]["timeDefines"]

    # 天気
    weathers = time_series[0]["areas"][0]["weathers"]

    # 温度（初期値）
    tmin = []
    tmax = []

    # 気温データがある場合のみ取得
    if len(time_series) >= 3:
        temps = time_series[2]["areas"][0]
        tmin = temps.get("tempsMin", [])
        tmax = temps.get("tempsMax", [])

    # ---- DB保存 ----
    for i in range(len(dates)):
        date = dates[i][:10]
        weather = weathers[i]
        min_t = tmin[i] if i < len(tmin) else "-"
        max_t = tmax[i] if i < len(tmax) else "-"

        save_forecast(area_code, date, weather, min_t, max_t)



# -------------- Flet アプリ -----------------
def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.window_width = 1000
    page.window_height = 700

    init_db()

    # UI パーツ
    forecast_cards = ft.Row(wrap=True, spacing=10)

    def show_forecast(area_code):
        # APIから取得 → DBに保存
        fetch_and_store_weather(area_code)

        # DBから読み込み
        rows = load_forecast(area_code)

        forecast_cards.controls.clear()

        for date, weather, tmin, tmax in rows:
            card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column(
                        [
                            ft.Text(date, weight="bold"),
                            ft.Text(weather),
                            ft.Text(f"{tmin}℃  /  {tmax}℃"),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                width=150,
            )
            forecast_cards.controls.append(card)

        page.update()

    # 地域一覧ロード
    areas = requests.get(AREA_URL).json()["offices"]

    list_view = ft.ListView(expand=True)

    for code, info in areas.items():
        name = info["name"]

        def tap_closure(c=code):
            def on_click(e):
                show_forecast(c)
            return on_click

        list_view.controls.append(
            ft.ListTile(title=ft.Text(f"{name}  ({code})"), on_click=tap_closure())
        )

    page.add(
        ft.Row(
            [
                ft.Container(width=250, content=list_view),
                ft.VerticalDivider(),
                ft.Container(expand=True, content=forecast_cards),
            ],
            expand=True,
        )
    )


ft.app(target=main)
