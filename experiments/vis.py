"""PV forecasting visualization/report entrypoint.

参数说明：

- --output-dir：实验输出目录，默认 artifacts/pv_experiment_light。
- --metrics-path：可手动指定指标文件路径。
- --predictions-path：可手动指定预测结果文件路径。
- --config-path：可手动指定实验配置文件路径。
- --plot-path：可手动指定图片输出路径。
- --report-path：可手动指定报告输出路径。
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


DEFAULT_OUTPUT_DIR = Path("artifacts/pv_experiment_light")
DEFAULT_CONFIG_NAME = "experiment_config.json"
REQUIRED_METRIC_COLUMNS = {"model", "mae", "rmse", "mape"}
REQUIRED_PREDICTION_COLUMNS = {"timestamp", "actual", "persistence", "mlp", "lstm"}
EPS = 1e-8


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate visualization and a short report from saved PV experiment outputs."
    )
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--metrics-path", type=str, default="")
    parser.add_argument("--predictions-path", type=str, default="")
    parser.add_argument("--config-path", type=str, default="")
    parser.add_argument("--plot-path", type=str, default="")
    parser.add_argument("--report-path", type=str, default="")
    return parser.parse_args()


def resolve_path(optional_path: str, output_dir: Path, default_name: str) -> Path:
    if optional_path:
        return Path(optional_path)
    return output_dir / default_name


def load_metrics_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Metrics file not found: {path}")

    metrics_df = pd.read_csv(path)
    missing = REQUIRED_METRIC_COLUMNS - set(metrics_df.columns)
    if missing:
        raise KeyError(f"Metrics file is missing columns: {sorted(missing)}")

    for column in ["mae", "rmse", "mape"]:
        metrics_df[column] = pd.to_numeric(metrics_df[column], errors="coerce")
    metrics_df = metrics_df.dropna(subset=["model", "mae", "rmse", "mape"]).reset_index(drop=True)
    if metrics_df.empty:
        raise ValueError("Metrics file does not contain valid rows.")
    return metrics_df


def load_predictions_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Predictions file not found: {path}")

    predictions_df = pd.read_csv(path)
    missing = REQUIRED_PREDICTION_COLUMNS - set(predictions_df.columns)
    if missing:
        raise KeyError(f"Predictions file is missing columns: {sorted(missing)}")

    predictions_df["timestamp"] = pd.to_datetime(predictions_df["timestamp"], errors="coerce")
    numeric_cols = ["actual", "persistence", "mlp", "lstm"]
    for column in numeric_cols:
        predictions_df[column] = pd.to_numeric(predictions_df[column], errors="coerce")
    predictions_df = (
        predictions_df
        .dropna(subset=["timestamp", *numeric_cols])
        .sort_values("timestamp")
        .reset_index(drop=True)
    )
    if predictions_df.empty:
        raise ValueError("Predictions file does not contain valid rows.")
    return predictions_df


def load_config(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_preferred_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    if bold:
        candidates = [
            Path(r"C:\Windows\Fonts\segoeuib.ttf"),
            Path(r"C:\Windows\Fonts\arialbd.ttf"),
            Path(r"C:\Windows\Fonts\calibrib.ttf"),
        ]
    else:
        candidates = [
            Path(r"C:\Windows\Fonts\segoeui.ttf"),
            Path(r"C:\Windows\Fonts\arial.ttf"),
            Path(r"C:\Windows\Fonts\calibri.ttf"),
        ]

    for font_path in candidates:
        if font_path.exists():
            try:
                return ImageFont.truetype(str(font_path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def downsample_frame(frame: pd.DataFrame, max_points: int = 220) -> pd.DataFrame:
    if len(frame) <= max_points:
        return frame.reset_index(drop=True)
    indices = np.linspace(0, len(frame) - 1, max_points).astype(int)
    return frame.iloc[indices].reset_index(drop=True)


def select_plot_frame(predictions: pd.DataFrame) -> pd.DataFrame:
    candidate = predictions.copy()
    candidate["timestamp"] = pd.to_datetime(candidate["timestamp"])
    return candidate.sort_values("timestamp").reset_index(drop=True)


def split_plot_segments(plot_frame: pd.DataFrame) -> list[pd.DataFrame]:
    timestamps = pd.to_datetime(plot_frame["timestamp"]).reset_index(drop=True)
    if len(timestamps) <= 1:
        return [plot_frame.reset_index(drop=True)]

    deltas = timestamps.diff().dropna()
    positive_deltas = deltas[deltas > pd.Timedelta(0)]
    if positive_deltas.empty:
        return [plot_frame.reset_index(drop=True)]

    expected_delta = positive_deltas.mode().iloc[0]
    gap_threshold = expected_delta * 1.5
    segment_breaks = timestamps.diff() > gap_threshold
    segment_ids = segment_breaks.fillna(False).cumsum()
    return [
        plot_frame.iloc[np.asarray(indexes, dtype=np.int64)].reset_index(drop=True)
        for _, indexes in segment_ids.groupby(segment_ids).groups.items()
    ]


def save_plot_with_matplotlib(plot_path: Path, plot_frame: pd.DataFrame) -> bool:
    try:
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    styled = plot_frame.copy()
    styled["timestamp"] = pd.to_datetime(styled["timestamp"])

    fig, ax = plt.subplots(figsize=(14, 7.5), facecolor="#f7f8fc")
    ax.set_facecolor("#ffffff")
    segments = split_plot_segments(styled)

    line_specs = [
        ("actual", "#183a5a", 2.8, "-", None, 5),
        ("persistence", "#f28e2b", 1.8, "--", 0.92, None),
        ("mlp", "#59a14f", 1.8, "-.", 0.9, None),
        ("lstm", "#d1495b", 2.4, "-", None, None),
    ]
    for column, color, width, linestyle, alpha, markevery in line_specs:
        first_segment = True
        for segment in segments:
            kwargs: dict[str, object] = {
                "label": column.upper() if first_segment else "_nolegend_",
                "linewidth": width,
                "color": color,
                "linestyle": linestyle,
                "zorder": 4 if column in {"actual", "lstm"} else 3,
            }
            if alpha is not None:
                kwargs["alpha"] = alpha
            if markevery is not None:
                kwargs["marker"] = "o"
                kwargs["markersize"] = 4
                kwargs["markerfacecolor"] = color
                kwargs["markeredgewidth"] = 0
                kwargs["markevery"] = markevery
            ax.plot(segment["timestamp"], segment[column], **kwargs)
            first_segment = False

    for segment in segments:
        ax.fill_between(
            pd.to_datetime(segment["timestamp"]),
            segment["actual"].to_numpy(dtype=np.float64),
            color="#183a5a",
            alpha=0.06,
            zorder=1,
        )

    ax.grid(axis="y", color="#d8dde7", linewidth=0.9, alpha=0.85)
    ax.grid(axis="x", color="#eef1f6", linewidth=0.8, alpha=0.65)
    ax.set_axisbelow(True)

    locator = mdates.AutoDateLocator(minticks=6, maxticks=10)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_title(
        "PV Power Forecasting on the Full Test Set",
        loc="left",
        fontsize=16,
        fontweight="bold",
        color="#183a5a",
        pad=16,
    )

    time_start = styled["timestamp"].iloc[0].strftime("%Y-%m-%d %H:%M")
    time_end = styled["timestamp"].iloc[-1].strftime("%Y-%m-%d %H:%M")
    ax.text(
        0.0,
        1.02,
        f"Test span: {time_start} to {time_end}",
        transform=ax.transAxes,
        fontsize=10.5,
        color="#5b6574",
    )

    ax.set_xlabel("Timestamp", fontsize=11, color="#364152", labelpad=10)
    ax.set_ylabel("Power", fontsize=11, color="#364152", labelpad=10)
    ax.tick_params(axis="x", labelsize=9.5, colors="#4b5563")
    ax.tick_params(axis="y", labelsize=9.5, colors="#4b5563")
    ax.margins(x=0.015)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#c7cfdb")
    ax.spines["bottom"].set_color("#c7cfdb")

    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=4,
        frameon=False,
        fontsize=10,
        handlelength=2.8,
        columnspacing=1.6,
    )
    for text in legend.get_texts():
        text.set_color("#364152")

    rmse_values = {
        name.upper(): math.sqrt(float(np.mean(np.square(styled["actual"] - styled[name]))))
        for name in ("persistence", "mlp", "lstm")
    }
    summary_text = "  ".join(
        [
            f"Persistence RMSE={rmse_values['PERSISTENCE']:.3f}",
            f"MLP RMSE={rmse_values['MLP']:.3f}",
            f"LSTM RMSE={rmse_values['LSTM']:.3f}",
        ]
    )
    ax.text(
        0.99,
        0.03,
        summary_text,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color="#5b6574",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#f6f8fb", "edgecolor": "#d9e0ea"},
    )

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(plot_path, dpi=220, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    return True


def save_plot_with_pillow(plot_path: Path, plot_frame: pd.DataFrame) -> None:
    width, height = 1600, 900
    margin_left, margin_right, margin_top, margin_bottom = 110, 80, 120, 120
    image = Image.new("RGB", (width, height), "#f7f8fc")
    draw = ImageDraw.Draw(image)
    title_font = load_preferred_font(24, bold=True)
    subtitle_font = load_preferred_font(15)
    axis_font = load_preferred_font(16, bold=True)
    tick_font = load_preferred_font(13)
    legend_font = load_preferred_font(15, bold=True)
    stats_font = load_preferred_font(13)

    plot_frame = downsample_frame(plot_frame)
    timestamps = pd.to_datetime(plot_frame["timestamp"])
    raw_positions = timestamps.astype("int64").to_numpy(dtype=np.float64)
    if len(raw_positions) == 0:
        raise ValueError("Plot frame is empty.")
    if np.allclose(raw_positions[0], raw_positions[-1]):
        x_values = np.arange(len(plot_frame), dtype=np.float64)
    else:
        x_values = raw_positions
    segments = split_plot_segments(plot_frame)
    series = {
        "actual": ("#183a5a", plot_frame["actual"].to_numpy(dtype=np.float32), 4),
        "persistence": ("#f28e2b", plot_frame["persistence"].to_numpy(dtype=np.float32), 3),
        "mlp": ("#59a14f", plot_frame["mlp"].to_numpy(dtype=np.float32), 3),
        "lstm": ("#d1495b", plot_frame["lstm"].to_numpy(dtype=np.float32), 4),
    }

    y_min = min(float(values.min()) for _, values, _ in series.values())
    y_max = max(float(values.max()) for _, values, _ in series.values())
    if math.isclose(y_min, y_max):
        y_max = y_min + 1.0
    y_pad = (y_max - y_min) * 0.08
    y_min -= y_pad
    y_max += y_pad

    def to_canvas_x(index: float) -> float:
        span = max(float(x_values[-1] - x_values[0]), 1.0)
        return margin_left + (index - x_values[0]) / span * (width - margin_left - margin_right)

    def to_canvas_y(value: float) -> float:
        return margin_top + (y_max - value) / (y_max - y_min) * (height - margin_top - margin_bottom)

    def draw_centered_multiline(x_pos: float, y_pos: float, text: str, font: ImageFont.ImageFont) -> None:
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=3, align="center")
        text_width = bbox[2] - bbox[0]
        draw.multiline_text(
            (x_pos - text_width / 2, y_pos),
            text,
            fill="#4b5563",
            font=font,
            spacing=3,
            align="center",
        )

    draw.rounded_rectangle(
        [(30, 30), (width - 30, height - 30)],
        radius=28,
        fill="#ffffff",
        outline="#e3e8f0",
        width=2,
    )
    draw.rectangle(
        [(margin_left, margin_top), (width - margin_right, height - margin_bottom)],
        fill="#fbfcff",
        outline="#ccd4df",
        width=2,
    )

    for step in range(6):
        y_tick = y_min + (y_max - y_min) * step / 5
        y_pos = to_canvas_y(y_tick)
        draw.line(
            [(margin_left, y_pos), (width - margin_right, y_pos)],
            fill="#dde3ec",
            width=1,
        )
        draw.text((20, y_pos - 9), f"{y_tick:.2f}", fill="#4b5563", font=tick_font)

    tick_count = min(6, max(len(plot_frame), 2))
    tick_times = pd.date_range(timestamps.iloc[0], timestamps.iloc[-1], periods=tick_count)
    tick_positions = tick_times.astype("int64").to_numpy(dtype=np.float64)
    for tick_time, tick_position in zip(tick_times, tick_positions):
        x_pos = to_canvas_x(float(tick_position))
        draw.line(
            [(x_pos, margin_top), (x_pos, height - margin_bottom)],
            fill="#eef2f7",
            width=1,
        )
        tick_label = tick_time.strftime("%m-%d\n%H:%M")
        draw_centered_multiline(x_pos, height - margin_bottom + 16, tick_label, tick_font)

    for segment in segments:
        segment_timestamps = pd.to_datetime(segment["timestamp"]).astype("int64").to_numpy(dtype=np.float64)
        segment_values = segment["actual"].to_numpy(dtype=np.float32)
        actual_points = [
            (to_canvas_x(float(x_val)), to_canvas_y(float(value)))
            for x_val, value in zip(segment_timestamps, segment_values)
        ]
        if len(actual_points) >= 2:
            polygon = actual_points + [
                (to_canvas_x(float(segment_timestamps[-1])), height - margin_bottom),
                (to_canvas_x(float(segment_timestamps[0])), height - margin_bottom),
            ]
            draw.polygon(polygon, fill="#e8eef5")

    for name, (color, _, width_px) in series.items():
        for segment in segments:
            segment_timestamps = pd.to_datetime(segment["timestamp"]).astype("int64").to_numpy(dtype=np.float64)
            segment_values = segment[name].to_numpy(dtype=np.float32)
            points = [
                (to_canvas_x(float(x_val)), to_canvas_y(float(value)))
                for x_val, value in zip(segment_timestamps, segment_values)
            ]
            draw.line(points, fill=color, width=width_px)
            if name in {"actual", "lstm"}:
                for point in points[:: max(len(points) // 8, 1)]:
                    x_pos, y_pos = point
                    draw.ellipse(
                        [(x_pos - 3, y_pos - 3), (x_pos + 3, y_pos + 3)],
                        fill=color,
                        outline=color,
                    )

    title = "PV Power Forecasting on the Full Test Set"
    subtitle = (
        f"Test span: {timestamps.iloc[0].strftime('%Y-%m-%d %H:%M')} to "
        f"{timestamps.iloc[-1].strftime('%Y-%m-%d %H:%M')}"
    )
    draw.text((margin_left, 42), title, fill="#183a5a", font=title_font)
    draw.text((margin_left, 75), subtitle, fill="#5b6574", font=subtitle_font)
    draw.text((width / 2 - 42, height - 54), "Timestamp", fill="#364152", font=axis_font)
    draw.text((18, margin_top - 34), "Power", fill="#364152", font=axis_font)

    legend_x = width - 315
    legend_y = 54
    for idx, (name, (color, _, _)) in enumerate(series.items()):
        y = legend_y + idx * 26
        draw.line([(legend_x, y + 6), (legend_x + 28, y + 6)], fill=color, width=3)
        if name in {"actual", "lstm"}:
            draw.ellipse(
                [(legend_x + 12, y + 2), (legend_x + 18, y + 8)],
                fill=color,
                outline=color,
            )
        draw.text((legend_x + 40, y - 3), name.upper(), fill="#364152", font=legend_font)

    rmse_values = {
        name.upper(): math.sqrt(float(np.mean(np.square(plot_frame["actual"] - plot_frame[name]))))
        for name in ("persistence", "mlp", "lstm")
    }
    stats_text = (
        f"Persistence RMSE={rmse_values['PERSISTENCE']:.3f}   "
        f"MLP RMSE={rmse_values['MLP']:.3f}   "
        f"LSTM RMSE={rmse_values['LSTM']:.3f}"
    )
    draw.rounded_rectangle(
        [(margin_left, 94), (margin_left + 470, 122)],
        radius=10,
        fill="#f6f8fb",
        outline="#d9e0ea",
        width=1,
    )
    draw.text((margin_left + 14, 100), stats_text, fill="#5b6574", font=stats_font)

    image.save(plot_path)


def save_prediction_plot(plot_path: Path, predictions: pd.DataFrame) -> None:
    plot_frame = select_plot_frame(predictions)
    if save_plot_with_matplotlib(plot_path, plot_frame):
        return
    save_plot_with_pillow(plot_path, plot_frame)


def build_config_summary(config: dict[str, object]) -> str:
    summary = str(config.get("config_summary", "")).strip()
    if summary:
        return summary

    resample_rule = str(config.get("resample_rule", "")).strip() or "none"
    add_time_features = bool(config.get("add_time_features", False))
    filter_night = bool(config.get("filter_night", False))
    input_feature_count = config.get("input_feature_count", "unknown")
    return (
        f"resample={resample_rule}, "
        f"time_features={'on' if add_time_features else 'off'}, "
        f"night_filter={'on' if filter_night else 'off'}, "
        f"input_features={input_feature_count}"
    )


def build_report_snippet(metrics_df: pd.DataFrame, config: dict[str, object]) -> str:
    metrics_sorted = metrics_df.sort_values("rmse").reset_index(drop=True)
    best_model = str(metrics_sorted.loc[0, "model"])
    lstm_row = metrics_df.loc[metrics_df["model"].str.lower() == "lstm"]
    persistence_row = metrics_df.loc[metrics_df["model"].str.lower() == "persistence"]
    lstm_rmse = float(lstm_row["rmse"].iloc[0]) if not lstm_row.empty else math.nan
    persistence_rmse = float(persistence_row["rmse"].iloc[0]) if not persistence_row.empty else math.nan

    improvement = 0.0
    if not math.isnan(lstm_rmse) and not math.isnan(persistence_rmse):
        improvement = (persistence_rmse - lstm_rmse) / max(persistence_rmse, EPS) * 100.0

    dataset_label = str(config.get("dataset_label", "unknown dataset"))
    window_size = config.get("window_size", "unknown")
    horizon = config.get("horizon", "unknown")
    config_summary = build_config_summary(config)

    lines = [
        "### 实验结果摘要",
        "",
        f"本实验使用 `{dataset_label}` 数据，采用长度为 `{window_size}` 的历史窗口预测未来 `{horizon}` 个时间步后的光伏功率。",
        "对比模型包括 Persistence、MLP 和 LSTM，评价指标为 MAE、RMSE 与 MAPE。",
        f"实验设置：{config_summary}。",
        "",
        "| Model | MAE | RMSE | MAPE(%) |",
        "| --- | ---: | ---: | ---: |",
    ]

    for row in metrics_sorted.itertuples(index=False):
        lines.append(
            f"| {str(row.model).upper()} | {row.mae:.4f} | {row.rmse:.4f} | {row.mape:.2f} |"
        )

    lines.extend(["", f"测试结果显示，`{best_model.upper()}` 在 RMSE 指标上表现最好。"])

    if best_model.lower() == "lstm" and improvement > 0:
        lines.append(
            f"相较于 Persistence 基线，LSTM 的 RMSE 下降约 `{improvement:.2f}%`，"
            "说明其能够更好地刻画光伏功率的时间依赖性。"
        )
    else:
        lines.append(
            "本次实验中 LSTM 与基线模型差距有限，这通常与数据规模、输入特征数量、"
            "天气突变程度以及夜间样本处理方式有关。"
        )

    return "\n".join(lines)


def build_terminal_summary(metrics_df: pd.DataFrame) -> str:
    metrics_sorted = metrics_df.sort_values("rmse").reset_index(drop=True)
    best_row = metrics_sorted.iloc[0]
    lines = [
        "实验结果概览：",
        f"- 最优模型：{str(best_row['model']).upper()}",
        f"- MAE={float(best_row['mae']):.4f}, RMSE={float(best_row['rmse']):.4f}, MAPE={float(best_row['mape']):.2f}%",
    ]

    persistence_row = metrics_sorted.loc[metrics_sorted["model"].str.lower() == "persistence"]
    lstm_row = metrics_sorted.loc[metrics_sorted["model"].str.lower() == "lstm"]
    if not persistence_row.empty and not lstm_row.empty:
        persistence_rmse = float(persistence_row["rmse"].iloc[0])
        lstm_rmse = float(lstm_row["rmse"].iloc[0])
        improvement = (persistence_rmse - lstm_rmse) / max(persistence_rmse, EPS) * 100.0
        lines.append(f"- LSTM 相比 Persistence 的 RMSE 变化：{improvement:.2f}%")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = resolve_path(args.metrics_path, output_dir, "metrics.csv")
    predictions_path = resolve_path(args.predictions_path, output_dir, "predictions.csv")
    config_path = resolve_path(args.config_path, output_dir, DEFAULT_CONFIG_NAME)
    plot_path = resolve_path(args.plot_path, output_dir, "prediction_curve.png")
    report_path = resolve_path(args.report_path, output_dir, "report_snippet.md")

    metrics_df = load_metrics_frame(metrics_path)
    predictions_df = load_predictions_frame(predictions_path)
    config = load_config(config_path)

    save_prediction_plot(plot_path, predictions_df)
    report_text = build_report_snippet(metrics_df, config)
    report_path.write_text(report_text, encoding="utf-8-sig")

    print(build_terminal_summary(metrics_df))
    print(f"Saved plot to: {plot_path}")
    print(f"Saved report snippet to: {report_path}")
    if config_path.exists():
        print(f"Loaded config from: {config_path}")
    else:
        print("Config file not found. Report used fallback metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
