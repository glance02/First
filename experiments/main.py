"""PV forecasting experiment entrypoint.

参数说明：

- --data-path：真实数据 CSV 路径，默认 data/processed/light_pv_id00002_201801.csv。
- --time-col：时间列名，默认 timestamp。
- --target-col：目标列名，默认 power。
- --feature-cols：额外特征列，多个特征用逗号分隔。
- --window-size：历史窗口长度，默认 12。
- --horizon：预测步长，默认 2。
- --epochs：训练轮数，默认 40。
- --batch-size：批大小，默认 32。
- --hidden-size：隐藏层宽度，默认 128。
- --resample-rule：重采样规则，例如 15min、30min、1h，默认 45min。
- --add-time-features：自动加入时间周期特征，默认开启，可用 --no-add-time-features 关闭。
- --filter-night：可选开启夜间低功率区段过滤，默认关闭。
- --device：cpu 或 cuda，默认 cuda。
- --output-dir：输出目录，默认 artifacts/pv_experiment_light。
- --demo-synthetic：启用内置 synthetic 数据。
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


DEFAULT_DATA_PATH = Path("data/processed/light_pv_id00002_201801.csv")
DEFAULT_TIME_COL = "timestamp"
DEFAULT_TARGET_COL = "power"
DEFAULT_WINDOW_SIZE = 12
DEFAULT_HORIZON = 2
DEFAULT_EPOCHS = 40
DEFAULT_BATCH_SIZE = 32
DEFAULT_HIDDEN_SIZE = 128
DEFAULT_RESAMPLE_RULE = "45min"
DEFAULT_DEVICE = "cuda"
DEFAULT_OUTPUT_DIR = Path("artifacts/pv_experiment_light")
DEFAULT_CONFIG_NAME = "experiment_config.json"
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
    parser.add_argument("--data-path", type=str, default=str(DEFAULT_DATA_PATH))
    parser.add_argument("--time-col", type=str, default=DEFAULT_TIME_COL)
    parser.add_argument("--target-col", type=str, default=DEFAULT_TARGET_COL)
    parser.add_argument("--feature-cols", type=str, default="")
    parser.add_argument("--window-size", type=int, default=DEFAULT_WINDOW_SIZE)
    parser.add_argument("--horizon", type=int, default=DEFAULT_HORIZON)
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--hidden-size", type=int, default=DEFAULT_HIDDEN_SIZE)
    parser.add_argument("--resample-rule", type=str, default=DEFAULT_RESAMPLE_RULE)
    parser.add_argument("--add-time-features", dest="add_time_features", action="store_true")
    parser.add_argument("--no-add-time-features", dest="add_time_features", action="store_false")
    parser.set_defaults(add_time_features=True)
    parser.add_argument("--filter-night", action="store_true")
    parser.add_argument("--device", type=str, default=DEFAULT_DEVICE)
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


def build_config_summary(
    resample_rule: str,
    time_feature_cols: list[str],
    filter_night: bool,
    feature_cols: list[str],
) -> str:
    config_bits = [f"resample={resample_rule or 'none'}"]
    config_bits.append(f"time_features={'on' if time_feature_cols else 'off'}")
    config_bits.append(f"night_filter={'on' if filter_night else 'off'}")
    config_bits.append(f"input_features={len(feature_cols)}")
    return ", ".join(config_bits)


def build_experiment_config(
    args: argparse.Namespace,
    dataset_label: str,
    device: torch.device,
    feature_cols: list[str],
    extra_features: list[str],
    time_feature_cols: list[str],
    row_count: int,
) -> dict[str, object]:
    return {
        "dataset_label": dataset_label,
        "data_path": args.data_path,
        "time_col": args.time_col,
        "target_col": args.target_col,
        "extra_features": extra_features,
        "time_feature_cols": time_feature_cols,
        "feature_cols": feature_cols,
        "window_size": args.window_size,
        "horizon": args.horizon,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "hidden_size": args.hidden_size,
        "resample_rule": args.resample_rule,
        "add_time_features": args.add_time_features,
        "filter_night": args.filter_night,
        "demo_synthetic": args.demo_synthetic,
        "seed": args.seed,
        "device": str(device),
        "row_count_after_preprocessing": row_count,
        "input_feature_count": len(feature_cols),
        "config_summary": build_config_summary(
            args.resample_rule,
            time_feature_cols,
            args.filter_night,
            feature_cols,
        ),
    }


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

    metrics_path = output_dir / "metrics.csv"
    predictions_path = output_dir / "predictions.csv"
    checkpoint_path = output_dir / "best_lstm.pt"
    config_path = output_dir / DEFAULT_CONFIG_NAME

    metrics_df.to_csv(metrics_path, index=False)
    predictions_df.to_csv(predictions_path, index=False)
    torch.save(lstm_model.state_dict(), checkpoint_path)

    config = build_experiment_config(
        args,
        dataset_label,
        device,
        feature_cols,
        extra_features,
        time_feature_cols,
        len(frame),
    )
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8-sig",
    )

    print("Experiment metrics:")
    print(metrics_df.to_string(index=False))
    print(f"Saved metrics to: {metrics_path}")
    print(f"Saved predictions to: {predictions_path}")
    print(f"Saved config to: {config_path}")
    print(f"Saved LSTM checkpoint to: {checkpoint_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
