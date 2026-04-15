### 实验结果摘要

本实验使用 `light_pv_id00002_201801.csv` 数据，采用长度为 `16` 的历史窗口预测未来 `4` 个时间步后的光伏功率。
对比模型包括 Persistence、MLP 和 LSTM，评价指标为 MAE、RMSE 与 MAPE。
实验设置：resample=15min, time_features=on, input_features=5。

| Model | MAE | RMSE | MAPE(%) |
| --- | ---: | ---: | ---: |
| LSTM | 0.3150 | 0.5390 | 36.57 |
| MLP | 0.3765 | 0.5502 | 43.86 |
| PERSISTENCE | 0.5931 | 0.7185 | 159.17 |

测试结果显示，`LSTM` 在 RMSE 指标上表现最好。
相较于 Persistence 基线，LSTM 的 RMSE 下降约 `24.99%`，说明其能够更好地刻画光伏功率的时间依赖性。
建议将上表替换到报告的“表3”，并把同目录下的 `prediction_curve.png` 作为“图2”插入。
