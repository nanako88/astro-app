import streamlit as st
from flatlib.chart import Chart
from flatlib import const
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import datetime

# -------------------------
# セッション状態の初期化
# -------------------------
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# -------------------------
# 惑星・星座 日本語マップ
# -------------------------
planet_jp = {
    "Sun": "太陽",
    "Moon": "月",
    "Mercury": "水星",
    "Venus": "金星",
    "Mars": "火星",
    "Jupiter": "木星",
    "Saturn": "土星"
}

sign_jp = {
    "Aries": "おひつじ座",
    "Taurus": "おうし座",
    "Gemini": "ふたご座",
    "Cancer": "かに座",
    "Leo": "しし座",
    "Virgo": "おとめ座",
    "Libra": "てんびん座",
    "Scorpio": "さそり座",
    "Sagittarius": "いて座",
    "Capricorn": "やぎ座",
    "Aquarius": "みずがめ座",
    "Pisces": "うお座"
}

st.title("あなたの7天体の星座")

# -------------------------
# 🌟 入力画面
# -------------------------
if not st.session_state.show_result:
    years = list(range(1900, datetime.now().year + 1))
    months = list(range(1, 13))
    days = list(range(1, 32))

    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.selectbox("年", years, index=years.index(1990))
    with col2:
        month = st.selectbox("月", months, index=0)
    with col3:
        day = st.selectbox("日", days, index=0)

    col4, col5 = st.columns(2)
    with col4:
        hour = st.selectbox("時", list(range(0, 24)), index=12)
    with col5:
        minute = st.selectbox("分", list(range(0, 60, 5)), index=0)

    time_str = f"{hour:02d}:{minute:02d}"

    country = st.selectbox("国", ["日本", "アメリカ", "イギリス"], index=0)
    pref = st.selectbox("都道府県", ["東京都", "大阪府", "北海道"], index=0)

    latitude = st.number_input("緯度（例: 35.6895）", format="%.6f", value=35.6895)
    longitude = st.number_input("経度（例: 139.6917）", format="%.6f", value=139.6917)

    if st.button("調べる"):
        st.write("✅ 調べるボタンが押された！")  # デバッグ表示

        try:
            _ = Datetime(f"{year:04d}/{month:02d}/{day:02d}", time_str, '+09:00')

            st.session_state.date_str = f"{year:04d}/{month:02d}/{day:02d}"
            st.session_state.time_str = time_str
            st.session_state.latitude = latitude
            st.session_state.longitude = longitude
            st.session_state.show_result = True

            st.rerun()

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# -------------------------
# 🌟 結果画面
# -------------------------
if st.session_state.show_result:
    try:
        dt = Datetime(st.session_state.date_str, st.session_state.time_str, '+09:00')
        pos = GeoPos(st.session_state.latitude, st.session_state.longitude)
        chart = Chart(dt, pos, IDs=const.LIST_SEVEN_PLANETS)

        st.subheader("7天体の星座")
        for planet in const.LIST_SEVEN_PLANETS:
            obj = chart.get(planet)
            planet_name = planet_jp.get(planet, planet)
            sign_name = sign_jp.get(obj.sign, obj.sign)
            st.write(f"{planet_name}：{sign_name}")

        if st.button("戻る"):
            st.session_state.show_result = False
            st.rerun()

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
