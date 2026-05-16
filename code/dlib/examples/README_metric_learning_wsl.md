# dlib 度量学习示例 WSL 复现实验

本文记录 `dnn_metric_learning_on_images_ex.cpp` 在 WSL Ubuntu 环境下的编译、运行、重新训练和日志保存流程。该流程用于课程实验复现，目标是跑通 dlib 深度度量学习训练链路，而不是训练生产级人脸识别模型。

## 1. 实验文件

- 示例源码：`dnn_metric_learning_on_images_ex.cpp`
- 自带数据集：`johns/`
- 构建目录：`build-wsl/`
- 训练同步文件：`face_metric_sync`、`face_metric_sync_`
- 最终模型文件：`metric_network_renset.dat`
- 训练日志文件：`train.log`

`johns/` 数据集按身份目录组织，每个子目录代表一个人，目录内图片属于同一身份。程序会读取这些目录，并在训练时构造包含多个身份和多张图片的 mini-batch。

## 2. WSL 环境检查

进入 WSL 后检查工具：

```bash
gcc --version
g++ --version
cmake --version
```

如果缺少基础编译工具，安装：

```bash
sudo apt update
sudo apt install -y build-essential cmake
```

可选安装 OpenBLAS/LAPACK，用于让 dlib 使用优化线性代数库：

```bash
sudo apt install -y libopenblas-dev liblapack-dev
```

安装后需要重新运行 CMake 配置，原有构建目录不会自动识别新库。

## 3. 配置与编译

进入 examples 目录：

```bash
cd /mnt/d/code/First/code/dlib/examples
```

如果 `build-wsl/` 为空或构建缓存异常，重新创建：

```bash
rm -rf build-wsl
mkdir build-wsl
cd build-wsl
```

配置项目：

```bash
cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_AVX_INSTRUCTIONS=1
```

参数说明：

- `..`：源码目录是当前构建目录的上一级，即 `examples/`。
- `-DCMAKE_BUILD_TYPE=Release`：使用 Release 优化编译。
- `-DUSE_AVX_INSTRUCTIONS=1`：启用 AVX 指令优化，前提是 CPU 支持 AVX。

编译目标程序：

```bash
cmake --build . --target dnn_metric_learning_on_images_ex -j4
```

参数说明：

- `--build .`：在当前构建目录执行编译。
- `--target dnn_metric_learning_on_images_ex`：只编译该示例程序，不编译全部 examples。
- `-j4`：使用 4 个并行任务编译。

如果出现 `Error: could not load cache`，说明当前目录不是有效构建目录，或缺少 `CMakeCache.txt`。回到上面的“重新创建 build-wsl”步骤即可。

## 4. 课程实验版源码改动

原始示例的停止条件较严格，需要学习率降低到 `1e-4` 以下才结束。为了课程实验更快进入模型保存和验证阶段，可以把源码改成固定最大训练步数。

已采用的改动：

```cpp
trainer.set_iterations_without_progress_threshold(80);
const unsigned long max_training_steps = 500;
```

训练循环改为：

```cpp
while(trainer.get_learning_rate() >= 1e-4 && trainer.get_train_one_step_calls() < max_training_steps)
{
    qimages.dequeue(images);
    qlabels.dequeue(labels);
    trainer.train_one_step(images, labels);
}
cout << "training steps: " << trainer.get_train_one_step_calls() << endl;
```

这样程序最多训练 500 个 step，然后正常进入 `done training`、模型保存和 `num_right/num_wrong` 验证阶段。若 500 步仍太久，可以把 `max_training_steps` 改为 300。

修改源码后必须重新编译：

```bash
cd /mnt/d/code/First/code/dlib/examples/build-wsl
cmake --build . --target dnn_metric_learning_on_images_ex -j4
```

## 5. 重新训练

如果要从头重新训练，先删除旧同步文件和旧模型：

