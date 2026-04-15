### 实验结果摘要

本实验使用 `light_pv_id00002_201801.csv` 数据，采用长度为 `24` 的历史窗口预测未来 `2` 个时间步后的光伏功率。
对比模型包括 Persistence、MLP 和 LSTM，评价指标为 MAE、RMSE 与 MAPE。
实验设置：resample=15min, time_features=on, input_features=5。

| Model | MAE | RMSE | MAPE(%) |
| --- | ---: | ---: | ---: |
| PERSISTENCE | 0.3551 | 0.5034 | 107.75 |
| MLP | 0.3640 | 0.5451 | 57.02 |
| LSTM | 0.3519 | 0.5563 | 55.03 |

测试结果显示，`PERSISTENCE` 在 RMSE 指标上表现最好。
本次实验中 LSTM 与基线模型差距有限，这通常与数据规模、输入特征数量、天气突变程度以及夜间样本处理方式有关。
建议将上表替换到报告的“表3”，并把同目录下的 `prediction_curve.png` 作为“图2”插入。
