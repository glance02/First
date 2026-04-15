from __future__ import annotations

import argparse
import copy
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import torch
from PIL import Image, ImageDraw, ImageFont
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


DEFAULT_OUTPUT_DIR = Path("artifacts/pv_experiment")
DEFAULT_SEED = 42
EPS = 1e-8


@dataclass
class Standardizer:
    mean: np.ndarray
    std: np.ndarray

    @classmethod
    def fit(cls, values: np.ndarray) -> "Standardizer":
        mean = values.mean(axis=0)
        std = values.std(axis=0)
        std = np.where(std < EPS, 1.0, std)
        return cls(mean=mean, std=std)

    def transform(self, values: np.ndarray) -> np.ndarray:
        return (values - self.mean) / self.std

    def inverse_transform(self, values: np.ndarray) -> np.ndarray:
        return values * self.std + self.mean


class MLPRegressor(nn.Module):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        mid_size = max(hidden_size // 2, 16)
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, mid_size),
            nn.ReLU(),
            nn.Linear(mid_size, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        flattened = x.reshape(x.size(0), -1)
        return self.network(flattened).squeeze(-1)


class LSTMRegressor(nn.Module):
    def __init__(self, num_features: int, hidden_size: int) -> None:
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_size,
            num_layers=1,
            batch_first=True,
        )
        self.output = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded, _ = self.lstm(x)
        return self.output(encoded[:, -1, :]).squeeze(-1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a compact photovoltaic power forecasting experiment."
    )
    parser.add_argument("--data-path", type=str, default="")
    parser.add_argument("--time-col", type=str, default="timestamp")
    parser.add_argument("--target-col", type=str, default="power")
    parser.add_argument("--feature-cols", type=str, default="")
    parser.add_argument("--window-size", type=int, default=8)
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--hidden-size", type=int, default=64)
    parser.add_argument("--resample-rule", type=str, default="")
    parser.add_argument("--add-time-features", action="store_true")
    parser.add_argument("--filter-night", action="store_true")
    parser.add_argument("--device", type=str, default="auto")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--demo-synthetic", action="store_true")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def parse_feature_columns(feature_cols: str) -> list[str]:
    if not feature_cols:
        return []
    return [column.strip() for column in feature_cols.split(",") if column.strip()]


def detect_device(requested: str) -> torch.device:
    requested = requested.lower()
    if requested == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")
    if requested == "cuda" and not torch.cuda.is_available():
        print("CUDA is unavailable. Falling back to CPU.")
        return torch.device("cpu")
    return torch.device(requested)


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


def generate_synthetic_frame(num_days: int = 40, freq: str = "15min") -> pd.DataFrame:
    timestamps = pd.date_range("2024-01-01", periods=num_days * 24 * 4, freq=freq)
    hours = timestamps.hour + timestamps.minute / 60.0
    daylight_curve = np.clip(1.0 - ((hours - 12.0) / 6.0) ** 2, 0.0, None)
    day_index = (timestamps.dayofyear - timestamps.dayofyear.min()).to_numpy(dtype=np.float32)
    seasonal = 0.95 + 0.08 * np.sin(2 * np.pi * day_index / 30.0)
    cloud = 0.88 + 0.12 * np.sin(2 * np.pi * np.arange(len(timestamps)) / (24 * 4 * 5))
    cloud += np.random.normal(0, 0.05, len(timestamps))
    cloud = np.clip(cloud, 0.45, 1.15)

    irradiance = 850 * daylight_curve * seasonal * cloud
    temperature = 16 + 10 * daylight_curve + 4 * np.sin(2 * np.pi * day_index / 20.0)
    humidity = 70 - 18 * daylight_curve + np.random.normal(0, 2.0, len(timestamps))
    noise = np.random.normal(0, 18, len(timestamps))
    power = np.clip(irradiance * 0.22 + noise, 0, None)

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "power": power.astype(np.float32),
            "irradiance": irradiance.astype(np.float32),
            "temperature": temperature.astype(np.float32),
            "humidity": humidity.astype(np.float32),
        }
    )


