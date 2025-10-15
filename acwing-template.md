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