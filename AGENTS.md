# Repository Guidelines

## 项目结构与模块组织
当前分支的核心目录如下：

- `experiments/`：可运行的 Python 实验脚本，当前主要是 `pv_forecast.py`。
- `data/raw/`：原始下载数据。
- `data/processed/`：清洗后的实验输入数据。
- `artifacts/`：实验输出结果，如 `metrics.csv`、`predictions.csv`、模型权重和图表。
- 根目录文档：`README.md`、`smart_energy_report.md` 等说明和报告文件。

`artifacts/` 下的内容应视为生成物，尽量通过脚本重新生成，不要直接手工修改。

## 构建、测试与开发命令
仓库当前没有独立的构建系统，主要直接运行 Python 脚本：

- `python experiments/pv_forecast.py --demo-synthetic --epochs 10`：使用合成数据做快速自测。
- `python experiments/pv_forecast.py --data-path data/processed/light_pv_id00002_201801.csv --resample-rule 15min --add-time-features --window-size 20 --horizon 2 --epochs 40 --batch-size 32 --hidden-size 128 --output-dir artifacts/pv_experiment_light --device cpu`：推荐的真实数据实验命令。
- `mamba install python pandas numpy pytorch pillow matplotlib -c pytorch -c conda-forge`：按 `experiments/README.md` 安装最小依赖。

请在仓库根目录执行命令，避免相对路径失效。

## 代码风格与命名规范
保持与 `experiments/pv_forecast.py` 一致的风格：

- Python 使用 4 空格缩进，遵循 PEP 8。
- 函数、变量、命令行参数、文件名使用 `snake_case`。
- 类名使用 `PascalCase`，例如 `Standardizer`、`LSTMRegressor`。
- 优先拆分为清晰的小函数，避免把预处理、训练、评估逻辑堆在同一段代码里。

## 测试规范
当前仓库没有单独的 `tests/` 目录，测试以可复现实验运行为主：

- 提交前至少运行一次 synthetic 模式，确认脚本可执行。
- 修改数据流程或参数后，建议输出到新的 `artifacts/<run_name>/` 目录，避免覆盖已有结果。
- 最少检查 `metrics.csv`、`predictions.csv`、`prediction_curve.png` 是否成功生成。
