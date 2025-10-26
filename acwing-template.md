## 基础算法

### 快速排序
```cpp
void quick_sort(int q[],int l,int r){
    //递归函数首先考虑的都是退出条件
    if(l>=r) return;

    //定义需要的变量
    int i=l-1,j=r+1,x=q[l+r>>1];
    while(i<j){
        //左边的都小于x，右边的都大于x
        while(q[i]<x) ++i;
        while(q[j]>x) ++j;
        if(i<j) swap(q[i],q[j]);
    }
    //递归再找一遍
    quick_sort(q,l,j);
    quick_sort(q,j+1,r);
}
```

### 归并排序

### 整数二分搜索
```cpp
int b_search1(int q[],int l,int r){
    //二分查找不是递归算法，所以不用优先考虑退出条件
    while(l<r){
        int mid=l+r>>1;
        if(check()) r=mid;
        else l=mid+1;//总之l要在r的右边
    }
    return l;//最后l和r是相同的
}

int b_search2(int q[],int l,int r){
    //第二种情况，关键在于r还是l取mid
    while(l<r){
        int mid=l+r+1>>1;//l取mid的话，这里要+1，至于为啥我也不懂，背就是了
        if(check()) l=mid;
        else r=mid-1;
    }
}
```

### 浮点数二分
```cpp
double b_search3(double l,double r){
    const double esp=1e-8;
    while(r-l>esp){//通过精度控制，也可以用for循环算一百次
        double mid=(l+r)/2;
        if(check()) r=mid;
        else l=mid;//浮点数二分不用像整数那样仔细地考虑边界
    }
    return l;
}
```

### 高精度加法
```cpp
vector<int> add(vector<int>&A,vector<int>&B){//使用引用加快传参速度
    //A的位数更多的加法
    if(A.size()<B.size()) return add(B,A);

    int t=0;
    vector<int>C;//存储结果
    for(int i=0;i<A.size();i++){
        //先把i位两个数字加上，注意要加B的前提是B对应位上有数字
        t+=A[i];
        if(i<B.size()) t+=B[i];
        //放进C中
        C.push_back(t%10);
        t/=10;
    }

    //检查要不要给最高位进位
    if(t) C.push_back(1);

    return C;
}
```

### 高精度减法
```csharp
//减法要有一定的前提，A>=B，A>0,B>0
vector<int> sub(vector<int>&A,vector<int>&B){
    vector<int>C;
    int t=0;

    for(int i=0;i<A.size();i++){
        //先减借位,再减B
        t=A[i]-t;
        if(i<B.size()) t-=B[i];
        //处理C
        C.push_back((t+10)%10);
        //处理t
        if(t<0) t=1;
        else t=0;
    }

    //去除前导零
    while(C.size()>1&&C.back()==0) C.pop_back();
    
    return C;
}
```

### 高精度乘法
高精度乘低精度
```csharp
vector<int> mul(vector<int>&A,int b){
    vector<int>C;
    int t=0;//进位用

    for(int i=0;i<A.size();i++){
        t+=A[i]*b;
        C.push_back(t%10);
        t/=10;
    }
    //对剩下的t进行处理，这里t可能有多位，所以得用while
    while(t){
        C.push_back(t%10);
        t/=10;
    }
    //去除前导零
    while(C.size()>1&&C.back()==0) C.pop_back();

    return C;
}
```

### 高精度除法
高精度除以低精度
```csharp
//除法多一个余数r，r可以使用引用，这样可以直接对本体的r进行修改
vector<int> div(vector<int> &A,int b,int &r){
    vector<int>C;
    r=0;//最开始余数为0

    //除法一般从高位算起
    for(int i=A.size()-1;i>=0;i--){
        r=r*10+A[i];
        C.push_back(r/b);//上位
        r%=b;//相减得到下一次的余数
    }

    //此时的C是高位在前，需要反转
    reverse(C.begin(),C.end());

    //去除前导零
    while(C.size()>1&&C.back()==0) C.pop_back();

    return C;
}
```

### 一维前缀和
```csharp
s[i] = a[1] + a[2] + ... a[i]
a[l] + ... + a[r] = s[r] - s[l - 1]//这边l要多往左边减一个
```

### 二维前缀和
```csharp
s[i][j] = 第i行j列格子左上部分所有元素的和
以(x1, y1)为左上角，(x2, y2)为右下角的子矩阵的和为：
s[x2][y2] - s[x1][1, y2] - s[x2][y1 - 1] + s[x1 - 1][y1 - 1]
```

