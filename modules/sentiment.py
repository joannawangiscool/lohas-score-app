import numpy as np

def classify_sentiment(row):
    c = row["Close"]
    if np.isnan(row["U2"]) or np.isnan(row["L2"]):
        return "資料不足"
    if c >= row["U2"]:
        return "極度樂觀"
    if c <= row["L2"]:
        return "極度悲觀"
    if c >= row["U1"]:
        return "偏樂觀"
    if c <= row["L1"]:
        return "偏悲觀"
    return "中性"