import matplotlib.pyplot as plt
import pandas as pd

def plot_lohas(df: pd.DataFrame, title="樂活五線譜 + 樂活通道", sentiment=None):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["date"], df["Close"], color="#333", linewidth=1.5, label="收盤")

    # 長期五線譜
    ax.plot(df["date"], df["MA_L"], color="green", lw=2, label="中線")
    ax.plot(df["date"], df["U1"], ls="--", color="gray", label="+1σ")
    ax.plot(df["date"], df["L1"], ls="--", color="gray", label="-1σ")
    ax.plot(df["date"], df["U2"], ls="-.", color="red", label="+2σ")
    ax.plot(df["date"], df["L2"], ls="-.", color="blue", label="-2σ")

    # 短期樂活通道（淡色填充）
    ax.fill_between(df["date"], df["C_L"], df["C_U"], color="#FFD54F", alpha=0.2, label="樂活通道")

    if sentiment:
        ax.set_title(f"{title}｜市場情緒：{sentiment}")
    else:
        ax.set_title(title)

    ax.set_xlabel("日期")
    ax.set_ylabel("價格")
    ax.grid(alpha=0.25)
    ax.legend(ncol=3)
    plt.tight_layout()
    return fig