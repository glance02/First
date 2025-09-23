# 项目概述

此目录包含一个使用 C++ 编写的项目，主要实现大整数（高精度）的基本算术运算。项目中包含了加法、减法和乘法的实现。这些程序使用 `vector<int>` 来存储大整数的每一位，从而可以处理超出标准整数类型范围的数字。

## 文件说明

- `ac791.cpp`: 实现了大整数加法运算。
- `ac792.cpp`: 实现了大整数减法运算。
- `ac793.cpp`: 实现了大整数与单个整数的乘法运算。
- `.vscode/`: 包含 VS Code 的配置文件，用于编译和调试项目。

## 构建和运行

项目使用 `g++` 编译器进行编译。VS Code 的任务配置文件 `.vscode/tasks.json` 提供了默认的构建任务。

### 构建命令

```bash
g++ -fdiagnostics-color=always -g <source_file.cpp> -o <output_file.exe>
```

例如，编译 `ac791.cpp`：

```bash
g++ -fdiagnostics-color=always -g ac791.cpp -o ac791.exe
```

### 运行

编译后，可以直接运行生成的 `.exe` 文件。

```bash
./ac791.exe
```

## 开发约定

- 使用 `vector<int>` 存储大整数，低位在前，高位在后。
- 所有源文件都包含必要的头文件，如 `<iostream>` 和 `<vector>`。
- 代码风格遵循常见的 C++ 编码规范，使用 `using namespace std;` 简化代码。 