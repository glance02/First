# Photovoltaic Forecasting Experiment

这个目录提供一套适合课程报告的小实验代码，用于做光伏短时功率预测，并输出可直接写入报告的结果文件。

## 目标

- 对比 `Persistence`、`MLP`、`LSTM` 三种模型。
- 完成从数据读取、预处理、训练、评估到出图的完整流程。
- 自动生成以下文件到默认目录 `artifacts/pv_experiment/`：
  - `metrics.csv`
  - `predictions.csv`
  - `prediction_curve.png`
  - `report_snippet.md`
  - `best_lstm.pt`

## 建议依赖

你使用 `mamba` 管理环境的话，最小依赖可以按下面安装：

```bash
mamba install python pandas numpy pytorch pillow matplotlib -c pytorch -c conda-forge
```

说明：

- `matplotlib` 主要用于出图。
- 如果没有 `matplotlib`，脚本会自动退回到 `Pillow` 画图，仍然会输出 `prediction_curve.png`。
- 如果你要租显卡，确保 `pytorch` 与 CUDA 版本匹配即可。

## 输入数据格式

脚本默认需要一个 CSV 文件，至少包含两列：

- `timestamp`
- `power`

可选附加特征：

- `irradiance`
- `temperature`
- `humidity`

只要你的数据能映射到这些字段，脚本结构就不需要改。如果你用的是别的列名，可以通过命令行参数指定。

## 运行方式

### 0. 直接使用仓库里已经下载好的真实数据

仓库中已经放了一份公开真实小数据集，路径是：

- [light_pv_id00002_201801.csv](/e:/code/github/First/data/processed/light_pv_id00002_201801.csv)

推荐直接这样跑，这也是当前更适合写进报告的配置：

```bash
python experiments/pv_forecast.py \
  --data-path data/processed/light_pv_id00002_201801.csv \
  --time-col timestamp \
  --target-col power \
  --resample-rule 15min \
  --add-time-features \
  --window-size 16 \
  --horizon 2 \
  --epochs 25 \
  --hidden-size 64 \
  --output-dir artifacts/pv_experiment_light \
  --device cuda
```

数据来源与整理说明见 [README.md](/e:/code/github/First/data/README.md)。

这组参数的含义是：

- 先把 1 分钟数据重采样为 15 分钟数据。
- 使用过去 `16` 个时间步，也就是过去 `4` 小时的数据。
- 预测未来 `2` 个时间步，也就是未来 `30` 分钟的功率。
- 自动加入昼夜周期和周内周期的时间特征。

这样做的原因是：对原始 1 分钟单变量数据而言，`Persistence` 基线会非常强，深度学习模型不容易体现优势；而在 `15min` 重采样后的 `30` 分钟 ahead 设置下，图形会比 `1` 小时 ahead 更平滑，也更适合课程报告展示。

### 1. 无真实数据时的自测

```bash
python experiments/pv_forecast.py --demo-synthetic --epochs 10
```

在 synthetic 模式下，如果你没有显式传 `--feature-cols`，脚本会自动使用内置的 `irradiance`、`temperature` 和 `humidity` 三个特征。

### 2. 用真实光伏 CSV 跑实验

```bash
python experiments/pv_forecast.py \
  --data-path data/your_pv.csv \
  --time-col timestamp \
  --target-col power \
  --feature-cols irradiance,temperature,humidity \
  --window-size 8 \
  --horizon 1 \
  --epochs 40 \
  --batch-size 64 \
  --hidden-size 64 \
  --device cuda
```

如果你暂时只想用历史功率一个变量，也可以不传 `--feature-cols`：

```bash
python experiments/pv_forecast.py --data-path data/your_pv.csv --epochs 40
```

## 参数说明

- `--data-path`：真实数据 CSV 路径。
- `--time-col`：时间列名，默认 `timestamp`。
- `--target-col`：目标列名，默认 `power`。
- `--feature-cols`：额外特征列，多个特征用逗号分隔。
- `--window-size`：历史窗口长度，默认 `8`。
- `--horizon`：预测步长，默认 `1`。
- `--epochs`：训练轮数，默认 `40`。
- `--batch-size`：批大小，默认 `64`。
- `--hidden-size`：隐藏层宽度，默认 `64`。
- `--resample-rule`：重采样规则，例如 `15min`、`30min`、`1h`。
- `--add-time-features`：自动加入时间周期特征，如昼夜周期和周内周期。
- `--device`：`auto`、`cpu` 或 `cuda`。
- `--output-dir`：输出目录，默认 `artifacts/pv_experiment`。
- `--demo-synthetic`：启用内置 synthetic 数据。

脚本会自动识别时间间隔的断点，不会跨越长缺失段或被过滤掉的夜间区段去拼接训练窗口。这一点对 LSTM 这类序列模型尤其重要。

## 输出如何写回报告

你可以把生成结果按下面方式填回 [`smart_energy_report.md`](/e:/code/github/First/smart_energy_report.md)：

- 把 `metrics.csv` 的结果填入“表 3”。
- 直接插入 `prediction_curve.png` 作为“图 2”。
- 把 `report_snippet.md` 的文字贴到报告第 4 节“实验结果与分析”部分。

## 数据建议

如果你后面想换成真实公开数据，优先选择时间戳清晰、功率列完整、白天出力明显的数据源。对课程实验来说，最重要的不是电站规模，而是：

- 时间序列连续
- 缺失值不要太多
- 至少覆盖几周到几个月
- 最好附带辐照度或温度等气象特征

只要满足这些条件，就足够支撑一份课程报告中的实验部分。