```bash
cd /mnt/d/code/First/code/dlib/examples
rm -f face_metric_sync face_metric_sync_ metric_network_renset.dat train.log
```

运行训练并保存日志：

```bash
./build-wsl/dnn_metric_learning_on_images_ex ./johns 2>&1 | tee train.log
```

参数说明：

- `./build-wsl/dnn_metric_learning_on_images_ex`：运行编译得到的示例程序。
- `./johns`：传入示例数据集目录。
- `2>&1`：把标准错误合并到标准输出。
- `| tee train.log`：终端显示训练日志，同时保存到 `train.log`。

如果要继续保存到已有日志末尾，用：

```bash
./build-wsl/dnn_metric_learning_on_images_ex ./johns 2>&1 | tee -a train.log
```

## 6. 训练输出解读

训练开始会输出：

```text
objs.size(): 5
```

表示读取到 5 个身份目录。

训练中会输出类似：

```text
step#: 400   learning rate: 0.1   average loss: 0.000188676  steps without apparent progress: 90
Saved state to face_metric_sync
```

含义：

- `step#`：已经训练的 step 数。
- `learning rate`：当前学习率。
- `average loss`：近期平均损失。
- `steps without apparent progress`：dlib 判断没有明显进步的累计步数。
- `Saved state to face_metric_sync`：保存训练器同步状态。

训练完成后应看到：

```text
training steps: 500
done training
num_right: ...
num_wrong: ...
```

其中：

- `metric_network_renset.dat`：最终模型文件。
- `face_metric_sync`、`face_metric_sync_`：中断恢复用同步文件。
- `num_right`、`num_wrong`：程序在一个随机 mini-batch 上做两两距离判断的结果。

需要注意，`num_right/num_wrong` 只是训练数据上的一次随机 batch 验证，不能等同于独立测试集准确率。

## 7. 常见问题

### 7.1 缺少 GUI/X11

CMake 可能提示：

```text
DLIB GUI SUPPORT DISABLED BECAUSE X11 DEVELOPMENT LIBRARIES NOT FOUND
```

该示例不需要 GUI，可以忽略。需要 GUI 示例时再安装：

```bash
sudo apt install -y libx11-dev
```

### 7.2 缺少 BLAS/LAPACK

CMake 可能提示：

```text
No BLAS library found so using dlib's built in BLAS.
```

这不是错误，只是速度可能较慢。可安装：

```bash
sudo apt install -y libopenblas-dev liblapack-dev
```

然后删除 `build-wsl/` 并重新配置。

### 7.3 Clock skew detected

在 `/mnt/d` 这种 Windows 挂载目录中构建时，可能出现：

```text
Clock skew detected. Your build may be incomplete.
```

通常是 Windows 文件系统和 WSL 时间戳略有偏差。如果编译已成功，可先忽略；若反复出现异常，可以删除 `build-wsl/` 重新构建，或把项目复制到 WSL Linux 文件系统中编译。

### 7.4 serialization_error

如果运行时出现：

```text
Error deserializing object of type int
```

先删除旧同步文件：

```bash
rm -f face_metric_sync face_metric_sync_
```

如果仍然出现，检查数据集中是否混入非图片文件：

```bash
find johns -type f | sort
```

`load_objects_list()` 会把子目录中的文件路径都加入列表，若混入非图片文件，后续 `load_image()` 可能失败。

## 8. 报告记录建议

报告中建议保留以下证据：

- CMake 配置成功截图或文字记录。
- 编译完成信息。
- 训练日志中若干 `step#` 行。
- `Saved state to face_metric_sync` 说明同步文件保存。
- `training steps`、`done training`、`num_right`、`num_wrong`。
- `metric_network_renset.dat` 文件生成情况。

实验结论应表述为：本实验复现了 dlib 深度度量学习示例的训练、保存和简单验证流程。由于 `johns/` 数据集规模很小，且验证样本仍来自训练数据目录，结果只能说明示例流程能够运行，不能代表模型具备真实场景泛化能力。
