### 实验结果摘要

本实验使用 `light_pv_id00002_201801.csv` 数据，采用长度为 `12` 的历史窗口预测未来 `2` 个时间步后的光伏功率。
对比模型包括 Persistence、MLP 和 LSTM，评价指标为 MAE、RMSE 与 MAPE。
实验设置：resample=45min, time_features=on, night_filter=off, input_features=5。

| Model | MAE | RMSE | MAPE(%) |
| --- | ---: | ---: | ---: |
| LSTM | 0.1951 | 0.3630 | 56.49 |
| PERSISTENCE | 0.2306 | 0.4186 | 139.77 |
| MLP | 0.2538 | 0.4424 | 64.61 |

测试结果显示，`LSTM` 在 RMSE 指标上表现最好。
相较于 Persistence 基线，LSTM 的 RMSE 下降约 `13.28%`，说明其能够更好地刻画光伏功率的时间依赖性。
建议将上表替换到报告的“表3”，并把同目录下的 `prediction_curve.png` 作为“图2”插入。
