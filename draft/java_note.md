# java笔记
## 语言基础
### 类型转换
1. 小容量向大容量转换，称为**自动类型转换**，容量从小到大排序：
    >byte < short ，char < int < long < float < double
2. 大容量转换成小容量，叫做**强制类型转换**，需要加强制类型转换符，程序才能编译通过，但是在运行阶段可能会损失精度，所以谨慎使用。   如：
    ```
    double d = 3.14;
    int i = (int) d;
    ```
3. byte，short，char混合运算的时候，各自先转换成int类型再做运算。比int大的就不会转。
4. 多种数据类型混合运算，先转换成容量最大的那种类型再做运算。

### 运算符
1. **逻辑运算符**

| 逻辑运算符 | 解释 |
|:-----------:|:-----------------------------------------------------------:|
| &           | 逻辑与（两边的算子都是true，结果才是true）                  |
| !           | 逻辑非（取反，! false就是true，! true就是假，这是一个单目运算符）|
| ^           | 逻辑异或（两边的算子只要不一样，结果就是true）                |
| &&          | 短路与（第一个表达式执行结果是false，会发生短路与）            |
| \|          | 逻辑或（两边的算子只要有一个是true，结果就是true）            |
| \|\|        | 短路或（第一个表达式执行结果是true，会发生短路或）            |

1. **字符串连接运算符**
    +运算符在java语言中当中有两个作用
    - 加法
    - 字符串连接。可以将字符串和非字符串数据直接连接起来

2. **三元运算符/三目运算符/条件运算符**
   >布尔表达式？表达式1：表达式2

   如：
   `String result = a > c ? "a大于c" : "a小于等于c";`
   
### 其他
- 所有浮点字面值，比如3.14，都是double型，如果想把这个浮点字面值当作float来处理，应该在其后面添加f/F，如3.14f
- 变量的作用域只要记住一句话：出了大括号就不认识了。

## 容器
### ArrayLIst

## GUI编程
企业几乎不用java来写图形界面

java提供两套GUI编程包
1. AWT，在windows上使用，现在几乎不用
2. Swing，基于AWT，提供了更丰富的组件，不依赖于本地串口系统

## SWing
### 常用组件
- JFrame:窗口
- JPanel:用于组织其他组件的容器
- JButton:按钮组件
- JTextField:输入框
- JTable: 表格
- JLabel: 文本栏

### 布局管理器
目前常见的有四种
1. FlowLayout，流式布局管理
    ```java
    JLabel label3=new JLabel("请输入一元二次方程的系数c：");
    jf.add(label3);
    ```
2. BorderLayout，将容器划分为东、南、西、北、中五个区域
   `jf.add(new Button("请输入一元二次方程的系数a："),BorderLayout.NORTH);`
3. GridLayout，网格布局管理器
   `jf.setLayout(new GridLayout(2,3));`
   `jf.add(new JButton("请输入一元二次方程的系数a："));`
4. BoxLayout,盒子布局，可以做竖向布局，配合panel使用
    ` JPanel panel=new JPanel();`
    `panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));`
    `panel.add(new JButton("Button 1"));`

### 事件监听
常用的有两个事件监听器：
- 点击事件监听
- 按键事件监听
#### 点击事件监听器ActionListener
```java
clearButton.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        textA.setText("");
        textB.setText("");
        textC.setText("");
    }
});
```

#### 按键事件监听器
```java
//按键事件监听器
jf.addKeyListener(new KeyAdapter() {
    @Override
    public void keyPressed(KeyEvent e) {
        //每个键帽都有一个编号
        int keycode =e.getKeyCode();
        if (keycode == KeyEvent.VK_UP) {
            System.out.println("Up arrow key pressed");
        }
    }
})

//记得让窗口成为焦点
jf.requestFocus();
```

#### 事件监听的三种写法
1. 使用匿名内部类
```java
// 按钮事件处理，使用匿名内部类
solveButton.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            double a = Double.parseDouble(textA.getText());
            double b = Double.parseDouble(textB.getText());
            double c = Double.parseDouble(textC.getText());
            f equation = new f(a, b, c);
            String result = equation.cal();
            JOptionPane.showMessageDialog(jf, result, "求解结果", JOptionPanINFORMATION_MESSAGE);
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(jf, "请输入有效的数字", "输入错误", JOptionPanERROR_MESSAGE);
        }
    }
});
```
2. 使用lambda
```java
// 使用 Lambda 表达式
clearButton.addActionListener(e -> {
    textA.setText("");
    textB.setText("");
    textC.setText("");
});
```
3. 事件源合而为一
```java
//与事件源合二为一
        JButton exitButton = new JButton("退出"){
            @Override
            protected void fireActionPerformed(ActionEvent event) {
                System.exit(0);
            }
        };
```
### 示例代码

代码太长了，直接贴个文件得了

[一元二次方程求解GUI](./t3.java)
