import requests
import pandas as pd

FINMIND_URL = "https://api.finmindtrade.com/api/v4/data"

def get_stock_data(stock_id: str, start_date: str, end_date: str, token: str):
    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
        "token": token
    }
    try:
        r = requests.get(FINMIND_URL, params=params, timeout=15)
        r.raise_for_status()
        js = r.json()
    except Exception as e:
        return pd.DataFrame(), f"API 請求失敗：{e}"

    if "data" not in js or not isinstance(js["data"], list) or len(js["data"]) == 0:
        return pd.DataFrame(), js.get("msg", "查無資料")

    df = pd.DataFrame(js["data"])
    if "close" not in df.columns or "date" not in df.columns:
        return pd.DataFrame(), f"回傳欄位缺失：{df.columns.tolist()}"

    df["date"] = pd.to_datetime(df["date"])
    df["Close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.sort_values("date").reset_index(drop=True)
    return df[["date", "Close"]], None