### 一维差分
一维的差分数组上的一个数，可以理解成原数组上前一个数给当前数的影响。
```csharp
给区间[l, r]中的每个数加上c：B[l] += c, B[r + 1] -= c
```

### 二维差分
二维的差分矩阵上的值可以理解成原矩阵左上两个相邻的数的影响再加上一个补偿值（多减去的那一部分）
```csharp
给以(x1, y1)为左上角，(x2, y2)为右下角的子矩阵中的所有元素加上c：
S[x1, y1] += c, S[x2 + 1, y1] -= c, S[x1, y2 + 1] -= c, S[x2 + 1, y2 + 1] += c
```

### 位运算
```csharp
求n的第k位数字: n >> k & 1
返回n的最后一位1：lowbit(n) = n & -n
```

### 离散化
```csharp
vector<int>alls;//存储所有离散化的值，类似于一个映射表，把所有需要的值存进数组当中
sort(alls.begin(),alls.end());//排序，默认是从小到大排序
alls.erase(unique(alls.begin(),alls.end()),alls.end());//去重

//利用二分查找，在离散数组当中查找对应的下标
int find(int x){
    int l=0,r=alls.size()-1;//左右两边正好是两个端点
    while(l<r){
        int mid=l+r>>1;
        if(alls[mid]>=x) r=mid;//这里为什么又是等于
        else l=mid+1;
    }

    return l+1;//返回从1开始的下标。
}
```

### 区间合并
```csharp
// 将所有存在交集的区间合并
void merge(vector<PII> &segs)
{
    vector<PII> res;

    sort(segs.begin(), segs.end());

    int st = -2e9, ed = -2e9;
    for (auto seg : segs)
        if (ed < seg.first)
        {
            if (st != -2e9) res.push_back({st, ed});
            st = seg.first, ed = seg.second;
        }
        else ed = max(ed, seg.second);

    if (st != -2e9) res.push_back({st, ed});

    segs = res;
}
```

## 数据结构
### 并查集
并查集最重要的就是find函数，如下：

```cpp
//找到x的根节点，并优化路径
int find(int x){
    if(p[x]!=x) p[x]=find(p[x]);
    return p[x];
}
```

### 堆

手写堆最重要的两个操作

```csharp
void down(int x){
    //t用来存x的左右两个儿子中最小的数的下标
    int t=x;

    if(x*2<=cnt&&h[x*2]<h[t]) t=x*2;
    if(x*2+1<=cnt&&h[x*2+1]<h[t]) t=x*2+1;

    if(t!=x){
        //如果下标改变了，说明要更换两个数的位置
        swap(h[x],h[t]);
        //此时x已经换到t处，然后要对t再进行递归更换
        down(t);
    }
}

void up(int x){
    while(x/2>0&&h[x/2]>h[x]){
        swap(h[x/2],h[x]);
        x/=2;
    }
}
```

### 哈希表

哈希表有两种解决冲突的办法

1. 第一种是拉链法

```csharp
//N的设置上面选择质数冲突的概率小
const int N=1e5+3;
int h[N],e[N],ne[N],idx;

//插入一个数x
void insert(int x){
    int k=(x%N+N)%N;
    //这边使用头插
    e[idx]=x;
    ne[idx]=h[k];
    h[k]=idx++;
}

//查找有没有x
bool find(int x){
    int k=(x%N+N)%N;

    for(int i=h[k];i!=-1;i=ne[i]){
        if(e[i]==x) return true;
    }

    return false;
}
```

1. 第二种是开放寻址法，

```csharp
//N要比设置的值大2-3倍，并且如果有删除操作，进行逻辑删除而不是物理删除
const int N=2e5+3;
//0x3f3f3f3f是一个比1e9大的数
int h[N],null=0x3f3f3f3f;

//核心方法，如果有x则返回x的位置，没有则返回x应该插入的位置
int find(int x){
    int k=(x%N+N)%N;

    while(h[k]!=null&&h[k]!=x){//如果k处有数并不等于x，则去下一个位置
        k++;
        if(k==N) k=0;
    }

    return k;
}
```

### 字符串前缀哈希

似乎可以代替kmp算法。经验得出，当P=131或者13331，取模于2^64的时候，不会出现冲突，对于取模部分，使用unsigned long long的自然溢出来替代。

