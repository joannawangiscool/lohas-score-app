import streamlit as st
from datetime import date
from modules.data_fetcher import get_stock_data
from modules.data_processor import compute_lohas
from modules.visualizer import plot_lohas
from modules.sentiment import classify_sentiment

# 頁面設定：響應式寬版、標題與圖示
st.set_page_config(
    page_title="樂活五線譜",
    layout="wide",
    page_icon="🎼"
)

# 頁面標題
st.title("🎼 樂活五線譜 × 台股情緒分析")

# 側邊欄輸入區
with st.sidebar:
    st.header("🔧 分析參數設定")
    stock_id = st.text_input("股票代碼", "0056")
    start_date = st.date_input("開始日期", date(2022, 1, 1)).isoformat()
    end_date = st.date_input("結束日期", date.today()).isoformat()
    token = st.text_input("FinMind API Token", type="password").strip()
    long_win = st.slider("長期視窗（天）", 100, 300, 200, step=10)
    short_win = st.slider("短期視窗（天）", 10, 60, 20, step=1)
    run_analysis = st.button("📊 開始分析")

# 主區域：分析結果
if run_analysis:
    with st.spinner("🚀 正在擷取資料與分析中..."):
        df, err = get_stock_data(stock_id, start_date, end_date, token)

    if err:
        st.error(f"❌ 錯誤：{err}")
    elif df.empty:
        st.warning("⚠️ 查無資料，請確認代碼與日期範圍是否正確。")
    else:
        out = compute_lohas(df, long_win=long_win, short_win=short_win)
        last_row = out.dropna().iloc[-1]
        senti = classify_sentiment(last_row)

        st.success(f"✅ 市場情緒：**{senti}**")
        fig = plot_lohas(out, title=f"{stock_id} 樂活五線譜", sentiment=senti)
        st.pyplot(fig)

        with st.expander("📋 顯示原始資料"):
            st.dataframe(df, use_container_width=True)

        with st.expander("📘 分析說明"):
            st.markdown("""
            - **樂活五線譜**：以長期移動平均為中線，±1σ、±2σ 為上下區間。
            - **樂活通道**：以短期移動平均為中線，±1σ 為短期波動區。
            - **市場情緒判斷**：根據收盤價位置，判斷為極度樂觀、中性、極度悲觀等。
            """)