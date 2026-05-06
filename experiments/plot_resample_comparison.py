"""Plot raw 1-minute PV power data against 45-minute resampled data."""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


DATA_PATH = Path("data/processed/light_pv_id00002_201801.csv")
OUTPUT_PATH = Path("Img/fig4_resample_comparison.png")
PLOT_DAY = "2018-01-30"
RESAMPLE_RULE = "45min"


def load_day_frame(path: Path, plot_day: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
    frame["power"] = pd.to_numeric(frame["power"], errors="coerce")
    frame = frame.dropna(subset=["timestamp", "power"]).sort_values("timestamp")

    day_frame = frame.loc[frame["timestamp"].dt.strftime("%Y-%m-%d") == plot_day].copy()
    if day_frame.empty:
        raise ValueError(f"No rows found for plot day: {plot_day}")
    return day_frame


def resample_power(frame: pd.DataFrame, rule: str) -> pd.DataFrame:
    return (
        frame.set_index("timestamp")[["power"]]
        .resample(rule)
        .mean()
        .dropna()
        .reset_index()
    )


def save_plot(day_frame: pd.DataFrame, resampled: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10.5, 5.0), facecolor="#f7f8fc")
    ax.set_facecolor("#ffffff")

    ax.plot(
        day_frame["timestamp"],
        day_frame["power"],
        color="#183a5a",
        linewidth=0.9,
        alpha=0.45,
        label="1-minute raw data",
        zorder=2,
    )
    ax.plot(
        resampled["timestamp"],
        resampled["power"],
        color="#d1495b",
        linewidth=2.2,
        marker="o",
        markersize=4.0,
        markerfacecolor="#d1495b",
        markeredgewidth=0,
        label="45-minute resampled data",
        zorder=4,
    )

    ax.set_title(
        "PV Power Before and After 45-minute Resampling",
        loc="left",
        fontsize=14,
        fontweight="bold",
        color="#183a5a",
        pad=12,
    )
    ax.text(
        0.0,
        1.02,
        f"Sample day: {PLOT_DAY}",
        transform=ax.transAxes,
        fontsize=10,
        color="#5b6574",
    )

    locator = mdates.HourLocator(interval=3)
    formatter = mdates.DateFormatter("%H:%M")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_xlabel("Timestamp", fontsize=10.5, color="#364152", labelpad=8)
    ax.set_ylabel("Power (kW)", fontsize=10.5, color="#364152", labelpad=8)
    ax.tick_params(axis="x", labelsize=9.5, colors="#4b5563")
    ax.tick_params(axis="y", labelsize=9.5, colors="#4b5563")
    ax.grid(axis="y", color="#d8dde7", linewidth=0.8, alpha=0.85)
    ax.grid(axis="x", color="#eef1f6", linewidth=0.7, alpha=0.65)
    ax.set_axisbelow(True)
    ax.margins(x=0.015)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#c7cfdb")
    ax.spines["bottom"].set_color("#c7cfdb")

    legend = ax.legend(
        loc="upper right",
        ncol=1,
        frameon=False,
        fontsize=10,
        handlelength=2.6,
    )
    for text in legend.get_texts():
        text.set_color("#364152")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(output_path, dpi=220, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    day_frame = load_day_frame(DATA_PATH, PLOT_DAY)
    resampled = resample_power(day_frame, RESAMPLE_RULE)
    save_plot(day_frame, resampled, OUTPUT_PATH)
    print(f"Saved resampling comparison plot to: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
