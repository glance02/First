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
```