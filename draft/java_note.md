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

## 常用类
### ArrayLIst - 泛型集合


### Collection - 单列集合

Collection是所有单列集合的祖宗类，有一些通用的功能。使用时候需要`import java.util.Collection;`

考试的时候可以直接`import java.util.*`

| 方法名                  | 说明                           |
|-------------------------|--------------------------------|
| add(E e)                | 向集合中添加元素               |
| addAll(Collection<? extends E> c) | 添加一个集合中的所有元素 |
| remove(Object o)        | 移除指定元素                   |
| removeAll(Collection<?> c) | 移除集合中所有与指定集合相同的元素 |
| clear()                 | 清空集合中的所有元素           |
| isEmpty()               | 判断集合是否为空               |
| size()                  | 返回集合中元素的个数           |
| toArray()               | 将集合转换为数组               |
| contains(Object o)      | 判断集合是否包含指定元素        |
| containsAll(Collection<?> c) | 判断集合是否包含指定集合的所有元素 |
| iterator()              | 返回集合的迭代器               |
| retainAll(Collection<?> c) | 只保留集合中与指定集合相同的元素 |

**第一种遍历**，使用Iterator

对于iterator，当然也需要`import java.util.Iterator`，迭代器类有两个常用的函数：
1. `next()`，返回当前索引的值并且使得指针加一，类似于`it++`
2. `hasNext()`，返回是否可以往后移
3. `remove()`，删除当前迭代器所指的元素
用该方法删除元素不会出现并发问题

**第二种遍历**，增强for循环，代码如下：
```java
for (String s : list) {
    System.out.println(s);
}
```

**第三种遍历**，使用forEach方法，可以使用lambda简化
```java
//最原始的使用
list.forEach(new Consumer<String>() {
    public void accept(String s) {
        System.out.println(s);
    }
});
//简化
list.forEach(s->System.out.println(s));
//再简化
list.forEach(System.out::println);
```

#### List集合
有序，可重复，有索引。Collection的所有功能都有。
需要`import java.util.List`
1. 定义集合
   ```java
    List<String> list=new ArrayList<>();
    //添加数据
    list.add("Hello");
    list.add("World");
    list.add(2,"whee!");//List特殊的add方式
    //直接打印ArrayList
    System.out.println(list);//[Hello, World]
   ```

2. 查看数据
   ```java
    String s1=list.get(0);
    System.out.println(s1);
    System.out.println(list.get(1));
   ```

3. 删除数据。有两种使用方式。
    ```java
    String removed = list.remove(0);//返回被删除数据的具体值
    System.out.println(removed);//Hello
    ```

4. 修改数据
   ```java
    list.set(0,"Java");
    System.out.println(list.get(0));//Java
   ```

5. `toArray()`：转为数组，有两种用法。

   第一种是直接使用Object来接收。`Object[] arr = list.toArray();`

   第二种是指定类型。`String[] arr=list.toArray(new String[0]);`

   注意，两种方法后续使用也有区别，第一种需要使用Object来接收值，第二种使用String。
6.  `indexOf(Object o)`：返回元素第一次出现的位置
7.  `lastIndexOf(Object o)`：返回元素最后一次出现的位置
8.  l`istIterator() `和 `listIterator(int index)`：返回 ListIterator，支持双向遍历、previous、set、add 等
9.  `sort(Comparator<? super E> c)`：就地排序（Java 8+）

##### ArrayList
基于数组存储数据，有如下特点：
1. 查询速度快，查询任意数据耗时相同
2. 增删效率低

##### LinkedList
基于双链表存储数据，有如下的特点：
1. 查询速度慢
2. 增删相对较快

新增了许多首位操作特有的办法
| 方法名                           | 作用说明                   |
|----------------------------------|----------------------------|
| addFirst(E e)                    | 在头部添加元素             |
| addLast(E e)                     | 在尾部添加元素             |
| getFirst()                       | 获取头部元素               |
| getLast()                        | 获取尾部元素               |
| removeFirst()                    | 移除并返回头部元素         |
| removeLast()                     | 移除并返回尾部元素         |
| offerFirst(E e)                  | 在头部插入元素（队列语义） |
| offerLast(E e)                   | 在尾部插入元素（队列语义） |
| pollFirst()                      | 移除并返回头部元素         |
| pollLast()                       | 移除并返回尾部元素         |
| peekFirst()                      | 查看头部元素，不移除       |
| peekLast()                       | 查看尾部元素，不移除       |
| push(E e)                        | 作为栈顶压入元素           |
| pop()                            | 作为栈顶弹出元素           |
| descendingIterator()             | 反向迭代器（从尾到头）     |

#### Set集合
无序（添加数据的顺序和获取数据的顺序不一致），无索引，不重复。由于set无索引，所以大部分功能都来自于Collection。

##### HashSet
基于哈希表实现的一个Set容器

##### LinkedHashSet
有序的集合

##### TreeSet
基于红黑树实现的集合，会自动排序，默认按照从小到大排序,如果是字符串，则按照字典序排序


### Map - 双列集合
考试不考好像，嘻嘻。


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
