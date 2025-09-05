import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta


def make_sample_data(n_days: int = 120, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    start = datetime.today() - timedelta(days=n_days)
    dates = [start + timedelta(days=i) for i in range(n_days)]
    categories = rng.choice(
        ["Alpha", "Beta", "Gamma"], size=n_days, p=[0.4, 0.35, 0.25]
    )
    baseline = np.linspace(10, 40, n_days)
    seasonal = 6 * np.sin(np.linspace(0, 4 * np.pi, n_days))
    noise = rng.normal(0, 3, n_days)
    cat_offset = {"Alpha": 0, "Beta": 5, "Gamma": -4}
    values = baseline + seasonal + noise + np.vectorize(cat_offset.get)(categories)
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(dates),
            "category": categories,
            "value": values,
        }
    )
    return df


def make_plot(df: pd.DataFrame, out_path: str = "sample_plot.png"):
    sns.set_theme(style="whitegrid", context="talk", palette="viridis")
    plt.figure(figsize=(11, 6))
    # Line plot per category (rolling mean for smoothing)
    for cat, sub in df.groupby("category"):
        sub_sorted = sub.sort_values("date")
        smooth = sub_sorted.assign(
            smooth=sub_sorted["value"]
            .rolling(window=7, min_periods=1, center=True)
            .mean()
        )
        plt.plot(
            smooth["date"],
            smooth["smooth"],
            label=f"{cat} (7‑day smooth)",
            linewidth=2.2,
            alpha=0.9,
        )
        plt.scatter(
            sub_sorted["date"],
            sub_sorted["value"],
            s=18,
            alpha=0.35,
            edgecolor="none",
        )

    plt.title("Sample Time Series by Category")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend(frameon=True, title="Series")
    plt.tight_layout()
    plt.show()


df = make_sample_data()
print(make_plot(df))

# rando comment