def load_frame(args: argparse.Namespace, extra_features: list[str]) -> tuple[pd.DataFrame, str]:
    if args.demo_synthetic:
        return generate_synthetic_frame(), "synthetic PV-like dataset"

    if not args.data_path:
        raise ValueError("Provide --data-path or enable --demo-synthetic.")

    path = Path(args.data_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    return pd.read_csv(path), path.name


def find_irradiance_column(columns: Iterable[str]) -> str | None:
    normalized = {column.lower(): column for column in columns}
    for candidate in ("irradiance", "ghi", "solar_irradiance", "radiation"):
        if candidate in normalized:
            return normalized[candidate]
    return None


def prepare_frame(
    frame: pd.DataFrame,
    time_col: str,
    target_col: str,
    extra_features: list[str],
) -> pd.DataFrame:
    required = [time_col, target_col, *extra_features]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    prepared = frame.copy()
    prepared[time_col] = pd.to_datetime(prepared[time_col], errors="coerce")
    prepared = prepared.dropna(subset=[time_col]).drop_duplicates(subset=[time_col], keep="last")
    prepared = prepared.sort_values(time_col).reset_index(drop=True)

    for column in [target_col, *extra_features]:
        prepared[column] = pd.to_numeric(prepared[column], errors="coerce")

    prepared = prepared.dropna(subset=[target_col, *extra_features]).reset_index(drop=True)
    if prepared.empty:
        raise ValueError("No valid rows remain after preprocessing.")
    return prepared


def resample_frame(
    frame: pd.DataFrame,
    time_col: str,
    value_cols: list[str],
    rule: str,
) -> pd.DataFrame:
    if not rule:
        return frame.copy()

    resampled = (
        frame.set_index(time_col)[value_cols]
        .resample(rule)
        .mean()
        .dropna()
        .reset_index()
    )
    if resampled.empty:
        raise ValueError(f"Resampling with rule '{rule}' removed all rows.")
    return resampled


def add_time_features(frame: pd.DataFrame, time_col: str) -> tuple[pd.DataFrame, list[str]]:
    enriched = frame.copy()
    timestamp = pd.to_datetime(enriched[time_col])
    minute_of_day = timestamp.dt.hour * 60 + timestamp.dt.minute
    day_of_week = timestamp.dt.dayofweek

    enriched["time_of_day_sin"] = np.sin(2 * np.pi * minute_of_day / (24 * 60)).astype(np.float32)
    enriched["time_of_day_cos"] = np.cos(2 * np.pi * minute_of_day / (24 * 60)).astype(np.float32)
    enriched["day_of_week_sin"] = np.sin(2 * np.pi * day_of_week / 7).astype(np.float32)
    enriched["day_of_week_cos"] = np.cos(2 * np.pi * day_of_week / 7).astype(np.float32)

    return enriched, [
        "time_of_day_sin",
        "time_of_day_cos",
        "day_of_week_sin",
        "day_of_week_cos",
    ]


def filter_night_segments(frame: pd.DataFrame, signal_col: str) -> pd.DataFrame:
    signal = frame[signal_col].to_numpy(dtype=np.float32)
    max_signal = float(np.nanmax(np.abs(signal)))
    if max_signal <= EPS:
        return frame.copy()

    threshold = max(max_signal * 0.01, 1e-5)
    rolling_max = (
        pd.Series(np.abs(signal))
        .rolling(window=5, center=True, min_periods=1)
        .max()
        .to_numpy(dtype=np.float32)
    )
    mask = rolling_max > threshold
    filtered = frame.loc[mask].reset_index(drop=True)
    if len(filtered) < max(64, int(len(frame) * 0.25)):
        return frame.copy()
    return filtered


def split_frame(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    total = len(frame)
    train_end = int(total * 0.70)
    val_end = int(total * 0.85)
    train = frame.iloc[:train_end].reset_index(drop=True)
    val = frame.iloc[train_end:val_end].reset_index(drop=True)
    test = frame.iloc[val_end:].reset_index(drop=True)
    return train, val, test


def ensure_split_length(frame: pd.DataFrame, split_name: str, window_size: int, horizon: int) -> None:
    minimum = window_size + horizon + 2
    if len(frame) < minimum:
        raise ValueError(
            f"{split_name} split is too short after preprocessing. "
            f"Need at least {minimum} rows, got {len(frame)}."
        )


def create_sequences(
    frame: pd.DataFrame,
    feature_cols: list[str],
    target_col: str,
    time_col: str,
    window_size: int,
    horizon: int,
    feature_scaler: Standardizer,
    target_scaler: Standardizer,
) -> dict[str, np.ndarray]:
    raw_features = frame[feature_cols].to_numpy(dtype=np.float32)
    raw_target = frame[target_col].to_numpy(dtype=np.float32)
    timestamp_series = pd.to_datetime(frame[time_col]).reset_index(drop=True)
    timestamps = timestamp_series.astype("string").to_numpy()

    scaled_features = feature_scaler.transform(raw_features.astype(np.float32)).astype(np.float32)
    scaled_target = target_scaler.transform(raw_target.reshape(-1, 1)).astype(np.float32).reshape(-1)

    x_scaled, x_raw, y_scaled, y_raw, ts = [], [], [], [], []

    deltas = timestamp_series.diff().dropna()
    positive_deltas = deltas[deltas > pd.Timedelta(0)]
    if positive_deltas.empty:
        segment_ids = pd.Series(np.zeros(len(frame), dtype=np.int32))
    else:
        expected_delta = positive_deltas.mode().iloc[0]
        gap_threshold = expected_delta * 1.5
        segment_breaks = timestamp_series.diff() > gap_threshold
        segment_ids = segment_breaks.fillna(False).cumsum()

    for _, segment_index in segment_ids.groupby(segment_ids).groups.items():
        segment_index = np.asarray(segment_index, dtype=np.int64)
        if len(segment_index) < window_size + horizon:
            continue

        for end in range(window_size, len(segment_index) - horizon + 1):
            start = end - window_size
            target_index = end + horizon - 1

            window_indices = segment_index[start:end]
            target_row = segment_index[target_index]

            x_scaled.append(scaled_features[window_indices])
            x_raw.append(raw_features[window_indices])
            y_scaled.append(scaled_target[target_row])
            y_raw.append(raw_target[target_row])
            ts.append(timestamps[target_row])

    return {
        "x_scaled": np.asarray(x_scaled, dtype=np.float32),
        "x_raw": np.asarray(x_raw, dtype=np.float32),
        "y_scaled": np.asarray(y_scaled, dtype=np.float32),
        "y_raw": np.asarray(y_raw, dtype=np.float32),
        "timestamp": np.asarray(ts, dtype=object),
    }


def ensure_nonempty_sequences(sequence_dict: dict[str, np.ndarray], split_name: str) -> None:
    if len(sequence_dict["x_scaled"]) == 0:
        raise ValueError(
            f"{split_name} split produced zero valid sequences. "
            "Try reducing --window-size/--horizon or using a coarser --resample-rule."
        )


def make_loader(x: np.ndarray, y: np.ndarray, batch_size: int, shuffle: bool) -> DataLoader:
    dataset = TensorDataset(torch.from_numpy(x), torch.from_numpy(y))
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def inverse_target(target_scaler: Standardizer, values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float32).reshape(-1, 1)
    return target_scaler.inverse_transform(values).reshape(-1)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean(np.square(y_true - y_pred))))
    threshold = max(float(np.max(np.abs(y_true))) * 0.05, 1e-3)
    valid = np.abs(y_true) >= threshold
    if not np.any(valid):
        valid = np.abs(y_true) >= 1e-3
    denominator = np.clip(np.abs(y_true[valid]), threshold, None)
    mape = float(np.mean(np.abs((y_true[valid] - y_pred[valid]) / denominator)) * 100.0)
    return {"mae": mae, "rmse": rmse, "mape": mape}