```csharp
typedef unsigned long long ULL;
const int N=1e5+10,P=131;

char s[N];
int h[N],p[N];

ULL getans(int l,int r){
    return h[r]-h[l-1]*p[r-l+1];
}

//处理一下p次方和h，这里把ASCII码值当作每个字母的值
    p[0]=1;//p的0次方等于1
    for(int i=1;i<=n;i++){
        p[i]=p[i-1]*P;
        h[i]=h[i-1]*P+s[i];
    }
```

### STL

#### vector

变长数组，倍增的思想

```csharp
    vectcor<int>a(10,3)  大小为10，每个数都是3的vector容器
    size()  返回元素个数
    empty()  返回是否为空
    clear()  清空
    front()/back()
    push_back()/pop_back()
    begin()/end()
    []  支持随机寻址
    支持比较运算，按字典序
```

#### pair

```csharp
pair<int, int>p
    first, 第一个元素
    second, 第二个元素
    支持比较运算，以first为第一关键字，以second为第二关键字（字典序）
    
    p={10,11};
    p=make_pair(10,11);
```

#### string

```csharp
string，字符串
    size()/length()  返回字符串长度
    empty()
    clear()
    substr(起始下标，子串长度)  返回子串,如果大于该串长度，则返回直到最后一个字母
    c_str()  返回字符串所在字符数组的起始地址
```

#### queue

```csharp
queue, 队列
    size()
    empty()
    push()  向队尾插入一个元素
    front()  返回队头元素
    back()  返回队尾元素
    pop()  弹出队头元素

没有clear函数，q=vector<int>();重新建立一个以达到清空的目的
```

#### priority_queue

```csharp
priority_queue, 优先队列，默认是大根堆,堆顶是最大的数
    size()
    empty()
    push()  插入一个元素
    top()  返回堆顶元素
    pop()  弹出堆顶元素
    定义成小根堆的方式：priority_queue<int, vector<int>, greater<int>> q;
```

#### stack

```csharp
stack, 栈
    size()
    empty()
    push()  向栈顶插入一个元素
    top()  返回栈顶元素
    pop()  弹出栈顶元素
```

#### deque

```csharp
deque, 双端队列
    size()
    empty()
    clear()
    front()/back()
    push_back()/pop_back()
    push_front()/pop_front()
    begin()/end()
    []
```

#### set, map, multiset, multimap

```csharp
set, map, multiset, multimap, 基于平衡二叉树（红黑树），动态维护有序序列
    size()
    empty()
    clear()
    begin()/end()
    ++, -- 返回前驱和后继，时间复杂度 O(logn)

    set/multiset
        insert()  插入一个数
        find()  查找一个数,不存在则返回end()
        count()  返回某一个数的个数
        erase()
            (1) 输入是一个数x，删除所有x   O(k + logn)
            (2) 输入一个迭代器，删除这个迭代器
        lower_bound()/upper_bound()
            lower_bound(x)  返回大于等于x的最小的数的迭代器，最小上界
            upper_bound(x)  返回大于x的最小的数的迭代器，最大下界
    map/multimap
        insert()  插入的数是一个pair
        erase()  输入的参数是pair或者迭代器
        find()
        []  注意multimap不支持此操作。 时间复杂度是 O(logn)
        lower_bound()/upper_bound()

unordered_set, unordered_map, unordered_multiset, unordered_multimap, 哈希表
    和上面类似，增删改查的时间复杂度是 O(1)
    不支持 lower_bound()/upper_bound()， 迭代器的++，--
```

#### bitset
```csharp
bitset, 圧位
    bitset<10000> s;
    ~, &, |, ^
    >>, <<
    ==, !=
    []

    count()  返回有多少个1

    any()  判断是否至少有一个1
    none()  判断是否全为0

    set()  把所有位置成1
    set(k, v)  将第k位变成v
    reset()  把所有位变成0
    flip()  等价于~
    flip(k) 把第k位取反
```

## 线性规划
### 01背包
未优化
```c++
for(int i=1;i<=n;i++){
    for(int j=0;j<=m;j++){
        f[i][j]=f[i-1][j];
        if(j>=v[i]) f[i][j]=max(f[i][j],f[i-1][j-v[i]]+w[i]);
    }
}
```

### 完全背包

### 多重背包

### 分组背包