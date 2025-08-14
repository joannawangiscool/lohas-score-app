import pandas as pd
import numpy as np

def _ensure_price_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # 日期欄位標準化
    if "date" in out.columns:
        out["date"] = pd.to_datetime(out["date"], errors="coerce")
    elif "Date" in out.columns:
        out["date"] = pd.to_datetime(out["Date"], errors="coerce")
    else:
        raise KeyError(f"缺少日期欄位，現有欄位：{out.columns.tolist()}")

    # 價格欄位標準化
    for cand in ["Close", "close", "Adj Close", "adj_close", "adjClose", "price"]:
        if cand in out.columns:
            out["Close"] = pd.to_numeric(out[cand], errors="coerce")
            break
    else:
        raise KeyError(f"缺少收盤價欄位，現有欄位：{out.columns.tolist()}")

    return out[["date", "Close"]].sort_values("date").reset_index(drop=True)

def compute_lohas(df: pd.DataFrame, long_win=200, short_win=20):
    out = _ensure_price_columns(df)

    # 長期五線譜
    out["MA_L"] = out["Close"].rolling(long_win, min_periods=long_win//2).mean()
    out["STD_L"] = out["Close"].rolling(long_win, min_periods=long_win//2).std(ddof=0)
    out["U1"] = out["MA_L"] + out["STD_L"]
    out["U2"] = out["MA_L"] + 2 * out["STD_L"]
    out["L1"] = out["MA_L"] - out["STD_L"]
    out["L2"] = out["MA_L"] - 2 * out["STD_L"]

    # 短期樂活通道
    out["MA_S"] = out["Close"].rolling(short_win, min_periods=short_win//2).mean()
    out["STD_S"] = out["Close"].rolling(short_win, min_periods=short_win//2).std(ddof=0)
    out["C_U"] = out["MA_S"] + out["STD_S"]
    out["C_L"] = out["MA_S"] - out["STD_S"]

    return out