def predict_scaled(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[np.ndarray, np.ndarray]:
    model.eval()
    preds, targets = [], []
    with torch.inference_mode():
        for batch_x, batch_y in loader:
            batch_x = batch_x.to(device)
            pred = model(batch_x).cpu().numpy()
            preds.append(pred)
            targets.append(batch_y.numpy())
    return np.concatenate(preds), np.concatenate(targets)


def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    target_scaler: Standardizer,
    epochs: int,
    device: torch.device,
) -> nn.Module:
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()
    patience = 8
    best_rmse = math.inf
    best_state: dict[str, torch.Tensor] | None = None
    stale_epochs = 0

    model.to(device)

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        sample_count = 0
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            optimizer.zero_grad()
            pred = model(batch_x)
            loss = criterion(pred, batch_y)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * batch_x.size(0)
            sample_count += batch_x.size(0)

        val_pred_scaled, val_true_scaled = predict_scaled(model, val_loader, device)
        val_pred = inverse_target(target_scaler, val_pred_scaled)
        val_true = inverse_target(target_scaler, val_true_scaled)
        val_rmse = compute_metrics(val_true, val_pred)["rmse"]
        train_loss = running_loss / max(sample_count, 1)
        print(
            f"Epoch {epoch:03d} | train_loss={train_loss:.5f} | "
            f"val_rmse={val_rmse:.5f}"
        )

        if val_rmse + 1e-6 < best_rmse:
            best_rmse = val_rmse
            best_state = copy.deepcopy(model.state_dict())
            stale_epochs = 0
        else:
            stale_epochs += 1
            if stale_epochs >= patience:
                print(f"Early stopping at epoch {epoch}.")
                break

    if best_state is None:
        raise RuntimeError("Training did not produce a valid checkpoint.")

    model.load_state_dict(best_state)
    return model


