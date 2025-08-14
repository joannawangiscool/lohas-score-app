# app.py
import streamlit as st
from modules.data_fetcher import get_stock_data
from modules.data_processor import compute_lohas
from modules.visualizer import plot_lohas
from modules.sentiment import classify_sentiment
from datetime import date

st.set_page_config(page_title="樂活五線譜", layout="wide")
st.title("🎼 樂活五線譜 × 台股情緒分析")

# === 使用者輸入區 ===
with st.sidebar:
    st.header("🔧 分析參數")
    stock_id = st.text_input("股票代碼", "0056")
    start_date = st.date_input("開始日期", date(2022, 1, 1)).isoformat()
    end_date = st.date_input("結束日期", date.today()).isoformat()
    token = st.text_input("FinMind Token", type="password")
    run_analysis = st.button("開始分析")

# === 主區域顯示結果 ===
if run_analysis:
    with st.spinner("資料擷取中..."):
        df, err = get_stock_data(stock_id, start_date, end_date, token)
    if err:
        st.error(f"❌ 錯誤：{err}")
    else:
        out = compute_lohas(df)
        last_row = out.dropna().iloc[-1]
        senti = classify_sentiment(last_row)
        st.success(f"✅ 市場情緒：{senti}")
        fig = plot_lohas(out, title=f"{stock_id} 樂活五線譜", sentiment=senti)
        st.pyplot(fig)