def evaluate_neural_model(
    model: nn.Module,
    test_loader: DataLoader,
    target_scaler: Standardizer,
    device: torch.device,
) -> tuple[np.ndarray, np.ndarray]:
    pred_scaled, true_scaled = predict_scaled(model, test_loader, device)
    pred = inverse_target(target_scaler, pred_scaled)
    true = inverse_target(target_scaler, true_scaled)
    return pred, true


def save_plot_with_matplotlib(plot_path: Path, plot_frame: pd.DataFrame) -> bool:
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
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


def downsample_frame(frame: pd.DataFrame, max_points: int = 220) -> pd.DataFrame:
    if len(frame) <= max_points:
        return frame.reset_index(drop=True)
    indices = np.linspace(0, len(frame) - 1, max_points).astype(int)
    return frame.iloc[indices].reset_index(drop=True)


def select_plot_frame(predictions: pd.DataFrame) -> pd.DataFrame:
    candidate = predictions.copy()
    candidate["timestamp"] = pd.to_datetime(candidate["timestamp"])
    candidate = candidate.sort_values("timestamp").reset_index(drop=True)
    return candidate


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

    for name, (color, values, width_px) in series.items():
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
    for idx, (name, (color, _, width_px)) in enumerate(series.items()):
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


def build_report_snippet(
    metrics_df: pd.DataFrame,
    dataset_label: str,
    window_size: int,
    horizon: int,
    config_summary: str,
) -> str:
    metrics_sorted = metrics_df.sort_values("rmse").reset_index(drop=True)
    best_model = metrics_sorted.loc[0, "model"]
    lstm_rmse = float(metrics_df.loc[metrics_df["model"] == "lstm", "rmse"].iloc[0])
    persistence_rmse = float(metrics_df.loc[metrics_df["model"] == "persistence", "rmse"].iloc[0])
    improvement = (persistence_rmse - lstm_rmse) / max(persistence_rmse, EPS) * 100.0

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
            f"| {row.model.upper()} | {row.mae:.4f} | {row.rmse:.4f} | {row.mape:.2f} |"
        )

    lines.extend(["", f"测试结果显示，`{best_model.upper()}` 在 RMSE 指标上表现最好。"])

    if best_model == "lstm" and improvement > 0:
        lines.append(
            f"相较于 Persistence 基线，LSTM 的 RMSE 下降约 `{improvement:.2f}%`，"
            "说明其能够更好地刻画光伏功率的时间依赖性。"
        )
    else:
        lines.append(
            "本次实验中 LSTM 与基线模型差距有限，这通常与数据规模、输入特征数量、"
            "天气突变程度以及夜间样本处理方式有关。"
        )

    lines.extend(
        [
            "建议将上表替换到报告的“表3”，并把同目录下的 `prediction_curve.png` 作为“图2”插入。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    set_seed(args.seed)
    device = detect_device(args.device)

    extra_features = parse_feature_columns(args.feature_cols)
    raw_frame, dataset_label = load_frame(args, extra_features)
    if args.demo_synthetic and not extra_features:
        extra_features = ["irradiance", "temperature", "humidity"]
    frame = prepare_frame(raw_frame, args.time_col, args.target_col, extra_features)
    frame = resample_frame(
        frame,
        args.time_col,
        [args.target_col, *extra_features],
        args.resample_rule,
    )

    time_feature_cols: list[str] = []
    if args.add_time_features:
        frame, time_feature_cols = add_time_features(frame, args.time_col)

    if args.filter_night:
        irradiance_col = find_irradiance_column(frame.columns)
        signal_col = irradiance_col or args.target_col
        frame = filter_night_segments(frame, signal_col)

    feature_cols = [args.target_col, *extra_features, *time_feature_cols]
    train_frame, val_frame, test_frame = split_frame(frame)

    for split_name, split_frame_data in [
        ("train", train_frame),
        ("validation", val_frame),
        ("test", test_frame),
    ]:
        ensure_split_length(split_frame_data, split_name, args.window_size, args.horizon)

    feature_scaler = Standardizer.fit(train_frame[feature_cols].to_numpy(dtype=np.float32))
    target_scaler = Standardizer.fit(train_frame[[args.target_col]].to_numpy(dtype=np.float32))

    train_seq = create_sequences(
        train_frame,
        feature_cols,
        args.target_col,
        args.time_col,
        args.window_size,
        args.horizon,
        feature_scaler,
        target_scaler,
    )
    val_seq = create_sequences(
        val_frame,
        feature_cols,
        args.target_col,
        args.time_col,
        args.window_size,
        args.horizon,
        feature_scaler,
        target_scaler,
    )
    test_seq = create_sequences(
        test_frame,
        feature_cols,
        args.target_col,
        args.time_col,
        args.window_size,
        args.horizon,
        feature_scaler,
        target_scaler,
    )

    ensure_nonempty_sequences(train_seq, "train")
    ensure_nonempty_sequences(val_seq, "validation")
    ensure_nonempty_sequences(test_seq, "test")

    train_loader = make_loader(train_seq["x_scaled"], train_seq["y_scaled"], args.batch_size, True)
    val_loader = make_loader(val_seq["x_scaled"], val_seq["y_scaled"], args.batch_size, False)
    test_loader = make_loader(test_seq["x_scaled"], test_seq["y_scaled"], args.batch_size, False)

    mlp_model = MLPRegressor(
        input_size=args.window_size * len(feature_cols),
        hidden_size=args.hidden_size,
    )
    lstm_model = LSTMRegressor(
        num_features=len(feature_cols),
        hidden_size=args.hidden_size,
    )

    print(f"Using device: {device}")
    print(f"Dataset label: {dataset_label}")
    print(f"Rows after preprocessing: {len(frame)}")
    print(f"Feature columns: {feature_cols}")

    mlp_model = train_model(
        mlp_model,
        train_loader,
        val_loader,
        target_scaler,
        args.epochs,
        device,
    )
    lstm_model = train_model(
        lstm_model,
        train_loader,
        val_loader,
        target_scaler,
        args.epochs,
        device,
    )

    mlp_pred, y_true = evaluate_neural_model(mlp_model, test_loader, target_scaler, device)
    lstm_pred, _ = evaluate_neural_model(lstm_model, test_loader, target_scaler, device)
    persistence_pred = test_seq["x_raw"][:, -1, 0]

    metrics_rows = []
    for model_name, prediction in [
        ("persistence", persistence_pred),
        ("mlp", mlp_pred),
        ("lstm", lstm_pred),
    ]:
        metrics = compute_metrics(y_true, prediction)
        metrics_rows.append({"model": model_name, **metrics})

    metrics_df = pd.DataFrame(metrics_rows).sort_values("rmse").reset_index(drop=True)
    predictions_df = pd.DataFrame(
        {
            "timestamp": test_seq["timestamp"],
            "actual": y_true,
            "persistence": persistence_pred,
            "mlp": mlp_pred,
            "lstm": lstm_pred,
        }
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    config_bits = []
    if args.resample_rule:
        config_bits.append(f"resample={args.resample_rule}")
    else:
        config_bits.append("resample=none")
    if time_feature_cols:
        config_bits.append("time_features=on")
    else:
        config_bits.append("time_features=off")
    config_bits.append(f"night_filter={'on' if args.filter_night else 'off'}")
    config_bits.append(f"input_features={len(feature_cols)}")

    metrics_path = output_dir / "metrics.csv"
    predictions_path = output_dir / "predictions.csv"
    plot_path = output_dir / "prediction_curve.png"
    report_path = output_dir / "report_snippet.md"
    checkpoint_path = output_dir / "best_lstm.pt"

    metrics_df.to_csv(metrics_path, index=False)
    predictions_df.to_csv(predictions_path, index=False)
    save_prediction_plot(plot_path, predictions_df)
    report_path.write_text(
        build_report_snippet(
            metrics_df,
            dataset_label,
            args.window_size,
            args.horizon,
            ", ".join(config_bits),
        ),
        encoding="utf-8-sig",
    )
    torch.save(lstm_model.state_dict(), checkpoint_path)

    print(f"Saved metrics to: {metrics_path}")
    print(f"Saved predictions to: {predictions_path}")
    print(f"Saved plot to: {plot_path}")
    print(f"Saved report snippet to: {report_path}")
    print(f"Saved LSTM checkpoint to: {checkpoint_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
